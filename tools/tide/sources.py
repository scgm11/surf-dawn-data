"""The tide sources of tools/tide/build_tides.py: station catalogs and hourly heights (cm, UTC).

Every heights function returns a numpy array with one value per UTC hour of the year
(8760 or 8784), NaN where the source has nothing, or raises SourceError.

- NOAA CO-OPS (US public domain): harmonic (type R) stations, hourly predictions on MLLW.
- JMA (Public Data License 1.0): hourly tide tables in JST on the tide-table datum (DL).
- Marine Institute Ireland (CC BY 4.0): ERDDAP IMI-TidePrediction, 5-minute predictions -> hourly.
- LINZ (CC BY 4.0, Crown copyright): highs and lows in NZ local time -> hourly by half cosines.
- TICON-3 (CC BY 4.0, Hart-Davis et al. 2022): harmonic constants of GESLA-3 gauges.
"""
import calendar
import csv
import datetime as dt
import html
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from zoneinfo import ZoneInfo

import numpy as np

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from tools.lib import tide as tidelib  # noqa: E402

UA = {"User-Agent": "surf-dawn-data/1.0 (+https://github.com/scgm11/surf-dawn-data)"}
NOAA_API = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
NOAA_STATIONS = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=tidepredictions"
JMA_LIST = "https://www.data.jma.go.jp/kaiyou/db/tide/suisan/station%d.php"
JMA_TXT = "https://www.data.jma.go.jp/kaiyou/data/db/tide/suisan/txt/%d/%s.txt"
IMI = "https://erddap.marine.ie/erddap/tabledap/IMI-TidePrediction.csv"
IMI_INFO = "https://erddap.marine.ie/erddap/info/IMI-TidePrediction/index.csv"
LINZ_LIST = "https://www.linz.govt.nz/products-services/tides-and-tidal-streams/tide-predictions/tide-predictions-list-view"
LINZ_CSV = "https://static.charts.linz.govt.nz/tide-tables/maj-ports/csv/"
TICON_ZIP = "https://download.pangaea.de/dataset/951610/files/TICON_3.zip"


class SourceError(Exception):
    pass


def get(url, tries=3, timeout=120, pause=0.0, quiet404=False):
    """Bytes of url, with retries; 404 raises SourceError at once."""
    last = None
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                data = r.read()
            if pause:
                time.sleep(pause)
            return data
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                if not quiet404:
                    print("  404 %s" % url, flush=True)
                raise SourceError("404 %s" % url)
        except Exception as e:  # noqa: BLE001 (timeouts, resets)
            last = e
        time.sleep(5 * (k + 1))
    raise SourceError("%s: %s" % (url, last))


def year_hours(year):
    """UTC epochs of every hour of the year."""
    t0 = calendar.timegm((year, 1, 1, 0, 0, 0))
    t1 = calendar.timegm((year + 1, 1, 1, 0, 0, 0))
    return np.arange(t0, t1, 3600, dtype=np.int64)


# ---------------------------------------------------------------- NOAA

def noaa_stations():
    st = json.loads(get(NOAA_STATIONS))["stations"]
    out = []
    for s in st:
        if s.get("type") != "R" or s.get("lat") is None or s.get("lng") is None:
            continue
        name = s["name"].strip()
        if s.get("state"):
            name += ", " + s["state"]
        out.append({"id": s["id"], "name": name, "lat": float(s["lat"]), "lon": float(s["lng"])})
    return out


def noaa_year(sid, year, datum="MLLW"):
    q = {"product": "predictions", "application": "surf-dawn", "begin_date": "%d0101" % year,
         "end_date": "%d1231" % year, "datum": datum, "station": sid, "time_zone": "gmt", "units": "metric",
         "interval": "h", "format": "json"}
    d = json.loads(get(NOAA_API + "?" + urllib.parse.urlencode(q), pause=1.0))
    if "predictions" not in d:
        raise SourceError("noaa %s %d %s: %s" % (sid, year, datum, json.dumps(d)[:200]))
    hours = year_hours(year)
    out = np.full(len(hours), np.nan)
    t0 = hours[0]
    for p in d["predictions"]:
        t = calendar.timegm(time.strptime(p["t"], "%Y-%m-%d %H:%M"))
        i = (t - t0) // 3600
        if 0 <= i < len(out) and (t - t0) % 3600 == 0 and p["v"] not in ("", None):
            out[i] = float(p["v"]) * 100.0
    return out


# ---------------------------------------------------------------- JMA

def jma_stations(year):
    t = get(JMA_LIST % year).decode("utf-8", "replace")
    rx = re.compile(r"<td>(\d+)</td>\s*<td>([A-Z0-9]{2})</td>\s*<td><a[^>]*>([^<]+)</a></td>\s*"
                    r"<td>(\d+)\D(\d+)'</td>\s*<td>(\d+)\D(\d+)'</td>")
    out = []
    for m in rx.finditer(t):
        out.append({"code": m.group(2), "name": html.unescape(m.group(3)).strip(),
                    "lat": int(m.group(4)) + int(m.group(5)) / 60.0, "lon": int(m.group(6)) + int(m.group(7)) / 60.0})
    if not out:
        raise SourceError("jma: no stations parsed in %s" % (JMA_LIST % year))
    return out


def jma_jst_year(code, year):
    """Hourly heights (cm, tide-table datum) of a JST year, indexed from Jan 1 00:00 JST; None when
    JMA has not published that year (404)."""
    try:
        b = get(JMA_TXT % (year, code), pause=0.5, quiet404=True)
    except SourceError as e:
        if str(e).startswith("404"):
            return None
        raise
    days = 366 if calendar.isleap(year) else 365
    out = np.full(days * 24, np.nan)
    for ln in b.decode("ascii", "replace").splitlines():
        if len(ln) < 80:
            continue
        try:
            yy, mm, dd = int(ln[72:74]), int(ln[74:76]), int(ln[76:78])
        except ValueError:
            continue
        if ln[78:80] != code or 2000 + yy != year:
            continue
        doy = (dt.date(year, mm, dd) - dt.date(year, 1, 1)).days
        for h in range(24):
            f = ln[h * 3:h * 3 + 3].strip()
            if f and f not in ("999", "***"):
                out[doy * 24 + h] = float(f)
    if np.isnan(out).sum() > 48:
        raise SourceError("jma %s %d: %d hours missing" % (code, year, int(np.isnan(out).sum())))
    return out


def jma_year(code, year):
    """UTC year from the JST tables of year and year+1 (JST = UTC+9); NaN where JMA has not
    published yet (the last 9 hours of the year until next year's table is out)."""
    a = jma_jst_year(code, year)
    if a is None:
        raise SourceError("jma %s %d: not published" % (code, year))
    b = jma_jst_year(code, year + 1)
    n = len(year_hours(year))
    tail = b[:9] if b is not None else np.full(9, np.nan)
    return np.concatenate([a, tail])[9:9 + n]


# ---------------------------------------------------------------- Marine Institute (Ireland)

def imi_info():
    """{variable: {attribute: value}} of the ERDDAP dataset (datum and time coverage)."""
    rows = list(csv.reader(io.StringIO(get(IMI_INFO).decode("utf-8", "replace"))))
    out = {}
    for r in rows[1:]:
        if len(r) >= 5:
            out.setdefault(r[1], {})[r[2]] = r[4]
    return out


def imi_stations():
    b = get(IMI + "?stationID,latitude,longitude&distinct()")
    out = []
    for r in list(csv.reader(io.StringIO(b.decode("utf-8"))))[2:]:
        if len(r) == 3 and r[0]:
            name = r[0].replace("_MODELLED", "").replace("_", " ")
            out.append({"id": r[0], "name": name, "lat": float(r[1]), "lon": float(r[2]),
                        "modelled": r[0].endswith("_MODELLED")})
    return out


def imi_year(sid, year, var="Water_Level"):
    q = "?" + urllib.parse.quote("time,%s" % var, safe=",") + "&stationID=" + urllib.parse.quote('"%s"' % sid) + \
        "&time%3E=" + "%d-01-01T00:00:00Z" % year + "&time%3C=" + "%d-01-01T00:30:00Z" % (year + 1)
    hours = year_hours(year)
    try:
        b = get(IMI + q, pause=1.0, quiet404=True, timeout=300)
    except SourceError as e:
        if str(e).startswith("404"):           # ERDDAP: "Your query produced no matching results"
            return np.full(len(hours), np.nan)
        raise
    T, V = [], []
    for r in list(csv.reader(io.StringIO(b.decode("utf-8"))))[2:]:
        if len(r) != 2 or not r[1] or r[1] == "NaN":
            continue
        T.append(calendar.timegm(time.strptime(r[0], "%Y-%m-%dT%H:%M:%SZ")))
        V.append(float(r[1]) * 100.0)
    out = np.full(len(hours), np.nan)
    if len(T) < 2:
        return out
    T, V = np.array(T, dtype=np.int64), np.array(V)
    o = np.argsort(T)
    T, V = T[o], V[o]
    j = np.searchsorted(T, hours)
    jl, jr = np.clip(j - 1, 0, len(T) - 1), np.clip(j, 0, len(T) - 1)
    gap = np.minimum(np.abs(T[jl] - hours), np.abs(T[jr] - hours))
    vals = np.interp(hours, T, V)
    ok = (gap <= 900) & (hours >= T[0]) & (hours <= T[-1])
    out[ok] = vals[ok]
    return out


# ---------------------------------------------------------------- LINZ (New Zealand)

def linz_ports(year):
    """{name: set(years)} of the major/secondary ports LINZ publishes as CSV."""
    t = get(LINZ_LIST).decode("utf-8", "replace")
    out = {}
    for href in re.findall(r'href="([^"]+\.csv)"', t):
        href = urllib.parse.unquote(html.unescape(href))
        m = re.search(r"/maj-ports/csv/(.+) (\d{4})\.csv$", href)
        if m:
            out.setdefault(m.group(1), set()).add(int(m.group(2)))
    if not out:
        raise SourceError("linz: no CSV links in the list page")
    return out


def _linz_csv(name, year):
    return get(LINZ_CSV + urllib.parse.quote("%s %d.csv" % (name, year)), pause=0.3, quiet404=True) \
        .decode("utf-8-sig", "replace")


def _dm(deg, mins, hemi):
    v = int(deg) + float(mins) / 60.0
    return -v if hemi in "SW" else v


def linz_position(name, year):
    """The port's position in the CSV header: 41°17'S or 41°54.5'S (the minute mark is sometimes missing)."""
    head = _linz_csv(name, year).splitlines()[0]
    m = re.search(r"(\d+)°\s*(\d+(?:\.\d+)?)'?\s*([NS])\s*,\s*(\d+)°\s*(\d+(?:\.\d+)?)'?\s*([EW])", head)
    if not m:
        raise SourceError("linz %s: no position in %r" % (name, head[:80]))
    return _dm(*m.group(1, 2, 3)), _dm(*m.group(4, 5, 6))


def linz_extremes(name, year):
    """[(UTC epoch, height cm)] of the year's highs and lows, from local (standard or daylight) time."""
    tz = ZoneInfo("Pacific/Chatham" if "Chatham" in name else "Pacific/Auckland")
    out = []
    for r in csv.reader(io.StringIO(_linz_csv(name, year))):
        if len(r) < 6 or not r[0].strip().isdigit() or not r[3].strip().isdigit():
            continue
        d, m, y = int(r[0]), int(r[2]), int(r[3])
        for k in range(4, len(r) - 1, 2):
            hm, v = r[k].strip(), r[k + 1].strip()
            if not hm or not v:
                continue
            hh, mi = (int(x) for x in hm.split(":"))
            local = dt.datetime(y, m, d, hh, mi, tzinfo=tz)
            t = local.timestamp()
            if out and t <= out[-1][0]:          # the repeated hour when daylight saving ends
                t = local.replace(fold=1).timestamp()
            out.append((t, float(v) * 100.0))
    if len(out) < 600:
        raise SourceError("linz %s %d: only %d turns" % (name, year, len(out)))
    return out


def linz_year(name, year, have_years):
    """Hourly UTC heights by half cosines between the turns of the year and its neighbours."""
    ext = []
    for y in (year - 1, year, year + 1):
        if y in have_years:
            try:
                ext += linz_extremes(name, y)
            except SourceError as e:
                if y == year:
                    raise
                print("  linz %s: %s" % (name, e), flush=True)
    if not ext:
        raise SourceError("linz %s %d: not published" % (name, year))
    ext.sort()
    hours = year_hours(year)
    first, last = ext[0][0], ext[-1][0]
    h, _ = tidelib.half_cosine([((t - hours[0]) / 3600.0, v) for t, v in ext], [float(i) for i in range(len(hours))])
    out = np.array(h)
    out[(hours < first) | (hours > last)] = np.nan      # no extrapolation past the published turns
    return out


# ---------------------------------------------------------------- TICON-3

def ticon_gauges(zip_path):
    """Gauges of TICON_3.txt: lat, lon (-180..180), source, type, start/end dates, record days and
    {constituent: (amplitude cm, Greenwich phase lag deg)}."""
    z = zipfile.ZipFile(zip_path)
    name = [i.filename for i in z.infolist() if i.filename.lower().endswith(".txt")][0]
    gauges = {}
    for ln in z.read(name).decode("utf-8", "replace").splitlines():
        p = [x.strip() for x in ln.split("\t")]
        if len(p) < 14:
            p = ln.split()
        if len(p) < 14:
            continue
        try:
            lat, lon = float(p[0]), float(p[1])
            amp, pha = float(p[3]), float(p[4])
        except ValueError:
            continue
        key = (p[0], p[1], p[12], p[10], p[11])
        g = gauges.get(key)
        if g is None:
            try:
                d0 = dt.datetime.strptime(p[10], "%d/%m/%Y").date()
                d1 = dt.datetime.strptime(p[11], "%d/%m/%Y").date()
            except ValueError:
                continue
            g = gauges[key] = {"lat": lat, "lon": (lon + 180.0) % 360.0 - 180.0, "source": p[12], "type": p[13],
                               "start": d0.isoformat(), "end": d1.isoformat(), "days": (d1 - d0).days,
                               "nobs": p[8], "col8": p[7], "col10": p[9], "cons": {}}
        g["cons"][p[2].upper()] = (amp, pha)
    return list(gauges.values())


def ticon_manual(zip_path):
    """The column description of the user manual, for the log (needs pypdf; optional)."""
    try:
        import pypdf
    except ImportError:
        return ""
    z = zipfile.ZipFile(zip_path)
    pdf = [i.filename for i in z.infolist() if i.filename.lower().endswith(".pdf")]
    if not pdf:
        return ""
    r = pypdf.PdfReader(io.BytesIO(z.read(pdf[0])))
    text = "\n".join((p.extract_text() or "") for p in r.pages[:6])
    keep = [ln for ln in text.splitlines() if re.search(r"(?i)column|record|missing|observ|length|phase|amplitude", ln)]
    return "\n".join(keep[:60])
