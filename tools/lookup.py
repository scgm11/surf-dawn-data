#!/usr/bin/env python3
"""What the public sources have under a spot's name around it, for a review by hand (issue #7, §5.8):
the flagship spots that tools/check_spots.py found no source for, or found far from theirs.

For each spot, within --km of its published position (spots/r) and named like it (tools/lib/names.py),
or like one of the distinctive words of its name:
- Wikidata: items with coordinates, with what they are (P31) — a beach, a village, a hotel...
- Wikipedia (en): articles with coordinates (geosearch, 10 km at most).
- GeoNames: the country's places of any kind (beaches, reefs, points, villages, hotels...).
- Nominatim: OpenStreetMap's search in the country (up to 60 km).
- Overpass (--overpass): OSM features around it (slow; often busy).

Writes validation/lookup.md (a table per spot, nearest first). Nothing is changed: a better position
goes into the seed by hand, with its source in `src`.

Usage: python3 tools/lookup.py [--km 15] [--overpass] [REGION/NAME ...]
  without names: the flagships "sin fuente" or "lejos" in validation/spots.json
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, geonames, osm, seeds  # noqa: E402
from tools.lib.names import GENERIC, key, matches, regex, variants  # noqa: E402

ROOT = seeds.ROOT
OUT = os.path.join(ROOT, "validation")
WD = "https://query.wikidata.org/sparql"
WP = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)"}
NOMINATIM_KM = 60
WORDS_SKIP = GENERIC | {"BEACH", "POINT", "REEF", "BAY", "HEAD", "PIER", "RIGHT", "LEFT", "RIGHTS", "LEFTS", "BREAK",
                        "PLAYA", "PRAIA", "PLAGE", "PUNTA", "PONTA", "THE", "LES", "LOS", "LAS", "DEL", "DOS",
                        "DAS", "HARBOR", "HARBOUR", "STREET", "ROCK", "ROCKS", "POOL", "POOLS", "PEAKS", "SPIT"}


def names_for(name):
    """The name's variants, and its distinctive words (4 letters or more) on their own."""
    out = variants(name)
    for w in key(name).upper().split():
        if len(w) >= 4 and w not in WORDS_SKIP:
            out.append(w)
    return list(dict.fromkeys(out))


def get(url, data=None, timeout=90, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data, UA)
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        except Exception as e:  # noqa: BLE001 - busy endpoint: retry
            print("  %s failed (%s)" % (url.split("?")[0], str(e)[:80]), file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return None


def wikidata(lat, lon, names, km):
    rx = "|".join(regex(v) for v in names).replace("\\", "\\\\").replace('"', '\\"')
    q = """SELECT ?item ?label ?coord (GROUP_CONCAT(DISTINCT ?tl; separator=", ") AS ?types) WHERE {
      SERVICE wikibase:around { ?item wdt:P625 ?coord . bd:serviceParam wikibase:center "Point(%f %f)"^^geo:wktLiteral .
                                bd:serviceParam wikibase:radius "%d" . }
      ?item rdfs:label ?label . FILTER(REGEX(STR(?label), "%s", "i"))
      OPTIONAL { ?item wdt:P31 ?t . ?t rdfs:label ?tl . FILTER(LANG(?tl) = "en") }
    } GROUP BY ?item ?label ?coord LIMIT 300""" % (lon, lat, km, rx)
    data = get(WD + "?" + urllib.parse.urlencode({"query": q, "format": "json"}))
    time.sleep(1.0)
    if data is None:
        return None
    out, seen = [], set()
    for b in data["results"]["bindings"]:
        wkt = b["coord"]["value"]
        try:
            x, y = wkt[wkt.index("(") + 1:wkt.index(")")].split()
        except ValueError:
            continue
        qid = b["item"]["value"].rsplit("/", 1)[-1]
        label = b["label"]["value"]
        if qid in seen or not matches(label, names):
            continue
        seen.add(qid)
        out.append({"name": label, "lat": float(y), "lon": float(x), "kind": b.get("types", {}).get("value", ""),
                    "link": "[%s](https://www.wikidata.org/wiki/%s)" % (qid, qid)})
    return out


def wikipedia(lat, lon, names, km):
    q = urllib.parse.urlencode({"action": "query", "list": "geosearch", "gscoord": "%f|%f" % (lat, lon),
                                "gsradius": int(min(km, 10) * 1000), "gslimit": 500, "format": "json"})
    data = get(WP + "?" + q)
    if data is None:
        return None
    out = []
    for p in data.get("query", {}).get("geosearch", []):
        if matches(p["title"], names):
            t = p["title"].replace(" ", "_")
            out.append({"name": p["title"], "lat": p["lat"], "lon": p["lon"], "kind": "artículo",
                        "link": "[en.wikipedia](https://en.wikipedia.org/wiki/%s)" % urllib.parse.quote(t)})
    return out


def geonames_all(lat, lon, names, cc, km):
    """GeoNames places of any kind (not only the ones geonames.RANK keeps)."""
    path = geonames.path(cc)
    if not path:
        return None
    want = [key(v) for v in names if len(key(v)) >= 3]
    out = []
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if len(r) < 9:
                continue
            la, lo = float(r[4]), float(r[5])
            if abs(la - lat) > km / 100.0 or geo.km((lat, lon), (la, lo)) > km:
                continue
            all_names = {key(r[1]), key(r[2])} | {key(a) for a in r[3].split(",") if a}
            if any(w in n or (len(n) >= 4 and n in w) for w in want for n in all_names):
                out.append({"name": r[1], "lat": la, "lon": lo, "kind": "%s.%s" % (r[6], r[7]),
                            "link": "[geonames:%s](https://www.geonames.org/%s)" % (r[0], r[0])})
    return out


def nominatim(lat, lon, names, cc):
    out = []
    for c in osm.nominatim(names, cc):
        if geo.km((lat, lon), (c["lat"], c["lon"])) <= NOMINATIM_KM and matches(c["name"], names):
            t, i = c["src"].split(":", 1)[-1].split("/")
            out.append({"name": c["name"], "lat": c["lat"], "lon": c["lon"], "kind": c["kind"],
                        "link": "[osm:%s/%s](https://www.openstreetmap.org/%s/%s)" % (t, i, t, i)})
    return out


def overpass(lat, lon, names, km):
    try:
        cands = osm.named_near(lat, lon, names, km, tries=2)
    except RuntimeError:
        return None
    out = []
    for c in cands:
        if matches(c["name"], names):
            t, i = c["src"].split(":", 1)[-1].split("/")
            out.append({"name": c["name"], "lat": c["lat"], "lon": c["lon"], "kind": c["kind"],
                        "link": "[osm:%s/%s](https://www.openstreetmap.org/%s/%s)" % (t, i, t, i)})
    return out


def published(code, name):
    with open(os.path.join(ROOT, "spots", "r", code + ".json"), encoding="utf-8") as f:
        z = json.load(f)
    for s in z["s"]:
        if s[0] == name:
            return z, s
    return z, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--km", type=float, default=15)
    ap.add_argument("--overpass", action="store_true")
    a = ap.parse_args()
    todo = []
    if a.names:
        todo = [tuple(n.split("/", 1)) for n in a.names]
    else:
        with open(os.path.join(OUT, "spots.json"), encoding="utf-8") as f:
            for c in json.load(f).get("flagship", []):
                if c.get("status") in ("sin fuente", "lejos"):
                    todo.append((c["region"], c["spot"]))
    lines = ["# Picos: búsqueda por nombre en fuentes públicas", "",
             "Generado %s por `tools/lookup.py` (issue #7, §5.8), a %g km de cada pico: lo que tienen Wikidata, "
             "Wikipedia, GeoNames y OpenStreetMap con su nombre o una de sus palabras. Sirve para revisar a mano "
             "los emblemáticos sin fuente o lejos de la suya (`validation/spots.md`): una posición mejor va a la "
             "semilla con su fuente en `src`." % (time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), a.km), ""]
    seed_rows = {}
    for code, name in todo:
        if code not in seed_rows:
            seed_rows[code] = {r["name"]: r for r in seeds.spots(code)}
        z, s = published(code, name)
        r = seed_rows[code].get(name)
        if s is None and r is None:
            lines += ["## %s/%s" % (code, name), "", "No está en las semillas ni en la zona.", ""]
            continue
        lat, lon = (s[1], s[2]) if s else (r["lat"], r["lon"])
        cc = z["c"]
        names = names_for(name)
        print("%s/%s %s" % (code, name, names), flush=True)
        lines += ["## %s/%s" % (code, name), "",
                  "Publicado en %.4f, %.4f ([mapa](https://www.openstreetmap.org/?mlat=%.5f&mlon=%.5f#map=14/%.5f/%.5f)). "
                  "Semilla: %s, confianza %s, fuente `%s`%s. Se buscó: %s." % (
                      lat, lon, lat, lon, lat, lon, r and "%.4f, %.4f" % (r["lat"], r["lon"]) or "?", r and r["conf"] or "?",
                      r and r["src"] or "?", r and r["note"] and " (%s)" % r["note"] or "",
                      ", ".join("«%s»" % n for n in names)), ""]
        found, missing = [], []
        for label, res in (("Wikidata", wikidata(lat, lon, names, a.km)),
                           ("Wikipedia", wikipedia(lat, lon, names, a.km)),
                           ("GeoNames", geonames_all(lat, lon, names, cc, a.km)),
                           ("Nominatim", nominatim(lat, lon, names, cc)),
                           ("Overpass", overpass(lat, lon, names, a.km) if a.overpass else [])):
            if res is None:
                missing.append(label)
                continue
            for c in res:
                c["source"] = label
                c["km"] = geo.km((lat, lon), (c["lat"], c["lon"]))
                found.append(c)
        found.sort(key=lambda c: c["km"])
        if found:
            lines += ["| km | Fuente | Nombre | Qué es | Posición | Ítem |", "|---|---|---|---|---|---|"]
            for c in found[:25]:
                lines.append("| %.1f | %s | %s | %s | %.5f, %.5f | %s |" % (
                    c["km"], c["source"], c["name"].replace("|", "/"), (c["kind"] or "").replace("|", "/")[:60],
                    c["lat"], c["lon"], c["link"]))
            if len(found) > 25:
                lines.append("| | | … y %d más | | | |" % (len(found) - 25))
        else:
            lines.append("Nada con ese nombre.")
        if missing:
            lines += ["", "Sin respuesta: %s." % ", ".join(missing)]
        lines.append("")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "lookup.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("%d spots looked up" % len(todo))


if __name__ == "__main__":
    main()
