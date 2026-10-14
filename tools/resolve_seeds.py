#!/usr/bin/env python3
"""Fixes the seeds that build_zones.py cannot place: a seed more than osm.SNAP_MAX_M from any
coastline (and not marked `nosnap`) is looked up by name in OpenStreetMap, and moved to the
named feature that is on the coast.

For each such seed:
1. Name variants: the seed name, and without a leading "PRAIA DE", "PLAYA", "BAHÍA"... (the
   distinctive part), matched without case or accents.
2. Candidates: OSM features with that name within SEARCH_KM of the seed (Overpass: beaches,
   bays, capes, places, surf spots, beach resorts), plus Nominatim's search in the seed's
   country (catches a seed with a wrong sign or a typo in a coordinate, up to FAR_KM away).
3. A candidate counts only if it is within osm.SNAP_MAX_M / 2 of the coastline. The best one is
   a beach or surf spot before a bay or cape, before a place; then the nearest to the seed.
4. The seed row gets the candidate's position (4 decimals), `src=osm:<type>/<id>` and the note
   "posición OSM"; its confidence becomes K.

Seeds with no candidate are listed for a fix by hand. Everything goes to seeds/resolve.log.

Usage: python3 tools/resolve_seeds.py [--regions CODE ...] [--names REGION/NAME ...] [--no-overpass] [--dry-run]
  --names        these seeds are looked up even if they are on the coast (a position without a
                 source: it gets the OSM feature's), and only them
  --no-overpass  candidates from Nominatim only (Overpass's name search is the slow part)
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, osm, seeds  # noqa: E402
from tools.lib.osm import kind, nominatim  # noqa: E402
from tools.lib.names import fold, regex, variants  # noqa: E402

ROOT = seeds.ROOT
LOG = os.path.join(ROOT, "seeds", "resolve.log")
SEARCH_KM = 60
FAR_KM = 150
FROZEN = {"UY-MAL", "UY-ROC", "BR-SC-FLN", "BR-SC-SUL"}
RANK = {"beach": 0, "surf": 0, "bay": 1, "cape": 1, "peninsula": 1, "headland": 1, "place": 2, "other": 3}


def overpass(lat, lon, names):
    rx = "|".join(regex(v) for v in names)
    q = ('[out:json][timeout:90];('
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["natural"~"^(beach|bay|cape|peninsula|headland)$"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["place"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["sport"~"surf"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["leisure"="beach_resort"];'
         ');out center tags;').format(r=SEARCH_KM * 1000, la=lat, lo=lon, rx=rx)
    body = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(6):
        url = osm.MIRRORS[attempt % len(osm.MIRRORS)]
        try:
            req = urllib.request.Request(url, body, osm.UA)
            data = json.loads(urllib.request.urlopen(req, timeout=120).read())
            out = []
            for e in data.get("elements", []):
                c = e.get("center") or e
                if "lat" in c:
                    t = e.get("tags", {})
                    out.append({"lat": c["lat"], "lon": c["lon"], "name": t.get("name", ""), "kind": kind(t),
                                "src": "osm:%s/%d" % (e["type"], e["id"])})
            time.sleep(1.5)
            return out
        except Exception as e:  # noqa: BLE001
            print("  overpass %s failed (%s)" % (url.split("/")[2], str(e)[:80]), file=sys.stderr)
            time.sleep(8 + 8 * attempt)
    return []


def matches(cand, names):
    f = fold(cand["name"])
    return any(fold(v) in f for v in names)


def resolve(code, row, cc, use_overpass=True):
    names = variants(row["name"])
    seed = (row["lat"], row["lon"])
    cands = [c for c in overpass(row["lat"], row["lon"], names) if matches(c, names)] if use_overpass else []
    cands += [c for c in nominatim(names, cc) if matches(c, names) and geo.km(seed, (c["lat"], c["lon"])) <= FAR_KM]
    seen, good = set(), []
    for c in cands:
        k = (round(c["lat"], 3), round(c["lon"], 3))
        if k in seen:
            continue
        seen.add(k)
        try:
            ways = osm.coastline("resolve-%s" % code, [(c["lat"], c["lon"])])
        except RuntimeError:
            continue
        s = osm.snap(c["lat"], c["lon"], ways)
        if s is None or s[0] > osm.SNAP_MAX_M / 2:
            continue
        full = fold(row["name"]) in fold(c["name"]) or fold(c["name"]) in fold(row["name"])
        good.append((0 if full else 1, RANK.get(c["kind"], 3), geo.km(seed, (c["lat"], c["lon"])), s[0], c))
    good.sort(key=lambda g: (g[0], g[1], g[2]))
    return good, len(cands)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--no-overpass", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    regions = seeds.regions()
    named = {}
    for n in a.names or []:
        code, _, name = n.partition("/")
        named.setdefault(code, set()).add(name)
    log = []
    fixed = unresolved = 0
    for code in (list(named) if named else a.regions or list(regions)):
        if code in FROZEN:
            continue
        rows = seeds.spots(code)
        if named:
            far = [(r, None) for r in rows if r["name"] in named[code]]
            missing = named[code] - {r["name"] for r in rows}
            log += ["NO ESTÁ %s/%s" % (code, n) for n in sorted(missing)]
        else:
            bad = [r for r in rows if not r["f"].get("nosnap")]
            if not bad:
                continue
            try:
                ways = osm.coastline(code, [(r["lat"], r["lon"]) for r in bad])
            except RuntimeError as e:
                log.append("%s: %s" % (code, e))
                continue
            far = []
            for r in bad:
                s = osm.snap(r["lat"], r["lon"], ways)
                if s is None or s[0] > osm.SNAP_MAX_M:
                    far.append((r, None if s is None else s[0]))
        if not far:
            continue
        path = os.path.join(seeds.SEEDS, "spots", code + ".csv")
        with open(path, newline="", encoding="utf-8") as f:
            table = list(csv.reader(f))
        cc = regions[code]["country"]
        for r, d in far:
            good, n = resolve(code, r, cc, not a.no_overpass)
            where = "%s/%s (%.4f, %.4f; costa a %s)" % (code, r["name"], r["lat"], r["lon"],
                                                       "?" if d is None else "%.0f m" % d)
            if not good:
                unresolved += 1
                log.append("SIN RESOLVER %s: %d candidatos por nombre, ninguno en la costa" % (where, n))
                continue
            _, rank, km_, snap_m, c = good[0]
            fixed += 1
            log.append("OK %s -> %.4f, %.4f (%s, %s %r, a %.1f km de la semilla, costa a %.0f m)" % (
                where, c["lat"], c["lon"], c["src"], c["kind"], c["name"], km_, snap_m))
            for row in table[1:]:
                if row and row[0] == r["name"]:
                    row[1], row[2] = "%.4f" % c["lat"], "%.4f" % c["lon"]
                    row[4] = "K" if row[4] == "L" else row[4]
                    row[5] = c["src"]
                    keep = [x for x in row[7].split("; ") if x and not re.search(
                        r"GSHHS|sin fuente|aprox|dudosa|estimada|buscar por nombre", x)]
                    row[7] = "; ".join(keep + ["posición OSM"])
        if not a.dry_run:
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f, lineterminator="\n").writerows(table)
    log.append("%d semillas movidas, %d sin resolver" % (fixed, unresolved))
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
