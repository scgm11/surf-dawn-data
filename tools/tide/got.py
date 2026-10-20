"""Tides from a global ocean tide model where no gauge is near (tools/tide/build_tides.py, tier 6):
NASA GSFC's GOT5.6 (Richard Ray; public domain; it builds on GOT5.5, so both are downloaded), once,
by pyTMD into the tide cache, and predicted at the spots with pyTMD (minor constituents inferred).
The grids extrapolated to the coast are used ("GOT5.6_extrapolated"), else the ocean ones with the
nearest valid cell within CUTOFF_KM. Heights in cm about mean sea level, hourly, UTC.
"""
import os

import numpy as np

MODEL = "GOT5.6"
DOWNLOADS = ["GOT5.5", "GOT5.6"]
DEFINITIONS = ["GOT5.6_extrapolated", "GOT5.6"]     # pyTMD's names, the coastal grids first
CUTOFF_KM = 25.0                 # a spot on the coastline takes the model cell this close (extrapolation)
EPOCH = 946684800                # 2000-01-01 00:00 UTC, pyTMD's default epoch


class ModelError(Exception):
    pass


def ensure(cache):
    """The model's files in cache (downloaded the first time); returns the directory pyTMD reads."""
    import pyTMD.datasets
    os.makedirs(cache, exist_ok=True)
    for m in DOWNLOADS:
        marker = os.path.join(cache, ".%s-ok" % m)
        if not os.path.exists(marker):
            print("  downloading %s (NASA GSFC) into %s" % (m, cache), flush=True)
            pyTMD.datasets.fetch_gsfc_got(m, directory=cache)
            open(marker, "w").close()
    return cache


def heights(lat, lon, t_unix, cache):
    """Hourly heights (cm, about MSL) at (lat, lon) for the UTC epochs t_unix; raises ModelError."""
    import pyTMD.compute
    directory = ensure(cache)
    t = np.asarray(t_unix, dtype=float)
    h, errs = None, []
    for name in DEFINITIONS:
        try:
            h = pyTMD.compute.tide_elevations(np.array([lon], dtype=float), np.array([lat], dtype=float),
                                              t - EPOCH, directory=directory, model=name, crs=4326,
                                              type="time series", standard="UTC", method="linear",
                                              extrapolate=True, cutoff=CUTOFF_KM)
            break
        except Exception as e:                             # noqa: BLE001 - try the next definition
            errs.append("%s: %s" % (name, str(e)[:140]))
    if h is None:
        raise ModelError("%s at %.3f,%.3f: %s" % (MODEL, lat, lon, "; ".join(errs)))
    v = np.asarray(getattr(h, "values", h), dtype=float).reshape(-1)
    if v.size != t.size or not np.isfinite(v).any():
        raise ModelError("%s at %.3f,%.3f: no model water there" % (MODEL, lat, lon))
    big = float(np.nanmax(np.abs(v)))
    cm = v if big > 20 else v * 100.0                      # pyTMD answers in metres (no tide is 20 m)
    if float(np.nanmax(np.abs(cm))) < 2:
        raise ModelError("%s at %.3f,%.3f: no tide in the model there" % (MODEL, lat, lon))
    return np.where(np.isfinite(cm), cm, np.nan)


def heights_many(points, t_unix, cache):
    """heights() for several (lat, lon) at once (the model's grids are read once): a list with an
    array of cm or a ModelError for each point."""
    import pyTMD.compute
    directory = ensure(cache)
    t = np.asarray(t_unix, dtype=float)
    lats = np.array([p[0] for p in points], dtype=float)
    lons = np.array([p[1] for p in points], dtype=float)
    out = None
    for name in DEFINITIONS:
        try:
            h = pyTMD.compute.tide_elevations(lons, lats, t - EPOCH, directory=directory, model=name, crs=4326,
                                              type="time series", standard="UTC", method="linear",
                                              extrapolate=True, cutoff=CUTOFF_KM)
            v = np.asarray(getattr(h, "values", h), dtype=float)
            if v.shape == (len(points), t.size):
                out = v
            elif v.shape == (t.size, len(points)):
                out = v.T
            if out is not None:
                break
        except Exception as e:                             # noqa: BLE001 - per point below
            print("  %s for %d points at once: %s" % (name, len(points), str(e)[:160]), flush=True)
    res = []
    for i, (lat, lon) in enumerate(points):
        if out is None:                                    # one by one
            try:
                res.append(heights(lat, lon, t, cache))
            except ModelError as e:
                res.append(e)
            continue
        v = out[i]
        big = float(np.nanmax(np.abs(v))) if np.isfinite(v).any() else 0.0
        cm = v if big > 20 else v * 100.0
        if not np.isfinite(cm).any() or float(np.nanmax(np.abs(cm))) < 2:
            res.append(ModelError("%s at %.3f,%.3f: no tide in the model there" % (MODEL, lat, lon)))
        else:
            res.append(cm)
    return res
