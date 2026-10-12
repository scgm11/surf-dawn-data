#!/usr/bin/env python3
"""Temporary: prints the raw shape of every tide source (run in CI, read tide/build.log)."""
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile

UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)"}


def get(url, n=None):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            data = r.read()
        print("GET %s -> %d bytes" % (url, len(data)))
        return data
    except Exception as e:  # noqa: BLE001
        print("GET %s -> ERROR %s" % (url, e))
        return None


def head(b, n=1500):
    if b is None:
        return
    print(repr(b[:n].decode("utf-8", "replace")))


def section(t):
    print("\n==== %s ====" % t, flush=True)


section("NOAA stations")
b = get("https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=tidepredictions")
if b:
    st = json.loads(b)["stations"]
    print("count", len(st), "R", sum(1 for s in st if s["type"] == "R"))
    print(json.dumps(st[0]))
    for sid in ("9684403", "9812501", "1910000", "1732417", "9410230"):
        print([s for s in st if s["id"] == sid])
    print("non-US R:", [(s["id"], s["name"], round(s["lat"], 2), round(s["lng"], 2)) for s in st
                        if s["type"] == "R" and not s["state"]][:200])
for sid, datum in (("1910000", "MLLW"), ("1732417", "MLLW"), ("9812501", "MLLW"), ("9684403", "MLLW"), ("1732417", "MSL")):
    head(get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=surf-dawn"
             "&begin_date=20260101&end_date=20260101&datum=%s&station=%s&time_zone=gmt&units=metric&interval=h&format=json" % (datum, sid)), 400)
head(get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=surf-dawn"
         "&begin_date=20260101&end_date=20271231&datum=MLLW&station=9410230&time_zone=gmt&units=metric&interval=h&format=json"), 300)
head(get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=surf-dawn"
         "&begin_date=20260101&end_date=20260102&datum=MLLW&station=9410230&time_zone=gmt&units=metric&interval=hilo&format=json"), 600)
head(get("https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/1732417/harcon.json?units=metric"), 800)
head(get("https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/1732417/datums.json?units=metric"), 1200)

section("JMA")
b = get("https://www.data.jma.go.jp/kaiyou/db/tide/suisan/station2026.php")
if b:
    t = b.decode("utf-8", "replace")
    i = t.find("<table")
    print(repr(t[i:i + 4000]))
    print("rows with codes:", len(re.findall(r"<tr", t)))
for y in (2026, 2027, 2028):
    b = get("https://www.data.jma.go.jp/kaiyou/data/db/tide/suisan/txt/%d/TK.txt" % y)
    if b:
        lines = b.decode("ascii", "replace").splitlines()
        print(y, "lines", len(lines))
        for ln in lines[:2] + lines[-1:]:
            print(repr(ln))

section("IMI")
b = get("https://erddap.marine.ie/erddap/tabledap/IMI-TidePrediction.csv?stationID,latitude,longitude&distinct()")
head(b, 6000)
b = get("https://erddap.marine.ie/erddap/tabledap/IMI-TidePrediction.csv?time,stationID,Water_Level"
        "&time%3E=2026-01-01T00:00:00Z&time%3C=2026-01-01T02:00:00Z")
head(b, 3000)

section("LINZ")
b = get("https://www.linz.govt.nz/products-services/tides-and-tidal-streams/tide-predictions/tide-predictions-list-view")
if not b:
    b = get("https://www.linz.govt.nz/node/10906")
if b:
    t = b.decode("utf-8", "replace")
    links = sorted(set(re.findall(r'href="([^"]+\.csv)"', t)))
    print(len(links), "csv links")
    for ln in links:
        print(" ", ln)
    pdfs = sorted(set(re.findall(r'href="([^"]+sec-ports[^"]+)"', t)))
    print(len(pdfs), "sec-port links; first:", pdfs[:10])
for name in ("Manu Bay 2026", "Manu Bay 2028", "Auckland 2027"):
    b = get("https://static.charts.linz.govt.nz/tide-tables/maj-ports/csv/" + urllib.parse.quote(name) + ".csv")
    if b:
        lines = b.decode("utf-8", "replace").splitlines()
        print(name, "lines", len(lines))
        for ln in lines[:8] + lines[-2:]:
            print(repr(ln))
b = get("https://www.linz.govt.nz/sites/default/files/2026-06/NZNA_Secondary-ports-2026-27.csv")
if b:
    lines = b.decode("utf-8-sig", "replace").splitlines()
    print("secondary lines", len(lines))
    for ln in lines:
        if re.search(r"hhmm,|Manu|Anawhata|Raglan|Castlepoint|Kaikoura|Kaik", ln):
            print(repr(ln))

section("TICON-3")
b = get("https://download.pangaea.de/dataset/951610/files/TICON_3.zip")
if b:
    z = zipfile.ZipFile(io.BytesIO(b))
    for i in z.infolist():
        print(i.filename, i.file_size)
    for i in z.infolist():
        if i.filename.lower().endswith(".txt"):
            lines = z.read(i).decode("utf-8", "replace").splitlines()
            print(i.filename, "lines", len(lines))
            for ln in lines[:6]:
                print(repr(ln))
            cons = sorted(set(ln.split()[2] for ln in lines if len(ln.split()) > 3))
            print("cons", len(cons), cons)
            locs = set(tuple(ln.split()[:2]) for ln in lines if len(ln.split()) > 3)
            print("locations", len(locs))
            print("types", sorted(set(ln.split()[-1] for ln in lines if ln.split())))
            print("sources", sorted(set(ln.split()[-2] for ln in lines if ln.split()))[:80])
            for ln in lines:
                if ln.startswith("32.8") or ln.startswith("21.3"):
                    print(repr(ln))
                    break
sys.stdout.flush()
