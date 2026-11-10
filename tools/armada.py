#!/usr/bin/env python3
"""Los mareógrafos de la Armada (meteo.armada.mil.uy), guardados: la página muestra solo las últimas
48 h de cada estación, cada 5 minutos, y para bajar más pide usuario. Esto las junta día a día en
validation/armada/<estación>.csv (utc, nivel en m, agua en °C cuando la estación la da), sin
repetir horas, para tener una serie observada de Uruguay con la que validar la marea de las apps:
la tabla del SOHMA sola contra la tabla más la parte meteorológica de Open-Meteo (issue
scgm11/surf-dawn#72, revisión del 6/11, R2 y R10). La corre .github/workflows/armada.yml una vez
por día; las 48 h se solapan, así que un día que falla no deja hueco.

Las horas de la página son las de Uruguay (UTC-3, sin cambio de hora: el "Huso +3" del SOHMA);
contra la tabla, la correlación es máxima sin corrimiento (10/11/2026, La Paloma y Punta Lobos).

    python3 tools/armada.py                 baja las 48 h de cada estación y las suma a los CSV
    python3 tools/armada.py --html DIR      lo mismo, de páginas ya bajadas (DIR/Est<N>.html)
"""
import argparse
import csv
import datetime as dt
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "validation", "armada")
URL = "https://meteo.armada.mil.uy/Est%dArmada.php"
UY = dt.timezone(dt.timedelta(hours=-3))

# Las estaciones mareográficas (Est<N>: su nombre de archivo); Colonia, Piriápolis y Punta del Este
# figuran "en desarrollo" en la página.
STATIONS = {4: "la-paloma", 5: "punta-lobos", 8: "colonia", 9: "piriapolis", 10: "punta-del-este"}

SERIES = re.compile(r'getElementById\("(graph[A-Z])"\)\s*,\s*\[(.*?)\]\s*,\s*\{', re.S)
POINT = re.compile(r'new Date\("([^"]+)"\)\)?\s*,\s*([-\d.eE+]+|null|NaN)')


def parse(html):
    """{serie: {epoch UTC: valor}} de las series Dygraph de una página (graphM, el nivel en m;
    graphT, el agua en °C), sin los valores vacíos."""
    out = {}
    for m in SERIES.finditer(html):
        rows = {}
        for when, v in POINT.findall(m.group(2)):
            try:
                x = float(v)
            except ValueError:
                continue
            if x != x:
                continue
            t = dt.datetime.strptime(when, "%Y/%m/%d %H:%M:%S").replace(tzinfo=UY)
            rows[int(t.timestamp())] = x
        out[m.group(1)] = rows
    return out


def fetch(n):
    """La página de la estación n con el botón de 48 H apretado (un POST del formulario)."""
    data = urllib.parse.urlencode({"48h": "48h"}).encode()
    req = urllib.request.Request(URL % n, data=data, headers={"User-Agent": "surf-dawn-data (validación de mareas)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def merge(path, series):
    """Suma las filas nuevas al CSV (utc, nivel_m, agua_c); las que ya estaban se quedan. Devuelve
    cuántas sumó."""
    rows = {}
    if os.path.exists(path):
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                rows[r["utc"]] = r
    level = series.get("graphM", {})
    water = series.get("graphT", {})
    added = 0
    for t in sorted(set(level) | set(water)):
        key = dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if key in rows:
            continue
        rows[key] = {"utc": key,
                     "nivel_m": "%.3f" % level[t] if t in level else "",
                     "agua_c": "%.1f" % water[t] if t in water else ""}
        added += 1
    if added:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["utc", "nivel_m", "agua_c"], lineterminator="\n")
            w.writeheader()
            for k in sorted(rows):
                w.writerow(rows[k])
    return added


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--html", help="páginas ya bajadas, DIR/Est<N>.html")
    a = ap.parse_args()
    ok = 0
    for n, name in STATIONS.items():
        try:
            html = open(os.path.join(a.html, "Est%d.html" % n), encoding="utf-8").read() if a.html else fetch(n)
            s = parse(html)
            if not s.get("graphM"):
                print("Est%d %s: sin nivel en la página" % (n, name))
                continue
            added = merge(os.path.join(OUT, name + ".csv"), s)
            m = s["graphM"]
            print("Est%d %s: %d valores, %s a %s UTC, %d nuevos" % (
                n, name, len(m), dt.datetime.fromtimestamp(min(m), dt.timezone.utc).strftime("%d/%m %H:%M"),
                dt.datetime.fromtimestamp(max(m), dt.timezone.utc).strftime("%d/%m %H:%M"), added))
            ok += 1
        except Exception as e:                          # una estación caída no frena a las otras
            print("Est%d %s: %s" % (n, name, e))
    if ok == 0:
        print("ninguna estación respondió")
        sys.exit(1)


if __name__ == "__main__":
    main()
