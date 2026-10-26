"""OpenStreetMap coastline: fixed tiles of it (cached) and snapping a seed to it.

The snap is the one tools/make_spots.py used for Uruguay and Santa Catarina: the nearest
point of any `natural=coastline` line, and the direction the beach faces as the coastline's
normal towards the water (OSM draws coastlines with the land on the left), averaged over
SMOOTH_M each side so a rock or a groyne does not decide it.

The coastline comes in fixed TILE° tiles kept in tools/.osm_cache/coast/ (CI keeps that folder
between runs), so moving a seed only needs the tiles it lands on. A missing tile is cut from
osmdata.openstreetmap.de's coastline file (OSM's coastline as lines split in small pieces, drawn
the other way round: SRC_URL, ~1 GB, downloaded once into tools/.osm_src/ and kept by CI apart);
Overpass is the fallback when that file cannot be had. Each segment of a line goes to the tile
of its middle, so the tiles do not overlap and a tile's pieces join their neighbours' end to
start (coastline() stitches them back into lines).
"""
import json
import math
import os
import shutil
import struct
import sys
import time
import urllib.parse
import urllib.request
import zipfile

from . import geo

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", ".osm_cache"))
TILES = os.path.join(CACHE, "coast")
SRC = os.path.normpath(os.path.join(HERE, "..", ".osm_src"))
SRC_URL = "https://osmdata.openstreetmap.de/download/coastlines-split-4326.zip"
MIRRORS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.private.coffee/api/interpreter",
           "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]
UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)"}
TILE = 0.5                # degrees of a coastline tile
BOX_DEG = 0.05            # each side of a seed (~5 km): enough to snap within SNAP_MAX_M and smooth
SNAP_MAX_M = 2500         # a seed further than this from any coastline is reported, not guessed
SMOOTH_M = 350            # coastline length (each side) averaged for the facing
E7 = 1e7                  # tiles keep OSM's 7 decimals as integers (exact, so pieces join exactly)
NT = int(round(360 / TILE))


def tiles_for(points, box=BOX_DEG):
    """The (row, col) tiles within box degrees of the points (col wraps at ±180°)."""
    out = set()
    for lat, lon in points:
        for i in range(math.floor((lat - box) / TILE), math.floor((lat + box) / TILE) + 1):
            for j in range(math.floor((lon - box) / TILE), math.floor((lon + box) / TILE) + 1):
                out.add((i, (j + NT // 2) % NT - NT // 2))
    return sorted(out)


def _tile_path(t):
    return os.path.join(TILES, "%d_%d.json" % t)


def _read_tile(t):
    """[[lat_e7, lon_e7, ...], ...] pieces of a cached tile, or None if it is not cached."""
    try:
        with open(_tile_path(t)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def missing_tiles(points, box=BOX_DEG):
    """The tiles around the points that are not cached yet."""
    return [t for t in tiles_for(points, box) if not os.path.exists(_tile_path(t))]


def _cut(lines, wanted):
    """{tile: pieces} of the lines ([(lat, lon), ...]) for the wanted tiles: each segment goes to the
    tile of its middle, consecutive segments of a tile make one piece."""
    out = {t: [] for t in wanted}
    for g in lines:
        cur, piece = None, None
        for k in range(len(g) - 1):
            (a, b), (c, d) = g[k], g[k + 1]
            t = (math.floor((a + c) / 2 / TILE), math.floor((b + d) / 2 / TILE) if abs(b - d) < 180 else -NT // 2)
            if t != cur:
                cur = t
                piece = None
                if t in out:
                    piece = [round(a * E7), round(b * E7)]
                    out[t].append(piece)
            if piece is not None:
                piece += [round(c * E7), round(d * E7)]
    return out


def _save(cut):
    os.makedirs(TILES, exist_ok=True)
    for t, pieces in cut.items():
        tmp = _tile_path(t) + ".tmp"
        with open(tmp, "w") as f:
            json.dump(pieces, f, separators=(",", ":"))
        os.replace(tmp, _tile_path(t))


class _Shapefile:
    """The lines of osmdata's coastline file (an ESRI shapefile of polylines), read with struct."""

    def __init__(self, shp, shx):
        self.f = open(shp, "rb")
        with open(shx, "rb") as f:
            data = f.read()
        n = (len(data) - 100) // 8
        self.offs = [2 * o for o in struct.unpack(">%di" % (2 * n), data[100:100 + 8 * n])[0::2]]
        self.index = {}                            # tile: records whose box touches it
        for n, o in enumerate(self.offs):
            self.f.seek(o + 12)
            x0, y0, x1, y1 = struct.unpack("<4d", self.f.read(32))
            for i in range(math.floor(y0 / TILE), math.floor(y1 / TILE) + 1):
                for j in range(math.floor(x0 / TILE), math.floor(x1 / TILE) + 1):
                    self.index.setdefault((i, j), []).append(n)

    def lines(self, tiles):
        """The lines ([(lat, lon), ...]) of the records whose box touches one of the tiles."""
        for n in sorted({n for t in tiles for n in self.index.get(t, ())}):
            o = self.offs[n]
            self.f.seek(o + 8)
            head = self.f.read(44)
            if struct.unpack("<i", head[:4])[0] != 3:   # a polyline
                continue
            nparts, npts = struct.unpack("<2i", head[36:44])
            parts = list(struct.unpack("<%di" % nparts, self.f.read(4 * nparts))) + [npts]
            xy = struct.unpack("<%dd" % (2 * npts), self.f.read(16 * npts))
            for p in range(nparts):                 # osmcoastline writes them with the water on the left:
                yield [(xy[2 * k + 1], xy[2 * k]) for k in range(parts[p + 1] - 1, parts[p] - 1, -1)]   # turned to OSM's way


_SHP = []                                          # the opened file, once per run ([None]: not to be had)


def _source():
    """osmdata's coastline file, downloaded and unpacked the first time a run needs it, or None."""
    if _SHP:
        return _SHP[0]
    os.makedirs(SRC, exist_ok=True)
    zpath = os.path.join(SRC, "coastlines-split-4326.zip")
    shp, shx = os.path.join(SRC, "lines.shp"), os.path.join(SRC, "lines.shx")
    try:
        if not (os.path.exists(shp) and os.path.exists(shx)):
            if not os.path.exists(zpath):
                print("  osmdata: downloading %s" % SRC_URL, file=sys.stderr, flush=True)
                for attempt in range(3):
                    try:
                        req = urllib.request.Request(SRC_URL, headers=UA)
                        with urllib.request.urlopen(req, timeout=120) as r, open(zpath + ".tmp", "wb") as f:
                            shutil.copyfileobj(r, f, 1 << 20)
                        os.replace(zpath + ".tmp", zpath)
                        break
                    except Exception as e:  # noqa: BLE001
                        print("  osmdata failed (%s)" % str(e)[:80], file=sys.stderr, flush=True)
                        time.sleep(30)
                else:
                    raise RuntimeError("osmdata unavailable")
            with zipfile.ZipFile(zpath) as z:
                for m in z.namelist():
                    if m.endswith("/lines.shp") or m.endswith("/lines.shx"):
                        with z.open(m) as src, open(os.path.join(SRC, os.path.basename(m)), "wb") as dst:
                            shutil.copyfileobj(src, dst, 1 << 20)
        _SHP.append(_Shapefile(shp, shx))
        print("  osmdata: %d coastline pieces" % len(_SHP[0].offs), file=sys.stderr, flush=True)
    except Exception as e:  # noqa: BLE001 - a broken file or no network: Overpass then
        print("  osmdata coastline not available (%s): Overpass instead" % str(e)[:80], file=sys.stderr, flush=True)
        _SHP.append(None)
    return _SHP[0]


def _overpass(name, tiles):
    """The missing tiles from Overpass (in one query): {tile: pieces}."""
    stmts = "".join('way["natural"="coastline"](%.4f,%.4f,%.4f,%.4f);' % (
        i * TILE, j * TILE, (i + 1) * TILE, (j + 1) * TILE) for i, j in tiles)
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
            lines = [[(p["lat"], p["lon"]) for p in e["geometry"]] for e in data.get("elements", []) if e.get("geometry")]
            time.sleep(2)                        # be polite between regions
            return _cut(lines, tiles), bool(lines)
        except Exception as e:                   # busy mirrors answer with HTML, 429 or time out
            print("  overpass %s failed (%s), retrying" % (url.split("/")[2], str(e)[:80]), file=sys.stderr)
            time.sleep(10 + 10 * attempt)
    raise RuntimeError("no coastline for region %s (osmdata and Overpass unavailable)" % name)


def _stitch(pieces):
    """Lines [[(lat, lon), ...]] from tile pieces, joined where one ends where another starts."""
    pieces = [list(zip(p[0::2], p[1::2])) for p in pieces]
    seen, uniq = set(), []
    for p in pieces:
        k = (p[0], p[-1], len(p))
        if k not in seen:
            seen.add(k)
            uniq.append(p)
    starts = {}
    for n, p in enumerate(uniq):
        starts.setdefault(p[0], n)
    has_prev = {starts[p[-1]] for p in uniq if p[-1] in starts}
    used, lines = set(), []
    for n in [n for n in range(len(uniq)) if n not in has_prev] + list(range(len(uniq))):
        if n in used:
            continue
        line = []
        while n is not None and n not in used:
            used.add(n)
            line += uniq[n] if not line else uniq[n][1:]
            n = starts.get(uniq[n][-1])
        lines.append([(a / E7, b / E7) for a, b in line])
    return lines


def coastline(name, points, offline=False, box=BOX_DEG):
    """Coastline lines within box degrees of the points ([{"g": [[lat, lon], ...]}, ...]) from the
    cached tiles, the missing ones cut from osmdata's file (Overpass if that is not to be had);
    offline: None if a tile is missing."""
    want = tiles_for(points, box)
    have = {t: _read_tile(t) for t in want}
    missing = [t for t in want if have[t] is None]
    if missing:
        if offline:
            return None
        src = _source()
        if src is not None:
            cut = _cut(src.lines(missing), missing)
            _save(cut)
        else:
            cut, found = _overpass(name, missing)
            if found:                            # an empty answer may have been a busy server's: asked again
                _save(cut)
        have.update(cut)
    return [{"g": g} for g in _stitch([p for t in want for p in have[t]])]


def _near(g, lat, lon, wlat, wlon):
    """Indexes i of the segments g[i]-g[i+1] whose box touches the window around (lat, lon)."""
    out = []
    for i in range(len(g) - 1):
        (a, b), (c, d) = g[i], g[i + 1]
        if (a < lat - wlat and c < lat - wlat) or (a > lat + wlat and c > lat + wlat):
            continue
        da, dc = geo.dlon(lon, b), geo.dlon(lon, d)
        if (da < -wlon and dc < -wlon) or (da > wlon and dc > wlon):
            continue
        out.append(i)
    return out


def snap(lat, lon, ways):
    """(distance m, lat, lon, facing) of the nearest coastline point, or None without coastline
    within BOX_DEG (what coastline() loads around a seed)."""
    xy = geo.local_xy(lat, lon)
    best = None
    for w in ways:
        g = w["g"]
        for i in _near(g, lat, lon, BOX_DEG, BOX_DEG):
            (ax, ay), (bx, by) = xy(*g[i]), xy(*g[i + 1])
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy
            if not L2:
                continue
            t = max(0.0, min(1.0, -(ax * dx + ay * dy) / L2))
            px, py = ax + t * dx, ay + t * dy
            d = math.hypot(px, py)
            if best is None or d < best[0]:
                best = (d, g, i, px, py)
    if best is None:
        return None
    d, g, i, px, py = best
    slat, slon = geo.unxy(lat, lon, px, py)
    wlat = 1.5 * SMOOTH_M / 110540.0
    sx = sy = 0.0
    for j in _near(g, slat, slon, wlat, wlat / max(0.05, math.cos(math.radians(abs(slat))))):
        (ax, ay), (bx, by) = xy(*g[j]), xy(*g[j + 1])
        if math.hypot((ax + bx) / 2 - px, (ay + by) / 2 - py) <= SMOOTH_M:
            sx, sy = sx + bx - ax, sy + by - ay
    if not sx and not sy:
        (ax, ay), (bx, by) = xy(*g[i]), xy(*g[i + 1])
        sx, sy = bx - ax, by - ay
    along = math.degrees(math.atan2(sx, sy))     # bearing of the coastline direction (x east, y north)
    facing = int(round((along + 90) % 360))      # water on the right: turn right
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
