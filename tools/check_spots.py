#!/usr/bin/env python3
"""Checks every spot of spots/ the way issue #7 §5 asks, and writes validation/spots.md and
validation/spots.json (docs/formatos.md):

- §5.2 Facing: the waves of the spot's own wave point over the last DAYS days (its zone's model,
  Open-Meteo Marine). A spot whose waves almost never come from within FACING_DEG of the way its
  beach faces (under NEVER of the hours) while its zone's spots do (at least NEIGHBOURS) is looked at
  again over LONG_DAYS (a season can hide a swell window); still so, it is flagged: that is usually a
  facing computed on the wrong side of a headland or a lagoon, or a point the swell wraps into.
- §5.4 Neighbours: a spot whose waves are 0 m (or missing) all along, or more than twice its
  zone's median, is flagged.
- §5.8 Flagship spots (`top` in the seeds): their position against Wikidata, a public source: the
  nearest item within WD_KM whose name matches the spot's (tools/lib/names.py); without one, against
  OpenStreetMap (Nominatim, in the spot's country). Farther than WD_FAR_KM is flagged; with neither
  it is "sin fuente" (to check by hand).

Open-Meteo is asked once per wave grid cell (spots of a cell share their waves), several cells per
request, paced well under the free limits. Usage: python3 tools/check_spots.py [--regions CODE ...]
[--no-wikidata]
"""
import argparse
import glob
import json
import math
import os
import statistics
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.lib import geo, openmeteo, osm, seeds  # noqa: E402
from tools.lib.names import matches, regex, variants  # noqa: E402

ROOT = seeds.ROOT
OUT = os.path.join(ROOT, "validation")
DAYS = 14                       # past days of waves (plus FORECAST days ahead)
LONG_DAYS = 92                  # the spots flagged for their facing, looked at again over this many
FORECAST = 2
FACING_DEG = 75                 # waves within this of the beach's facing reach it (issue #7 §5.2)
NEVER = 0.05                    # "almost never": under this share of the hours with waves
NEIGHBOURS = 0.25               # ... while the zone's median spot gets them at least this often
MIN_H = 0.3                     # m: hours with less are not counted for the direction
DOUBLE = 2.0                    # more than this times the zone's median mean height (§5.4)
BATCH = 40                      # locations per Open-Meteo request
NEAR_KM = 30                    # neighbours whose facing a spot's is compared with
FLIPPED = 135                   # a facing this far from its neighbours' and the waves', and close to them
                                # turned around, was most likely computed on the wrong side of the coast
WD = "https://query.wikidata.org/sparql"
WD_KM = 6                       # Wikidata items looked at around a flagship spot
WD_FAR_KM = 1.5                 # farther than this from the matching item: flagged
OVERPASS_MIN = 25                # minutes of Overpass name searches per run (it is often busy)
OVERPASS_UNTIL = [time.time() + OVERPASS_MIN * 60]
UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)",
      "Accept": "application/sparql-results+json"}


def ang(a, b):
    d = abs(a - b) % 360
    return 360 - d if d > 180 else d


def zones(only):
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "spots", "r", "*.json"))):
        with open(path, encoding="utf-8") as f:
            z = json.load(f)
        if not only or z["id"] in only:
            out.append(z)
    return out


def cell(model, lat, lon):
    dlat, dlon = openmeteo.STEP.get(model, (0.25, 0.25))
    return model, round(lat / dlat), round(geo.wrap(lon) / dlon)


def fetch_waves(zs, used, days=DAYS, only=None):
    """{(model, i, j): (heights, directions)} for the wave cell of every spot (only: those (zone, name))."""
    want = {}
    for z in zs:
        model = z["m"][0]
        for s in z["s"]:
            if only is not None and (z["id"], s[0]) not in only:
                continue
            lat, lon = (s[5], s[6]) if len(s) == 7 else (s[1], s[2])
            want.setdefault(cell(model, lat, lon), (lat, lon))
    out = {}
    by_model = {}
    for k, p in want.items():
        by_model.setdefault(k[0], []).append((k, p))
    for model, items in by_model.items():
        for i in range(0, len(items), BATCH):
            part = items[i:i + BATCH]
            params = {"latitude": ",".join("%.4f" % p[0] for _, p in part),
                      "longitude": ",".join("%.4f" % p[1] for _, p in part),
                      "hourly": "wave_height,wave_direction", "models": model, "past_days": days,
                      "forecast_days": FORECAST, "timeformat": "unixtime", "timezone": "GMT"}
            res = openmeteo.get_json(params)
            used["calls"] += openmeteo.call_weight(len(part), 2, days + FORECAST)
            used["requests"] += 1
            if isinstance(res, dict):
                print("  open-meteo refused %s x%d: %s" % (model, len(part), res.get("reason")), file=sys.stderr)
                continue
            for (k, _), b in zip(part, res):
                h = (b.get("hourly") or {}) if isinstance(b, dict) else {}
                out[k] = (h.get("wave_height") or [], h.get("wave_direction") or [])
            time.sleep(1.5)
    return out


def spot_stats(series, facing):
    hs, ds = series
    vals = [h for h in hs if isinstance(h, (int, float))]
    mean = sum(vals) / len(vals) if vals else None
    hours = [(h, d) for h, d in zip(hs, ds) if isinstance(h, (int, float)) and isinstance(d, (int, float)) and h >= MIN_H]
    share = sum(1 for _, d in hours if ang(d, facing) < FACING_DEG) / len(hours) if hours else None
    x = sum(h * math.sin(math.radians(d)) for h, d in hours)
    y = sum(h * math.cos(math.radians(d)) for h, d in hours)
    swell = round(math.degrees(math.atan2(x, y)) % 360) if hours else None   # where the waves come from, mostly
    return {"mean": mean, "max": max(vals) if vals else None, "share": share, "hours": len(hours), "swell": swell}


def neighbours_facing(z, i, km=NEAR_KM):
    """The circular median-ish (mean of unit vectors) facing of the zone's other spots within km of spot i."""
    s = z["s"][i]
    fs = [r[3] for k, r in enumerate(z["s"]) if k != i and geo.km((s[1], s[2]), (r[1], r[2])) <= km]
    if len(fs) < 2:
        return None
    x = sum(math.sin(math.radians(f)) for f in fs)
    y = sum(math.cos(math.radians(f)) for f in fs)
    if math.hypot(x, y) < 0.5 * len(fs):
        return None                                  # they face every way (an island, a cape): no reference
    return round(math.degrees(math.atan2(x, y)) % 360)


def wikidata(lat, lon, names):
    """Items with coordinates within WD_KM whose label matches one of the names (accents and case
    aside): [(label, lat, lon, qid)]."""
    rx = "|".join(regex(v) for v in names).replace("\\", "\\\\").replace('"', '\\"')
    q = """SELECT ?item ?label ?coord WHERE {
      SERVICE wikibase:around { ?item wdt:P625 ?coord . bd:serviceParam wikibase:center "Point(%f %f)"^^geo:wktLiteral .
                                bd:serviceParam wikibase:radius "%d" . }
      ?item rdfs:label ?label . FILTER(REGEX(STR(?label), "%s", "i"))
    } LIMIT 500""" % (lon, lat, WD_KM, rx)
    url = WD + "?" + urllib.parse.urlencode({"query": q, "format": "json"})
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = json.loads(urllib.request.urlopen(req, timeout=90).read())
            out = []
            for b in data["results"]["bindings"]:
                wkt = b["coord"]["value"]                    # Point(lon lat)
                try:
                    x, y = wkt[wkt.index("(") + 1:wkt.index(")")].split()
                except ValueError:
                    continue
                out.append((b["label"]["value"], float(y), float(x), b["item"]["value"].rsplit("/", 1)[-1]))
            time.sleep(1.0)
            return out
        except Exception as e:  # noqa: BLE001 - busy endpoint: retry
            print("  wikidata failed (%s), retrying" % str(e)[:80], file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return None


def check_flagship(code, s, cc):
    names = variants(s[0])
    items = wikidata(s[1], s[2], names)
    if items is None:
        return {"status": "error"}
    if not any(matches(i[0], names) for i in items):          # not in Wikidata: OpenStreetMap
        items = [(c["name"], c["lat"], c["lon"], c["src"]) for c in osm.nominatim(names, cc)
                 if geo.km((s[1], s[2]), (c["lat"], c["lon"])) <= WD_KM]
    if not any(matches(i[0], names) for i in items) and time.time() < OVERPASS_UNTIL[0]:
        # nor Nominatim: OSM features around it (Overpass, when it answers: a time budget for the run)
        items = [(c["name"], c["lat"], c["lon"], c["src"]) for c in osm.named_near(s[1], s[2], names, WD_KM, tries=2)]
    best = None
    for label, lat, lon, qid in items:
        if matches(label, names):
            d = geo.km((s[1], s[2]), (lat, lon))
            if best is None or d < best["km"]:
                best = {"km": round(d, 2), "qid": qid, "label": label, "wd_lat": round(lat, 5), "wd_lon": round(lon, 5)}
    if best is None:
        return {"status": "sin fuente"}
    best["status"] = "ok" if best["km"] <= WD_FAR_KM else "lejos"
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--no-wikidata", action="store_true")
    a = ap.parse_args()
    zs = zones(set(a.regions or []))
    tops, checked = {}, set()
    for z in zs:
        for r in seeds.spots(z["id"]):
            tops[(z["id"], r["name"])] = bool(r["f"].get("top"))
            if r["f"].get("checked"):
                checked.add((z["id"], r["name"]))
    used = {"calls": 0.0, "requests": 0}
    waves = fetch_waves(zs, used)
    result = {"days": DAYS + FORECAST, "facing_deg": FACING_DEG, "regions": {}, "flags": [], "flagship": []}
    for z in zs:
        model = z["m"][0]
        rows = []
        for i, s in enumerate(z["s"]):
            lat, lon = (s[5], s[6]) if len(s) == 7 else (s[1], s[2])
            st = spot_stats(waves.get(cell(model, lat, lon), ([], [])), s[3])
            st["name"] = s[0]
            st["facing"] = s[3]
            st["near"] = neighbours_facing(z, i)
            rows.append(st)
        means = [r["mean"] for r in rows if r["mean"]]
        shares = [r["share"] for r in rows if r["share"] is not None]
        med = statistics.median(means) if means else None
        med_share = statistics.median(shares) if shares else None
        result["regions"][z["id"]] = {"model": model, "median_m": med and round(med, 2),
                                      "median_share": med_share and round(med_share, 2)}
        for r in rows:
            why = []
            if r["max"] is None or r["max"] < 0.05:
                why.append("sin olas en %d días" % (DAYS + FORECAST))
            elif med and r["mean"] > DOUBLE * med:
                why.append("%.1f m de media, más del doble de la zona (%.1f m)" % (r["mean"], med))
            flipped = False
            if r["share"] is not None and r["share"] < NEVER and med_share is not None and med_share >= NEIGHBOURS:
                why.append("las olas casi nunca le entran de frente (%d %% de las horas; la zona %d %%)"
                           % (round(100 * r["share"]), round(100 * med_share)))
                f, n, w = r["facing"], r["near"], r["swell"]
                flipped = (n is not None and w is not None and ang(f, n) >= FLIPPED and ang(f, w) >= FLIPPED
                           and ang((f + 180) % 360, n) <= 180 - FLIPPED)
            if why:
                result["flags"].append({"region": z["id"], "spot": r["name"], "why": why, "facing": r["facing"],
                                        "swell": r["swell"], "near": r["near"], "flipped": flipped,
                                        "top": tops.get((z["id"], r["name"]), False)})
        print("%-11s %2d spots  media %s m  de frente %s" % (z["id"], len(rows), med and "%.1f" % med,
                                                              med_share is not None and "%d %%" % round(100 * med_share)))
    # the facing flags, again over a season
    facing_flags = {(f["region"], f["spot"]): f for f in result["flags"] if any("de frente" in w for w in f["why"])}
    if facing_flags:
        long = fetch_waves(zs, used, LONG_DAYS, set(facing_flags))
        for z in zs:
            for s in z["s"]:
                f = facing_flags.get((z["id"], s[0]))
                if f is None:
                    continue
                lat, lon = (s[5], s[6]) if len(s) == 7 else (s[1], s[2])
                st = spot_stats(long.get(cell(z["m"][0], lat, lon), ([], [])), s[3])
                f["share_long"] = st["share"]
                if st["share"] is not None and st["share"] >= NEVER:
                    f["why"] = [w for w in f["why"] if "de frente" not in w]
                    f["flipped"] = False
                else:
                    f["why"] = [w + (" y en %d días %d %%" % (LONG_DAYS, round(100 * st["share"])) if "de frente" in w
                                     and st["share"] is not None else "") for w in f["why"]]
        cleared = sum(1 for f in facing_flags.values() if not f["why"])
        result["flags"] = [f for f in result["flags"] if f["why"]]
        result["season_cleared"] = cleared
        print("%d facing flags cleared over %d days" % (cleared, LONG_DAYS))
    if a.no_wikidata:                              # the last run's, as they were
        try:
            with open(os.path.join(OUT, "spots.json"), encoding="utf-8") as f:
                result["flagship"] = json.load(f).get("flagship", [])
        except (OSError, ValueError):
            pass
        for c in result["flagship"]:
            if c.get("status") in ("lejos", "revisado"):
                c["status"] = "revisado" if (c["region"], c["spot"]) in checked else "lejos"
    else:
        OVERPASS_UNTIL[0] = time.time() + OVERPASS_MIN * 60
        for z in zs:
            for s in z["s"]:
                if tops.get((z["id"], s[0])):
                    c = check_flagship(z["id"], s, z["c"])
                    if c["status"] == "lejos" and (z["id"], s[0]) in checked:
                        c["status"] = "revisado"            # the item is a town, a hotel, another wave... (seed flag)
                    c.update({"region": z["id"], "spot": s[0], "lat": s[1], "lon": s[2]})
                    result["flagship"].append(c)
                    print("  %s/%s: %s %s" % (z["id"], s[0], c["status"], c.get("km", "")))
    result["open_meteo"] = {"requests": used["requests"], "calls": round(used["calls"])}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "spots.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "spots.md"), "w", encoding="utf-8") as f:
        f.write(report(result, zs))
    print("%d spots flagged; flagship: %s; Open-Meteo %d requests, ~%d calls" % (
        len(result["flags"]), {k: sum(1 for c in result["flagship"] if c["status"] == k)
                                for k in ("ok", "lejos", "sin fuente", "error")},
        used["requests"], used["calls"]))


def report(r, zs):
    n = sum(len(z["s"]) for z in zs)
    fl = r["flagship"]
    count = {k: sum(1 for c in fl if c["status"] == k) for k in ("ok", "lejos", "revisado", "sin fuente", "error")}
    L = ["# Picos: controles por pico", "",
         "Generado %s UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). %d regiones, %d picos." % (
             time.strftime("%Y-%m-%d %H:%M", time.gmtime()), len(zs), n), "",
         "- **Orientación (§5.2):** olas de los últimos %d días y los próximos %d en el punto de olas de cada pico "
         "(el modelo de su zona). Se marca un pico al que las olas de al menos %.1f m casi nunca le llegan a menos "
         "de %d° de hacia donde mira (menos del %d %% de las horas) mientras a su zona sí (al menos %d %%)." % (
             DAYS, FORECAST, MIN_H, FACING_DEG, round(100 * NEVER), round(100 * NEIGHBOURS)),
         "- **Temporada:** los marcados por la orientación se miran de nuevo con %d días de olas; %d dejaron de "
         "estarlo (en dos semanas no les tocaba su ventana de swell)." % (LONG_DAYS, r.get("season_cleared", 0)),
         "- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media "
         "de su zona.",
         "- **Emblemáticos (§5.8):** la posición contra Wikidata (el ítem más cercano con su nombre, hasta %d km; "
         "si no tiene, OpenStreetMap): %d bien (a menos de %.1f km), %d lejos, %d lejos pero revisados a mano (el "
         "ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), %d sin fuente (revisar a mano), "
         "%d sin respuesta." % (
             WD_KM, count["ok"], WD_FAR_KM, count["lejos"], count["revisado"], count["sin fuente"], count["error"]),
         "- Open-Meteo: %d pedidos, ~%d llamadas de las 10.000 diarias gratuitas." % (
             r["open_meteo"]["requests"], r["open_meteo"]["calls"]), ""]
    flipped = [f for f in r["flags"] if f.get("flipped")]
    L += ["## Orientación probablemente del lado equivocado (%d)" % len(flipped), "",
          "Mira a más de %d° de sus vecinos (a %d km) y de las olas, y dada vuelta coincide con ellos: casi seguro "
          "se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla." % (
              FLIPPED, NEAR_KM), ""]
    if flipped:
        L += ["| Región | Pico | Mira a | Vecinos | Olas desde |", "|---|---|---|---|---|"]
        for f in flipped:
            L.append("| %s | %s | %d° | %d° | %d° |" % (f["region"], f["spot"], f["facing"], f["near"], f["swell"]))
    else:
        L.append("Ninguno.")
    L += ["", "## Picos marcados (%d)" % len(r["flags"]), "",
          "Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y "
          "el semáforo del swell es conservador ahí); se revisan a mano.", ""]
    if r["flags"]:
        L += ["| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |", "|---|---|---|---|---|---|---|"]
        for f in r["flags"]:
            L.append("| %s | %s | %s | %s° | %s | %s | %s |" % (
                f["region"], f["spot"], "sí" if f["top"] else "", f["facing"],
                "—" if f["swell"] is None else "%d°" % f["swell"], "—" if f["near"] is None else "%d°" % f["near"],
                "; ".join(f["why"])))
    else:
        L.append("Ninguno.")
    L += ["", "## Emblemáticos lejos de su ítem de Wikidata u OpenStreetMap", ""]
    far = [c for c in fl if c["status"] == "lejos"]
    if far:
        L += ["| Región | Pico | Distancia | Ítem |", "|---|---|---|---|"]
        for c in sorted(far, key=lambda c: -c["km"]):
            ref = c["qid"]
            link = ("https://www.wikidata.org/wiki/%s" % ref if ref.startswith("Q")
                    else "https://www.openstreetmap.org/%s" % ref.split(":", 1)[-1])
            L.append("| %s | %s | %.1f km | [%s](%s) %s (%s, %s) |" % (
                c["region"], c["spot"], c["km"], ref, link, c["label"], c.get("wd_lat"), c.get("wd_lon")))
    else:
        L.append("Ninguno.")
    L += ["", "## Emblemáticos sin fuente en Wikidata ni OpenStreetMap (revisar a mano)", ""]
    nos = ["%s/%s" % (c["region"], c["spot"]) for c in fl if c["status"] == "sin fuente"]
    L.append(", ".join(nos) if nos else "Ninguno.")
    L += ["", "## Zonas", "", "| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |", "|---|---|---|---|"]
    for code, z in r["regions"].items():
        L.append("| %s | %s | %s | %s |" % (code, z["model"], "—" if z["median_m"] is None else "%.1f m" % z["median_m"],
                                           "—" if z["median_share"] is None else "%d %%" % round(100 * z["median_share"])))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
