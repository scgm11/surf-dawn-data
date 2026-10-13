#!/usr/bin/env python3
"""Builds spots/ (docs/formatos.md) from the seed tables (seeds/README.md): one file per
region, the continent indexes and the 10° cells the watch looks up by position.

For every spot: the position snapped to the OpenStreetMap coastline and the direction its
beach faces (tools/lib/osm.py, the rule tools/make_spots.py used), unless the seed says
`nosnap` / `facing=`; the wave point when the region's wave model has land in the spot's
cell (tools/lib/openmeteo.py, what tools/wave_points.py did); the break type from the seed.
Each region gets its Open-Meteo models (models.csv, else the default rule) and its tide
ports (tide/regions.json, written by tools/tide/).

The regions of Uruguay and Santa Catarina are frozen: their seeds carry the validated
positions, facings and wave points of 2026-10, and nothing is recomputed for them.

Usage: python3 tools/build_zones.py [--regions CODE ...] [--offline] [--strict]
  --offline  no downloads: only what is cached (spots that would need the network are reported)
  --strict   exit 1 on any error (CI); otherwise a region with errors is still written without
             the spots in error
"""
import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, osm, seeds  # noqa: E402

ROOT = seeds.ROOT
OUT = os.path.join(ROOT, "spots")
MAX_BYTES = 6144                     # per file: the face's background process has 64 KB
NEAR_KM = 25                         # Spots.RADIUS_KM on the watch: a region's circle reaches this far past its spots
CELL = 10                            # degrees of a lookup cell (spots/g/)
FROZEN = {"UY-MAL", "UY-ROC", "BR-SC-FLN", "BR-SC-SUL"}
FIXED = {"UY", "AR"}                 # countries fixed to today's models (issue #7: Windguru)
FIXED_REGIONS = {"BR-SC-FLN", "BR-SC-SUL", "BR-SC-NOR", "BR-RS"}
DEFAULT_WIND = "gfs_seamless"


def default_models(code, country, lat):
    if country in FIXED or code in FIXED_REGIONS:
        return ["ncep_gfswave025", DEFAULT_WIND]
    return ["ncep_gfswave016" if -15.0 <= lat <= 52.5 else "ncep_gfswave025", DEFAULT_WIND]


def read_models():
    path = os.path.join(ROOT, "models.csv")
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["region"]: [r["wave"], r["wind"]] for r in csv.DictReader(f)}


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


def build_region(code, reg, country, models, ports, offline, rep):
    rows = seeds.spots(code)
    if not rows:
        return None
    frozen = code in FROZEN
    errs, warns = rep["errors"], rep["warnings"]
    need_coast = [r for r in rows if not frozen and (not r["f"].get("nosnap") or "facing" not in r["f"])]
    ways = None
    if need_coast:
        cache_only = offline
        try:
            ways = osm.coastline(code, [(r["lat"], r["lon"]) for r in need_coast]) if not cache_only else _cached_coast(code, need_coast)
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
                      "conf": r["conf"], "nosnap": bool(f.get("nosnap")), "seed": (r["lat"], r["lon"])})
    if not spots:
        errs.append("%s: no spot left" % code)
        return None
    clat, clon = geo.center([(s["lat"], s["lon"]) for s in spots])
    m = models.get(code) or default_models(code, country, clat)
    if not frozen:
        todo = [s for s in spots if s["wave"] is None]
        if todo and not offline:
            from tools.lib import openmeteo
            try:
                wps = openmeteo.wave_points(m[0], [(s["lat"], s["lon"]) for s in todo])
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
    v = version(body)
    out = {"id": code, "v": v}
    out.update({k: body[k] for k in ("c", "n", "m", "p", "s")})
    text = dump(out)
    size = len(text.encode("utf-8"))
    if size > MAX_BYTES:
        errs.append("%s: %d bytes (max %d): split the region" % (code, size, MAX_BYTES))
    rep["regions"][code] = {"spots": spots, "models": m, "ports": len(body["p"]), "bytes": size}
    return {"code": code, "country": country, "v": v, "text": text, "bytes": size, "n": len(srows),
            "lat": round(clat, 3), "lon": round(clon, 3), "km": radius}


def _cached_coast(code, rows):
    """The coastline from the cache only (offline runs), or None."""
    pts = [(r["lat"], r["lon"]) for r in rows]
    boxes = osm._boxes(pts)
    key = hashlib.sha1(json.dumps([[round(v, 3) for v in b] for b in boxes]).encode()).hexdigest()[:10]
    path = os.path.join(osm.CACHE, "coast-%s-%s.json" % (code, key))
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


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
        r = rep["regions"][b["code"]]
        sn = [s["snap"] for s in r["spots"] if s["snap"] is not None and not s["nosnap"]]
        lines.append("| %s | %d | %d | %s | %s | %d | %s | %d |" % (
            b["code"], b["n"], b["bytes"], r["models"][0], r["models"][1], r["ports"],
            "%.0f m" % (sum(sn) / len(sn)) if sn else "—", sum(1 for s in r["spots"] if s["wave"] is not None)))
    lines += ["", "## Emblemáticos (revisión a mano)", "",
              "| Región | Pico | Conf. | Ajuste a la costa | Orientación | Punto de olas |", "|---|---|---|---|---|---|"]
    for b in built:
        for s in rep["regions"][b["code"]]["spots"]:
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
    a = ap.parse_args()
    conts, countries, regions = seeds.continents(), seeds.countries(), seeds.regions()
    models, ports = read_models(), read_ports()
    want = a.regions or list(regions)
    rep = {"errors": [], "warnings": [], "regions": {}, "offline_waves": 0}
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
            continue
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
