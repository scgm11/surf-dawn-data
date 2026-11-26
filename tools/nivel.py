#!/usr/bin/env python3
"""La referencia del nivel del mar de cada puerto, para que las apps digan cuánta agua de más o de menos
viene (issue scgm11/surf-dawn#84): nivel/<puerto>.json.

Las apps ya piden a Open-Meteo el nivel del mar del pico (sea_level_height_msl) y, donde hay un puerto con
tabla, dibujan la tabla. La tabla es la marea astronómica; lo que le suman el viento y la presión (en
Uruguay, más que la marea misma) sale del nivel de Open-Meteo: su promedio de 25 h, que saca la marea,
menos lo normal ahí. Lo normal es esta referencia: la media del nivel de Open-Meteo en el puerto en los
últimos 92 días. Las apps no pueden pedir 92 días cada vez (el reloj no tiene dónde), así que se publica.

En los puertos de tide/regions.json, menos los de SIN. Un puerto sin su archivo queda con la tabla sola; el
archivo de un puerto que ya no está se borra.

La media cambia centímetros por mes: una corrida que falla deja la de antes, que sigue sirviendo. A Open-Meteo
se le pide de a BATCH puertos, con una pausa entre pedidos (un pedido de 92 días pesa unas 7 llamadas por
puerto, y el tope es 600 por minuto).

    python3 tools/nivel.py            baja el nivel de cada puerto y reescribe nivel/<puerto>.json si cambió
"""
import datetime as dt
import json
import os
import statistics as st
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from armada import MARINE  # noqa: E402

OUT = os.path.join(ROOT, "nivel")
# puertos sin referencia: Open-Meteo no sigue a su mareógrafo, o un pico suyo se aparta de la media del puerto
SIN = ("ticon-55de77", "ticon-d44c01", "ticon-041ef0", "jma-zf", "ticon-de0584", "noaa-1617433")
BATCH = 50                                  # puertos por pedido a Open-Meteo
DAYS = 92                                   # lo más que da Open-Meteo para atrás, y lo medido en marea_meteo.py
MIN_HOURS = 24 * 60                         # con menos horas que estas no se publica
PER_MINUTE = 450                            # llamadas de Open-Meteo por minuto, con margen
AGENT = {"User-Agent": "surf-dawn-data (nivel del mar)"}


def points():
    """{puerto: (lat, lon)} de tide/ports.json (los meses de las tablas de afuera de Uruguay no lo dicen)."""
    with open(os.path.join(ROOT, "tide", "ports.json"), encoding="utf-8") as f:
        return {p["key"]: (p["lat"], p["lon"]) for p in json.load(f)}


def ports():
    """Los puertos de las regiones (tide/regions.json), menos SIN."""
    with open(os.path.join(ROOT, "tide", "regions.json"), encoding="utf-8") as f:
        used = {p[0] for ps in json.load(f).values() for p in ps}
    return sorted(used - set(SIN))


def ask(url):
    """El JSON de url, con tres reintentos (Open-Meteo contesta 429 si se pasa del minuto o la hora)."""
    err = None
    for wait in (0, 60, 120, 240):
        time.sleep(wait)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=120) as r:
                return json.load(r)
        except Exception as e:                       # noqa: BLE001
            err = e
    raise err


def fetch(keys):
    """{puerto: [nivel en m de cada hora de los últimos DAYS días hasta ahora]}, BATCH puertos por pedido; los de
    un pedido que falla no están (queda su referencia de antes)."""
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    where = points()
    pause = 60 * BATCH * (DAYS + 1) / 14 / PER_MINUTE
    out = {}
    for i in range(0, len(keys), BATCH):
        if i:
            time.sleep(pause)
        part = keys[i:i + BATCH]
        pts = [where[p] for p in part]
        q = urllib.parse.urlencode({
            "latitude": ",".join("%.4f" % la for la, _ in pts), "longitude": ",".join("%.4f" % lo for _, lo in pts),
            "hourly": "sea_level_height_msl", "past_days": DAYS, "forecast_days": 1,
            "timezone": "GMT", "timeformat": "unixtime"}, safe=",")
        try:
            res = ask(MARINE + "?" + q)
        except Exception as e:                       # noqa: BLE001
            print("%s a %s: Open-Meteo no contestó (%s): quedan las de antes" % (part[0], part[-1], e))
            continue
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
    keys = ports()
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".json") and f[:-5] not in keys:
            os.remove(os.path.join(OUT, f))
            print("%s: ya no tiene referencia" % f[:-5])
    for port, levels in fetch(keys).items():
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
