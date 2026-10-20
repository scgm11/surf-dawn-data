"""Tide helpers shared by every tide tool: the watch's 30 harmonic periods and the least-squares
fit to them (tools/fit_tide.py, tools/tide/), the half-cosine interpolation between highs and lows
(tools/ciram_tide.py, LINZ), month files and JSON writing.

Pure Python: the CIRAM and SOHMA tools run without numpy."""
import calendar
import json
import math
import os

# The watch's TideTable.PERIODS (hours), same order: changing it breaks every harm.json.
CONS = {"M2": 12.4206012, "S2": 12.0, "N2": 12.65834751, "K2": 11.96723606, "K1": 23.93447213, "O1": 25.81933871,
        "P1": 24.06588766, "Q1": 26.868350, "M4": 6.210300601, "MS4": 6.103339275, "MN4": 6.269173724, "M6": 4.140200401,
        "2MS6": 4.092, "Mf": 327.8599387, "Mm": 661.3111655, "Sa": 8766.15265, "Ssa": 4383.076325, "2N2": 12.90537297,
        "L2": 12.19162085, "NU2": 12.62600509, "MU2": 12.8717576, "J1": 23.09848146, "OO1": 22.30607420, "2Q1": 28.00622,
        "S1": 24.0, "MK3": 8.1771, "MO3": 8.3863, "S4": 6.0, "M8": 3.1052, "2SM2": 11.6069516}
NAMES = list(CONS)
PERIODS = [CONS[n] for n in NAMES]


def fit(T, Y, periods=PERIODS):
    """Least-squares fit of Y (cm) at hours T to mean + Σ c·cos(2πT/P) + s·sin(2πT/P).
    Returns (mean, cos[], sin[], rms, max abs residual)."""
    W = [2 * math.pi / p for p in periods]
    ncol = 1 + 2 * len(W)

    def row(t):
        r = [1.0]
        for w in W:
            r.append(math.cos(w * t))
            r.append(math.sin(w * t))
        return r

    N = [[0.0] * ncol for _ in range(ncol)]
    b = [0.0] * ncol
    for t, y in zip(T, Y):
        r = row(t)
        for i in range(ncol):
            b[i] += r[i] * y
            Ni = N[i]
            ri = r[i]
            for j in range(i, ncol):
                Ni[j] += ri * r[j]
    for i in range(ncol):
        for j in range(i):
            N[i][j] = N[j][i]
    M = [N[i][:] + [b[i]] for i in range(ncol)]
    for c in range(ncol):
        p = max(range(c, ncol), key=lambda k: abs(M[k][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [v / piv for v in M[c]]
        for k in range(ncol):
            if k != c and M[k][c] != 0.0:
                f = M[k][c]
                M[k] = [x - f * y for x, y in zip(M[k], M[c])]
    coef = [M[i][ncol] for i in range(ncol)]
    res = [y - sum(ci * ri for ci, ri in zip(coef, row(t))) for t, y in zip(T, Y)]
    rms = math.sqrt(sum(e * e for e in res) / len(res))
    return coef[0], coef[1::2], coef[2::2], rms, max(abs(e) for e in res)


def harmonic(mean, cos, sin, hours, periods=PERIODS):
    """The watch's TideTable.harmonic in cm at hours since t0."""
    W = [2 * math.pi / p for p in periods]
    return [mean + sum(c * math.cos(w * t) + s * math.sin(w * t) for c, s, w in zip(cos, sin, W)) for t in hours]


def harm_json(port, t0, mean, cos, sin, rms):
    """The compact harm.json (docs/formatos.md): what the watch reads when a month is missing."""
    return {"port": port, "t0": t0, "mean": round(mean, 2), "cos": [round(v, 3) for v in cos],
            "sin": [round(v, 3) for v in sin], "rms": round(rms, 2)}


def half_cosine(ext, hours):
    """Heights at `hours` (sorted) from turns ext [(hour, height)] (sorted, alternating highs and
    lows): a half cosine between consecutive turns, as the DHN and LINZ tables are drawn. Turns
    closer than 20 min are merged first (a table's "stand"). Outside the turns the nearest pair
    is extended."""
    clean = [ext[0]]
    for t, v in ext[1:]:
        if t - clean[-1][0] < 0.33:
            clean[-1] = ((clean[-1][0] + t) / 2, (clean[-1][1] + v) / 2)
        else:
            clean.append((t, v))
    ext = clean
    out = []
    j = 0
    for h in hours:
        while j + 1 < len(ext) and ext[j + 1][0] <= h:
            j += 1
        if h <= ext[0][0]:
            a, b = ext[0], ext[1]
        elif j + 1 >= len(ext):
            a, b = ext[-2], ext[-1]
        else:
            a, b = ext[j], ext[j + 1]
        f = (h - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0.0
        f = min(max(f, 0.0), 1.0) if ext[0][0] <= h <= ext[-1][0] else f
        out.append(a[1] + (b[1] - a[1]) * (1 - math.cos(math.pi * f)) / 2)
    return out, ext


def days_in(year, month):
    return calendar.monthrange(year, month)[1]


def write_json(path, obj, indent=None):
    """Writes obj compact (or indented); only when it changed, so an unchanged run makes no commit."""
    if indent is None:
        new = json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n"
    else:
        new = json.dumps(obj, indent=indent, ensure_ascii=False) + "\n"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            if f.read() == new:
                return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True
