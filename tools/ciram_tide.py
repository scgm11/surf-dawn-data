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
import calendar
import datetime as dt
import os
import re
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from ciram_parse_core import parse  # noqa: E402
from tools.lib import tide as T  # noqa: E402

PORTS = {
    "imbituba": {"name": "Porto de Imbituba (DHN)", "file": "Tabua_Mare_Imbituba.pdf", "lat": -28.2297, "lon": -48.6525},
    "florianopolis": {"name": "Florianópolis (DHN)", "file": "Tabua_Mare_Florianopolis.pdf", "lat": -27.5933, "lon": -48.5567},
}
BASE = "https://ciram.epagri.sc.gov.br/ciram_arquivos/oceano/tabuamare/anual/"
UA = {"User-Agent": "Mozilla/5.0 (surf-dawn-data; +https://github.com/scgm11/surf-dawn-data)"}


def hourly(year, data):
    """Alturas por hora (cm) para todo el año, por medios cosenos entre extremos (tools/lib/tide.py)."""
    t0 = dt.datetime(year, 1, 1)
    ext = sorted(((dt.datetime(year, m, d, hh, mm) - t0).total_seconds() / 3600.0, v * 100.0)
                 for (m, d), rows in data.items() for hh, mm, v, high in rows)
    days = 366 if calendar.isleap(year) else 365
    h, ext = T.half_cosine(ext, range(days * 24))
    return [int(round(v)) for v in h], ext


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
    days = 366 if calendar.isleap(year) else 365
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
        changed += T.write_json(os.path.join(out, key + ".json"), dict(base, month=key, days=nd, h=h[start:start + nd * 24], x=x))
    have = sorted(f[:-5] for f in os.listdir(out) if re.match(r"^\d{4}-\d{2}\.json$", f))
    changed += T.write_json(os.path.join(out, "index.json"), dict(base, months=have))
    print("%s %d: 12 meses, %d archivos cambiados" % (a.port, year, changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
