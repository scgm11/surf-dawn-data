#!/usr/bin/env python3
"""Validates the Open-Meteo wave models against wave buoys over the last 30 days and writes
validation/ (docs/formatos.md, section Validación; validate/README.md):

  validation/<REGION>.json       scores per region and model, best model, confidence
  validation/report.md           the summary in Spanish
  validation/models-suggested.csv  rows for models.csv: regions with a confident best that is not
                                 the model they use today (never the fixed regions of issue #7)
  validation/buoys.csv           the buoys used, with the regions each one validates

Usage: python3 validate/run.py [--regions CODE ...] [--sources cdip aodn mi ndbc]
"""
import argparse
import csv
import glob
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import buoys  # noqa: E402
import cache  # noqa: E402
import evaluate  # noqa: E402
import models  # noqa: E402
import regions as regs  # noqa: E402
import report  # noqa: E402
from tools.lib import geo  # noqa: E402  (regions put the repo root on the path)

OUT = os.path.join(regs.ROOT, "validation")
T0 = time.time()


def log(msg):
    print("[%5.0fs] %s" % (time.time() - T0, msg), flush=True)


def write(name, text):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def direction_check(results):
    """Mean signed model - buoy direction and period differences per source (convention check)."""
    acc = {}
    for body, info in results:
        for st, _, sc in info["matched"]:
            for m, s in sc.items():
                a = acc.setdefault(st.source, {}).setdefault(m, {"n": 0, "tp": [], "tm": [], "dir": [], "db": []})
                a["n"] += s["n"]
                if s["tp_bias"] is not None:
                    a["tp"].append((s["tp_bias"], s["n"]))
                if s["tm_bias"] is not None:
                    a["tm"].append((s["tm_bias"], s["n"]))
                if s["dir_mae"] is not None:
                    a["dir"].append((s["dir_mae"], s["n"]))
                if s["dir_bias"] is not None:
                    a["db"].append((s["dir_bias"], s["n"]))
    out = {}
    for src, ms in acc.items():
        for m, a in ms.items():
            def wavg(xs):
                w = sum(n for _, n in xs)
                return round(sum(x * n for x, n in xs) / w, 2) if w else None
            out.setdefault(src, {})[m] = {"n": a["n"], "tp_bias": wavg(a["tp"]), "tm_bias": wavg(a["tm"]), "dir_mae": wavg(a["dir"]),
                                         "dir_bias": wavg(a["db"])}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--sources", nargs="*", default=["cdip", "aodn", "mi", "ndbc"])
    a = ap.parse_args()
    cache.prune()
    now = time.time()
    day0 = int(now // 86400) * 86400 - models.PAST_DAYS * 86400          # the model window starts at 00 UTC
    window = (time.strftime("%Y-%m-%d", time.gmtime(day0)), time.strftime("%Y-%m-%d", time.gmtime(now)))
    rs = regs.load()
    if a.regions:
        rs = [r for r in rs if r.code in set(a.regions)]
    log("%d regions, window %s .. %s" % (len(rs), *window))

    stations, status = buoys.fetch_all(regs.near_any(rs), day0, log, a.sources)
    stations, twins = buoys.dedupe(stations, geo.km)
    for s, k in twins:
        log("  same buoy: %s = %s (kept %s)" % (s.id, k.id, k.id))
    log("%d stations after removing %d duplicates" % (len(stations), len(twins)))

    matched = {r.code: regs.match(r, stations) for r in rs}
    used = {s.id: s for m in matched.values() for s, _ in m}
    log("%d buoys within %d km of %d regions" % (len(used), regs.MATCH_KM, sum(1 for m in matched.values() if m)))
    at_buoys = models.series([(s.lat, s.lon) for s in used.values()], log, "buoy")
    at_spots = models.series([r.mid for r in rs], log, "spread", ["wave_height"])
    log("open-meteo: %d requests, %d locations, %.0f weighted calls (free limit 10000/day); cache %s"
        % (models.USED["requests"], models.USED["locations"], models.USED["weight"], cache.STATS))

    for p in glob.glob(os.path.join(OUT, "*.json")):
        os.remove(p)
    results = []
    for r in rs:
        sp = at_spots.get((round(r.mid[0], 4), round(r.mid[1], 4)))
        body, info = evaluate.region_result(r, matched[r.code], at_buoys, window, sp)
        results.append((body, info))
        write("%s.json" % r.code, json.dumps(body, ensure_ascii=False, indent=1) + "\n")
        b = body.get("best", {}).get("wave", "-")
        w = body.get("wave", {}).get(b, {})
        log("%-11s %-38s best %-17s n %4s rmse %-5s bias %-6s %s" % (
            r.code, ",".join(body["buoys"]) or "(no buoys; spread %s)" % body.get("spread", {}).get("hs"),
            b, w.get("n", ""), w.get("hs_rmse", ""), w.get("hs_bias", ""), body["confidence"]))

    rows = report.suggestions(results)
    f = io.StringIO()
    wr = csv.writer(f, lineterminator="\n")
    wr.writerow(["region", "wave", "wind", "why"])
    wr.writerows(rows)
    write("models-suggested.csv", f.getvalue())
    f = io.StringIO()
    wr = csv.writer(f, lineterminator="\n")
    wr.writerow(["id", "name", "lat", "lon", "hours", "regions"])
    validates = {}
    for body, _ in results:
        for b in body["buoys"]:
            validates.setdefault(b, []).append(body["region"])
        for x in body.get("excluded", []):
            validates.setdefault(x["id"], []).append("(%s: no representativa)" % body["region"])
    for sid, s in sorted(used.items()):
        if sid in validates:
            wr.writerow([sid, s.name, round(s.lat, 4), round(s.lon, 4), len(s.hourly), " ".join(validates[sid])])
    write("buoys.csv", f.getvalue())
    checks = direction_check(results)
    for src, ms in sorted(checks.items()):
        for m, c in ms.items():
            log("check %-5s %-17s %s" % (src, m, c))
    write("report.md", report.markdown(results, window, status, checks, models.USED, twins))
    nb = sum(1 for b, _ in results if b["buoys"])
    log("done: %d regions, %d with buoys, %d suggestions" % (len(results), nb, len(rows)))
    failed = [s for s, v in status.items() if v.startswith("falló")]
    if failed:
        log("ERROR: sources that failed: %s (the outputs are written without them)" % ", ".join(failed))
    sys.exit(1 if failed or nb == 0 else 0)


if __name__ == "__main__":
    main()
