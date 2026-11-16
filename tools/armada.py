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

Además guarda, una vez por día, el nivel del mar que pronostica Open-Meteo (sea_level_height_msl, el
día anterior y los 7 que vienen) en los puertos de la tabla que tienen mareógrafo vivo:
validation/armada/openmeteo/<puerto>.csv (emitido, utc, nivel_m). El pasado de Open-Meteo ya viene
corregido; esto es lo que habría visto la app días antes, para probar R2 como pronóstico
(tools/marea_meteo.py --dia N).

    python3 tools/armada.py                 baja las 48 h de cada estación y el pronóstico de Open-Meteo
    python3 tools/armada.py --html DIR      las 48 h de páginas ya bajadas (DIR/Est<N>.html), sin Open-Meteo
"""
import argparse
import csv
import datetime as dt
import glob
import json
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

# Los puertos de la tabla (tide/<puerto>) con un mareógrafo que manda datos nuevos: La Paloma se mide en
# La Paloma y Montevideo en Punta Lobos. Colonia, Piriápolis y Punta del Este repiten datos viejos
# desde que se guardan (13/11/2026); si vuelven, se suman acá y en marea_meteo.PAIRS.
FORECAST_PORTS = ("la-paloma", "montevideo")
MARINE = "https://marine-api.open-meteo.com/v1/marine"
FORECAST_DAYS = 7                                       # lo que muestra el iPhone

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


def port_point(port):
    """(lat, lon) del puerto, del último mes de su tabla (tide/<puerto>/AAAA-MM.json)."""
    last = sorted(glob.glob(os.path.join(ROOT, "tide", port, "[0-9][0-9][0-9][0-9]-[0-9][0-9].json")))[-1]
    with open(last) as f:
        d = json.load(f)
    return d["lat"], d["lon"]


def fetch_forecast(ports):
    """{puerto: {epoch UTC: nivel en m}}: el nivel que da hoy Open-Meteo, del día anterior a los
    FORECAST_DAYS que vienen, en un solo pedido para todos los puertos."""
    pts = [port_point(p) for p in ports]
    q = urllib.parse.urlencode({
        "latitude": ",".join("%.4f" % la for la, _ in pts), "longitude": ",".join("%.4f" % lo for _, lo in pts),
        "hourly": "sea_level_height_msl", "past_days": 1, "forecast_days": FORECAST_DAYS,
        "timezone": "GMT", "timeformat": "unixtime"}, safe=",")
    req = urllib.request.Request(MARINE + "?" + q, headers={"User-Agent": "surf-dawn-data (validación de mareas)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    res = res if isinstance(res, list) else [res]
    out = {}
    for port, block in zip(ports, res):
        h = block.get("hourly") or {}
        out[port] = {int(t): v for t, v in zip(h.get("time") or [], h.get("sea_level_height_msl") or [])
                     if v is not None}
    return out


def merge_forecast(path, issued, series):
    """Suma al CSV (emitido, utc, nivel_m) el pronóstico emitido el día `issued` (AAAA-MM-DD, UTC),
    una sola vez por día: si ese día ya estaba, no suma nada. Devuelve cuántas filas sumó."""
    rows = []
    if os.path.exists(path):
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
    if not series or any(r["emitido"] == issued for r in rows):
        return 0
    for t in sorted(series):
        rows.append({"emitido": issued,
                     "utc": dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                     "nivel_m": "%.3f" % series[t]})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["emitido", "utc", "nivel_m"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return len(series)


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
    if not a.html:
        try:                                            # Open-Meteo caído no frena los mareógrafos
            issued = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
            for port, series in fetch_forecast(FORECAST_PORTS).items():
                added = merge_forecast(os.path.join(OUT, "openmeteo", port + ".csv"), issued, series)
                print("Open-Meteo %s: %d horas del pronóstico del %s%s" % (
                    port, len(series), issued, "" if added else " (ya estaba)"))
        except Exception as e:
            print("Open-Meteo: %s" % e)
    if ok == 0:
        print("ninguna estación respondió")
        sys.exit(1)


if __name__ == "__main__":
    main()
