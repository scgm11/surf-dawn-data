"""The regions to validate, from the seed tables: spots, centre, default models and whether the
region is fixed by issue #7 (tools/lib/models.py, the rule tools/build_zones.py uses)."""
import math
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from tools.lib import geo, seeds  # noqa: E402
from tools.lib import models as rule  # noqa: E402
from tools.lib.models import DEFAULT_WIND, is_fixed  # noqa: E402,F401  (evaluate, report, run)
MATCH_KM = 150.0                               # a buoy validates a region if this close to one of its spots
MAX_BUOYS = 3
CANDIDATES = 5                                 # buoys looked at per region (some may not be representative)
WIND_CANDIDATES = 8                            # wind stations looked at per region (many coastal ones are sheltered)
# Same sea: a buoy validates a region if it is open to the directions the region's spots are open
# to. A direction is open at a point when a ray of RAY_KM in that bearing meets no land (the 1 km
# mask tools/ use), starting RAY_SKIP_KM out (spots sit on the coastline; buoys a bit off it).
RAYS = 32
RAY_KM, RAY_STEP_KM = 60.0, 1.0
RAY_SKIP_KM = {"spot": 2.0, "buoy": 0.5}
SEA_MIN = 0.5                                  # the buoy must see at least half of the spots' open directions
SEA_DROP = 0.3                                 # ... and not much less than the best buoy of the region


def default_models(code, country, lat):
    return rule.default(code, country, lat)


class Region:
    def __init__(self, code, country, name, spots, models_row=None):
        self.code, self.country, self.name = code, country, name
        self.spots = spots                                     # [(lat, lon)]
        self.lat, self.lon = geo.center(spots)
        self.radius = max(geo.km((self.lat, self.lon), s) for s in spots)
        self.fixed = is_fixed(code, country)
        self.default = default_models(code, country, self.lat)
        self.current = list(models_row) if models_row else list(self.default)   # what the watch uses today
        # the spot nearest the centre: a coastal point for the inter-model spread
        self.mid = min(spots, key=lambda s: geo.km((self.lat, self.lon), s))

    def km_to(self, lat, lon):
        """Distance from (lat, lon) to the region's nearest spot."""
        if geo.km((self.lat, self.lon), (lat, lon)) > self.radius + MATCH_KM + 50:
            return float("inf")
        return min(geo.km(s, (lat, lon)) for s in self.spots)


def load(models_csv=None):
    rows = rule.read(models_csv)
    out = []
    for code, r in seeds.regions().items():
        sp = [(s["lat"], s["lon"]) for s in seeds.spots(code)]
        if sp:
            out.append(Region(code, r["country"], r["name_es"], sp, rows.get(code)))
    return out


def near_any(regions, km=MATCH_KM):
    """near(lat, lon) -> True if within km of some region's spot (for the NDBC pre-filter)."""
    def near(lat, lon):
        return any(r.km_to(lat, lon) <= km for r in regions)
    return near


def land_mask():
    """is_land(lats, lons) -> list of bools, from global-land-mask (1 km, the mask tools/ use)."""
    from global_land_mask import globe          # imported here: the parsers and scores do not need it
    import numpy as np

    def is_land(lats, lons):
        return [bool(x) for x in globe.is_land(np.array(lats, dtype=float), np.array([geo.wrap(x) for x in lons], dtype=float))]
    return is_land


def open_rays(lat, lon, is_land, skip):
    """For RAYS bearings (0 = north, clockwise), True where RAY_KM of sea lie ahead (after `skip` km)."""
    lats, lons = [], []
    k = math.cos(math.radians(lat))
    steps = []
    d = skip
    while d <= RAY_KM + 1e-9:
        steps.append(d)
        d += RAY_STEP_KM
    for i in range(RAYS):
        b = math.radians(360.0 * i / RAYS)
        for d in steps:
            lats.append(lat + d * math.cos(b) / geo.KM_PER_DEG)
            lons.append(geo.wrap(lon + d * math.sin(b) / (geo.KM_PER_DEG * k)))
    land = is_land(lats, lons)
    n = len(steps)
    return tuple(not any(land[i * n:(i + 1) * n]) for i in range(RAYS))


class Exposure:
    """Open directions of spots and buoys, memoised (a spot or buoy serves several regions)."""
    def __init__(self, is_land):
        self.is_land, self.memo = is_land, {}

    def rays(self, p, kind):
        key = (round(p[0], 4), round(p[1], 4), kind)
        if key not in self.memo:
            self.memo[key] = open_rays(p[0], p[1], self.is_land, RAY_SKIP_KM[kind])
        return self.memo[key]

    def shared(self, region, lat, lon, km=MATCH_KM):
        """Mean over the region's spots within km of the buoy of the fraction of each spot's open
        directions that are open at the buoy too; None if no such spot sees open sea."""
        b = self.rays((lat, lon), "buoy")
        vals = []
        for s in region.spots:
            if geo.km(s, (lat, lon)) > km:
                continue
            o = self.rays(s, "spot")
            n = sum(o)
            if n:
                vals.append(sum(1 for x, y in zip(o, b) if x and y) / n)
        return sum(vals) / len(vals) if vals else None


def match(region, stations, km=MATCH_KM, top=CANDIDATES, exposure=None):
    """The region's candidate buoys, nearest first (a buoy close to the breaks is the nearshore one):
    within km of one of its spots and, with an Exposure, open to the same sea (shared directions >=
    SEA_MIN and >= the best buoy's - SEA_DROP). At most `top`.
    Returns ([(station, km, shared)], [(station, km, shared) left out: another coast or sheltered])."""
    c = [(region.km_to(s.lat, s.lon), s) for s in stations]
    c = sorted(((d, s) for d, s in c if d <= km), key=lambda x: (x[0], x[1].id))
    sh = {s.id: (exposure.shared(region, s.lat, s.lon, km) if exposure else None) for _, s in c}
    known = [v for v in sh.values() if v is not None and v >= SEA_MIN]
    floor = max(SEA_MIN, max(known) - SEA_DROP) if known else SEA_MIN
    out, blocked = [], []
    for d, s in c:
        v = sh[s.id]
        if v is not None and v < floor:
            blocked.append((s, d, v))
        elif len(out) < top:
            out.append((s, d, v))
    return out, blocked
