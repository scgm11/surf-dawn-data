"""How open a spot is to the sea around it, from the OpenStreetMap coastline: for each of
SECTORS directions, how far the water reaches before land. The watch (Score.open) uses it
for the wind (blowing over land close by it raises little chop: El Emir, behind the Punta del
Este peninsula, with a SW wind) and for the swell (land or an island that way cuts it).

code() packs a level per sector in one integer, base 3, sector i (centred on i * 360 /
SECTORS degrees, the direction the wind or the swell comes FROM) worth 3^i: 0 land within
NEAR_M, 1 within OPEN_M, 2 open sea. 3^18 fits the watch's 32-bit Number.
"""
import math

import numpy as np

from tools.lib import geo

SECTORS = 18                 # of 20°
NEAR_M = 2000                # land closer than this: sheltered
OPEN_M = 25000               # water this far: open sea
BOX_DEG = 0.3                # the coastline needed around a spot (osm.coastline box): OPEN_M and some
OUT_M = 150                  # the rays start this far out to sea along the facing (a spot sits on the line)
RAYS = (-6, -3, 0, 3, 6)     # degrees around a sector's middle; the median ray decides (a rock is not a wall)
MOVE_M = 2000                # how far from its seed a spot with no sector open may move (relocate)
STEP_M = 100                 # coastline points tried every this much
SMOOTH_M = 350               # coastline length (each side) averaged for a facing (osm.SMOOTH_M)
MIN_OPEN = 3                 # sectors open to the sea a new place needs (60°)...
MASK_FROM_M = 4000           # an open ray is checked against the land mask from here (its 1 km cells)...
MASK_STEP_M = 2000           # ...every this much: a hole in the coastline file is not open sea
COARSE_STEP_M = 200          # the coarse pass (a ray per sector) tries a point every this much...
REFINE = 8                   # ...and the full one (RAYS per sector) its best few
SECTOR_M = 500               # ...and the most open wins, a sector more worth this much further from the seed


def _segments(ways, lat, lon, reach=OPEN_M + 5000):
    """[a, b] arrays (metres around the spot) of the coastline segments within reach."""
    xy = geo.local_xy(lat, lon)
    a, b = [], []
    for w in ways:
        pts = [xy(p[0], p[1]) for p in w["g"]]
        for p, q in zip(pts, pts[1:]):
            if min(abs(p[0]), abs(q[0])) < reach and min(abs(p[1]), abs(q[1])) < reach:
                a.append(p)
                b.append(q)
    return np.array(a, dtype=float).reshape(-1, 2), np.array(b, dtype=float).reshape(-1, 2)


def _mask():
    """global_land_mask's is_land (the build installs it, as for the wave points), or None."""
    try:
        from global_land_mask import globe
        return globe.is_land
    except ImportError:
        return None


def fetch(ways, lat, lon, facing, bearings):
    """Metres of water from the spot toward each bearing (up to OPEN_M)."""
    a, b = _segments(ways, lat, lon)
    return _fetch(a, b, 0.0, 0.0, facing, bearings, lat, lon)


def _fetch(a, b, x, y, facing, bearings, lat0, lon0):
    """fetch() from the point (x, y) of the segments' frame (metres around lat0, lon0), every
    bearing at once (a rays x segments matrix, the segments within OPEN_M of the point)."""
    f = np.radians(facing)
    p = np.array([x + OUT_M * np.sin(f), y + OUT_M * np.cos(f)])
    near = ((np.minimum(np.abs(a[:, 0] - p[0]), np.abs(b[:, 0] - p[0])) < OPEN_M)
            & (np.minimum(np.abs(a[:, 1] - p[1]), np.abs(b[:, 1] - p[1])) < OPEN_M))
    a, b = a[near], b[near]
    r = np.radians(np.asarray(bearings, dtype=float))
    dx, dy = np.sin(r)[:, None], np.cos(r)[:, None]
    m = np.full(len(r), float(OPEN_M))
    if len(a):
        e = b - a
        ap = a - p
        den = dx * e[None, :, 1] - dy * e[None, :, 0]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (ap[:, 0] * e[:, 1] - ap[:, 1] * e[:, 0])[None, :] / den
            u = (ap[None, :, 0] * dy - ap[None, :, 1] * dx) / den
        t = np.where((np.abs(den) > 1e-9) & (t > 0) & (u >= 0) & (u <= 1), t, np.inf)
        m = np.minimum(m, t.min(axis=1))
    is_land = _mask()
    open_ = np.nonzero(m >= OPEN_M)[0]
    if is_land is not None and len(open_):
        ks = np.arange(MASK_FROM_M, OPEN_M + 1, MASK_STEP_M, dtype=float)
        px = p[0] + ks[None, :] * dx[open_]
        py = p[1] + ks[None, :] * dy[open_]
        la = lat0 + py / 110540.0
        lo = (lon0 + px / (111320.0 * np.cos(np.radians(lat0))) + 540.0) % 360.0 - 180.0
        la = np.clip(la, -89.9, 89.9)
        try:
            land = np.asarray(is_land(la, lo), dtype=bool).reshape(la.shape)
        except Exception:                          # noqa: BLE001 - a version that takes one point at a time
            land = np.array([[bool(is_land(float(u), float(v))) for u, v in zip(ra, ro)] for ra, ro in zip(la, lo)])
        for j, i in enumerate(open_):
            hit = np.nonzero(land[j])[0]
            if len(hit):
                m[i] = ks[hit[0]]
    return [float(v) for v in m]


def _bearings():
    step = 360.0 / SECTORS
    return [(i * step + r) % 360 for i in range(SECTORS) for r in RAYS]


def levels(ways, lat, lon, facing):
    """The SECTORS levels (0, 1, 2) of a spot."""
    return _levels(fetch(ways, lat, lon, facing, _bearings()))


def _levels(f):
    out = []
    for i in range(SECTORS):
        m = sorted(f[i * len(RAYS):(i + 1) * len(RAYS)])[len(RAYS) // 2]
        out.append(0 if m < NEAR_M else (2 if m >= OPEN_M else 1))
    return out


def relocate(ways, lat, lon):
    """For a spot whose rays all meet land (snapped to a river, a ria or a harbour, its facing across
    the water): (lat, lon, facing, metres) of the coastline point nearest to its seed (lat, lon),
    within MOVE_M, with at least MIN_OPEN sectors open to the sea, facing the way osm.snap works it
    out (the coastline averaged SMOOTH_M each side, water on the right); None if there is none.
    Of those, the most open, one sector more worth SECTOR_M further: the nearest open point is
    often a river mouth or a harbour entrance with a sliver of sea."""
    xy = geo.local_xy(lat, lon)
    a, b = _segments(ways, lat, lon, OPEN_M + MOVE_M + 5000)
    cands = []
    for w in ways:
        pts = [xy(p[0], p[1]) for p in w["g"]]
        for k in range(len(pts) - 1):
            (ax, ay), (bx, by) = pts[k], pts[k + 1]
            if min(math.hypot(ax, ay), math.hypot(bx, by)) > MOVE_M + STEP_M * 5:
                continue
            n = max(1, int(math.hypot(bx - ax, by - ay) // STEP_M))
            for j in range(n):
                px, py = ax + (bx - ax) * j / n, ay + (by - ay) * j / n
                d = math.hypot(px, py)
                if d <= MOVE_M:
                    cands.append((d, px, py, pts, k))
    coarse = [i * 360.0 / SECTORS for i in range(SECTORS)]
    bear = _bearings()
    scored = []
    for d, px, py, pts, k in cands[::max(1, COARSE_STEP_M // STEP_M)]:
        sx = sy = 0.0
        for m in range(max(0, k - 40), min(len(pts) - 1, k + 41)):
            (ax, ay), (bx, by) = pts[m], pts[m + 1]
            if math.hypot((ax + bx) / 2 - px, (ay + by) / 2 - py) <= SMOOTH_M:
                sx, sy = sx + bx - ax, sy + by - ay
        if not sx and not sy:
            continue
        facing = int(round((math.degrees(math.atan2(sx, sy)) + 90) % 360))
        n = sum(1 for v in _fetch(a, b, px, py, facing, coarse, lat, lon) if v >= OPEN_M)
        scored.append((n - d / SECTOR_M, d, px, py, facing))
    best = None
    for _, d, px, py, facing in sorted(scored, key=lambda c: -c[0])[:REFINE]:
        n = _levels(_fetch(a, b, px, py, facing, bear, lat, lon)).count(2)
        if n >= MIN_OPEN and (best is None or n - d / SECTOR_M > best[0]):
            best = (n - d / SECTOR_M, px, py, facing, d)
    if best is None:
        return None
    nlat, nlon = geo.unxy(lat, lon, best[1], best[2])
    return round(nlat, 4), round(nlon, 4), best[3], best[4]


def code(ways, lat, lon, facing):
    return sum(lv * 3 ** i for i, lv in enumerate(levels(ways, lat, lon, facing)))


def decode(c):
    return [(c // 3 ** i) % 3 for i in range(SECTORS)]
