"""Tide heights from harmonic constants, with numpy and pyTMD (pip install pyTMD).

- predict(): hourly heights from amplitudes and Greenwich phase lags (TICON-3), with the nodal
  corrections (f, u) and the astronomical arguments (V0 + u) of pyTMD.constituents.arguments.
  Convention (the one of TICON, NOAA and the IHO): h(t) = sum f*A*cos(V(t) + u(t) - g), g the
  phase lag on Greenwich in degrees, t in UTC.
- analyse(): the inverse, a least-squares harmonic analysis with the same f, u and V; used to
  extend an official series a few hours or months past what the source publishes.
- fit30(): the watch's model (tools/lib/tide.py PERIODS, no nodal corrections), for harmonics.json.
"""
import math

import numpy as np
import pyTMD.constituents

MJD_UNIX = 40587.0                      # MJD of 1970-01-01T00:00Z
# TICON-3 names that pyTMD spells differently
TICON_TO_PYTMD = {"EP2": "eps2", "LM2": "lambda2", "MI2": "mu2", "NI2": "nu2", "MKS": "mks2", "MSQ": "msqm",
                  "MA2": "m2a", "MB2": "m2b"}
# Constituents for analyse(): all separable in one year of hourly data (Rayleigh), none needs inference.
ANALYSIS = ["sa", "ssa", "mm", "msf", "mf", "mtm", "msqm", "2q1", "q1", "o1", "m1", "p1", "s1", "k1", "j1", "oo1",
            "2n2", "mu2", "n2", "nu2", "m2", "lambda2", "l2", "t2", "s2", "r2", "k2", "eps2", "mks2", "2sm2", "m3",
            "s3", "mk3", "mn4", "m4", "ms4", "n4", "s4", "m6", "m8"]
CORRECTIONS = ("FES", "GOT", "perth3", "OTIS")


def pytmd_name(name):
    return TICON_TO_PYTMD.get(name.upper(), name.lower())


def arguments(t_unix, names, corrections="FES"):
    """(f, theta) with shape (len(t), len(names)): nodal factor and V + u in radians."""
    mjd = MJD_UNIX + np.asarray(t_unix, dtype=float) / 86400.0
    pu, pf, G = pyTMD.constituents.arguments(mjd, list(names), corrections=corrections)
    return np.asarray(pf), np.radians(np.asarray(G)) + np.asarray(pu)


def predict(t_unix, names, amp, phase_deg, corrections="FES"):
    """Heights (units of amp) at UTC epochs t_unix; names in pyTMD spelling."""
    f, th = arguments(t_unix, names, corrections)
    return (f * np.asarray(amp)[None, :] * np.cos(th - np.radians(np.asarray(phase_deg))[None, :])).sum(axis=1)


def max_nodal(names, corrections="FES", years=(2020, 2039)):
    """Largest nodal factor of each constituent over a whole nodal cycle (19 years, monthly)."""
    t0 = (dt_unix(years[0], 1, 1), dt_unix(years[1], 12, 1))
    t = np.arange(t0[0], t0[1], 30 * 86400.0)
    f, _ = arguments(t, names, corrections)
    return f.max(axis=0)


def dt_unix(y, m, d, h=0):
    import calendar
    return calendar.timegm((y, m, d, h, 0, 0))


def analyse(t_unix, y, names=ANALYSIS, corrections="FES"):
    """Least-squares harmonic analysis of y (NaN skipped) at t_unix.
    Returns (mean, amp[], phase_deg[], rms)."""
    t_unix = np.asarray(t_unix, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(y)
    f, th = arguments(t_unix[ok], names, corrections)
    X = np.hstack([np.ones((ok.sum(), 1)), f * np.cos(th), f * np.sin(th)])
    coef, *_ = np.linalg.lstsq(X, y[ok], rcond=None)
    n = len(names)
    a, b = coef[1:n + 1], coef[n + 1:]
    rms = float(np.sqrt(np.mean((X @ coef - y[ok]) ** 2)))
    return float(coef[0]), np.hypot(a, b), np.degrees(np.arctan2(b, a)) % 360.0, rms


def fill(t_unix, y, corrections="FES"):
    """y with its NaN replaced by an analysis of the rest (needs ~a year of data).
    Returns (filled y, number of filled values, analysis rms)."""
    y = np.asarray(y, dtype=float).copy()
    bad = ~np.isfinite(y)
    if not bad.any():
        return y, 0, 0.0
    mean, amp, pha, rms = analyse(t_unix, y, ANALYSIS, corrections)
    y[bad] = mean + predict(np.asarray(t_unix, dtype=float)[bad], ANALYSIS, amp, pha, corrections)
    return y, int(bad.sum()), rms


def fit30(tau_hours, y, periods):
    """The watch's harmonic model: y ~ mean + sum c*cos(2pi tau/P) + s*sin(2pi tau/P), tau in hours
    since t0. Returns (mean, cos[], sin[], rms)."""
    tau = np.asarray(tau_hours, dtype=float)
    w = 2 * math.pi / np.asarray(periods, dtype=float)
    X = np.hstack([np.ones((len(tau), 1)), np.cos(np.outer(tau, w)), np.sin(np.outer(tau, w))])
    coef, *_ = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)
    n = len(periods)
    rms = float(np.sqrt(np.mean((X @ coef - y) ** 2)))
    return float(coef[0]), coef[1:n + 1].tolist(), coef[n + 1:].tolist(), rms
