"""Wave buoy observations: one adapter per source, each giving Station objects with hourly
records (time UTC in s, Hs m, Tp s peak, Dp deg the waves come FROM, Tm s mean period).

The parsers are pure (text or rows in, records out) and tested offline; the fetchers download
and cache the raw answers of the day in validate/.cache/<date>/ (cache.py).

Sources (no account needed):
  ndbc   NOAA NDBC realtime2 standard met files (WVHT, DPD, APD, MWD), last 45 days
  cdip   CDIP (Scripps) ERDDAP wave_agg, primary QC flag 1 (waveHs, waveTp, waveTa, waveDp)
  aodn   AODN/IMOS Australian wave buoys, cloud-optimised parquet on S3 (WSSH, WPPE, WPDI, WPFM)
  mi     Marine Institute Ireland ERDDAP IWaveBNetwork30Min (Hs in cm; PeakDirection is "to")
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
MI_ERDDAP = "https://erddap.marine.ie/erddap/tabledap/IWaveBNetwork30Min.csv"
AODN_S3 = "aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet"
PRIORITY = {"cdip": 0, "aodn": 1, "mi": 2, "ndbc": 3}   # same buoy in two sources: keep the first
DAYS = 31                                                # observations asked for (the model window is 30 + today)


class Station:
    def __init__(self, source, sid, name, lat, lon, records):
        self.source, self.sid, self.name = source, str(sid), name
        self.lat, self.lon = lat, lon
        self.records = records                           # [(t, hs, tp, dp, tm)], any order
        self.hourly = {}                                 # hour (t // 3600) -> (hs, tp, dp, tm)

    @property
    def id(self):
        return "%s:%s" % (self.source, self.sid)

    def __repr__(self):
        return "<%s %.3f,%.3f %d h>" % (self.id, self.lat, self.lon, len(self.hourly))


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
    """Clean the station's records, keep the window and resample hourly."""
    recs = []
    for t, hs, tp, dp, tm in st.records:
        if t < since:
            continue
        hs, tp, dp, tm = clean(hs, tp, dp, tm)
        recs.append((t, hs, tp, dp, tm))
    st.records = recs
    st.hourly = hourly(recs)
    return st


# --- NDBC --------------------------------------------------------------------------------------

def parse_ndbc_stations(xml_text):
    """activestations.xml -> {id: (name, lat, lon, type)}."""
    out = {}
    for e in ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text).iter("station"):
        try:
            out[e.get("id").upper()] = (e.get("name") or "", float(e.get("lat")), float(e.get("lon")), e.get("type") or "")
        except (TypeError, ValueError):
            continue
    return out


def parse_ndbc_listing(html):
    """The realtime2 directory listing -> {file name: 'YYYY-MM-DD HH:MM'}."""
    return {m.group(1): m.group(2) for m in re.finditer(r'href="([^"/]+)">[^<]*</a></td><td[^>]*>\s*(\d{4}-\d\d-\d\d \d\d:\d\d)', html)}


def parse_ndbc_txt(text):
    """A realtime2 standard meteorological file -> [(t, hs, tp, dp, tm)]."""
    lines = text.splitlines()
    head = None
    out = []
    for ln in lines:
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
        out.append((t, num(row.get("WVHT")), num(row.get("DPD")), num(row.get("MWD")), num(row.get("APD"))))
    return out


def fetch_ndbc(near, since, log):
    """NDBC buoys near the regions (near(lat, lon) -> bool) with a recent standard met file."""
    stations = parse_ndbc_stations(cache.get_text("ndbc", "activestations.xml", NDBC_STATIONS, UA))
    listing = parse_ndbc_listing(cache.get_text("ndbc", "realtime2.html", NDBC_DIR, UA))
    recent = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 3 * 86400))
    files = {f[:-4].upper(): f for f in listing if f.endswith(".txt")}
    spec = {f[:-5].upper() for f in listing if f.endswith(".spec")}
    cand = []
    for sid, (name, lat, lon, kind) in stations.items():
        f = files.get(sid)
        if not f or listing[f][:10] < recent or kind in ("dart", "tao", "usv"):
            continue
        if (sid in spec or kind == "buoy") and near(lat, lon):
            cand.append((sid, name, lat, lon, f))
    log("ndbc: %d active stations, %d with recent files near the regions" % (len(stations), len(cand)))
    out = []
    for sid, name, lat, lon, f in sorted(cand):
        try:
            text = cache.get_text("ndbc", f, NDBC_DIR + f, UA, pause=0.3)
        except Exception as e:                    # noqa: BLE001 - one station does not stop the rest
            log("  ndbc %s: %s" % (sid, str(e)[:80]))
            continue
        out.append(finish(Station("ndbc", sid, name, lat, lon, parse_ndbc_txt(text)), since))
    return out


# --- ERDDAP (CDIP, Marine Institute) ------------------------------------------------------------

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


def stations_from_rows(source, rows, sid_key, conv, name_key=None, names=None, slug=False):
    """Group ERDDAP rows by station: position = median of the rows' positions."""
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
        recs = []
        for r in rs:
            try:
                recs.append((iso(r["time"]),) + conv(r))
            except (KeyError, ValueError):
                continue
        out.append(Station(source, sid, name, statistics.median(lats), statistics.median(lons), recs))
    return out


def cdip_conv(r):
    return num(r.get("waveHs")), num(r.get("waveTp")), num(r.get("waveDp")), num(r.get("waveTa"))


def fetch_cdip(since, log):
    url = erddap_url(CDIP_ERDDAP, ["station_id", "time", "latitude", "longitude", "waveHs", "waveTp", "waveTa", "waveDp"],
                     ["time>=now-%ddays" % DAYS, "waveFlagPrimary=1"])
    rows = parse_erddap_csv(cache.get_text("cdip", "wave_agg.csv", url, UA, timeout=600))
    nurl = erddap_url(CDIP_ERDDAP, ["station_id", "metaStationName"], ["time>=now-3days", "distinct()"])
    try:
        names = {r["station_id"]: r["metaStationName"] for r in parse_erddap_csv(cache.get_text("cdip", "names.csv", nurl, UA))}
    except Exception as e:                        # noqa: BLE001 - names are cosmetic
        log("  cdip names: %s" % str(e)[:80])
        names = {}
    st = stations_from_rows("cdip", rows, "station_id", cdip_conv, names=names)
    log("cdip: %d rows, %d stations" % (len(rows), len(st)))
    return [finish(s, since) for s in st]


def mi_conv(r):
    hs = num(r.get("SignificantWaveHeight"))
    to = num(r.get("PeakDirection"))
    return (hs / 100.0 if hs is not None else None, num(r.get("PeakPeriod")),
            (to + 180.0) % 360.0 if to is not None else None, num(r.get("EnergyPeriod")))


def fetch_mi(since, log):
    url = erddap_url(MI_ERDDAP, ["station_id", "time", "latitude", "longitude", "SignificantWaveHeight", "PeakPeriod",
                                 "PeakDirection", "EnergyPeriod"], ["time>=now-%ddays" % DAYS])
    rows = parse_erddap_csv(cache.get_text("mi", "IWaveBNetwork30Min.csv", url, UA, timeout=300))
    st = stations_from_rows("mi", rows, "station_id", mi_conv, slug=True)
    log("mi: %d rows, %d stations" % (len(rows), len(st)))
    return [finish(s, since) for s in st]


# --- AODN --------------------------------------------------------------------------------------

def aodn_stations(cols):
    """Columns of the AODN parquet (dict of lists) -> stations by site name."""
    by = {}
    n = len(cols["TIME"])
    for i in range(n):
        by.setdefault(cols["site_name"][i], []).append(i)
    out = []
    for site, idx in by.items():
        lats = [x for x in (num(cols["LATITUDE"][i]) for i in idx) if x is not None]
        lons = [x for x in (num(cols["LONGITUDE"][i]) for i in idx) if x is not None]
        if not lats or not lons:
            continue
        recs = []
        for i in idx:
            t = cols["TIME"][i]
            t = calendar.timegm(t.utctimetuple()) if hasattr(t, "utctimetuple") else int(t)
            recs.append((t, num(cols["WSSH"][i]), num(cols["WPPE"][i]), num(cols["WPDI"][i]), num(cols["WPFM"][i])))
        sid = re.sub(r"[^A-Za-z0-9]+", "-", urllib.parse.unquote(site)).strip("-").lower()
        out.append(Station("aodn", sid, urllib.parse.unquote(site), statistics.median(lats), statistics.median(lons), recs))
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
    tab = d.to_table(columns=cols, filter=ds.field("timestamp") >= month0)
    log("aodn: %d rows since %s" % (tab.num_rows, time.strftime("%Y-%m-%d", time.gmtime(month0))))
    for f in ("TIME", "WSSH", "WPPE", "WPDI", "WPFM"):
        md = d.schema.field(f).metadata or {}
        desc = {k.decode(): v.decode()[:70] for k, v in md.items() if k in (b"long_name", b"standard_name", b"units")}
        log("  aodn %s %s %s" % (f, d.schema.field(f).type, desc or ""))
    t = tab.column("TIME")
    unit = getattr(t.type, "unit", "ns")
    div = {"s": 1, "ms": 10 ** 3, "us": 10 ** 6, "ns": 10 ** 9}[unit]
    secs = pc.divide(t.cast(pa.int64()), div)
    tab = tab.set_column(0, "TIME", secs).filter(pc.greater_equal(secs, since))
    return [finish(s, since) for s in aodn_stations(tab.to_pydict())]


# --- all ---------------------------------------------------------------------------------------

def dedupe(stations, km_fn, within=3.0, same=1.0):
    """The same buoy published twice (an NDBC id for a CDIP buoy, an AODN site renamed): keep one,
    by PRIORITY of source and then by hours of data. Returns (kept, [(dropped, kept twin)])."""
    order = sorted(stations, key=lambda s: (PRIORITY.get(s.source, 9), -len(s.hourly), s.id))
    kept, dropped = [], []
    for s in order:
        twin = next((k for k in kept if km_fn((k.lat, k.lon), (s.lat, s.lon)) <= (within if k.source != s.source else same)), None)
        if twin:
            dropped.append((s, twin))
        else:
            kept.append(s)
    return kept, dropped


def fetch_all(near, since, log, sources=("cdip", "aodn", "mi", "ndbc")):
    """Every source's stations; a source that fails is logged and skipped."""
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
            good = [s for s in st if len(s.hourly) >= 72]
            status[src] = "%d estaciones, %d con ≥ 72 h de Hs" % (len(st), len(good))
            log("%s: %d stations with >= 72 hourly Hs (%.0fs)" % (src, len(good), time.time() - t))
            out += good
        except Exception as e:                    # noqa: BLE001 - one source down does not stop the rest
            status[src] = "falló: %s" % str(e)[:120]
            log("%s FAILED: %s" % (src, e))
            print("%s FAILED" % src, file=sys.stderr)
    return out, status

