#!/usr/bin/env python3
"""Tablas de mareas oficiales del SOHMA (Armada Nacional, Uruguay) -> JSON por mes.

Para cada puerto busca el PDF "Tablas de Mareas <año>" en el sitio del SOHMA,
lo convierte con pdftotext y escribe tide/<puerto>/<año>-<mes>.json con las
alturas horarias en cm sobre el cero del puerto (hora local, UTC-3, sin
horario de verano). Idempotente: sólo reescribe un archivo si cambió.

Uso: python3 tools/sohma_tide.py --year 2026 [--port punta-del-este] [--pdf archivo.pdf]
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

# clave -> nombre y variantes con las que el SOHMA nombra el PDF
PORTS = {
    "punta-del-este": {"name": "Puerto de Punta del Este", "names": ["PUNTADELESTE"]},
    "la-paloma": {"name": "Puerto de La Paloma", "names": ["LAPALOMA"]},
}
MONTHS = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6, "JULIO": 7, "AGOSTO": 8,
          "SETIEMBRE": 9, "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12}
SITE = "https://sohma.armada.mil.uy"
PAGES = [SITE + "/index.php/servicios/informacion-mareografica", SITE + "/index.php/servicios/publicaciones-nauticas"]
UA = {"User-Agent": "Mozilla/5.0 (surf-dawn-data; +https://github.com/scgm11/surf-dawn-data)"}


def squash(name):
    """Nombre de archivo normalizado para comparar: mayúsculas, sin espacios ni separadores."""
    return re.sub(r"[^A-Z0-9]", "", urllib.parse.unquote(name).upper())


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def find_pdf(year, port):
    """URL del PDF de `port` para `year`, entre los enlaces del sitio del SOHMA."""
    for page in PAGES:
        try:
            html = fetch(page)
        except Exception as e:  # noqa: BLE001
            print("aviso: no pude leer", page, e, file=sys.stderr)
            continue
        for href in re.findall(r'href="([^"]+\.pdf)"', html, flags=re.I):
            name = squash(os.path.basename(href))
            if str(year) in name and any(v in name for v in PORTS[port]["names"]):
                url = href if href.startswith("http") else SITE + "/" + href.lstrip("/")
                return urllib.parse.quote(url, safe=":/%?=&")      # los enlaces traen espacios literales
    return None


def position(text):
    """(lat, lon) en grados decimales desde el encabezado "Latitud 34° 57.7' S / Longitud 54° 57.1' W"."""
    la = re.search(r"Latitud\s+(\d+)\s*°\s*([\d.]+)'\s*([NS])", text)
    lo = re.search(r"Longitud\s+(\d+)\s*°\s*([\d.]+)'\s*([EW])", text)
    if not la or not lo:
        return None, None
    lat = (int(la.group(1)) + float(la.group(2)) / 60) * (-1 if la.group(3) == "S" else 1)
    lon = (int(lo.group(1)) + float(lo.group(2)) / 60) * (-1 if lo.group(3) == "W" else 1)
    return round(lat, 4), round(lon, 4)


def parse(text, year):
    """{(mes, día): [24 alturas]} a partir del texto de pdftotext -layout."""
    data = {}
    month = None
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^([A-ZÉ]+)\s+(\d{4})$", s)
        if m and m.group(1) in MONTHS and int(m.group(2)) == year:
            month = MONTHS[m.group(1)]
            continue
        if month and re.match(r"^\d{1,2}(\s+\d{2,3}){24}$", s):
            nums = [int(x) for x in s.split()]
            data[(month, nums[0])] = nums[1:]
    return data


def write_json(path, obj):
    new = json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == new:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True


def run(year, port, pdf_arg, out_root):
    if pdf_arg:
        pdf, src = pdf_arg, os.path.basename(pdf_arg)
    else:
        url = find_pdf(year, port)
        if not url:
            print("no encontré la tabla %d de %s en el SOHMA" % (year, PORTS[port]["name"]), file=sys.stderr)
            return 2
        print("PDF:", url)
        pdf = tempfile.mktemp(suffix=".pdf")
        with open(pdf, "wb") as f:
            f.write(fetch(url, binary=True))
        src = url
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
    data = parse(text, year)
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    if len(data) != days_in_year:
        print("%s: tabla incompleta, %d días de %d" % (port, len(data), days_in_year), file=sys.stderr)
        return 3
    lat, lon = position(text)
    info = {"port": port, "name": PORTS[port]["name"], "lat": lat, "lon": lon, "utc_offset": -3, "unit": "cm",
            "datum": "cero del puerto (plano de reducción de la carta)"}
    out = os.path.join(out_root, port)
    changed = 0
    for month in range(1, 13):
        ndays = (dt.date(year + (month == 12), month % 12 + 1, 1) - dt.date(year, month, 1)).days
        h = []
        for day in range(1, ndays + 1):
            h.extend(data[(month, day)])
        key = "%d-%02d" % (year, month)
        obj = dict(info, month=key, days=ndays, source="SOHMA, Tablas de Mareas %d (Publicación Nº 3), %s" % (year, src), h=h)
        changed += write_json(os.path.join(out, key + ".json"), obj)
    have = sorted(f[:-5] for f in os.listdir(out) if re.match(r"^\d{4}-\d{2}\.json$", f))
    changed += write_json(os.path.join(out, "index.json"), dict(info, months=have))   # sin fecha: sin novedades no hay commit
    print("%s %d: 12 meses, %d archivos cambiados (%.4f, %.4f)" % (port, year, changed, lat or 0, lon or 0))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=dt.date.today().year)
    ap.add_argument("--port", choices=sorted(PORTS), help="por defecto, todos")
    ap.add_argument("--pdf", help="PDF ya bajado (sólo con --port)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tide"))
    a = ap.parse_args()
    ports = [a.port] if a.port else sorted(PORTS)
    worst = 0
    for port in ports:
        worst = max(worst, run(a.year, port, a.pdf if a.port else None, a.out))
    return worst


if __name__ == "__main__":
    sys.exit(main())
