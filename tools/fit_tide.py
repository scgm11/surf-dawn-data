#!/usr/bin/env python3
"""Armónicos de marea ajustados a la tabla anual de un puerto (respaldo offline del reloj cuando
no puede bajar el mes). Lee tide/<puerto>/<año>-MM.json, ajusta por mínimos cuadrados los 30
períodos del reloj (tools/lib/tide.py, los mismos de TideTable.PERIODS) y escribe
tide/<puerto>/harmonics.json en el formato que baja el reloj (docs/formatos.md). Imprime además
las constantes en Monkey C para los puertos de fábrica (shared-bg/TideTable.mc del repo del
reloj, que scripts/build.sh copia para Pronóstico y Sesión).

Uso: python3 tools/fit_tide.py --port la-paloma --year 2026
"""
import argparse
import calendar
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from tools.lib import tide as T  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--year", type=int, default=dt.date.today().year)
    a = ap.parse_args()
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tide", a.port)
    hours, heights, off = [], [], None
    t0 = dt.datetime(a.year, 1, 1)
    for m in range(1, 13):
        with open(os.path.join(root, "%d-%02d.json" % (a.year, m)), encoding="utf-8") as f:
            d = json.load(f)
        off = d.get("utc_offset", 0) if off is None else off
        base = (dt.datetime(a.year, m, 1) - t0).total_seconds() / 3600.0
        for i, v in enumerate(d["h"]):
            if v is not None:
                hours.append(base + i)
                heights.append(float(v))
    mean, cos, sin, rms, worst = T.fit(hours, heights)
    epoch = calendar.timegm(t0.timetuple()) - int(off * 3600)        # the port's local midnight, in UTC
    print("%s %d: media %.1f cm, RMS %.2f cm, max %.1f cm" % (a.port, a.year, mean, rms, worst))
    T.write_json(os.path.join(root, "harmonics.json"), T.harm_json(a.port, epoch, mean, cos, sin, rms))
    print("// Monkey C (TideTable): T0 =", epoch)
    print("// FIT_MEAN %.3f" % mean)
    print("// PERIODS [%s]" % ", ".join("%.7f" % p for p in T.PERIODS))
    print("// COS [%s]" % ", ".join("%.3f" % v for v in cos))
    print("// SIN [%s]" % ", ".join("%.3f" % v for v in sin))


if __name__ == "__main__":
    main()
