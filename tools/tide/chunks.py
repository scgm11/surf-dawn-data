#!/usr/bin/env python3
"""Tramos de las tablas de marea para el campo de datos Marea: `tide/<clave>/d/AAAA-MM-DD.json`.

Un mes (`AAAA-MM.json`, 744 alturas y sus pleamares y bajamares) ocupa unos 11 KB en la memoria
del reloj una vez leído, y el servicio de fondo de un campo de datos tiene 32 KB en los relojes
anteriores a Connect IQ 4 (fēnix 6 Pro, MARQ de 1ª generación…). Un tramo son 156 alturas
horarias (unos 650 bytes): desde las 12:00 del día anterior al día D, en el reloj del puerto,
hasta 6 días después de D, con D = 1, 5, 9… 29 de cada mes. Con el tramo del día de ahora el
reloj tiene las 12 horas para atrás y las 48 para adelante que usa, en un solo pedido.

Se arman para el mes en curso y el siguiente (UTC) desde los meses ya escritos, y se borran los
demás: tools/tide/build_tides.py corre los días 1 y 15 (.github/workflows/tides.yml), así que
siempre quedan al menos dos semanas por delante. Un tramo al que le falta el mes siguiente sale
más corto; con menos de MIN_H horas no sale (el reloj usa entonces los armónicos del puerto).

    python3 tools/tide/chunks.py [--hoy AAAA-MM-DD]
"""
import argparse
import calendar
import datetime
import glob
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TIDE = os.path.join(ROOT, "tide")
STEP = 4                                     # días entre un tramo y el siguiente
BACK_H = 12                                  # horas antes del día D
HOURS = BACK_H + (STEP + 2) * 24             # hasta 48 h después del último instante del tramo
MIN_H = 60                                   # lo que usa el reloj: 12 h atrás y 48 adelante


def add_month(y, m, k):
    i = y * 12 + (m - 1) + k
    return i // 12, i % 12 + 1


def series(port_dir, months):
    """Alturas horarias del puerto (cm) por segundo Unix, de los meses que haya, y su utc_offset."""
    out, off = {}, None
    for y, m in months:
        path = os.path.join(port_dir, "%04d-%02d.json" % (y, m))
        if not os.path.exists(path):
            continue
        d = json.load(open(path, encoding="utf-8"))
        off = int(d.get("utc_offset", 0))
        base = calendar.timegm((y, m, 1, 0, 0, 0)) - off * 3600
        for i, h in enumerate(d["h"]):
            out[base + i * 3600] = h
    return out, off


def chunks(port_dir, today):
    """{nombre: tramo} del mes de `today` y el siguiente."""
    cur = (today.year, today.month)
    months = [add_month(cur[0], cur[1], k) for k in (-1, 0, 1, 2)]
    hs, off = series(port_dir, months)
    if off is None:
        return {}
    out = {}
    for y, m in months[1:3]:
        for day in range(1, calendar.monthrange(y, m)[1] + 1, STEP):
            t0 = calendar.timegm((y, m, day, 0, 0, 0)) - off * 3600 - BACK_H * 3600
            h = []
            for i in range(HOURS):
                v = hs.get(t0 + i * 3600)
                if v is None:
                    break
                h.append(v)
            if len(h) >= MIN_H:
                out["%04d-%02d-%02d" % (y, m, day)] = {"t0": t0, "h": h}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoy", help="AAAA-MM-DD (por defecto, hoy en UTC)")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.hoy) if a.hoy else datetime.datetime.now(datetime.timezone.utc).date()
    ports = written = removed = 0
    for port_dir in sorted(glob.glob(os.path.join(TIDE, "*", ""))):
        port_dir = port_dir.rstrip(os.sep)
        want = chunks(port_dir, today)
        if not want:
            continue
        ports += 1
        d = os.path.join(port_dir, "d")
        os.makedirs(d, exist_ok=True)
        for name, c in want.items():
            path = os.path.join(d, name + ".json")
            text = json.dumps(c, separators=(",", ":"))
            if not os.path.exists(path) or open(path).read() != text:
                open(path, "w").write(text)
                written += 1
        for path in glob.glob(os.path.join(d, "*.json")):
            if os.path.basename(path)[:-5] not in want:
                os.remove(path)
                removed += 1
    print("tramos: %d puertos, %d escritos, %d borrados (%s)" % (ports, written, removed, today.isoformat()))


if __name__ == "__main__":
    main()
