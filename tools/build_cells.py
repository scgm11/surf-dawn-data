#!/usr/bin/env python3
"""The spots around each 0.2° cell, for the data fields Marea and Olas y viento:
spots/c/<I>_<J>.json, with I = floor(lat × 5) and J = floor(lon × 5).

A data field's background service has 32 KB on the watches before Connect IQ 4 (fēnix 6
Pro, first MARQ...), and there an answer of much more than 1 KB does not fit once read: a
region (spots/r/) goes up to 3 KB (US-NE, 60 spots). A cell file has what a field needs to
find the spot nearest to it and fetch its data: the spots within MARGIN_KM of the cell (at
most MAX_SPOTS, inside the cell first, then the nearest to its centre, and fewer while the file
is over MAX_BYTES), each with its
region's models and the tide port that stands for it, chosen here as the watch does
(TideTable.portFor: the nearest port whose radius covers the spot). Written from the
regions after tools/build_zones.py (.github/workflows/zones.yml); the cells with no spot
near have no file (404: no spots around there).

    {"z": [[region, wave model, wind model]],
     "p": [[port key, lat, lon, radius km, UTC offset s]],
     "s": [[NAME, lat, lon, facing, z index, p index or -1, (wave lat, wave lon)]],
     "w": [[height top m, period top s] or null],
     "sw": [swell window or null]}

"w", one per row of "z", is each region's wave scale (its "w", tools/build_scale.py), apart from
"z": the fields before it take rows of 3 there. "sw", one per row of "s", each spot's swell
window (its region's "sw"), apart from "s" for the same reason; only in cells that have one.

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
# Measured 4/11/2026 in the simulator (surf-dawn tools/e2e_fields.py, fēnix 6 Pro, Marea): Bali's
# cell (-44_576, 24 spots of 3 regions, 1351 bytes) came as -403, too big to read in the 32 KB
# service, and the field said there were no spots near; Gold Coast's (1289 bytes) was read with
# 3.7 KB left. The densest cells drop their last spots (the farthest outside the cell) to this.
MAX_BYTES = 1100


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
        sw = z.get("sw") if len(z.get("sw") or []) == len(z["s"]) else None
        for i, r in enumerate(z["s"]):
            spots.append({"z": z["id"], "m": z["m"], "sc": z.get("w"), "ports": z["p"], "name": r[0], "lat": r[1], "lon": r[2],
                          "f": r[3], "w": r[5:7] if len(r) >= 7 and r[5] is not None else None,
                          "p": port_for(z["p"], r[1], r[2]), "sw": sw[i] if sw else None})
    cells = {}
    for s in spots:
        for c in cells_near(s["lat"], s["lon"]):
            cells.setdefault(c, []).append(s)
    out = os.path.join(SPOTS, "c")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    sizes = []
    cut = 0
    for c, ss in sorted(cells.items()):
        ss = sorted(ss, key=lambda s: rank(c, s))[:MAX_SPOTS]
        text = cell_text(ss)
        while len(text.encode("utf-8")) > MAX_BYTES and len(ss) > 1:
            ss = ss[:-1]
            text = cell_text(ss)
            cut += 1
        open(os.path.join(out, "%d_%d.json" % c), "w", encoding="utf-8").write(text)
        sizes.append(len(text.encode("utf-8")))
    sizes.sort()
    print("celdas: %d archivos de %d picos; mediana %d bytes, máximo %d; %d picos de menos en las celdas de más de %d bytes" % (
        len(sizes), len(spots), sizes[len(sizes) // 2], sizes[-1], cut, MAX_BYTES))


def cell_text(ss):
    """The cell file of spots ss (ranked), as JSON."""
    zs = list(dict.fromkeys(s["z"] for s in ss))
    ms = {s["z"]: s["m"] for s in ss}
    scs = {s["z"]: s["sc"] for s in ss}
    ports = list(dict.fromkeys(tuple(s["ports"][s["p"]]) for s in ss if s["p"] >= 0))
    rows = []
    for s in ss:
        pi = ports.index(tuple(s["ports"][s["p"]])) if s["p"] >= 0 else -1
        row = [s["name"], round(s["lat"], 4), round(s["lon"], 4), s["f"], zs.index(s["z"]), pi]
        rows.append(row + list(s["w"]) if s["w"] else row)
    doc = {"z": [[z, ms[z][0], ms[z][1]] for z in zs], "p": [list(p) for p in ports], "s": rows}
    if any(scs[z] for z in zs):
        doc["w"] = [scs[z] for z in zs]
    if any(s["sw"] is not None for s in ss):
        doc["sw"] = [s["sw"] for s in ss]
    return json.dumps(doc, separators=(",", ":"), ensure_ascii=False)


if __name__ == "__main__":
    main()
