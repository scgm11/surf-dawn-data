"""Open-Meteo marine probes: which points of a wave model are sea, and where to ask for the
waves of a spot whose own cell is land (what tools/wave_points.py did for Florianópolis,
now for every model and region).

A wave model answers from its nearest grid cell; on a coastal cell that the model treats as
land the answer is null or 0.0 m. For those spots the wave point is the nearest grid cell
centre that is sea in a fine land mask (global-land-mask, 1 km) and gives waves in the model.

The free API is for non-commercial use, up to 10,000 calls a day, and each location of a
multi-location request counts: probes are cached forever in tools/.cache/ (land does not move)
and batched BATCH locations per request.
"""
import json
import math
import os
import sys
import time
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


def _cache_path(model):
    return os.path.join(CACHE, "probe-%s.json" % model)


def _load(model):
    try:
        with open(_cache_path(model)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save(model, c):
    os.makedirs(CACHE, exist_ok=True)
    tmp = _cache_path(model) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(c, f, separators=(",", ":"))
    os.replace(tmp, _cache_path(model))


def _key(lat, lon):
    return "%.4f,%.4f" % (lat, lon)


def _fetch(model, points):
    q = urllib.parse.urlencode({
        "latitude": ",".join("%.4f" % p[0] for p in points),
        "longitude": ",".join("%.4f" % p[1] for p in points),
        "current": "wave_height", "models": model})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(MARINE + "?" + q, timeout=60) as r:
                res = json.load(r)
            res = res if isinstance(res, list) else [res]
            return [(b.get("current") or {}).get("wave_height") for b in res]
        except Exception as e:
            print("  open-meteo failed (%s), retrying" % str(e)[:80], file=sys.stderr)
            time.sleep(15 * (attempt + 1))
    raise RuntimeError("Open-Meteo unavailable")


def heights(model, points):
    """Current wave height (m) at each point in the model, None where the model has land."""
    c = _load(model)
    todo = [p for p in dict.fromkeys((round(p[0], 4), round(p[1], 4)) for p in points) if _key(*p) not in c]
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]
        for p, h in zip(part, _fetch(model, part)):
            c[_key(*p)] = h if h else None          # 0.0 is a land cell in these models
        _save(model, c)
        time.sleep(1.5)
    return [c[_key(round(p[0], 4), round(p[1], 4))] for p in points]


def _is_sea(lat, lon):
    from global_land_mask import globe          # imported here: only the wave-point step needs it
    return not globe.is_land(lat, geo.wrap(lon))


def candidates(model, lat, lon, rings=4, keep=4):
    """Grid cell centres around (lat, lon), nearest first, that are sea in the land mask (the
    centre and four points half a cell away), up to `keep` of them."""
    dlat, dlon = STEP.get(model, (0.25, 0.25))
    i0, j0 = round(lat / dlat), round(lon / dlon)
    out = []
    for i in range(i0 - rings, i0 + rings + 1):
        for j in range(j0 - rings, j0 + rings + 1):
            clat, clon = i * dlat, geo.wrap(j * dlon)
            if abs(clat) > 85:
                continue
            ring = [(clat, clon)] + [(clat + a * dlat / 2, clon + b * dlon / 2) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if all(_is_sea(a, b) for a, b in ring):
                out.append((geo.km((lat, lon), (clat, clon)), round(clat, 4), round(clon, 4)))
    out.sort()
    return [(a, b) for _, a, b in out[:keep]]


def wave_points(model, spots):
    """For spots [(lat, lon)], the wave point (lat, lon) of each one, None where its own cell
    has waves; a spot whose land cell has no sea cell nearby gets 'none' (reported)."""
    hs = heights(model, spots)
    land = [i for i, h in enumerate(hs) if h is None]
    out = [None] * len(spots)
    if not land:
        return out
    cands = {i: candidates(model, *spots[i]) for i in land}
    flat = list(dict.fromkeys(c for cs in cands.values() for c in cs))
    ch = dict(zip(flat, heights(model, flat))) if flat else {}
    for i in land:
        good = [c for c in cands[i] if ch.get(c)]
        if not good:                               # a wider look, once
            more = candidates(model, *spots[i], rings=8, keep=8)
            mh = dict(zip(more, heights(model, more))) if more else {}
            good = [c for c in more if mh.get(c)]
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
