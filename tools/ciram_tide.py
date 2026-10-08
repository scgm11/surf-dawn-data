#!/usr/bin/env python3
"""Tábua de marés oficial da DHN (Marinha do Brasil) republicada pela Epagri/CIRAM
(Santa Catarina) -> JSON por mês, no mesmo formato das tablas do SOHMA.

O PDF anual trae hora y altura (m, sobre el nivel de reducción de la DHN) de
cada pleamar/bajamar; se convierte a alturas horarias en cm interpolando con
medios cosenos entre extremos consecutivos (la esfera vuelve a encontrar los
extremos con una parábola, con ±5 min de error). Los extremos originales van
en "x" para control. Hora local UTC-3 (Santa Catarina no tiene horario de verano).

Uso: python3 tools/ciram_tide.py [--port imbituba] [--pdf archivo.pdf]
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ciram_parse_core import parse  # noqa: E402

PORTS = {
    "imbituba": {"name": "Porto de Imbituba (DHN)", "file": "Tabua_Mare_Imbituba.pdf", "lat": -28.2297, "lon": -48.6525},
    "florianopolis": {"name": "Florianópolis (DHN)", "file": "Tabua_Mare_Florianopolis.pdf", "lat": -27.5933, "lon": -48.5567},
}
BASE = "https://ciram.epagri.sc.gov.br/ciram_arquivos/oceano/tabuamare/anual/"
UA = {"User-Agent": "Mozilla/5.0 (surf-dawn-data; +https://github.com/scgm11/surf-dawn-data)"}


def write_json(path, obj):
    new = json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == new:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True


def hourly(year, data):
    """Alturas por hora (cm) para todo el año, por medios cosenos entre extremos."""
    t0 = dt.datetime(year, 1, 1)
    ext = []
    for (m, d), rows in sorted(data.items()):
        for hh, mm, v, high in sorted(rows):
            ext.append(((dt.datetime(year, m, d, hh, mm) - t0).total_seconds() / 3600.0, v * 100.0))
    ext.sort()
    # saneo: extremos a menos de 20 min se funden (la tabla trae algún "estofo")
    clean = [ext[0]]
    for t, v in ext[1:]:
        if t - clean[-1][0] < 0.33:
            clean[-1] = ((clean[-1][0] + t) / 2, (clean[-1][1] + v) / 2)
        else:
            clean.append((t, v))
    ext = clean
    days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    out = []
    j = 0
    for h in range(days * 24):
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
        out.append(int(round(a[1] + (b[1] - a[1]) * (1 - math.cos(math.pi * f)) / 2)))
    return out, ext


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", choices=sorted(PORTS), default="imbituba")
    ap.add_argument("--pdf")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tide"))
    a = ap.parse_args()
    info = PORTS[a.port]
    if a.pdf:
        pdf, src = a.pdf, os.path.basename(a.pdf)
    else:
        src = BASE + info["file"]
        pdf = tempfile.mktemp(suffix=".pdf")
        with urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=60) as r, open(pdf, "wb") as f:
            f.write(r.read())
    year, data = parse(pdf)
    days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    if len(data) != days:
        print("%s %d: tabla incompleta, %d días de %d" % (a.port, year, len(data), days), file=sys.stderr)
        return 3
    h, ext = hourly(year, data)
    base = {"port": a.port, "name": info["name"], "lat": info["lat"], "lon": info["lon"], "utc_offset": -3, "unit": "cm",
            "datum": "nível de redução da DHN", "source": "DHN/Marinha do Brasil, Tábua de Marés %d, via Epagri/CIRAM %s" % (year, src)}
    out = os.path.join(a.out, a.port)
    changed = 0
    for m in range(1, 13):
        start = (dt.date(year, m, 1) - dt.date(year, 1, 1)).days * 24
        nd = (dt.date(year + (m == 12), m % 12 + 1, 1) - dt.date(year, m, 1)).days
        key = "%d-%02d" % (year, m)
        x = [[d, hh * 60 + mm, int(round(v * 100)), 1 if high else 0] for (mm_, d), rows in sorted(data.items()) if mm_ == m for hh, mm, v, high in sorted(rows)]
        changed += write_json(os.path.join(out, key + ".json"), dict(base, month=key, days=nd, h=h[start:start + nd * 24], x=x))
    have = sorted(f[:-5] for f in os.listdir(out) if re.match(r"^\d{4}-\d{2}\.json$", f))
    changed += write_json(os.path.join(out, "index.json"), dict(base, months=have))
    print("%s %d: 12 meses, %d archivos cambiados" % (a.port, year, changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
