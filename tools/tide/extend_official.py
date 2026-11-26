#!/usr/bin/env python3
"""The next year of the ports whose official tables reach only this one (SOHMA's for Uruguay,
tools/sohma_tide.py; the DHN's for Imbituba, tools/ciram_tide.py): a harmonic analysis of this
year's hourly heights (tools/tide/harmonic.py fill: the constituents separable in a year, with the
nodal corrections) predicts the next, in month files like the official ones, marked "ext". Those
tables come out late in the year, and without the next one the field Marea's last piece of
December came out short (84 h, so it was asked for again every 15 min from the 30th) and January
had only the watch's 30 harmonics without nodal corrections. The official tables of the next year
replace these months when they are run (those scripts); until then these are written again on each
run, so a fix to this year's table reaches them. While this year's official table has not come out
(this year's months are extended themselves), the next one comes from the last official year, so
there is always a next year even if a table never comes out. The other sources (build_tides.py) already bring
the next year. tools/tide/chunks.py runs after this (.github/workflows/tides.yml).

    python3 tools/tide/extend_official.py [--year 2026]
"""
import argparse
import calendar
import datetime
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harmonic as H  # noqa: E402
from lib import tide as T  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TIDE = os.path.join(ROOT, "tide")
KEEP = ("port", "name", "lat", "lon", "utc_offset", "unit", "datum")
BACK = 3                                     # años para atrás que se busca uno oficial


def month_epochs(y, m, off):
    """Unix seconds of every hour of month (y, m) in the port's clock (UTC + off h)."""
    base = calendar.timegm((y, m, 1, 0, 0, 0)) - off * 3600
    return [base + i * 3600 for i in range(calendar.monthrange(y, m)[1] * 24)]


def extend(key, year):
    """Writes key's months of year + 1 from its last official year (year itself, or an earlier one while the
    official table of year has not come out); (rms of the analysis, months, that year) or None."""
    d = os.path.join(TIDE, key)
    idx_path = os.path.join(d, "index.json")
    idx = json.load(open(idx_path, encoding="utf-8"))
    have = idx.get("months", [])
    nxt = ["%04d-%02d" % (year + 1, m) for m in range(1, 13)]
    if nxt[0] in have and not json.load(open(os.path.join(d, nxt[0] + ".json"), encoding="utf-8")).get("ext"):
        return None                          # the next year's official table is out
    src = next((y for y in range(year, year - BACK - 1, -1) if T.official(d, y, have)), None)
    if src is None:
        return None                          # only from an official year, not from one extended
    mine = ["%04d-%02d" % (src, m) for m in range(1, 13)]
    first = json.load(open(os.path.join(d, mine[-1] + ".json"), encoding="utf-8"))
    off = int(first.get("utc_offset", 0))
    t, y = [], []
    for m in range(1, 13):
        doc = json.load(open(os.path.join(d, mine[m - 1] + ".json"), encoding="utf-8"))
        t += month_epochs(src, m, off)
        y += [np.nan if v is None else float(v) for v in doc["h"]]
    tn = []
    for m in range(1, 13):
        tn += month_epochs(year + 1, m, off)
    filled, n, rms = H.fill(np.array(t + tn, dtype=float), np.array(y + [np.nan] * len(tn)))
    ahead = filled[len(t):]
    source = "Extendido con un análisis armónico de %d (tools/tide/extend_official.py) hasta que salga la tabla oficial de %d; %d: %s" % (
        src, year + 1, src, first.get("source", ""))
    i = 0
    for m in range(1, 13):
        days = calendar.monthrange(year + 1, m)[1]
        doc = {k: first[k] for k in KEEP if k in first}
        doc.update({"month": nxt[m - 1], "days": days, "source": source, "ext": True,
                    "h": [int(round(v)) for v in ahead[i:i + days * 24]]})
        i += days * 24
        T.write_json(os.path.join(d, nxt[m - 1] + ".json"), doc)
    idx["months"] = have + [k for k in nxt if k not in have]
    T.write_json(idx_path, idx)
    return rms, 12, src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=datetime.datetime.now(datetime.timezone.utc).year)
    a = ap.parse_args()
    done = 0
    for key in sorted(os.listdir(TIDE)):
        if not os.path.exists(os.path.join(TIDE, key, "index.json")):
            continue
        r = extend(key, a.year)
        if r:
            done += 1
            print("%s: %d meses de %d, análisis de %d con rms %.1f cm" % (key, r[1], a.year + 1, r[2], r[0]))
    print("puertos extendidos: %d" % done)


if __name__ == "__main__":
    main()
