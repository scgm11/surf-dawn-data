#!/usr/bin/env python3
"""Each region's wave scale: the height and the period where the apps' score of the waves tops out
there (seeds/scale.csv, "w" in spots/r/ and spots/c/, docs/formatos.md).

The apps score an hour's waves by their size and period (Score.wave in surf-dawn: shared-bg/Score.mc,
SurfDawnKit/Score.swift): nothing with 30 cm and 5 s, all of it from 1.8 m and 13 s. One scale for the
whole world tops out most days where the sea is big (Peniche, Nazaré, Cape Town, Chile, Peru: full size
and period on 85-100 % of the days) and seldom where it is small (the Mediterranean, the Gulf of Mexico,
the North Sea). Each region gets its own: its height top is 88 % of its Hs that 10 % of the daylight
hours of a year go over (p90), its period top 1.7 s over its p90 period, so that Rocha (UY-ROC, p90
2.04 m and 11.3 s) keeps the scale the apps had (1.8 m and 13 s). The rest of the scale goes with it
(the 30 cm and 5 s floors in the same proportion), and the levels of the sea's energy too.

A year of hourly waves (07-18 h at the region's time) at one point per region, its middle spot's wave
point, in its wave model; the ECMWF WAM models have no history in Open-Meteo for that year, so those
regions go with GFS Wave 0.25°. They have no wave points of their own: where GFS has land at the middle
spot (0.0 m all year, not null) it goes to the sea cell in front of it that build_zones would choose.
A year weighs 26 calls of the free API (10,000 a day, 5,000 an hour): the answers are cached in
tools/.cache/scale/ and the requests paced.

    python3 tools/build_scale.py [REGION ...]      all the regions in spots/r/ (or these), into seeds/scale.csv
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)
from tools.lib import openmeteo  # noqa: E402

REGIONS = os.path.join(ROOT, "spots", "r")
CACHE = os.path.join(ROOT, "tools", ".cache", "scale")
OUT = os.path.join(ROOT, "seeds", "scale.csv")
MARINE = "https://marine-api.open-meteo.com/v1/marine"
FROM, TO = "2024-11-01", "2025-10-31"             # a whole year: every season once
HOURS = range(7, 19)                             # daylight at any latitude where people surf
HEIGHT = 0.88                                    # of the p90 height: Rocha's 2.04 m gives 1.8 m
PERIOD = 1.7                                     # s over the p90 period: Rocha's 11.3 s gives 13 s
PACE = 18                                        # s between requests: 26 calls each, 5,000 an hour
GFS = "ncep_gfswave025"                          # the global grid: the one with a year of history everywhere
MIN_HS, MIN_T, MIN_HOURS = 0.3, 4.0, 4000        # less is not the sea: a land cell gives 0.0 m, 0.0 s (null before 5/2025)


def pct(a, p):
    a = sorted(a)
    return a[min(len(a) - 1, int(p / 100 * len(a)))]


def point(z):
    """The middle spot's wave point (its own position when it has none) and the wave model to ask."""
    s = z["s"][len(z["s"]) // 2]
    lat, lon = (s[5], s[6]) if len(s) >= 7 else (s[1], s[2])
    model = z["m"][0] if "ecmwf" not in z["m"][0] else GFS
    return lat, lon, model


def sea_point(z, model):
    """The sea cell in front of the middle spot, for a spot whose own cell is land in this model."""
    i = len(z["s"]) // 2
    s = z["s"][i]
    window = (z.get("sw") or [None] * len(z["s"]))[i]
    wp = openmeteo.wave_points(model, [(s[1], s[2])], [window if window is not None else s[3]])[0]
    return wp if wp not in (None, "none") else None


def fetch(code, lat, lon, model):
    path = os.path.join(CACHE, "%s.json" % code)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    url = ("%s?latitude=%.4f&longitude=%.4f&hourly=wave_height,wave_period&models=%s&start_date=%s&end_date=%s&timezone=auto"
           % (MARINE, lat, lon, model, FROM, TO))
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(70 * (attempt + 1))         # over the minute's or the hour's calls: wait
    os.makedirs(CACHE, exist_ok=True)
    with open(path + ".tmp", "w") as f:
        json.dump(d, f)
    os.replace(path + ".tmp", path)                # whole or not at all: a run stopped halfway leaves no half answer
    time.sleep(PACE)
    return d


def scale(d):
    """(height top, period top, p90 height, p90 period, hours) of a year's answer, None without waves
    (a land cell answers 0.0 m and 0.0 s: the floors below would make that a scale, and a broken one)."""
    h = d.get("hourly", {})
    rows = [(a, b) for t, a, b in zip(h.get("time", []), h.get("wave_height", []), h.get("wave_period", []))
            if a is not None and b is not None and int(t[11:13]) in HOURS]
    if len(rows) < MIN_HOURS:
        return None
    hs = pct([a for a, _ in rows], 90)
    tp = pct([b for _, b in rows], 90)
    if hs < MIN_HS or tp < MIN_T:
        return None
    top = min(5.0, max(0.6, round(HEIGHT * hs, 2)))
    per = min(20.0, max(8.0, round(tp + PERIOD, 1)))
    return top, per, hs, tp, len(rows)


def main():
    codes = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(REGIONS) if f.endswith(".json"))
    old = {}
    if os.path.exists(OUT):
        with open(OUT, newline="") as f:
            old = {r["region"]: r for r in csv.DictReader(f)}
    for i, code in enumerate(codes):
        with open(os.path.join(REGIONS, "%s.json" % code), encoding="utf-8") as f:
            z = json.load(f)
        lat, lon, model = point(z)
        try:
            d = fetch(code, lat, lon, model)
            if scale(d) is None and model != GFS:
                model = GFS                          # a regional model without history there
                os.remove(os.path.join(CACHE, "%s.json" % code))
                d = fetch(code, lat, lon, model)
            if scale(d) is None:
                sea = sea_point(z, model)            # the spot's own cell is land in this model
                if sea is not None:
                    lat, lon = sea
                    os.remove(os.path.join(CACHE, "%s.json" % code))
                    d = fetch(code, lat, lon, model)
        except (urllib.error.URLError, OSError, ValueError, RuntimeError) as e:
            print("%s: %s" % (code, e), file=sys.stderr)
            continue
        s = scale(d)
        if s is None:
            print("%s: no waves at %.4f, %.4f in %s" % (code, lat, lon, model), file=sys.stderr)
            continue
        old[code] = {"region": code, "height": "%.2f" % s[0], "period": "%.1f" % s[1], "hs90": "%.2f" % s[2],
                     "t90": "%.1f" % s[3], "hours": s[4], "lat": "%.4f" % lat, "lon": "%.4f" % lon, "model": model}
        print("%3d/%d %-11s %.2f m %4.1f s  (p90 %.2f m %4.1f s)" % (i + 1, len(codes), code, s[0], s[1], s[2], s[3]), flush=True)
        with open(OUT, "w", newline="") as f:
            w = csv.DictWriter(f, ["region", "height", "period", "hs90", "t90", "hours", "lat", "lon", "model"])
            w.writeheader()
            for k in sorted(old):
                w.writerow(old[k])


if __name__ == "__main__":
    main()
