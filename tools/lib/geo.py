"""Distances and angles on the scale of a stretch of coast, one copy for every tool.
Longitudes wrap at ±180° (Fiji, Tonga, Samoa): every difference goes through dlon()."""
import math

KM_PER_DEG = 111.2


def dlon(a, b):
    """b - a in degrees of longitude, in (-180, 180]."""
    d = (b - a + 540.0) % 360.0 - 180.0
    return 180.0 if d == -180.0 else d


def km(a, b):
    """Equirectangular distance in km between (lat, lon) points (the watch's Geo.distanceKm, wrapped)."""
    dx = dlon(a[1], b[1]) * math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot(b[0] - a[0], dx) * KM_PER_DEG


def wrap(lon):
    return (lon + 540.0) % 360.0 - 180.0


def local_xy(lat0, lon0):
    """Equirectangular projection in metres around (lat0, lon0), wrapped."""
    k = math.cos(math.radians(lat0))
    return lambda lat, lon: (dlon(lon0, lon) * 111320.0 * k, (lat - lat0) * 110540.0)


def unxy(lat0, lon0, x, y):
    k = math.cos(math.radians(lat0))
    return lat0 + y / 110540.0, wrap(lon0 + x / (111320.0 * k))


def center(points):
    """Middle of the points' box, wrapped (a region across ±180° stays together)."""
    lats = [p[0] for p in points]
    ref = points[0][1]
    lons = [ref + dlon(ref, p[1]) for p in points]
    return (min(lats) + max(lats)) / 2, wrap((min(lons) + max(lons)) / 2)
