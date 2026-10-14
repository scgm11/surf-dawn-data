"""OpenStreetMap coastline: download (Overpass, cached) and snapping a seed to it.

The snap is the one tools/make_spots.py used for Uruguay and Santa Catarina: the nearest
point of any `natural=coastline` way, and the direction the beach faces as the coastline's
normal towards the water (OSM draws coastlines with the land on the left), averaged over
SMOOTH_M each side so a rock or a groyne does not decide it.

Downloads ask only for small boxes around the seeds (BOX_DEG each side), joined in one
query per region, so a long region (Florida, Western Australia) is not a huge download.
Responses are cached in tools/.osm_cache/ (CI keeps that folder between runs).
"""
import hashlib
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

from . import geo

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", ".osm_cache"))
MIRRORS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.private.coffee/api/interpreter",
           "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]
UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)"}
BOX_DEG = 0.04            # each side of a seed (~4 km): enough to snap within SNAP_MAX_M and smooth
SNAP_MAX_M = 2500         # a seed further than this from any coastline is reported, not guessed
SMOOTH_M = 350            # coastline length (each side) averaged for the facing


def _boxes(points):
    """Seed boxes, merged where they overlap (fewer statements in the query)."""
    boxes = []
    for lat, lon in points:
        b = [lat - BOX_DEG, lon - BOX_DEG, lat + BOX_DEG, lon + BOX_DEG]
        for o in boxes:
            if b[0] <= o[2] and o[0] <= b[2] and b[1] <= o[3] and o[1] <= b[3] and abs(o[1] - b[1]) < 1:
                o[0], o[1], o[2], o[3] = min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])
                break
        else:
            boxes.append(b)
    out = []
    for s, w, n, e in boxes:                     # a box across ±180° goes as two
        if w < -180:
            out += [(s, w + 360, n, 180.0), (s, -180.0, n, e)]
        elif e > 180:
            out += [(s, w, n, 180.0), (s, -180.0, n, e - 360)]
        else:
            out.append((s, w, n, e))
    return out


def coastline(name, points):
    """Coastline ways (with geometry) near the points; cached by region name and boxes."""
    boxes = _boxes(points)
    key = hashlib.sha1(json.dumps([[round(v, 3) for v in b] for b in boxes]).encode()).hexdigest()[:10]
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "coast-%s-%s.json" % (name, key))
    if os.path.exists(path):
        with open(path) as f:
            ways = json.load(f)
        if ways:                                 # an empty answer may have been a busy server's: asked again
            return ways
    stmts = "".join('way["natural"="coastline"](%.4f,%.4f,%.4f,%.4f);' % b for b in boxes)
    query = "[out:json][timeout:170];(%s);out geom;" % stmts
    body = urllib.parse.urlencode({"data": query}).encode()
    for attempt in range(9):
        url = MIRRORS[attempt % len(MIRRORS)]
        try:
            req = urllib.request.Request(url, body, UA)
            data = json.loads(urllib.request.urlopen(req, timeout=180).read())
            remark = data.get("remark") or ""
            if "error" in remark or "timed out" in remark or "out of memory" in remark:
                raise RuntimeError(remark)       # a 200 with a partial answer: not kept
            ways = [{"g": [[p["lat"], p["lon"]] for p in e["geometry"]]} for e in data.get("elements", []) if e.get("geometry")]
            with open(path, "w") as f:
                json.dump(ways, f)
            time.sleep(2)                        # be polite between regions
            return ways
        except Exception as e:                   # busy mirrors answer with HTML, 429 or time out
            print("  overpass %s failed (%s), retrying" % (url.split("/")[2], str(e)[:80]), file=sys.stderr)
            time.sleep(10 + 10 * attempt)
    raise RuntimeError("Overpass unavailable for region %s" % name)


def snap(lat, lon, ways):
    """(distance m, lat, lon, facing) of the nearest coastline point, or None without coastline."""
    xy = geo.local_xy(lat, lon)
    best = None
    for w in ways:
        pts = [xy(p[0], p[1]) for p in w["g"]]
        for i in range(len(pts) - 1):
            (ax, ay), (bx, by) = pts[i], pts[i + 1]
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy
            if not L2:
                continue
            t = max(0.0, min(1.0, -(ax * dx + ay * dy) / L2))
            px, py = ax + t * dx, ay + t * dy
            d = math.hypot(px, py)
            if best is None or d < best[0]:
                best = (d, pts, i, px, py)
    if best is None:
        return None
    d, pts, i, px, py = best
    sx = sy = 0.0
    for j in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[j], pts[j + 1]
        if math.hypot((ax + bx) / 2 - px, (ay + by) / 2 - py) <= SMOOTH_M:
            sx, sy = sx + bx - ax, sy + by - ay
    if not sx and not sy:
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        sx, sy = bx - ax, by - ay
    along = math.degrees(math.atan2(sx, sy))     # bearing of the coastline direction (x east, y north)
    facing = int(round((along + 90) % 360))      # water on the right: turn right
    slat, slon = geo.unxy(lat, lon, px, py)
    return d, slat, slon, facing


NOMINATIM = "https://nominatim.openstreetmap.org/search"


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


def nominatim(names, cc):
    """Nominatim's search for the first two name variants in a country: candidates {lat, lon, name,
    kind, src} (one request a second, as its policy asks)."""
    out = []
    for v in names[:2]:
        q = urllib.parse.urlencode({"q": v.title(), "countrycodes": cc.lower(), "format": "jsonv2", "limit": 10})
        try:
            req = urllib.request.Request(NOMINATIM + "?" + q, headers=UA)
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


def named_near(lat, lon, names, km, tries=6):
    """OSM features named like one of the names (accents and case aside) within km of (lat, lon): beaches,
    bays, capes, places, surf spots, beach resorts, as candidates {lat, lon, name, kind, src}."""
    from .names import regex
    rx = "|".join(regex(v) for v in names)
    q = ('[out:json][timeout:90];('
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["natural"~"^(beach|bay|cape|peninsula|headland)$"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["place"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["sport"~"surf"];'
         'nwr(around:{r},{la},{lo})["name"~"{rx}",i]["leisure"="beach_resort"];'
         ');out center tags;').format(r=int(km * 1000), la=lat, lo=lon, rx=rx)
    body = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(tries):
        url = MIRRORS[attempt % len(MIRRORS)]
        try:
            req = urllib.request.Request(url, body, UA)
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
