#!/usr/bin/env python3
"""La referencia del nivel del mar de cada puerto, para que las apps digan cuánta agua de más o de menos
viene (issue scgm11/surf-dawn#84): nivel/<puerto>.json.

Las apps ya piden a Open-Meteo el nivel del mar del pico (sea_level_height_msl) y, donde hay un puerto con
tabla, dibujan la tabla. La tabla es la marea astronómica; lo que le suman el viento y la presión (en
Uruguay, más que la marea misma) sale del nivel de Open-Meteo: su promedio de 25 h, que saca la marea,
menos lo normal ahí. Lo normal es esta referencia: la media del nivel de Open-Meteo en el puerto en los
últimos 92 días. Las apps no pueden pedir 92 días cada vez (el reloj no tiene dónde), así que se publica.

Solo en los puertos donde se midió contra mareógrafos (tools/marea_meteo.py, validation/armada): La Paloma
y Montevideo, y Punta del Este, que está entre los dos; y los de Brasil. Un puerto sin su archivo queda con la
tabla sola.

La media cambia centímetros por mes: una corrida que falla deja la de antes, que sigue sirviendo.

    python3 tools/nivel.py            baja el nivel de cada puerto y reescribe nivel/<puerto>.json si cambió
"""
import datetime as dt
import json
import os
import statistics as st
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from armada import MARINE  # noqa: E402

OUT = os.path.join(ROOT, "nivel")
BRASIL = (
    "got-0a9164", "got-1426bf", "got-1afd1e", "got-421e4e", "got-442fe7", "got-45461c", "got-47f025",
    "got-4fc66e", "got-59c9d7", "got-a0b2f5", "got-a6dd41", "got-a8e5b2", "got-aa96f4", "got-af45e1",
    "got-bc9748", "got-c9dd3b", "got-d43a78", "got-d8f761", "got-d9ce28", "got-f2f875", "got-f89309",
    "imbituba", "ticon-2559e1", "ticon-2b1454", "ticon-4c1497", "ticon-752b4c", "ticon-757122", "ticon-cf2b1c",
    "ticon-ee2dcc", "ticon-f5b09a",)
PORTS = ("la-paloma", "montevideo", "punta-del-este") + BRASIL
BATCH = 50                                  # puertos por pedido a Open-Meteo
DAYS = 92                                   # lo más que da Open-Meteo para atrás, y lo medido en marea_meteo.py
MIN_HOURS = 24 * 60                         # con menos horas que estas no se publica


def points():
    """{puerto: (lat, lon)} de tide/ports.json (los meses de las tablas de afuera de Uruguay no lo dicen)."""
    with open(os.path.join(ROOT, "tide", "ports.json"), encoding="utf-8") as f:
        return {p["key"]: (p["lat"], p["lon"]) for p in json.load(f)}


def fetch(ports):
    """{puerto: [nivel en m de cada hora de los últimos DAYS días hasta ahora]}, BATCH puertos por pedido."""
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    where = points()
    out = {}
    for i in range(0, len(ports), BATCH):
        part = ports[i:i + BATCH]
        pts = [where[p] for p in part]
        q = urllib.parse.urlencode({
            "latitude": ",".join("%.4f" % la for la, _ in pts), "longitude": ",".join("%.4f" % lo for _, lo in pts),
            "hourly": "sea_level_height_msl", "past_days": DAYS, "forecast_days": 1,
            "timezone": "GMT", "timeformat": "unixtime"}, safe=",")
        req = urllib.request.Request(MARINE + "?" + q, headers={"User-Agent": "surf-dawn-data (nivel del mar)"})
        with urllib.request.urlopen(req, timeout=90) as r:
            res = json.load(r)
        res = res if isinstance(res, list) else [res]
        for port, block in zip(part, res):
            h = block.get("hourly") or {}
            out[port] = [v for t, v in zip(h.get("time") or [], h.get("sea_level_height_msl") or [])
                         if v is not None and t <= now]
    return out


def reference(levels):
    """La media en m, al centímetro, o None con pocas horas."""
    return round(st.fmean(levels), 2) if len(levels) >= MIN_HOURS else None


def main():
    os.makedirs(OUT, exist_ok=True)
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    where = points()
    for port, levels in fetch(PORTS).items():
        ref = reference(levels)
        if ref is None:
            print("%s: %d horas, no alcanza: queda la de antes" % (port, len(levels)))
            continue
        path = os.path.join(OUT, port + ".json")
        old = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = json.load(f)
        if old and old.get("ref") == ref:
            print("%s: %+.2f m, sin cambios (del %s)" % (port, ref, old.get("at")))
            continue
        lat, lon = where[port]
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"port": port, "lat": lat, "lon": lon, "ref": ref, "days": DAYS, "at": today},
                               separators=(",", ":")) + "\n")
        print("%s: %+.2f m (antes %s)" % (port, ref, "%+.2f" % old["ref"] if old else "nada"))


if __name__ == "__main__":
    main()
