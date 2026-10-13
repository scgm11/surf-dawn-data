"""Buoy and coastal station observations: one adapter per source, each giving Station objects with
hourly wave records (time UTC in s, Hs m, Tp s peak, Dp deg the waves come FROM, Tm s mean period)
and hourly wind records (speed m/s at the anemometer, direction deg the wind comes FROM).

The parsers are pure (text or rows in, records out) and tested offline; the fetchers download
and cache the raw answers of the day in validate/.cache/<date>/ (cache.py).

Sources (no account needed):
  ndbc   NOAA NDBC realtime2 standard met files (WVHT, DPD, APD, MWD; WSPD, WDIR), last 45 days: wave
         buoys and every station with met data near the regions (buoys, C-MAN, NOS coastal stations);
         anemometer heights from the station pages (parse_ndbc_height)
  cdip   CDIP (Scripps) ERDDAP wave_agg, primary QC flag 1 (waveHs, waveTp, waveTa, waveDp); no wind
  aodn   AODN/IMOS Australian wave buoys, cloud-optimised parquet on S3 (WSSH, WPPE, WPDI, WPFM; wind
         if the parquet has it)
  mi     Marine Institute Ireland ERDDAP IWaveBNetwork30Min (Hs in cm; PeakDirection is "to") and
         IWBNetwork (weather buoys M2-M6, with wind); columns chosen by CF standard name (wave_columns,
         wind_columns)
"""
import calendar
import csv
import io
import math
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import cache

UA = {"User-Agent": "surf-dawn-validation/1.0 (+https://github.com/scgm11/surf-dawn-data)"}
NDBC_STATIONS = "https://www.ndbc.noaa.gov/activestations.xml"
NDBC_DIR = "https://www.ndbc.noaa.gov/data/realtime2/"
CDIP_ERDDAP = "https://erddap.cdip.ucsd.edu/erddap/tabledap/wave_agg.csv"
MI_BASE = "https://erddap.marine.ie/erddap/"
MI_DATASETS = ("IWaveBNetwork30Min", "IWBNetwork")       # wave buoys; weather buoys M2-M6
AODN_S3 = "aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet"
NDBC_PAGE = "https://www.ndbc.noaa.gov/station_page.php?station="
PRIORITY = {"cdip": 0, "aodn": 1, "mi": 2, "ndbc": 3}   # same buoy in two sources: keep the first
DAYS = 31                                                # observations asked for (the model window is 30 + today)
WIND_EXP = 0.11             # power law U(10) = U(z) (10 / z)^p over the sea, near neutral (Hsu et al. 1994)
Z_MIN, Z_MAX = 1.0, 100.0   # anemometer heights we trust (m above sea level)


class Station:
    def __init__(self, source, sid, name, lat, lon, records, kind="buoy", wind_records=None):
        self.source, self.sid, self.name = source, str(sid), name
        self.lat, self.lon = lat, lon
        self.kind = kind                                 # "buoy", or "fixed" (C-MAN, coastal station)
        self.records = records                           # [(t, hs, tp, dp, tm)], any order
        self.hourly = {}                                 # hour (t // 3600) -> (hs, tp, dp, tm)
        self.wind_records = wind_records or []           # [(t, speed m/s at the anemometer, dir from)]
        self.wind_raw = {}                               # hour -> (speed at the anemometer, dir)
        self.wind = {}                                   # hour -> (speed at 10 m, dir): set_height()
        self.z = None                                    # anemometer height, m above sea level (None: unknown)
        self.factor = 1.0                                # speed at 10 m / speed at z

    @property
    def id(self):
        return "%s:%s" % (self.source, self.sid)

    def set_height(self, z):
        """The anemometer height (m above sea level, None if unknown): the wind is taken to 10 m with
        the power law (no change when the height is unknown or out of Z_MIN..Z_MAX)."""
        self.z = z if z is not None and Z_MIN <= z <= Z_MAX else None
        self.factor = to_10m(self.z)
        self.wind = {h: (v[0] * self.factor if v[0] is not None else None, v[1]) for h, v in self.wind_raw.items()}

    def __repr__(self):
        return "<%s %.3f,%.3f %d h, %d h wind>" % (self.id, self.lat, self.lon, len(self.hourly), len(self.wind_raw))


def to_10m(z):
    """Factor from the wind speed at z m to 10 m (power law, WIND_EXP); 1 when z is unknown."""
    return 1.0 if not z else (10.0 / z) ** WIND_EXP


# --- values ------------------------------------------------------------------------------------

def num(s):
    """A float, or None for blanks, 'MM', 'NaN' and sentinels."""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        v = float(s)
    else:
        s = s.strip()
        if not s or s in ("MM", "NaN", "nan", "null"):
            return None
        try:
            v = float(s)
        except ValueError:
            return None
    if math.isnan(v) or v <= -900 or v >= 990:
        return None
    return v


def clean(hs, tp, dp, tm):
    """Physical ranges; whatever falls out is None (a record without Hs is dropped later)."""
    hs = hs if hs is not None and 0.05 <= hs <= 25 else None
    tp = tp if tp is not None and 1.0 <= tp <= 30 else None
    tm = tm if tm is not None and 1.0 <= tm <= 30 else None
    dp = dp % 360.0 if dp is not None and 0 <= dp <= 360 else None
    return hs, tp, dp, tm


def clean_wind(spd, d):
    """Wind speed 0..75 m/s and direction 0..360 (from); the rest is None."""
    spd = spd if spd is not None and 0.0 <= spd <= 75.0 else None
    d = d % 360.0 if d is not None and 0 <= d <= 360 else None
    return spd, d


def iso(s):
    """'2026-10-12T00:26:00Z' -> unix seconds."""
    s = s.strip().rstrip("Z")
    return calendar.timegm(time.strptime(s[:19], "%Y-%m-%dT%H:%M:%S"))


def hourly(records):
    """For each full hour, the record nearest to it within 30 minutes (Hs required)."""
    best = {}
    for r in records:
        if r[1] is None:
            continue
        t = int(r[0])
        h = (t + 1800) // 3600
        d = abs(t - h * 3600)
        if d > 1800:
            continue
        if h not in best or d < best[h][0] or (d == best[h][0] and t < best[h][1][0]):
            best[h] = (d, r)
    return {h: r[1:] for h, (_, r) in best.items()}


def finish(st, since):
    """Clean the station's records, keep the window and resample hourly (waves and wind)."""
    recs = []
    for t, hs, tp, dp, tm in st.records:
        if t < since:
            continue
        hs, tp, dp, tm = clean(hs, tp, dp, tm)
        recs.append((t, hs, tp, dp, tm))
    st.records = recs
    st.hourly = hourly(recs)
    st.wind_records = [(t,) + clean_wind(v, d) for t, v, d in st.wind_records if t >= since]
    st.wind_raw = hourly(st.wind_records)
    st.set_height(st.z)
    return st


# --- NDBC --------------------------------------------------------------------------------------

def parse_ndbc_stations(xml_text):
    """activestations.xml -> {id: (name, lat, lon, type, met)}; met: the station has meteorological data."""
    out = {}
    for e in ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text).iter("station"):
        try:
            out[e.get("id").upper()] = (e.get("name") or "", float(e.get("lat")), float(e.get("lon")), e.get("type") or "",
                                        (e.get("met") or "").lower() == "y")
        except (TypeError, ValueError):
            continue
    return out


def parse_ndbc_listing(html):
    """The realtime2 directory listing -> {file name: 'YYYY-MM-DD HH:MM'}."""
    return {m.group(1): m.group(2) for m in re.finditer(r'href="([^"/]+)">[^<]*</a></td><td[^>]*>\s*(\d{4}-\d\d-\d\d \d\d:\d\d)', html)}


def ndbc_rows(text):
    """A realtime2 standard meteorological file -> [(t, {column: value})]."""
    head = None
    out = []
    for ln in text.splitlines():
        if ln.startswith("#"):
            if head is None:
                head = ln.lstrip("#").split()
            continue
        if head is None:
            continue
        v = ln.split()
        if len(v) < len(head):
            continue
        row = dict(zip(head, v))
        try:
            yy = int(row.get("YY") or row.get("YYYY"))
            t = calendar.timegm((yy, int(row["MM"]), int(row["DD"]), int(row["hh"]), int(row["mm"]), 0))
        except (KeyError, ValueError):
            continue
        out.append((t, row))
    return out


def parse_ndbc_txt(text):
    """A realtime2 standard meteorological file -> [(t, hs, tp, dp, tm)]."""
    return [(t, num(r.get("WVHT")), num(r.get("DPD")), num(r.get("MWD")), num(r.get("APD"))) for t, r in ndbc_rows(text)]


def parse_ndbc_wind(text):
    """A realtime2 standard meteorological file -> [(t, WSPD m/s, WDIR deg from)]."""
    return [(t, num(r.get("WSPD")), num(r.get("WDIR"))) for t, r in ndbc_rows(text)]


def parse_ndbc_height(html):
    """A station page -> anemometer height in m above mean sea level, or None. The page says
    "Anemometer height: 4.1 m above site elevation" and "Site elevation: sea level" (buoys) or
    "Site elevation: 5.6 m above mean sea level" (stations ashore)."""
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html).replace("&nbsp;", " "))
    m = re.search(r"Anemometer height:\s*([0-9]+(?:\.[0-9]+)?)\s*m\s+above\s+(site elevation|mean sea level|sea level)", text, re.I)
    if not m:
        return None
    z = float(m.group(1))
    if m.group(2).lower() == "site elevation":
        e = re.search(r"Site elevation:\s*(-?[0-9]+(?:\.[0-9]+)?)\s*m\s+(above|below)\s+mean sea level", text, re.I)
        if e:
            z += float(e.group(1)) * (1 if e.group(2).lower() == "above" else -1)
    return z


def fetch_ndbc(near, since, log):
    """NDBC stations near the regions (near(lat, lon) -> bool) with a recent standard met file: wave
    buoys (a .spec file or type buoy) and every station with meteorological data (wind)."""
    stations = parse_ndbc_stations(cache.get_text("ndbc", "activestations.xml", NDBC_STATIONS, UA))
    listing = parse_ndbc_listing(cache.get_text("ndbc", "realtime2.html", NDBC_DIR, UA))
    recent = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 3 * 86400))
    files = {f[:-4].upper(): f for f in listing if f.endswith(".txt")}
    spec = {f[:-5].upper() for f in listing if f.endswith(".spec")}
    cand = []
    for sid, (name, lat, lon, kind, met) in stations.items():
        f = files.get(sid)
        if not f or listing[f][:10] < recent or kind in ("dart", "tao", "usv"):
            continue
        if (sid in spec or kind == "buoy" or met) and near(lat, lon):
            cand.append((sid, name, lat, lon, "buoy" if kind == "buoy" else "fixed", f))
    log("ndbc: %d active stations, %d with recent files near the regions (%d not buoys)"
        % (len(stations), len(cand), sum(1 for c in cand if c[4] != "buoy")))
    out = []
    for sid, name, lat, lon, kind, f in sorted(cand):
        try:
            text = cache.get_text("ndbc", f, NDBC_DIR + f, UA, pause=0.3)
        except Exception as e:                    # noqa: BLE001 - one station does not stop the rest
            log("  ndbc %s: %s" % (sid, str(e)[:80]))
            continue
        out.append(finish(Station("ndbc", sid, name, lat, lon, parse_ndbc_txt(text), kind, parse_ndbc_wind(text)), since))
    return out


def ndbc_heights(stations, log):
    """Set the anemometer height of NDBC stations from their station pages (cached for the day)."""
    got = 0
    for st in stations:
        if st.source != "ndbc":
            continue
        try:
            html = cache.get_text("ndbc", "page-%s.html" % st.sid.lower(), NDBC_PAGE + st.sid.lower(), UA, pause=0.3)
            z = parse_ndbc_height(html)
        except Exception as e:                    # noqa: BLE001 - no height: no adjustment
            log("  ndbc %s page: %s" % (st.sid, str(e)[:80]))
            z = None
        st.set_height(z)
        got += st.z is not None
    log("ndbc: anemometer height of %d of %d stations" % (got, sum(1 for s in stations if s.source == "ndbc")))


# --- ERDDAP (CDIP, Marine Institute) ------------------------------------------------------------

def erddap_time(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def erddap_url(base, variables, constraints):
    """A tabledap query with the constraints percent-encoded (the servers refuse a bare '>')."""
    q = ",".join(variables)
    for c in constraints:
        q += "&" + urllib.parse.quote(c, safe="=(),-:")
    return base + "?" + q


def parse_erddap_csv(text):
    """ERDDAP .csv (names row, units row, data) -> list of dicts."""
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2:
        return []
    names = rows[0]
    return [dict(zip(names, r)) for r in rows[2:] if r]


def stations_from_rows(source, rows, sid_key, conv, name_key=None, names=None, slug=False, wind_conv=None):
    """Group ERDDAP rows by station: position = median of the rows' positions. conv(row) -> (hs, tp,
    dp, tm); wind_conv(row) -> (speed m/s, dir from), when the dataset has wind."""
    by = {}
    for r in rows:
        by.setdefault(r[sid_key], []).append(r)
    out = []
    for sid, rs in by.items():
        lats = [num(r.get("latitude")) for r in rs]
        lons = [num(r.get("longitude")) for r in rs]
        lats, lons = [x for x in lats if x is not None], [x for x in lons if x is not None]
        if not lats or not lons:
            continue
        name = (names or {}).get(sid) or (rs[0].get(name_key) if name_key else "") or sid
        if slug:
            sid = re.sub(r"[^A-Za-z0-9]+", "-", sid).strip("-").lower()
        recs, wrecs = [], []
        for r in rs:
            try:
                t = iso(r["time"])
            except (KeyError, ValueError):
                continue
            recs.append((t,) + conv(r))
            if wind_conv:
                wrecs.append((t,) + wind_conv(r))
        out.append(Station(source, sid, name, statistics.median(lats), statistics.median(lons), recs, wind_records=wrecs))
    return out


def cdip_conv(r):
    return num(r.get("waveHs")), num(r.get("waveTp")), num(r.get("waveDp")), num(r.get("waveTa"))


def fetch_cdip(since, log):
    url = erddap_url(CDIP_ERDDAP, ["station_id", "time", "latitude", "longitude", "waveHs", "waveTp", "waveTa", "waveDp"],
                     ["time>=" + erddap_time(since - 3600), "waveFlagPrimary=1"])
    rows = parse_erddap_csv(cache.get_text("cdip", "wave_agg.csv", url, UA, timeout=600))
    nurl = erddap_url(CDIP_ERDDAP, ["station_id", "metaStationName"], ["time>=" + erddap_time(time.time() - 3 * 86400), "distinct()"])
    try:
        names = {r["station_id"]: r["metaStationName"] for r in parse_erddap_csv(cache.get_text("cdip", "names.csv", nurl, UA))}
    except Exception as e:                        # noqa: BLE001 - names are cosmetic
        log("  cdip names: %s" % str(e)[:80])
        names = {}
    st = stations_from_rows("cdip", rows, "station_id", cdip_conv, names=names)
    log("cdip: %d rows, %d stations" % (len(rows), len(st)))
    return [finish(s, since) for s in st]


# Columns by CF standard name (the Marine Institute datasets differ: cm or m, "to" or "from").
HS_NAMES = ("sea_surface_wave_significant_height",)
TP_NAMES = ("sea_surface_wave_period_at_variance_spectral_density_maximum",)
DIR_FROM = ("sea_surface_wave_from_direction_at_variance_spectral_density_maximum", "sea_surface_wave_from_direction")
DIR_TO = ("sea_surface_wave_to_direction_at_variance_spectral_density_maximum", "sea_surface_wave_to_direction")
TM_NAMES = ("sea_surface_wave_mean_period_from_variance_spectral_density_inverse_frequency_moment",
            "sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment",
            "sea_surface_wave_mean_period_from_variance_spectral_density_second_frequency_moment",
            "sea_surface_wave_mean_period")
BY_NAME = {"hs": ("SignificantWaveHeight", "WaveHeight"), "tp": ("PeakPeriod", "Tp"),
           "dir_to": ("PeakDirection",), "dir_from": ("MeanWaveDirection", "ThTp"), "tm": ("EnergyPeriod", "WavePeriod"),
           "wspd": ("WindSpeed", "wind_speed", "WSPD"), "wdir": ("WindDirection", "wind_from_direction", "WDIR")}
SPEED_UNITS = {"knots": 0.514444, "knot": 0.514444, "kn": 0.514444, "kt": 0.514444, "kts": 0.514444,
               "km/h": 1 / 3.6, "km h-1": 1 / 3.6, "kmh": 1 / 3.6, "m/s": 1.0, "m s-1": 1.0, "m.s-1": 1.0, "ms-1": 1.0}
HEIGHT_ATTRS = ("sensor_height", "instrument_height", "anemometer_height", "height", "sensor_height_above_sea_level")


def erddap_vars(info_csv):
    """ERDDAP info/<dataset>/index.csv -> {variable: {attribute: value}}."""
    out = {}
    for r in csv.reader(io.StringIO(info_csv)):
        if len(r) >= 5 and r[0] == "variable":
            out.setdefault(r[1], {})
        elif len(r) >= 5 and r[0] == "attribute" and r[1] != "NC_GLOBAL":
            out.setdefault(r[1], {})[r[2]] = r[4]
    return out


def wave_columns(vs):
    """Pick the Hs, Tp, direction and mean period columns of an ERDDAP dataset by standard name
    (else by the known names). Returns {"hs": (var, scale), "tp": var, "dir": (var, add), "tm": var}."""
    def by_std(names):
        for n in names:
            for v, a in vs.items():
                if a.get("standard_name") == n and not v.endswith("_qc"):
                    return v
        return None

    def by_name(key):
        return next((v for v in BY_NAME[key] if v in vs), None)
    hs = by_std(HS_NAMES) or by_name("hs")
    if hs is None:
        return None
    unit = (vs[hs].get("units") or "m").strip().lower()
    out = {"hs": (hs, 0.01 if unit == "cm" else 1.0), "tp": by_std(TP_NAMES) or by_name("tp"), "tm": by_std(TM_NAMES) or by_name("tm")}
    d = by_std(DIR_FROM)
    if d:
        out["dir"] = (d, 0.0)
    else:
        d = by_std(DIR_TO) or by_name("dir_to")
        out["dir"] = (d, 180.0) if d else (by_name("dir_from"), 0.0)
    return out


def wind_columns(vs):
    """Wind speed and direction columns of an ERDDAP dataset (CF standard name, else the known names):
    {"spd": (var, factor to m/s), "dir": var or None, "z": height m or None, "units": str}, or None.
    A speed in unknown units is not used (None)."""
    def pick(std, key):
        for v, a in vs.items():
            if a.get("standard_name") == std and not v.endswith("_qc"):
                return v
        return next((v for v in BY_NAME[key] if v in vs), None)
    spd = pick("wind_speed", "wspd")
    if spd is None:
        return None
    unit = (vs[spd].get("units") or "").strip().lower()
    k = SPEED_UNITS.get(unit)
    if k is None:
        return None
    z = None
    for a in HEIGHT_ATTRS:
        z = num(vs[spd].get(a))
        if z is not None:
            break
    return {"spd": (spd, k), "dir": pick("wind_from_direction", "wdir"), "z": z, "units": unit}


def wind_conv_of(cols):
    v, k = cols["spd"]
    d = cols["dir"]

    def conv(r):
        x = num(r.get(v))
        return (x * k if x is not None else None, num(r.get(d)) if d else None)
    return conv


def column_conv(cols):
    hs, k = cols["hs"]
    dv, add = cols.get("dir") or (None, 0.0)

    def conv(r):
        h = num(r.get(hs))
        d = num(r.get(dv)) if dv else None
        return (h * k if h is not None else None, num(r.get(cols["tp"])) if cols["tp"] else None,
                (d + add) % 360.0 if d is not None else None, num(r.get(cols["tm"])) if cols["tm"] else None)
    return conv


def fetch_mi(since, log):
    """Marine Institute: the wave buoy network (30 min) and the weather buoys M2-M6 (hourly)."""
    out, errs = [], []
    for ds in MI_DATASETS:
        base = MI_BASE + "tabledap/%s.csv" % ds
        try:
            vs = erddap_vars(cache.get_text("mi", ds + "-info.csv", MI_BASE + "info/%s/index.csv" % ds, UA))
            cols = wave_columns(vs)
            if not cols:
                raise RuntimeError("no significant wave height column in %s" % ", ".join(sorted(vs)))
            wcols = wind_columns(vs)
            log("mi %s: columns %s; wind %s" % (ds, cols, wcols))
            try:
                last = parse_erddap_csv(cache.get_text("mi", ds + "-last.csv", erddap_url(
                    base, ["station_id", "time"], ['orderByMax("station_id,time")']), UA, timeout=300))
                log("  last records: %s" % ", ".join("%s %s" % (r["station_id"], r["time"][:16]) for r in last))
            except Exception as e:                # noqa: BLE001 - only a diagnostic
                log("  last records: %s" % str(e)[:200])
            want = ["station_id", "time", "latitude", "longitude", cols["hs"][0]] + \
                [c for c in (cols["tp"], (cols.get("dir") or (None,))[0], cols["tm"]) if c]
            if wcols:
                want += [c for c in (wcols["spd"][0], wcols["dir"]) if c and c not in want]
            rows = parse_erddap_csv(cache.get_text("mi", ds + ".csv", erddap_url(base, want, ["time>=" + erddap_time(since - 3600)]),
                                                   UA, timeout=300))
            st = stations_from_rows("mi", rows, "station_id", column_conv(cols), slug=True,
                                    wind_conv=wind_conv_of(wcols) if wcols else None)
            for x in st:
                x.z = wcols["z"] if wcols else None
            log("mi %s: %d rows, %d stations" % (ds, len(rows), len(st)))
            out += [finish(x, since) for x in st]
        except Exception as e:                    # noqa: BLE001 - the other dataset may still work
            if "no matching results" in str(e).lower():
                log("  mi %s: no data in the window" % ds)
                continue
            errs.append("%s: %s" % (ds, str(e)[:300]))
            log("  mi %s failed: %s" % (ds, str(e)[:300]))
    if errs and len(errs) == len(MI_DATASETS):
        raise RuntimeError("; ".join(errs))
    return out


# --- AODN --------------------------------------------------------------------------------------

AODN_WIND = (("WSPD", "WIND_SPEED", "WINDSPEED", "WSPD_AVG"), ("WDIR", "WIND_DIR", "WINDDIR", "WDIR_AVG"))


def aodn_stations(cols):
    """Columns of the AODN parquet (dict of lists) -> stations by site name (with wind when the
    parquet has a wind speed column, AODN_WIND, in m/s)."""
    wspd = next((c for c in AODN_WIND[0] if c in cols), None)
    wdir = next((c for c in AODN_WIND[1] if c in cols), None)
    by, names = {}, {}
    n = len(cols["TIME"])
    for i in range(n):                            # one buoy can come under two spellings ("APOLLO-BAY", "Apollo%20Bay")
        site = urllib.parse.unquote(cols["site_name"][i])
        sid = re.sub(r"[^A-Za-z0-9]+", "-", site).strip("-").lower()
        by.setdefault(sid, []).append(i)
        names.setdefault(sid, site)
    out = []
    for sid, idx in by.items():
        lats = [x for x in (num(cols["LATITUDE"][i]) for i in idx) if x is not None]
        lons = [x for x in (num(cols["LONGITUDE"][i]) for i in idx) if x is not None]
        if not lats or not lons:
            continue
        recs, wrecs = [], []
        for i in idx:
            t = cols["TIME"][i]
            t = calendar.timegm(t.utctimetuple()) if hasattr(t, "utctimetuple") else int(t)
            recs.append((t, num(cols["WSSH"][i]), num(cols["WPPE"][i]), num(cols["WPDI"][i]), num(cols["WPFM"][i])))
            if wspd:
                wrecs.append((t, num(cols[wspd][i]), num(cols[wdir][i]) if wdir else None))
        out.append(Station("aodn", sid, names[sid], statistics.median(lats), statistics.median(lons), recs, wind_records=wrecs))
    return out


def fetch_aodn(since, log):
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.fs as pfs
    fs = pfs.S3FileSystem(anonymous=True, region="ap-southeast-2")
    d = ds.dataset(AODN_S3, filesystem=fs, format="parquet", partitioning="hive")
    t0 = time.gmtime(since - 86400)
    month0 = calendar.timegm((t0.tm_year, t0.tm_mon, 1, 0, 0, 0))
    cols = ["TIME", "LATITUDE", "LONGITUDE", "WSSH", "WPPE", "WPDI", "WPFM", "site_name"]
    names = d.schema.names
    spd = next((c for c in AODN_WIND[0] if c in names), None)
    wdir = next((c for c in AODN_WIND[1] if c in names), None)
    wind = []
    if spd:
        unit = ((d.schema.field(spd).metadata or {}).get(b"units") or b"").decode().strip().lower()
        if SPEED_UNITS.get(unit, 1.0) == 1.0:          # m/s (or no unit given: the IMOS convention)
            wind = [spd] + ([wdir] if wdir else [])
        else:
            log("  aodn: wind speed in %r, not used" % unit)
    log("aodn: columns %s; wind %s" % (" ".join(names), wind or "none"))
    cols += wind
    tab = d.to_table(columns=cols, filter=ds.field("timestamp") >= month0)
    log("aodn: %d rows since %s" % (tab.num_rows, time.strftime("%Y-%m-%d", time.gmtime(month0))))
    for f in ["TIME", "WSSH", "WPPE", "WPDI", "WPFM"] + wind:
        md = d.schema.field(f).metadata or {}
        desc = {k.decode(): v.decode()[:70] for k, v in md.items() if k in (b"long_name", b"standard_name", b"units")}
        log("  aodn %s %s %s" % (f, d.schema.field(f).type, desc or ""))
    t = tab.column("TIME")
    unit = getattr(t.type, "unit", "ns")
    div = {"s": 1, "ms": 10 ** 3, "us": 10 ** 6, "ns": 10 ** 9}[unit]
    secs = pc.divide(t.cast(pa.int64()), div)
    tab = tab.set_column(0, "TIME", secs).filter(pc.greater_equal(secs, since))
    st = [finish(s, since) for s in aodn_stations(tab.to_pydict())]
    short = [s for s in st if 0 < len(s.hourly) < 600]
    for s in short[:12]:                          # why does a buoy have few hours: late start, gaps, no Hs?
        hs = sorted(s.hourly)
        log("  aodn %s: %d records, %d hours, %s .. %s" % (s.id, len(s.records), len(hs),
                                                            time.strftime("%m-%d %H", time.gmtime(hs[0] * 3600)),
                                                            time.strftime("%m-%d %H", time.gmtime(hs[-1] * 3600))))
    return st


# --- all ---------------------------------------------------------------------------------------

STATIONS = []                                    # every station read (also the short ones), for stations.csv


def dedupe(stations, km_fn, within=3.0, same=1.0, hours=lambda s: len(s.hourly)):
    """The same buoy published twice (an NDBC id for a CDIP buoy, an AODN site renamed): keep one,
    by PRIORITY of source and then by hours of data (hours(station): of waves, or of wind for the
    wind stations). Returns (kept, [(dropped, kept twin)])."""
    order = sorted(stations, key=lambda s: (PRIORITY.get(s.source, 9), -hours(s), s.id))
    kept, dropped = [], []
    for s in order:
        twin = next((k for k in kept if km_fn((k.lat, k.lon), (s.lat, s.lon)) <= (within if k.source != s.source else same)), None)
        if twin:
            dropped.append((s, twin))
        else:
            kept.append(s)
    return kept, dropped


MIN_HOURS = 72                                   # a station needs this many hours of waves (or of wind)


def fetch_all(near, since, log, sources=("cdip", "aodn", "mi", "ndbc")):
    """Every source's stations with MIN_HOURS of waves or of wind; a source that fails is logged and skipped."""
    out, status = [], {}
    for src in sources:
        t = time.time()
        try:
            if src == "ndbc":
                st = fetch_ndbc(near, since, log)
            elif src == "cdip":
                st = fetch_cdip(since, log)
            elif src == "aodn":
                st = fetch_aodn(since, log)
            else:
                st = fetch_mi(since, log)
            wave = sum(1 for s in st if len(s.hourly) >= MIN_HOURS)
            wind = sum(1 for s in st if len(s.wind_raw) >= MIN_HOURS)
            status[src] = "%d estaciones, %d con ≥ 72 h de Hs, %d con ≥ 72 h de viento" % (len(st), wave, wind)
            STATIONS.extend(st)
            log("%s: %d stations with >= 72 hourly Hs, %d with >= 72 hourly wind (%.0fs)" % (src, wave, wind, time.time() - t))
            out += [s for s in st if len(s.hourly) >= MIN_HOURS or len(s.wind_raw) >= MIN_HOURS]
        except Exception as e:                    # noqa: BLE001 - one source down does not stop the rest
            status[src] = "falló: %s" % str(e)[:120]
            log("%s FAILED: %s" % (src, e))
            print("%s FAILED" % src, file=sys.stderr)
    return out, status

