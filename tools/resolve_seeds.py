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

Usage: python3 tools/resolve_seeds.py [--regions CODE ...] [--dry-run]
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, osm, seeds  # noqa: E402

ROOT = seeds.ROOT
LOG = os.path.join(ROOT, "seeds", "resolve.log")
SEARCH_KM = 60
FAR_KM = 150
FROZEN = {"UY-MAL", "UY-ROC", "BR-SC-FLN", "BR-SC-SUL"}
PREFIXES = ["PRAIA DO ", "PRAIA DA ", "PRAIA DE ", "PRAIA ", "PLAYA DE ", "PLAYA DEL ", "PLAYA ", "BAHÍA DE ",
            "BAHÍA ", "BAIA ", "PUNTA DE ", "PUNTA ", "PONTA DO ", "PONTA DA ", "PONTA ", "CABO ", "PLAGE DE ",
            "PLAGE ", "PRAIA DOS ", "PRAIA DAS ", "BARRA DE ", "BARRA DO ", "BARRA ", "EL ", "LA ", "LOS ", "LAS ",
            "THE "]
SUFFIXES = [" BEACH", " POINT", " BAY", " REEF", " HEAD", " HEADS", " PIER", " RIGHT", " LEFT", " LEFTS",
            " RIGHTS", " BREAK", " INLET", " COVE"]
RANK = {"beach": 0, "surf": 0, "bay": 1, "cape": 1, "peninsula": 1, "headland": 1, "place": 2, "other": 3}
NOMINATIM = "https://nominatim.openstreetmap.org/search"


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def variants(name):
    out = [name]
    n = name
    for p in PREFIXES:
        if n.startswith(p) and len(n) > len(p) + 2:
            out.append(n[len(p):])
            break
    for s in SUFFIXES:
        for v in list(out):
            if v.endswith(s) and len(v) > len(s) + 2:
                out.append(v[:-len(s)])
    return list(dict.fromkeys(v.strip(" '.-") for v in out if len(v.strip()) >= 3))


def regex(v):
    """An Overpass regex for v that ignores accents (case is ignored by the query flag)."""
    alts = {"a": "[aáàâãä]", "e": "[eéèêë]", "i": "[iíìîï]", "o": "[oóòôõö]", "u": "[uúùûü]",
            "c": "[cç]", "n": "[nñ]", "y": "[yý]"}
    out = []
    for ch in fold(v):
        if ch in alts:
            out.append(alts[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in " -'.":
            out.append(".?")
        else:
            out.append(".")
    return "".join(out)


def kind(tags):
    nat, place = tags.get("natural", ""), tags.get("place", "")
    if nat == "beach" or tags.get("leisure") == "beach_resort":
        return "beach"
    if "surf" in tags.get("sport", "") or tags.get("surfing") or nat == "surf_break":
        return "surf"
    if nat in ("bay", "cape", "peninsula", "headland"):
        return nat
    if place:
        return "place"
    return "other"


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


def nominatim(names, cc):
    out = []
    for v in names[:2]:
        q = urllib.parse.urlencode({"q": v.title(), "countrycodes": cc.lower(), "format": "jsonv2", "limit": 10})
        try:
            req = urllib.request.Request(NOMINATIM + "?" + q, headers=osm.UA)
            res = json.loads(urllib.request.urlopen(req, timeout=60).read())
        except Exception as e:  # noqa: BLE001
            print("  nominatim failed (%s)" % str(e)[:80], file=sys.stderr)
            res = []
        time.sleep(1.2)                                    # Nominatim's policy: 1 request a second
        for r in res:
            t = {"natural": r.get("type", "")} if r.get("category") == "natural" else {}
            if r.get("category") == "place":
                t["place"] = r.get("type", "")
            if r.get("category") == "leisure":
                t["leisure"] = r.get("type", "")
            out.append({"lat": float(r["lat"]), "lon": float(r["lon"]), "name": r.get("name") or r.get("display_name", ""),
                        "kind": kind(t), "src": "osm:%s/%s" % (r.get("osm_type", "?"), r.get("osm_id", "?"))})
    return out


def matches(cand, names):
    f = fold(cand["name"])
    return any(fold(v) in f for v in names)


def resolve(code, row, cc):
    names = variants(row["name"])
    seed = (row["lat"], row["lon"])
    cands = [c for c in overpass(row["lat"], row["lon"], names) if matches(c, names)]
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
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    regions = seeds.regions()
    log = []
    fixed = unresolved = 0
    for code in a.regions or list(regions):
        if code in FROZEN:
            continue
        rows = seeds.spots(code)
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
            good, n = resolve(code, r, cc)
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
                    row[7] = (row[7] + "; " if row[7] else "") + "posición OSM"
        if not a.dry_run:
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f, lineterminator="\n").writerows(table)
    log.append("%d semillas movidas, %d sin resolver" % (fixed, unresolved))
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
