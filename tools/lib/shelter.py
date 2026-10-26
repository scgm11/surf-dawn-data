"""How open a spot is to the sea around it, from the OpenStreetMap coastline: for each of
SECTORS directions, how far the water reaches before land. The watch (Score.open) uses it
for the wind (blowing over land close by it raises little chop: El Emir, behind the Punta del
Este peninsula, with a SW wind) and for the swell (land or an island that way cuts it).

code() packs a level per sector in one integer, base 3, sector i (centred on i * 360 /
SECTORS degrees, the direction the wind or the swell comes FROM) worth 3^i: 0 land within
NEAR_M, 1 within OPEN_M, 2 open sea. 3^18 fits the watch's 32-bit Number.
"""
import numpy as np

from tools.lib import geo

SECTORS = 18                 # of 20°
NEAR_M = 2000                # land closer than this: sheltered
OPEN_M = 25000               # water this far: open sea
BOX_DEG = 0.3                # the coastline needed around a spot (osm.coastline box): OPEN_M and some
OUT_M = 150                  # the rays start this far out to sea along the facing (a spot sits on the line)
RAYS = (-6, -3, 0, 3, 6)     # degrees around a sector's middle; the median ray decides (a rock is not a wall)


def _segments(ways, lat, lon):
    """[a, b] arrays (metres around the spot) of the coastline segments within reach."""
    xy = geo.local_xy(lat, lon)
    reach = OPEN_M + 5000
    a, b = [], []
    for w in ways:
        pts = [xy(p[0], p[1]) for p in w["g"]]
        for p, q in zip(pts, pts[1:]):
            if min(abs(p[0]), abs(q[0])) < reach and min(abs(p[1]), abs(q[1])) < reach:
                a.append(p)
                b.append(q)
    return np.array(a, dtype=float).reshape(-1, 2), np.array(b, dtype=float).reshape(-1, 2)


def fetch(ways, lat, lon, facing, bearings):
    """Metres of water from the spot toward each bearing (up to OPEN_M)."""
    a, b = _segments(ways, lat, lon)
    f = np.radians(facing)
    p = np.array([OUT_M * np.sin(f), OUT_M * np.cos(f)])
    e = b - a
    ap = a - p
    out = []
    for deg in bearings:
        r = np.radians(deg)
        d = np.array([np.sin(r), np.cos(r)])
        den = d[0] * e[:, 1] - d[1] * e[:, 0]
        ok = np.abs(den) > 1e-9
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (ap[:, 0] * e[:, 1] - ap[:, 1] * e[:, 0]) / den
            u = (ap[:, 0] * d[1] - ap[:, 1] * d[0]) / den
        hit = ok & (t > 0) & (u >= 0) & (u <= 1)
        out.append(float(min(OPEN_M, t[hit].min())) if hit.any() else float(OPEN_M))
    return out


def levels(ways, lat, lon, facing):
    """The SECTORS levels (0, 1, 2) of a spot."""
    step = 360.0 / SECTORS
    bearings = [(i * step + r) % 360 for i in range(SECTORS) for r in RAYS]
    f = fetch(ways, lat, lon, facing, bearings)
    out = []
    for i in range(SECTORS):
        m = sorted(f[i * len(RAYS):(i + 1) * len(RAYS)])[len(RAYS) // 2]
        out.append(0 if m < NEAR_M else (2 if m >= OPEN_M else 1))
    return out


def code(ways, lat, lon, facing):
    return sum(lv * 3 ** i for i, lv in enumerate(levels(ways, lat, lon, facing)))


def decode(c):
    return [(c // 3 ** i) % 3 for i in range(SECTORS)]
