#!/usr/bin/env python3
"""Tablas de mareas oficiales del SOHMA (Armada Nacional, Uruguay) -> JSON por mes.

Para cada puerto busca el PDF "Tablas de Mareas <año>" en el sitio del SOHMA,
lo convierte con pdftotext y escribe tide/<puerto>/<año>-<mes>.json con las
alturas horarias en cm sobre el cero del puerto (hora local, UTC-3, sin
horario de verano). Idempotente: sólo reescribe un archivo si cambió.

Cada PDF trae al final la página de enero del año siguiente, y no se importa: la edición 2026 la
trae 3 h corrida. Antes de escribir, cada mes se compara con un ajuste armónico de los otros 11
(odd_months): con la tabla entera en la mano no se escribe un mes que no sigue la marea del resto.

Salidas: 0 bien, 2 el SOHMA todavía no publicó esa tabla, 3 la tabla está incompleta o repite un
día, 4 un mes no sigue la marea del resto. En los casos 3 y 4 no se escribe nada.

Uso: python3 tools/sohma_tide.py --year 2026 [--port punta-del-este] [--pdf archivo.pdf]
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import statistics
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import tide as T  # noqa: E402

# clave -> nombre y variantes con las que el SOHMA nombra el PDF
PORTS = {
    "punta-del-este": {"name": "Puerto de Punta del Este", "names": ["PUNTADELESTE"]},
    "la-paloma": {"name": "Puerto de La Paloma", "names": ["LAPALOMA"]},
    "montevideo": {"name": "Puerto de Montevideo", "names": ["MONTEVIDEO"]},
}
MONTHS = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6, "JULIO": 7, "AGOSTO": 8,
          "SETIEMBRE": 9, "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12}
SITE = "https://sohma.armada.mil.uy"
PAGES = [SITE + "/index.php/servicios/informacion-mareografica", SITE + "/index.php/servicios/publicaciones-nauticas"]
UA = {"User-Agent": "Mozilla/5.0 (surf-dawn-data; +https://github.com/scgm11/surf-dawn-data)"}
# Los períodos con los que se revisa cada mes: los que un ajuste a los otros 11 todavía separa (sin
# Sa ni Ssa, que dependen de la parte del año que falta).
CHECK_PERIODS = [T.CONS[n] for n in ("M2", "S2", "N2", "K2", "K1", "O1", "P1", "Q1", "M4", "MS4", "MN4", "2N2", "L2", "Mf", "Mm")]
# El peor mes de las tablas buenas de 2025 y 2026 llega a 1,32 veces la mediana de los otros; la
# página de enero de 2027 importada como diciembre de 2026 daba 2,32 a 4,16.
CHECK_RATIO = 1.8


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
    """(lat, lon) en grados decimales desde el encabezado "Latitud 34° 57.7' S / Longitud 54° 57.1' W"
    (Montevideo trae segundos: "Latitud 34° 54' 12" S")."""
    dms = r"\s+(\d+)\s*°\s*([\d.]+)'\s*(?:([\d.]+)\s*[\"”″]\s*)?"
    la = re.search(r"Latitud" + dms + r"([NS])", text)
    lo = re.search(r"Longitud" + dms + r"([EW])", text)
    if not la or not lo:
        return None, None

    def deg(m):
        return (int(m.group(1)) + float(m.group(2)) / 60 + float(m.group(3) or 0) / 3600) * (-1 if m.group(4) in "SW" else 1)

    return round(deg(la), 4), round(deg(lo), 4)


def parse(text, year):
    """{(mes, día): [24 alturas]} a partir del texto de pdftotext -layout. El encabezado de un mes de
    otro año corta la lectura: sus filas no son de este año. ValueError si un día aparece dos veces."""
    data = {}
    month = None
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^([A-ZÉ]+)\s+(\d{4})$", s)
        if m and m.group(1) in MONTHS:
            month = MONTHS[m.group(1)] if int(m.group(2)) == year else None
            continue
        if month and re.match(r"^\d{1,2}(\s+\d{2,3}){24}$", s):
            nums = [int(x) for x in s.split()]
            if (month, nums[0]) in data:
                raise ValueError("el día %d del mes %d de %d está dos veces" % (nums[0], month, year))
            data[(month, nums[0])] = nums[1:]
    return data


def month_days(year, month):
    return (dt.date(year + (month == 12), month % 12 + 1, 1) - dt.date(year, month, 1)).days


def odd_months(data, year):
    """[(mes, rms, mediana de los otros)] de los meses que no siguen la marea de los demás: cada uno
    contra un ajuste a los otros 11, sin su media, que se mueve con la estación y no con la hora."""
    months, hour = {}, 0
    for month in range(1, 13):
        rows = [v for day in range(1, month_days(year, month) + 1) for v in data[(month, day)]]
        months[month] = (list(range(hour, hour + len(rows))), rows)
        hour += len(rows)
    rms = {}
    for month in months:
        hours = [h for k, (hs, _) in months.items() if k != month for h in hs]
        heights = [v for k, (_, vs) in months.items() if k != month for v in vs]
        mean, cos, sin, _, _ = T.fit(hours, heights, CHECK_PERIODS)
        hs, vs = months[month]
        errors = [v - p for v, p in zip(vs, T.harmonic(mean, cos, sin, hs, CHECK_PERIODS))]
        bias = sum(errors) / len(errors)
        rms[month] = math.sqrt(sum((e - bias) ** 2 for e in errors) / len(errors))
    odd = []
    for month, r in rms.items():
        rest = statistics.median(v for k, v in rms.items() if k != month)
        if r > CHECK_RATIO * rest:
            odd.append((month, r, rest))
    return odd


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
    try:
        data = parse(text, year)
    except ValueError as e:
        print("%s: %s" % (port, e), file=sys.stderr)
        return 3
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    if len(data) != days_in_year:
        print("%s: tabla incompleta, %d días de %d" % (port, len(data), days_in_year), file=sys.stderr)
        return 3
    odd = odd_months(data, year)
    if odd:
        for month, r, rest in odd:
            print("%s %d-%02d: no sigue la marea del resto (%.1f cm contra %.1f de los otros)" % (port, year, month, r, rest),
                  file=sys.stderr)
        return 4
    lat, lon = position(text)
    info = {"port": port, "name": PORTS[port]["name"], "lat": lat, "lon": lon, "utc_offset": -3, "unit": "cm",
            "datum": "cero del puerto (plano de reducción de la carta)"}
    out = os.path.join(out_root, port)
    changed = 0
    for month in range(1, 13):
        ndays = month_days(year, month)
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
