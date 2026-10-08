#!/usr/bin/env python3
"""Tabla de mareas oficial del SOHMA (Armada Nacional, Uruguay) -> JSON por mes.

Busca el PDF "Tablas de Mareas <año> - Punta del Este" en el sitio del SOHMA,
lo convierte con pdftotext y escribe tide/punta-del-este/<año>-<mes>.json con
las alturas horarias en cm sobre el cero del puerto (hora local, UTC-3, sin
horario de verano). Idempotente: sólo reescribe un archivo si cambió.

Uso: python3 tools/sohma_tide.py --year 2026 [--pdf archivo.pdf]
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

PORT = "punta-del-este"
PORT_INFO = {
    "port": PORT,
    "name": "Puerto de Punta del Este",
    "lat": -34.9617,                 # 34°57.7' S
    "lon": -54.9517,                 # 54°57.1' W
    "utc_offset": -3,
    "unit": "cm",
    "datum": "cero del puerto (plano de reducción de la carta)",
}
MONTHS = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6, "JULIO": 7, "AGOSTO": 8,
          "SETIEMBRE": 9, "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12}
SITE = "https://sohma.armada.mil.uy"
PAGES = [SITE + "/index.php/servicios/informacion-mareografica", SITE + "/index.php/servicios/publicaciones-nauticas"]
GUESSES = ["{s}/attachments/article/300/TABLA_DE_MAREAS_{y}_PUNTA%20DEL%20ESTE.pdf",
           "{s}/attachments/article/300/TABLA_DE_MAREAS_{y}_PUNTA_DEL_ESTE.pdf",
           "{s}/attachments/article/300/Tabla{y}PuntadelEste.pdf"]
UA = {"User-Agent": "Mozilla/5.0 (surf-dawn-data; +https://github.com/scgm11/surf-dawn-data)"}


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def find_pdf(year):
    """URL del PDF de Punta del Este para `year`: primero los enlaces del sitio, después los nombres conocidos."""
    for page in PAGES:
        try:
            html = fetch(page)
        except Exception as e:  # noqa: BLE001
            print("aviso: no pude leer", page, e, file=sys.stderr)
            continue
        for href in re.findall(r'href="([^"]+\.pdf)"', html, flags=re.I):
            name = href.upper().replace("%20", " ")
            if "PUNTA" in name and "ESTE" in name and str(year) in name:
                url = href if href.startswith("http") else SITE + "/" + href.lstrip("/")
                return urllib.parse.quote(url, safe=":/%?=&")      # the SOHMA links carry literal spaces
    for g in GUESSES:
        url = g.format(s=SITE, y=year)
        try:
            req = urllib.request.Request(url, headers=UA, method="HEAD")
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status == 200:
                    return url
        except Exception:  # noqa: BLE001
            pass
    return None


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=dt.date.today().year)
    ap.add_argument("--pdf", help="PDF ya bajado (si no, se busca en el sitio del SOHMA)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tide", PORT))
    a = ap.parse_args()
    if a.pdf:
        pdf, src = a.pdf, os.path.basename(a.pdf)
    else:
        url = find_pdf(a.year)
        if not url:
            print("no encontré la tabla", a.year, "de Punta del Este en el SOHMA", file=sys.stderr)
            return 2
        print("PDF:", url)
        pdf = tempfile.mktemp(suffix=".pdf")
        with open(pdf, "wb") as f:
            f.write(fetch(url, binary=True))
        src = url
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
    data = parse(text, a.year)
    days_in_year = 366 if (a.year % 4 == 0 and (a.year % 100 != 0 or a.year % 400 == 0)) else 365
    if len(data) != days_in_year:
        print("tabla incompleta: %d días de %d" % (len(data), days_in_year), file=sys.stderr)
        return 3
    changed = 0
    months = []
    for month in range(1, 13):
        ndays = (dt.date(a.year + (month == 12), month % 12 + 1, 1) - dt.date(a.year, month, 1)).days
        h = []
        for day in range(1, ndays + 1):
            h.extend(data[(month, day)])
        key = "%d-%02d" % (a.year, month)
        obj = dict(PORT_INFO, month=key, days=ndays, source="SOHMA, Tablas de Mareas %d (Publicación Nº 3), %s" % (a.year, src), h=h)
        changed += write_json(os.path.join(a.out, key + ".json"), obj)
        months.append(key)
    # índice: meses disponibles (todos los años ya publicados)
    have = sorted(f[:-5] for f in os.listdir(a.out) if re.match(r"^\d{4}-\d{2}\.json$", f))
    changed += write_json(os.path.join(a.out, "index.json"), dict(PORT_INFO, months=have, updated=dt.date.today().isoformat()))
    print("%s: %d meses, %d archivos cambiados" % (a.year, len(months), changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
