#!/usr/bin/env python3
"""Builds spots/ (docs/formatos.md) from the seed tables (seeds/README.md): one file per
region, the continent indexes and the 10° cells the watch looks up by position.

For every spot: the position snapped to the OpenStreetMap coastline and the direction its
beach faces (tools/lib/osm.py, the rule tools/make_spots.py used), unless the seed says
`nosnap` / `facing=`; the wave point when the region's wave model has land in the spot's
cell (tools/lib/openmeteo.py, what tools/wave_points.py did); the break type from the seed;
how open it is to the sea in each direction ("x", tools/lib/shelter.py: land that blocks the
wind's chop or the swell), for every region, the frozen ones too; a spot with no direction open
to the sea (snapped to a river, a ria or a harbour) moves to the most open coast near its seed.
Each region gets its Open-Meteo models (models.csv, else the default rule) and its tide
ports (tide/regions.json, written by tools/tide/).

The regions of Uruguay and Santa Catarina are frozen: their seeds carry the validated
positions, facings and wave points of 2026-10 (UY-CAN: computed here on 2026-10-22, then
frozen the same way), and nothing is recomputed for them.

Usage: python3 tools/build_zones.py [--regions CODE ...] [--offline] [--strict] [--missing-tiles]
  --offline  no downloads: only what is cached (spots that would need the network are reported)
  --strict   exit 1 on any error (CI); otherwise a region with errors is still written without
             the spots in error
  --missing-tiles  only print how many coastline tiles are not cached yet (CI fetches the
             coastline file only then)
"""
import argparse
import glob
import hashlib
import json
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, osm, seeds, shelter  # noqa: E402
from tools.lib import models as rule  # noqa: E402

ROOT = seeds.ROOT
OUT = os.path.join(ROOT, "spots")
MAX_BYTES = 6144                     # per file: the face's background process has 64 KB
NEAR_KM = 25                         # Spots.RADIUS_KM on the watch: a region's circle reaches this far past its spots
CELL = 10                            # degrees of a lookup cell (spots/g/)
FROZEN = {"UY-CAN", "UY-MAL", "UY-ROC", "BR-SC-FLN", "BR-SC-SUL"}


def read_ports():
    path = os.path.join(ROOT, "tide", "regions.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def version(obj):
    return hashlib.sha1(dump(obj).encode("utf-8")).hexdigest()[:6]


def cells(lat, lon, km):
    """The CELL° cells a circle touches, as 'LAT_LON' keys (floor multiples of CELL)."""
    dlat = km / geo.KM_PER_DEG
    dlon = km / (geo.KM_PER_DEG * max(0.05, math.cos(math.radians(min(85.0, abs(lat) + dlat)))))
    out = set()
    a = math.floor((lat - dlat) / CELL) * CELL
    while a <= lat + dlat:
        if -90 <= a < 90:
            b = math.floor((lon - dlon) / CELL) * CELL
            while b <= lon + dlon:
                w = int(geo.wrap(b + 0.001) // CELL * CELL)
                out.add("%d_%d" % (a, w))
                b += CELL
        a += CELL
    return out


def coast_rows(code, rows):
    """The seeds that need the coastline (to snap or to face)."""
    return [r for r in rows if code not in FROZEN and (not r["f"].get("nosnap") or "facing" not in r["f"])]


def build_region(code, reg, country, models, ports, offline, rep):
    rows = seeds.spots(code)
    if not rows:
        return None
    frozen = code in FROZEN
    errs, warns = rep["errors"], rep["warnings"]
    need_coast = coast_rows(code, rows)
    ways = None
    if need_coast:
        try:
            ways = osm.coastline(code, [(r["lat"], r["lon"]) for r in need_coast], offline=offline)
        except RuntimeError as e:
            errs.append("%s: %s" % (code, e))
            return None
        if ways is None:
            warns.append("%s: no cached coastline (offline): region skipped" % code)
            return None
    spots = []
    for r in rows:
        f = r["f"]
        lat, lon, facing, snapped = r["lat"], r["lon"], f.get("facing"), None
        if not frozen and (not f.get("nosnap") or facing is None):
            s = osm.snap(r["lat"], r["lon"], ways)
            if s is None or s[0] > osm.SNAP_MAX_M:
                if f.get("nosnap") and s is not None:
                    facing = s[3]
                    warns.append("%s/%s: offshore, facing %d from a coastline %.0f m away (check)" % (code, r["name"], facing, s[0]))
                else:
                    errs.append("%s/%s: not within %d m of a coastline (%s)" % (
                        code, r["name"], osm.SNAP_MAX_M, "none found" if s is None else "%.0f m" % s[0]))
                    continue
            else:
                snapped = s[0]
                if not f.get("nosnap"):
                    lat, lon = s[1], s[2]
                if facing is None:
                    facing = s[3]
        if facing is None:
            errs.append("%s/%s: no facing" % (code, r["name"]))
            continue
        spots.append({"name": r["name"], "lat": round(lat, 4), "lon": round(lon, 4), "facing": int(facing) % 360,
                      "kind": r["kind"], "wave": f.get("wave"), "top": bool(f.get("top")), "snap": snapped,
                      "conf": r["conf"], "nosnap": bool(f.get("nosnap")), "fixed": "facing" in f, "seed": (r["lat"], r["lon"])})
    if not spots:
        errs.append("%s: no spot left" % code)
        return None
    x = None
    try:
        wx = osm.coastline(code, [(s["lat"], s["lon"]) for s in spots], offline=offline, box=shelter.BOX_DEG)
    except RuntimeError as e:
        wx = None
        warns.append("%s: %s (no shelter)" % (code, e))
    if wx is None:
        warns.append("%s: no coastline around the spots: no shelter (x)" % code)
    else:
        x = []
        for s in spots:
            c = shelter.code(wx, s["lat"], s["lon"], s["facing"])
            if 2 not in shelter.decode(c) and not frozen and not s["nosnap"] and not s["fixed"]:
                # no sector open to the sea: snapped to a river, a ria or a harbour, its facing across
                # the water; moved to the most open coastline near its seed (wave point and all after)
                m = shelter.relocate(wx, s["seed"][0], s["seed"][1])
                if m is not None:
                    warns.append("%s/%s: no direction open to the sea, moved %.0f m from the seed (facing %d -> %d)" % (
                        code, s["name"], m[3], s["facing"], m[2]))
                    s["lat"], s["lon"], s["facing"] = m[0], m[1], m[2]
                    c = shelter.code(wx, s["lat"], s["lon"], s["facing"])
            if 2 not in shelter.decode(c):
                # still none (a facing or position set by hand, or no open coast near): the watch
                # scores it as before
                warns.append("%s/%s: no direction open to the sea from facing %d: check the facing (no shelter)" % (
                    code, s["name"], s["facing"]))
                c = None
            s["x"] = c
            x.append(c)
    clat, clon = geo.center([(s["lat"], s["lon"]) for s in spots])
    m = rule.for_region(code, country, clat, models)
    if not frozen:
        todo = [s for s in spots if s["wave"] is None]
        if todo and not offline:
            from tools.lib import openmeteo
            pts = [(s["lat"], s["lon"]) for s in todo]
            try:
                wps = openmeteo.wave_points(m[0], pts)
                if "none" in wps and code not in models and m[0] != rule.GLOBAL_WAVE:
                    # the 0.16° grids are regional (15°S–52.5°N, not every coast): a region the
                    # rule gave one that has no sea near some spot goes with the global grid
                    warns.append("%s: %s has no waves near %d spots: %s" % (code, m[0], wps.count("none"), rule.GLOBAL_WAVE))
                    m = [rule.GLOBAL_WAVE, m[1]]
                    wps = openmeteo.wave_points(m[0], pts)
            except RuntimeError as e:
                errs.append("%s: %s" % (code, e))
                return None
            for s, wp in zip(todo, wps):
                if wp == "none":
                    warns.append("%s/%s: land cell in %s and no sea cell nearby (no wave point)" % (code, s["name"], m[0]))
                elif wp is not None:
                    s["wave"] = wp
        elif todo:
            rep["offline_waves"] += len(todo)
    radius = int(math.ceil(max(geo.km((clat, clon), (s["lat"], s["lon"])) for s in spots))) + NEAR_KM
    srows = []
    for s in spots:
        row = [s["name"], s["lat"], s["lon"], s["facing"], s["kind"]]
        if s["wave"] is not None:
            row += [round(s["wave"][0], 4), round(s["wave"][1], 4)]
        srows.append(row)
    body = {"id": code, "c": country, "n": [reg["name_es"], reg["name_en"]], "m": m,
            "p": ports.get(code, []), "s": srows}
    if x is not None:
        body["x"] = x                              # apart from "s": the watches before it take rows of 5 or 7
    v = version(body)
    out = {"id": code, "v": v}
    out.update({k: body[k] for k in ("c", "n", "m", "p", "s", "x") if k in body})
    text = dump(out)
    size = len(text.encode("utf-8"))
    if size > MAX_BYTES:
        errs.append("%s: %d bytes (max %d): split the region" % (code, size, MAX_BYTES))
    rep["regions"][code] = {"spots": spots, "models": m, "ports": len(body["p"]), "bytes": size}
    return {"code": code, "country": country, "v": v, "text": text, "bytes": size, "n": len(srows),
            "lat": round(clat, 3), "lon": round(clon, 3), "km": radius}


def previous():
    """{code: region} of the spots/ published before this run (the indexes and the region files),
    in the shape build_region returns, so a region this run cannot build is not lost."""
    out = {}
    for path in sorted(glob.glob(os.path.join(OUT, "idx", "*.json"))):
        try:
            with open(path, encoding="utf-8") as f:
                rows = json.load(f).get("r", [])
        except (OSError, ValueError):
            continue
        for r in rows:
            try:
                with open(os.path.join(OUT, "r", r[0] + ".json"), encoding="utf-8") as f:
                    text = f.read()
            except OSError:
                continue
            out[r[0]] = {"code": r[0], "country": r[1], "v": r[9], "text": text, "bytes": r[8], "n": r[7],
                         "lat": r[4], "lon": r[5], "km": r[6]}
    return out


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def report_md(rep, built):
    lines = ["# Picos: reporte del último build", "",
             "%d regiones, %d picos. Errores: %d. Avisos: %d." % (
                 len(built), sum(b["n"] for b in built), len(rep["errors"]), len(rep["warnings"])), ""]
    if rep["offline_waves"]:
        lines += ["Sin red: %d picos sin revisar su celda de olas." % rep["offline_waves"], ""]
    if rep["errors"]:
        lines += ["## Errores", ""] + ["- " + e for e in rep["errors"]] + [""]
    if rep["warnings"]:
        lines += ["## Avisos", ""] + ["- " + w for w in rep["warnings"]] + [""]
    lines += ["## Regiones", "", "| Región | Picos | Bytes | Olas | Viento | Puertos | Ajuste medio a la costa | Punto de olas |",
              "|---|---|---|---|---|---|---|---|"]
    for b in built:
        r = rep["regions"].get(b["code"])
        if r is None:                              # kept from the previous run
            lines.append("| %s | %d | %d | (anterior) | | | | |" % (b["code"], b["n"], b["bytes"]))
            continue
        sn = [s["snap"] for s in r["spots"] if s["snap"] is not None and not s["nosnap"]]
        lines.append("| %s | %d | %d | %s | %s | %d | %s | %d |" % (
            b["code"], b["n"], b["bytes"], r["models"][0], r["models"][1], r["ports"],
            "%.0f m" % (sum(sn) / len(sn)) if sn else "—", sum(1 for s in r["spots"] if s["wave"] is not None)))
    lines += ["", "## Emblemáticos (revisión a mano)", "",
              "| Región | Pico | Conf. | Ajuste a la costa | Orientación | Punto de olas |", "|---|---|---|---|---|---|"]
    for b in built:
        for s in rep["regions"].get(b["code"], {"spots": []})["spots"]:
            if s["top"]:
                lines.append("| %s | %s | %s | %s | %d° | %s |" % (
                    b["code"], s["name"], s["conf"], "—" if s["snap"] is None else "%.0f m" % s["snap"], s["facing"],
                    "—" if s["wave"] is None else "%.2f, %.2f" % tuple(s["wave"])))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--missing-tiles", action="store_true")
    a = ap.parse_args()
    conts, countries, regions = seeds.continents(), seeds.countries(), seeds.regions()
    if a.missing_tiles:
        pts = [(r["lat"], r["lon"]) for code in (a.regions or regions) for r in coast_rows(code, seeds.spots(code))]
        near = [(r["lat"], r["lon"]) for code in (a.regions or regions) for r in seeds.spots(code)]
        print(len(set(osm.missing_tiles(pts)) | set(osm.missing_tiles(near, shelter.BOX_DEG))))
        return
    models, ports = rule.read(), read_ports()
    want = a.regions or list(regions)
    rep = {"errors": [], "warnings": [], "regions": {}, "offline_waves": 0}
    old = previous()
    built = []
    for code in want:
        reg = regions.get(code)
        if reg is None:
            rep["errors"].append("%s is not in seeds/regions.csv" % code)
            continue
        try:
            b = build_region(code, reg, reg["country"], models, ports, a.offline, rep)
        except Exception as e:                     # noqa: BLE001 - one region must not stop the rest
            import traceback
            rep["errors"].append("%s: %s (%s)" % (code, type(e).__name__, traceback.format_exc().strip().splitlines()[-2].strip()[:160]))
            print("ERROR %s:\n%s" % (code, traceback.format_exc()), file=sys.stderr, flush=True)
            b = None
        if not b and code in old and old[code]["country"] == reg["country"]:
            b = old[code]                          # a region that could not be built (a server down) keeps
            rep["warnings"].append("%s: kept the previous version" % code)   # what the apps already have
        if b:
            built.append(b)
            print("%-11s %2d spots %5d bytes  v%s" % (code, b["n"], b["bytes"], b["v"]), flush=True)
    if a.regions:                                  # a partial run only rewrites its regions
        for b in built:
            write("r/%s.json" % b["code"], b["text"])
    else:
        for sub in ("r", "g", "idx"):
            shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
        for b in built:
            write("r/%s.json" % b["code"], b["text"])
        bycont = {}
        for b in built:
            bycont.setdefault(countries[b["country"]]["continent"], []).append(b)
        for cc, bs in bycont.items():
            cs = list(dict.fromkeys(b["country"] for b in bs))
            idx = {"c": [[c, countries[c]["name_es"], countries[c]["name_en"]] for c in cs],
                   "r": [[b["code"], b["country"], regions[b["code"]]["name_es"], regions[b["code"]]["name_en"],
                          b["lat"], b["lon"], b["km"], b["n"], b["bytes"], b["v"]] for b in bs]}
            write("idx/%s.json" % cc, dump(idx))
        order = sorted(bycont, key=lambda c: int(conts[c]["order"]))
        write("idx.json", dump({"v": 1, "c": [[c, conts[c]["name_es"], conts[c]["name_en"], len(bycont[c])] for c in order]}))
        grid = {}
        for b in built:
            for k in cells(b["lat"], b["lon"], b["km"]):
                grid.setdefault(k, []).append([b["code"], b["lat"], b["lon"], b["km"], b["v"]])
        for k, rows in grid.items():
            text = dump(rows)
            if len(text.encode()) > MAX_BYTES:
                rep["errors"].append("cell %s: %d bytes" % (k, len(text.encode())))
            write("g/%s.json" % k, text)
        write("report.md", report_md(rep, built))
    for w in rep["warnings"]:
        print("warning:", w)
    for e in rep["errors"]:
        print("ERROR:", e)
    print("%d regions, %d spots, %d errors, %d warnings" % (len(built), sum(b["n"] for b in built), len(rep["errors"]), len(rep["warnings"])))
    sys.exit(1 if a.strict and rep["errors"] else 0)


if __name__ == "__main__":
    main()
