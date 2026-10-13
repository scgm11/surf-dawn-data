"""The regions to validate, from the seed tables: spots, centre, default models (the rule of
tools/build_zones.py and docs/formatos.md) and whether the region is fixed by issue #7."""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from tools.lib import geo, seeds  # noqa: E402

DEFAULT_WIND = "gfs_seamless"
FIXED_COUNTRIES = {"UY", "AR"}
FIXED_PREFIXES = ("BR-SC-", "BR-RS")          # Santa Catarina and Rio Grande do Sul
FIXED_MODELS = ("ncep_gfswave025", "gfs_seamless")
MATCH_KM = 150.0                               # a buoy validates a region if this close to one of its spots
MAX_BUOYS = 3
CANDIDATES = 5                                 # buoys looked at per region (some may not be representative)


def is_fixed(code, country):
    """Issue #7: Uruguay, Argentina, Santa Catarina and Rio Grande do Sul stay on GFS-Wave 0.25 +
    GFS (like Windguru). They are validated for information, never moved."""
    return country in FIXED_COUNTRIES or code.startswith(FIXED_PREFIXES)


def default_models(code, country, lat):
    if is_fixed(code, country):
        return list(FIXED_MODELS)
    return ["ncep_gfswave016" if -15.0 <= lat <= 52.5 else "ncep_gfswave025", DEFAULT_WIND]


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
    import csv
    rows = {}
    path = models_csv or os.path.join(ROOT, "models.csv")
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            rows = {r["region"]: (r["wave"], r["wind"]) for r in csv.DictReader(f)}
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


def match(region, stations, km=MATCH_KM, top=CANDIDATES):
    """The region's candidate buoys: within km of one of its spots, nearest first (a buoy close to
    the breaks is the nearshore one), at most `top`. Returns [(station, km)]."""
    c = [(region.km_to(s.lat, s.lon), s) for s in stations]
    c = [(d, s) for d, s in c if d <= km]
    c.sort(key=lambda x: (x[0], x[1].id))
    return [(s, d) for d, s in c[:top]]
