#!/usr/bin/env python3
"""La marea meteorológica de Uruguay (issue scgm11/surf-dawn#72, R2): lo que midieron los mareógrafos de
la Armada (validation/armada, tools/armada.py) contra la tabla del SOHMA sola (tide/<puerto>) y contra
la tabla más la anomalía de 25 h del nivel de Open-Meteo (sea_level_height_msl promediado 25 h, que
saca la marea astronómica, menos su media de 92 días en el puerto, que haría de media fija).

Para cada puerto da:
- sesgo, error sin sesgo, r y error total, hora por hora, de la tabla sola y de la tabla + anomalía;
- cuánto sigue a la anomalía lo que el agua se aparta de la tabla (las dos promediadas 25 h):
  r, pendiente (1 = Open-Meteo acierta el tamaño) y ordenada (lo que queda corrido sin viento);
- lo mismo por día (hora de Uruguay);
- fuera de muestra: una constante por puerto sacada de la primera mitad y probada en la segunda.

Los mareógrafos y la tabla usan el mismo cero, el Plano Hidrométrico Provisorio (ex Wharton): lo dicen
la página de cada estación ("Datos referidos al 0 de las lecturas correspondientes al Plano
Hidrométrico Provisorio") y la introducción de las tablas de La Paloma y de Montevideo (R9, 16/11/2026).
Así que una constante que queda no es de cero: es el nivel medio de hoy por encima del de la tabla, o
una media de 92 días de Open-Meteo que no es la del año (lo estacional). Con la serie larga se ve si
se mantiene.

Sin --dia usa el pasado de Open-Meteo, que ya viene corregido. Con --dia N usa lo que pronosticaba
N días antes (validation/armada/openmeteo, guardado desde el 16/11/2026), que es lo que vería la app.

    python3 tools/marea_meteo.py               contra el pasado de Open-Meteo
    python3 tools/marea_meteo.py --dia 2       contra el pronóstico emitido 2 días antes

Resultados del 16/11/2026 (8-15/11, sin --dia), en el comentario de esa fecha en el issue.
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import statistics as st
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
ARMADA = os.path.join(ROOT, "validation", "armada")
MARINE = "https://marine-api.open-meteo.com/v1/marine"
UTC = dt.timezone.utc
HOUR = dt.timedelta(hours=1)

# (mareógrafo, puerto de la tabla): Punta Lobos está en la bahía de Montevideo.
PAIRS = (("la-paloma", "la-paloma"), ("punta-lobos", "montevideo"))
SAMPLE_WINDOW = dt.timedelta(minutes=7.5)     # las muestras de cada 5 min que valen para una hora
REF_DAYS = 92                                 # la media del nivel de Open-Meteo, lo más que da para atrás


def hourly(raw):
    """{hora UTC: nivel}: la mediana de las muestras a menos de 7,5 min de cada hora, con dos o más."""
    acc = {}
    for t, v in raw:
        h = (t + SAMPLE_WINDOW).replace(minute=0, second=0, microsecond=0)
        if abs(t - h) <= SAMPLE_WINDOW:
            acc.setdefault(h, []).append(v)
    return {h: st.median(v) for h, v in acc.items() if len(v) >= 2}


def lowpass(series):
    """{hora: promedio de las 25 h centradas}, solo donde están las 25 (saca la marea astronómica)."""
    out = {}
    for t in series:
        win = [series.get(t + k * HOUR) for k in range(-12, 13)]
        if all(v is not None for v in win):
            out[t] = sum(win) / 25.0
    return out


def gauge(station):
    raw = []
    with open(os.path.join(ARMADA, station + ".csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["nivel_m"]:
                raw.append((dt.datetime.fromisoformat(r["utc"].replace("Z", "+00:00")), float(r["nivel_m"])))
    return hourly(raw)


def table(port, months):
    """{hora UTC: altura en m} de la tabla del puerto en esos meses (AAAA-MM), y (lat, lon)."""
    out, point = {}, None
    for m in months:
        path = os.path.join(ROOT, "tide", port, m + ".json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            d = json.load(f)
        point = (d["lat"], d["lon"])
        y, mo = map(int, m.split("-"))
        t0 = dt.datetime(y, mo, 1, tzinfo=UTC) - dt.timedelta(hours=d["utc_offset"])
        for i, v in enumerate(d["h"]):
            out[t0 + i * HOUR] = v / 100.0
    return out, point


def om_past(point):
    """{hora UTC: nivel} de Open-Meteo, los últimos REF_DAYS días y mañana."""
    q = urllib.parse.urlencode({"latitude": point[0], "longitude": point[1], "hourly": "sea_level_height_msl",
                                "past_days": REF_DAYS, "forecast_days": 1, "timezone": "GMT"})
    req = urllib.request.Request(MARINE + "?" + q, headers={"User-Agent": "surf-dawn-data (validación de mareas)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        h = json.load(r)["hourly"]
    return {dt.datetime.fromisoformat(t).replace(tzinfo=UTC): v
            for t, v in zip(h["time"], h["sea_level_height_msl"]) if v is not None}


def om_forecast(port, lead_days):
    """{hora UTC: nivel 25 h} con el pronóstico emitido lead_days antes del día (UTC) de cada hora:
    el promedio de 25 h sale de una sola emisión, como lo haría la app."""
    path = os.path.join(ARMADA, "openmeteo", port + ".csv")
    if not os.path.exists(path):
        return {}
    issues = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC)
            issues.setdefault(r["emitido"], {})[t] = float(r["nivel_m"])
    out = {}
    for issued, series in issues.items():
        day = dt.datetime.strptime(issued, "%Y-%m-%d").replace(tzinfo=UTC) + dt.timedelta(days=lead_days)
        for t, v in lowpass(series).items():
            if day <= t < day + dt.timedelta(days=1):
                out[t] = v
    return out


def stats(meas, pred):
    """(sesgo, error sin sesgo, r, error total) de medido - pronosticado."""
    res = [m - p for m, p in zip(meas, pred)]
    mm, mp = st.fmean(meas), st.fmean(pred)
    cov = sum((a - mm) * (b - mp) for a, b in zip(meas, pred))
    den = math.sqrt(sum((a - mm) ** 2 for a in meas) * sum((b - mp) ** 2 for b in pred))
    return st.fmean(res), st.pstdev(res), cov / den if den else float("nan"), math.sqrt(st.fmean(x * x for x in res))


def report(station, port, lead):
    g = gauge(station)
    if not g:
        print("%s: sin datos" % station)
        return
    months = sorted({h.strftime("%Y-%m") for h in g} | {(h - dt.timedelta(days=1)).strftime("%Y-%m") for h in g})
    tb, point = table(port, months)
    past = om_past(point)
    ref = st.fmean(past.values())
    low = om_forecast(port, lead) if lead is not None else lowpass(past)
    anom = {t: v - ref for t, v in low.items()}
    hs = sorted(h for h in g if h in tb and h in anom)
    src = "el pronóstico emitido %d días antes" % lead if lead is not None else "el pasado de Open-Meteo"
    if len(hs) < 48:
        print("\n%s (tabla %s), con %s: %d horas, faltan datos" % (station, port, src, len(hs)))
        return
    print("\n%s (tabla %s), con %s: %s a %s UTC, %d h; media de Open-Meteo en %d días %+.3f m" % (
        station, port, src, hs[0].strftime("%d/%m %H"), hs[-1].strftime("%d/%m %H"), len(hs), REF_DAYS, ref))
    meas = [g[h] for h in hs]
    for name, pred in (("tabla sola", [tb[h] for h in hs]), ("tabla + anomalía", [tb[h] + anom[h] for h in hs])):
        b, s, r, rms = stats(meas, pred)
        print("  %-17s sesgo %+.3f m  error sin sesgo %5.1f cm  r %.2f  error total %5.1f cm" % (
            name, b, s * 100, r, rms * 100))
    off = lowpass({h: g[h] - tb[h] for h in hs})
    both = sorted(h for h in off if h in anom)
    if len(both) >= 24:
        a, o = [anom[h] for h in both], [off[h] for h in both]
        ma, mo = st.fmean(a), st.fmean(o)
        slope = sum((x - ma) * (y - mo) for x, y in zip(a, o)) / sum((x - ma) ** 2 for x in a)
        print("  medido - tabla (25 h) contra la anomalía: %d h, r %.2f, pendiente %.2f, ordenada %+.3f m" % (
            len(both), stats(o, a)[2], slope, mo - slope * ma))
    days = {}
    for h in hs:
        days.setdefault((h - dt.timedelta(hours=3)).date(), []).append(h)
    print("  día     horas  medido-tabla  anomalía  medido-(tabla+anomalía)")
    for d, hh in sorted(days.items()):
        if len(hh) >= 12:
            x = st.fmean(g[h] - tb[h] for h in hh)
            y = st.fmean(anom[h] for h in hh)
            print("  %s  %5d  %+.3f        %+.3f    %+.3f" % (d.strftime("%d/%m"), len(hh), x, y, x - y))
    local = hs[len(hs) // 2] - dt.timedelta(hours=3)            # partida en la medianoche de Uruguay más cercana
    cut = local.replace(hour=0) + dt.timedelta(days=1 if local.hour >= 12 else 0, hours=3)
    first, second = [h for h in hs if h < cut], [h for h in hs if h >= cut]
    c_tab = st.fmean(g[h] - tb[h] for h in first)
    c_anom = st.fmean(g[h] - tb[h] - anom[h] for h in first)
    uy = [(x - dt.timedelta(hours=3)).strftime("%d/%m") for x in (first[0], first[-1], second[0], second[-1])]
    print("  fuera de muestra (constante del %s al %s, probada del %s al %s, días de Uruguay):" % tuple(uy))
    for name, f in (("tabla sola", lambda h: tb[h]), ("tabla + c", lambda h: tb[h] + c_tab),
                    ("tabla + anomalía", lambda h: tb[h] + anom[h]),
                    ("tabla + anomalía + c", lambda h: tb[h] + anom[h] + c_anom)):
        res = [g[h] - f(h) for h in second]
        print("    %-21s sesgo %+.3f  error total %5.1f cm  máximo %3.0f cm" % (
            name, st.fmean(res), math.sqrt(st.fmean(x * x for x in res)) * 100, max(abs(x) for x in res) * 100))
    print("    c = %+.3f m (tabla), %+.3f m (tabla + anomalía)" % (c_tab, c_anom))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dia", type=int, help="usar el pronóstico de Open-Meteo emitido N días antes")
    a = ap.parse_args()
    for station, port in PAIRS:
        report(station, port, a.dia)


if __name__ == "__main__":
    main()
