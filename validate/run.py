#!/usr/bin/env python3
"""Validates the Open-Meteo wave models against wave buoys and the wind models against buoys and
coastal stations over the last 30 days and writes validation/ (docs/formatos.md, section
Validación; validate/README.md):

  validation/<REGION>.json       scores per region and model (waves and wind), best models, confidence
  validation/report.md           the summary in Spanish
  validation/models-suggested.csv  rows for models.csv: regions with a confident best (waves and/or
                                 wind) that is not the model they use today (never the fixed regions
                                 of issue #7)
  validation/buoys.csv           the wave buoys used, with the regions each one validates
  validation/wind-stations.csv   the wind stations used, with their anemometer height
  validation/stations.csv        every station read from the sources, with its hours (diagnostics)

Usage: python3 validate/run.py [--regions CODE ...] [--sources cdip aodn mi ndbc cmems]
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


def wind_check(results):
    """Per source and wind model, over every station used: hours, mean observed speed (m/s), mean
    bias (m/s), rmse (m/s), direction error and circular bias (units and conventions check)."""
    acc = {}
    for body, info in results:
        for st, _, sc in info.get("wind", {}).get("matched", []):
            for m, s in sc.items():
                a = acc.setdefault(st.source, {}).setdefault(m, [])
                a.append((s["n"], s["obs_spd"], s["spd_bias_ms"], s["spd_rmse"], s["dir_mae"], s["dir_bias"], s["dir_n"]))
    out = {}
    for src, ms in acc.items():
        for m, xs in ms.items():
            n = sum(x[0] for x in xs)
            dn = sum(x[6] for x in xs if x[4] is not None)

            def avg(i, w=0):
                good = [x for x in xs if x[i] is not None]
                tot = sum(x[w] for x in good)
                return sum(x[i] * x[w] for x in good) / tot if tot else None
            rm = sum(x[3] ** 2 * x[0] for x in xs) / n if n else None
            out.setdefault(src, {})[m] = {"n": n, "obs_spd": avg(1), "bias_ms": avg(2), "rmse": rm ** 0.5 if rm is not None else None,
                                         "dir_mae": avg(4, 6) if dn else None, "dir_bias": avg(5, 6) if dn else None}
    return out


def spread_points(rs, log, tries=4):
    """For each region, the wave heights of every model at one spot for the inter-model spread: the
    spot nearest the centre, or the next ones while the region's own model has no sea there.
    Sets region.mid to the spot used. Returns {code: (times, {model: cols})}."""
    out, todo = {}, list(rs)
    order = {r.code: sorted(r.spots, key=lambda s: geo.km((r.lat, r.lon), s))[:tries] for r in rs}
    for k in range(tries):
        if not todo:
            break
        pts = {r.code: order[r.code][k] for r in todo if k < len(order[r.code])}
        got = models.series(list(pts.values()), log, "spread", ["wave_height"])
        left = []
        for r in todo:
            if r.code not in pts:
                continue
            p = (round(pts[r.code][0], 4), round(pts[r.code][1], 4))
            sp = got.get(p)
            if sp is None:
                continue
            if r.code not in out or len(sp[1]) > len(out[r.code][1]):
                out[r.code], r.mid = sp, pts[r.code]
            if r.current[0] not in sp[1]:
                left.append(r)
        todo = left
    if todo:
        log("spread: %d regions without their own model at %d spots: %s" % (len(todo), tries, " ".join(r.code for r in todo)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--sources", nargs="*", default=list(buoys.SOURCES))
    a = ap.parse_args()
    cache.prune()
    now = time.time()
    day0 = int(now // 86400) * 86400 - models.PAST_DAYS * 86400          # the model window starts at 00 UTC
    window = (time.strftime("%Y-%m-%d", time.gmtime(day0)), time.strftime("%Y-%m-%d", time.gmtime(now)))
    rs = regs.load()
    if a.regions:
        rs = [r for r in rs if r.code in set(a.regions)]
    log("%d regions, window %s .. %s" % (len(rs), *window))

    allst, status = buoys.fetch_all(regs.near_any(rs), day0, log, a.sources)
    stations, twins = buoys.dedupe([s for s in allst if len(s.hourly) >= buoys.MIN_HOURS], geo.km)
    for s, k in twins:
        log("  same buoy: %s = %s (kept %s)" % (s.id, k.id, k.id))
    log("%d wave stations after removing %d duplicates" % (len(stations), len(twins)))
    wstations, wtwins = buoys.dedupe([s for s in allst if len(s.wind_raw) >= buoys.MIN_HOURS], geo.km,
                                     hours=lambda s: len(s.wind_raw))
    for s, k in wtwins:
        log("  same wind station: %s = %s (kept %s)" % (s.id, k.id, k.id))
    log("%d wind stations after removing %d duplicates (%d buoys, %d ashore)" % (
        len(wstations), len(wtwins), sum(1 for s in wstations if s.kind == "buoy"), sum(1 for s in wstations if s.kind != "buoy")))

    try:
        exposure = regs.Exposure(regs.land_mask())
    except ImportError as e:
        log("ERROR: no land mask (%s): buoys are matched by distance only" % e)
        exposure = None
    found = {r.code: regs.match(r, stations, exposure=exposure) for r in rs}
    matched = {c: m for c, (m, _) in found.items()}
    blocked = {c: b for c, (_, b) in found.items()}
    log("%d buoy-region pairs left out: facing another sea or sheltered" % sum(len(b) for b in blocked.values()))
    used = {s.id: s for m in matched.values() for s, _, _ in m}
    log("%d buoys within %d km of %d regions" % (len(used), regs.MATCH_KM, sum(1 for m in matched.values() if m)))
    at_buoys = models.series([(s.lat, s.lon) for s in used.values()], log, "buoy")
    at_spots = spread_points(rs, log)

    wfound = {r.code: regs.match(r, wstations, top=regs.WIND_CANDIDATES, exposure=exposure) for r in rs}
    log("%d wind station-region pairs left out: facing another sea or sheltered" % sum(len(b) for _, b in wfound.values()))
    wused, serves = {}, {}
    for r in rs:
        for s, _, _ in wfound[r.code][0]:
            wused[s.id] = s
            serves.setdefault(s.id, []).append(r)
    log("%d wind stations within %d km of %d regions" % (len(wused), regs.MATCH_KM, sum(1 for m, _ in wfound.values() if m)))
    buoys.ndbc_heights([s for s in wused.values() if s.source == "ndbc"], log)
    models.probe_wind(log)
    req = []
    for sid, s in wused.items():
        ms = []
        for r in serves[sid]:
            ms += [r.current[1] if len(r.current) > 1 else regs.DEFAULT_WIND] + models.wind_models_for(r.lat, r.lon)
        req.append((s.lat, s.lon, s.kind, list(dict.fromkeys(ms))))
    at_wind = models.wind_series(req, log)
    for api, u in sorted(models.USED["by_api"].items()):
        log("open-meteo %s: %d requests, %d locations, %.0f weighted calls" % (api, u["requests"], u["locations"], u["weight"]))
    log("open-meteo: %d requests, %d locations, %.0f weighted calls (free limit 10000/day); cache %s"
        % (models.USED["requests"], models.USED["locations"], models.USED["weight"], cache.STATS))

    for p in glob.glob(os.path.join(OUT, "*.json")):
        os.remove(p)
    results = []
    for r in rs:
        sp = at_spots.get(r.code)
        body, info = evaluate.region_result(r, matched[r.code], at_buoys, window, sp, blocked[r.code],
                                            wind=(wfound[r.code][0], wfound[r.code][1], at_wind))
        results.append((body, info))
        if matched[r.code] and not body["buoys"]:
            log("  %s: no buoy left of %s; coverage %s" % (r.code, [s.id for s, _, _ in matched[r.code]], info.get("coverage")))
        write("%s.json" % r.code, json.dumps(body, ensure_ascii=False, indent=1) + "\n")
        b = body.get("best", {}).get("wave", "-")
        w = body.get("wave", {}).get(b, {})
        log("%-11s %-38s best %-17s n %4s rmse %-5s bias %-6s %s" % (
            r.code, ",".join(body["buoys"]) or "(no buoys; spread %s)" % body.get("spread", {}).get("hs"),
            b, w.get("n", ""), w.get("hs_rmse", ""), w.get("hs_bias", ""), body["confidence"]))
        wb = body["wind"]
        if wb["stations"]:
            bw = wb.get("best", "-")
            x = wb.get("models", {}).get(bw) or wb.get("models", {}).get(wb["current"], {})
            c = wb.get("models", {}).get(wb["current"], {})
            log("%-11s wind %-33s best %-17s n %4s rmse %-5s bias %-6s (%s rmse %s bias %s) %s%s" % (
                "", ",".join(wb["stations"]), bw, x.get("n", ""), x.get("spd_rmse", ""), x.get("spd_bias", ""),
                wb["current"], c.get("spd_rmse", ""), c.get("spd_bias", ""), wb.get("confidence", ""),
                "; few hours: %s" % " ".join(info["wind"]["dropped_models"]) if info["wind"]["dropped_models"] else ""))

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
            if x["id"] in used:
                validates.setdefault(x["id"], []).append("(%s: %s)" % (body["region"], x["why"]))
    for sid, s in sorted(used.items()):
        if sid in validates:
            wr.writerow([sid, s.name, round(s.lat, 4), round(s.lon, 4), len(s.hourly), " ".join(validates[sid])])
    write("buoys.csv", f.getvalue())
    f = io.StringIO()
    wr = csv.writer(f, lineterminator="\n")
    wr.writerow(["id", "name", "lat", "lon", "kind", "z", "factor", "hours", "regions"])
    wval = {}
    for body, _ in results:
        for b in body["wind"]["stations"]:
            wval.setdefault(b, []).append(body["region"])
        for x in body["wind"].get("excluded", []):
            if x["id"] in wused:
                wval.setdefault(x["id"], []).append("(%s: %s)" % (body["region"], x["why"]))
    for sid, s in sorted(wused.items()):
        if sid in wval:
            wr.writerow([sid, s.name, round(s.lat, 4), round(s.lon, 4), s.kind, round(s.z, 1) if s.z is not None else "",
                         round(s.factor, 3), len(s.wind), " ".join(wval[sid])])
    write("wind-stations.csv", f.getvalue())
    f = io.StringIO()
    wr = csv.writer(f, lineterminator="\n")
    wr.writerow(["id", "name", "lat", "lon", "kind", "records", "hours", "wind_hours", "first", "last"])
    for s in sorted(buoys.STATIONS, key=lambda s: s.id):
        hs = sorted(set(s.hourly) | set(s.wind_raw))
        wr.writerow([s.id, s.name, round(s.lat, 4), round(s.lon, 4), s.kind, len(s.records), len(s.hourly), len(s.wind_raw),
                     time.strftime("%Y-%m-%dT%H", time.gmtime(hs[0] * 3600)) if hs else "",
                     time.strftime("%Y-%m-%dT%H", time.gmtime(hs[-1] * 3600)) if hs else ""])
    write("stations.csv", f.getvalue())
    checks = direction_check(results)
    for src, ms in sorted(checks.items()):
        for m, c in ms.items():
            log("check %-5s %-17s %s" % (src, m, c))
    wchecks = wind_check(results)
    for src, ms in sorted(wchecks.items()):
        for m, c in ms.items():
            log("wind check %-5s %-20s %s" % (src, m, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()}))
    write("report.md", report.markdown(results, window, status, checks, models.USED, twins, wchecks, wtwins))
    nb = sum(1 for b, _ in results if b["buoys"])
    nw = sum(1 for b, _ in results if b["wind"]["stations"])
    log("done: %d regions, %d with buoys, %d with wind stations, %d suggestions" % (len(results), nb, nw, len(rows)))
    failed = [s for s, v in status.items() if v.startswith("falló")]
    if failed:
        log("ERROR: sources that failed: %s (the outputs are written without them)" % ", ".join(failed))
    sys.exit(1 if failed or nb == 0 else 0)


if __name__ == "__main__":
    main()
