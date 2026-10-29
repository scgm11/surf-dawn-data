#!/usr/bin/env python3
"""The spots around each 0.2° cell, for the data fields Marea and Olas y viento:
spots/c/<I>_<J>.json, with I = floor(lat × 5) and J = floor(lon × 5).

A data field's background service has 32 KB on the watches before Connect IQ 4 (fēnix 6
Pro, first MARQ...), and there an answer of much more than 1 KB does not fit once read: a
region (spots/r/) goes up to 3 KB (US-NE, 60 spots). A cell file has what a field needs to
find the spot nearest to it and fetch its data: the spots within MARGIN_KM of the cell (at
most MAX_SPOTS, inside the cell first, then the nearest to its centre), each with its
region's models and the tide port that stands for it, chosen here as the watch does
(TideTable.portFor: the nearest port whose radius covers the spot). Written from the
regions after tools/build_zones.py (.github/workflows/zones.yml); the cells with no spot
near have no file (404: no spots around there).

    {"z": [[region, wave model, wind model]],
     "p": [[port key, lat, lon, radius km, UTC offset s]],
     "s": [[NAME, lat, lon, facing, z index, p index or -1, (wave lat, wave lon)]]}

    python3 tools/build_cells.py
"""
import glob
import json
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import geo  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SPOTS = os.path.join(ROOT, "spots")
PER_DEG = 5                                   # cells per degree: 0.2°
MARGIN_KM = 10
MAX_SPOTS = 24


def km(lat1, lon1, lat2, lon2):
    """Great-circle distance, as Earth.km on the watch."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(geo.wrap(lon2 - lon1))
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0 * 2 * math.asin(min(1.0, math.sqrt(a)))


def port_for(ports, lat, lon):
    """TideTable.portFor: index of the nearest port whose radius covers (lat, lon), or -1."""
    best, best_km = -1, 1e9
    for i, p in enumerate(ports):
        d = km(lat, lon, p[1], p[2])
        if d <= p[3] and d < best_km:
            best, best_km = i, d
    return best


def cells_near(lat, lon):
    """The (I, J) cells within MARGIN_KM of (lat, lon)."""
    dlat = MARGIN_KM / 111.0
    dlon = MARGIN_KM / (111.0 * max(0.05, math.cos(math.radians(lat))))
    out = []
    for i in range(math.floor((lat - dlat) * PER_DEG), math.floor((lat + dlat) * PER_DEG) + 1):
        for j in range(math.floor((lon - dlon) * PER_DEG), math.floor((lon + dlon) * PER_DEG) + 1):
            out.append((i, (j + 180 * PER_DEG) % (360 * PER_DEG) - 180 * PER_DEG))
    return out


def rank(cell, s):
    """Inside the cell first, then by distance to its centre."""
    i, j = cell
    inside = math.floor(s["lat"] * PER_DEG) == i and math.floor(s["lon"] * PER_DEG) == j
    return (not inside, km(s["lat"], s["lon"], (i + 0.5) / PER_DEG, (j + 0.5) / PER_DEG))


def main():
    spots = []
    for path in sorted(glob.glob(os.path.join(SPOTS, "r", "*.json"))):
        z = json.load(open(path, encoding="utf-8"))
        for r in z["s"]:
            spots.append({"z": z["id"], "m": z["m"], "ports": z["p"], "name": r[0], "lat": r[1], "lon": r[2],
                          "f": r[3], "w": r[5:7] if len(r) >= 7 and r[5] is not None else None,
                          "p": port_for(z["p"], r[1], r[2])})
    cells = {}
    for s in spots:
        for c in cells_near(s["lat"], s["lon"]):
            cells.setdefault(c, []).append(s)
    out = os.path.join(SPOTS, "c")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    sizes = []
    for c, ss in sorted(cells.items()):
        ss = sorted(ss, key=lambda s: rank(c, s))[:MAX_SPOTS]
        zs = list(dict.fromkeys(s["z"] for s in ss))
        ms = {s["z"]: s["m"] for s in ss}
        ports = list(dict.fromkeys(tuple(s["ports"][s["p"]]) for s in ss if s["p"] >= 0))
        rows = []
        for s in ss:
            pi = ports.index(tuple(s["ports"][s["p"]])) if s["p"] >= 0 else -1
            row = [s["name"], round(s["lat"], 4), round(s["lon"], 4), s["f"], zs.index(s["z"]), pi]
            rows.append(row + list(s["w"]) if s["w"] else row)
        doc = {"z": [[z, ms[z][0], ms[z][1]] for z in zs], "p": [list(p) for p in ports], "s": rows}
        text = json.dumps(doc, separators=(",", ":"), ensure_ascii=False)
        open(os.path.join(out, "%d_%d.json" % c), "w", encoding="utf-8").write(text)
        sizes.append(len(text.encode("utf-8")))
    sizes.sort()
    print("celdas: %d archivos de %d picos; mediana %d bytes, máximo %d" % (
        len(sizes), len(spots), sizes[len(sizes) // 2], sizes[-1]))


if __name__ == "__main__":
    main()
