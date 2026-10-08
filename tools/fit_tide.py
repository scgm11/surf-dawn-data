#!/usr/bin/env python3
"""Armónicos de marea ajustados a la tabla anual de un puerto (respaldo offline
del reloj cuando no puede bajar el mes). Lee tide/<puerto>/<año>-MM.json,
ajusta por mínimos cuadrados 30 constituyentes y escribe
tide/<puerto>/harmonics.json; imprime además las constantes en Monkey C para
pegar en shared/TideTable.mc del repo del reloj.

Uso: python3 tools/fit_tide.py --port la-paloma --year 2026
"""
import argparse
import datetime as dt
import json
import math
import os

CONS = {"M2": 12.4206012, "S2": 12.0, "N2": 12.65834751, "K2": 11.96723606, "K1": 23.93447213, "O1": 25.81933871,
        "P1": 24.06588766, "Q1": 26.868350, "M4": 6.210300601, "MS4": 6.103339275, "MN4": 6.269173724, "M6": 4.140200401,
        "2MS6": 4.092, "Mf": 327.8599387, "Mm": 661.3111655, "Sa": 8766.15265, "Ssa": 4383.076325, "2N2": 12.90537297,
        "L2": 12.19162085, "NU2": 12.62600509, "MU2": 12.8717576, "J1": 23.09848146, "OO1": 22.30607420, "2Q1": 28.00622,
        "S1": 24.0, "MK3": 8.1771, "MO3": 8.3863, "S4": 6.0, "M8": 3.1052, "2SM2": 11.6069516}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--year", type=int, default=dt.date.today().year)
    a = ap.parse_args()
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tide", a.port)
    t0 = dt.datetime(a.year, 1, 1)
    T, Y = [], []
    for m in range(1, 13):
        d = json.load(open(os.path.join(root, "%d-%02d.json" % (a.year, m))))
        base = (dt.datetime(a.year, m, 1) - t0).total_seconds() / 3600.0
        for i, v in enumerate(d["h"]):
            T.append(base + i)
            Y.append(float(v))
    names = list(CONS)
    W = [2 * math.pi / CONS[n] for n in names]
    ncol = 1 + 2 * len(names)

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
            for j in range(i, ncol):
                Ni[j] += r[i] * r[j]
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
    print("%s %d: media %.1f cm, RMS %.2f cm, max %.1f cm" % (a.port, a.year, coef[0], rms, max(abs(e) for e in res)))
    out = {"port": a.port, "year": a.year, "t0": "%d-01-01T00:00-03:00" % a.year, "t0_epoch": int(t0.timestamp()) + 3 * 3600,
           "mean_cm": coef[0], "rms_cm": rms,
           "cons": {names[i]: {"period_h": CONS[names[i]], "cos": coef[1 + 2 * i], "sin": coef[2 + 2 * i]} for i in range(len(names))}}
    json.dump(out, open(os.path.join(root, "harmonics.json"), "w"), indent=1)
    print("// Monkey C (TideTable): T0 =", out["t0_epoch"])
    print("// FIT_MEAN %.3f" % coef[0])
    print("// PERIODS [%s]" % ", ".join("%.7f" % CONS[n] for n in names))
    print("// COS [%s]" % ", ".join("%.3f" % coef[1 + 2 * i] for i in range(len(names))))
    print("// SIN [%s]" % ", ".join("%.3f" % coef[2 + 2 * i] for i in range(len(names))))


if __name__ == "__main__":
    main()
