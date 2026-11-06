"""Open-Meteo marine probes: which points of a wave model are sea, and where to ask for the
waves of a spot whose own cell is land (what tools/wave_points.py did for Florianópolis,
now for every model and region).

A wave model answers from a grid cell near the point asked; on a coastal cell that the model treats
as land the answer is null or 0.0 m. For those spots the wave point is the nearest grid cell centre
that is sea in a fine land mask (global-land-mask, 1 km), gives waves in the model, lies in front of
the beach (within FRONT_DEG of where it faces, or of its swell window) and that the API answers from
itself.

That last one is not a given. The apps ask without cell_selection, and the API's default ("sea")
does not follow the wave model's own mask: it can move a point to a cell 28 km away even when the
point is a cell with waves (2026-11: (-27.75, -48.5) answers from (-28.0, -48.5), and no coordinate
reaches (-34.0, -53.5)). So every probe keeps the cell the answer came from (cells()).

The free API is for non-commercial use, up to 10,000 calls a day, and each location of a
multi-location request counts: probes are cached forever in tools/.cache/ (land does not move)
and batched BATCH locations per request.
"""
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from . import geo

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", ".cache"))
MARINE = "https://marine-api.open-meteo.com/v1/marine"
BATCH = 50
STEP = {                                         # grid spacing in degrees (lat, lon)
    "ncep_gfswave025": (0.25, 0.25), "ncep_gfswave016": (1 / 6, 1 / 6), "meteofrance_wave": (1 / 12, 1 / 12),
    "ecmwf_wam025": (0.25, 0.25), "ecmwf_wam": (0.1, 0.1), "dwd_gwam": (0.25, 0.25), "dwd_ewam": (0.05, 0.1),
}
FRONT_DEG = 75                                   # a wave point this far from where the beach faces is in front of it
FRONT_KM = 65                                    # ... and no farther than this (the farthest ones before were 62 km)
MOVED = 0.75                                     # the API moved a point: its answer is this many cells away, or more


def _cache_path(model, kind="probe"):
    return os.path.join(CACHE, "%s-%s.json" % (kind, model))


def _load(model, kind="probe"):
    try:
        with open(_cache_path(model, kind)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save(model, c, kind="probe"):
    os.makedirs(CACHE, exist_ok=True)
    tmp = _cache_path(model, kind) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(c, f, separators=(",", ":"))
    os.replace(tmp, _cache_path(model, kind))


def _key(lat, lon):
    return "%.4f,%.4f" % (lat, lon)


def _get(model, points):
    """The decoded answer for these points: a list (one entry per point), or an error dict."""
    q = urllib.parse.urlencode({
        "latitude": ",".join("%.4f" % p[0] for p in points),
        "longitude": ",".join("%.4f" % p[1] for p in points),
        "current": "wave_height", "models": model})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(MARINE + "?" + q, timeout=60) as r:
                res = json.load(r)
            return res if isinstance(res, list) else [res]
        except urllib.error.HTTPError as e:
            if e.code == 400:                     # the request itself is refused (e.g. a point off the model's grid)
                try:
                    return json.load(e)
                except ValueError:
                    return {"error": True, "reason": "HTTP 400"}
            print("  open-meteo failed (%s), retrying" % str(e)[:80], file=sys.stderr)
        except Exception as e:                    # noqa: BLE001 - timeouts, resets: retry
            print("  open-meteo failed (%s), retrying" % str(e)[:80], file=sys.stderr)
        time.sleep(15 * (attempt + 1))
    raise RuntimeError("Open-Meteo unavailable")


def _fetch(model, points):
    """(current wave height, the cell (lat, lon) it came from) at each point: (None, None) where the
    model has no sea. A refused request is split until the point it refuses is alone; that point
    counts as no sea."""
    res = _get(model, points)
    if isinstance(res, dict) or len(res) != len(points) or any(isinstance(b, dict) and b.get("error") for b in res):
        if len(points) == 1:
            reason = res.get("reason") if isinstance(res, dict) else "bad answer"
            print("  open-meteo: %s at %.4f,%.4f: %s" % (model, points[0][0], points[0][1], reason), file=sys.stderr)
            return [(None, None)]
        half = len(points) // 2
        return _fetch(model, points[:half]) + _fetch(model, points[half:])
    return [((b.get("current") or {}).get("wave_height"), (b.get("latitude"), b.get("longitude"))) if isinstance(b, dict) else (None, None)
            for b in res]


def _probe(model, points, kind):
    """Asks for the points not yet in the `kind` cache and keeps both what it learns: their height
    ("probe") and their cell ("cell"). Returns the two caches."""
    c, cc = _load(model), _load(model, "cell")
    have = c if kind == "probe" else cc
    todo = [p for p in dict.fromkeys((round(p[0], 4), round(p[1], 4)) for p in points) if _key(*p) not in have]
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]
        for p, (h, cell) in zip(part, _fetch(model, part)):
            c[_key(*p)] = h if h else None          # 0.0 is a land cell in these models
            cc[_key(*p)] = [round(cell[0], 4), round(cell[1], 4)] if cell and cell[0] is not None else None
        _save(model, c)
        _save(model, cc, "cell")
        time.sleep(1.5)
    return c, cc


def heights(model, points):
    """Current wave height (m) at each point in the model, None where the model has land."""
    c, _ = _probe(model, points, "probe")
    return [c[_key(round(p[0], 4), round(p[1], 4))] for p in points]


def cells(model, points):
    """The grid cell (lat, lon) the API answers from when asked at each point the way the apps ask
    (no cell_selection), None if it does not answer."""
    _, cc = _probe(model, points, "cell")
    out = []
    for p in points:
        cell = cc[_key(round(p[0], 4), round(p[1], 4))]
        out.append(tuple(cell) if cell else None)
    return out


def moved(model, point, cell):
    """Whether the API answers from a cell that is not the one at this point."""
    dlat, dlon = STEP.get(model, (0.25, 0.25))
    return cell is None or abs(cell[0] - point[0]) >= MOVED * dlat or abs(geo.wrap(cell[1] - point[1])) >= MOVED * dlon


def bearing(a, b):
    """Degrees from a to b (lat, lon), clockwise from north."""
    la1, la2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(geo.wrap(b[1] - a[1]))
    return math.degrees(math.atan2(math.sin(dl) * math.cos(la2), math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dl))) % 360


def off_front(spot, point, toward):
    """How many degrees a point is from the way a spot looks (its facing, or its swell window)."""
    return abs((bearing(spot, point) - toward + 180) % 360 - 180)


def _is_sea(lat, lon):
    from global_land_mask import globe          # imported here: only the wave-point step needs it
    return not globe.is_land(lat, geo.wrap(lon))


def candidates(model, lat, lon, rings=4, keep=4, toward=None):
    """Grid cell centres around (lat, lon), nearest first, that are sea in the land mask (the
    centre and four points half a cell away), up to `keep` of them. With `toward`, only those in
    front of a spot looking that way, FRONT_KM away at most."""
    dlat, dlon = STEP.get(model, (0.25, 0.25))
    i0, j0 = round(lat / dlat), round(lon / dlon)
    out = []
    for i in range(i0 - rings, i0 + rings + 1):
        for j in range(j0 - rings, j0 + rings + 1):
            clat, clon = i * dlat, geo.wrap(j * dlon)
            if abs(clat) > 85:
                continue
            km = geo.km((lat, lon), (clat, clon))
            if toward is not None and (km > FRONT_KM or off_front((lat, lon), (clat, clon), toward) > FRONT_DEG):
                continue
            ring = [(clat, clon)] + [(clat + a * dlat / 2, clon + b * dlon / 2) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if all(_is_sea(a, b) for a, b in ring):
                out.append((km, round(clat, 4), round(clon, 4)))
    out.sort()
    return [(a, b) for _, a, b in out[:keep]]


def _usable(model, cs):
    """Of these candidates, those with waves that the API answers from themselves."""
    if not cs:
        return []
    hs, where = heights(model, cs), cells(model, cs)
    return [c for c, h, w in zip(cs, hs, where) if h and not moved(model, c, w)]


def wave_points(model, spots, towards=None):
    """For spots [(lat, lon)], the wave point (lat, lon) of each one, None where its own cell
    has waves; a spot whose land cell has no sea cell nearby gets 'none' (reported). `towards`:
    where each one looks (its swell window, else its facing; None if unknown), to choose among the
    cells in front of it; a spot with none of those takes the nearest one, wherever it is."""
    towards = towards or [None] * len(spots)
    hs = heights(model, spots)
    land = [i for i, h in enumerate(hs) if h is None]
    out = [None] * len(spots)
    for i in land:
        good = []
        if towards[i] is not None:
            good = _usable(model, candidates(model, *spots[i], toward=towards[i])) or \
                _usable(model, candidates(model, *spots[i], rings=8, keep=8, toward=towards[i]))
        good = good or _usable(model, candidates(model, *spots[i])) or \
            _usable(model, candidates(model, *spots[i], rings=8, keep=8))    # a wider look, once
        out[i] = good[0] if good else "none"
    return out


# --- Hourly series (validate/): several models and points per request -------------------------

DAY_VARS = 10                                    # the free API counts a location as one call up to
DAY_SPAN = 14                                    # 10 variables and 2 weeks, proportionally more above


def call_weight(n_points, n_vars, n_days):
    """How many calls of the daily allowance a request costs (each location counts)."""
    return n_points * max(1.0, n_vars / DAY_VARS) * max(1.0, n_days / DAY_SPAN)


def get_json(params, url=MARINE, tries=6):
    """GET url?params: the decoded answer as a list (one entry per location), or the error dict of a
    request the API refuses (HTTP 400, e.g. a point outside every requested model). Retries the rest."""
    import urllib.error
    q = urllib.parse.urlencode(params, safe=",")
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url + "?" + q, timeout=120) as r:
                res = json.load(r)
            return res if isinstance(res, list) else [res]
        except urllib.error.HTTPError as e:
            if e.code == 400:
                try:
                    return json.load(e)
                except ValueError:
                    return {"error": True, "reason": "HTTP 400"}
            print("  open-meteo failed (%s), retrying" % str(e)[:80], file=sys.stderr)
        except Exception as e:                    # noqa: BLE001 - timeouts, resets: retry
            print("  open-meteo failed (%s), retrying" % str(e)[:80], file=sys.stderr)
        time.sleep(15 * (attempt + 1))
    raise RuntimeError("Open-Meteo unavailable")


def split_models(block, models, variables):
    """One location of a multi-model hourly answer -> (times, {model: {variable: [values]}}).
    Several models come as '<variable>_<model>'; a single one as the bare variable. A model the API
    left out (outside its domain) or with every value null is not in the result."""
    h = block.get("hourly") or {}
    times = h.get("time") or []
    out = {}
    for m in models:
        cols = {}
        for v in variables:
            col = h.get(v if len(models) == 1 else "%s_%s" % (v, m))
            if col is not None and len(col) == len(times):
                cols[v] = col
        if cols and any(x is not None for c in cols.values() for x in c):
            out[m] = cols
    return times, out
