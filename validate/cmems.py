"""Copernicus Marine In Situ (INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030, the moorings and the GTS
wave buoys of Europe, Morocco, the Canaries, South America...): the source the other ones lack
(issue #7, §5). It needs a Copernicus Marine account (free): the repository secrets
COPERNICUSMARINE_SERVICE_USERNAME and COPERNICUSMARINE_SERVICE_PASSWORD; without them the source
is skipped (run.py reports it as "sin credenciales").

1. index_latest.txt (the catalogue of the last 30 days' daily files, one per platform and day, with
   its box, times and parameters) -> the wave files (VHM0, VAVH or VGHS) of platforms near the
   regions, inside the window, not already given by another source.
2. Those files are downloaded with the Copernicus Marine Toolbox (copernicusmarine.get, file_list)
   and read with h5netcdf: TIME (days since 1950), LATITUDE / LONGITUDE (scalars or per time), and
   for each record Hs, Tp (peak), Dp (from) and Tm, with their *_QC flags (1 or 2 kept); wind
   WSPD / WDIR when the platform has it.

parse_index() and read_file() are pure and tested offline (validate/test_validate.py).
"""
import calendar
import os
import re
import sys
import time

DATASET = "cmems_obs-ins_glo_phybgcwav_mynrt_na_irr"
INDEX = "index_latest.txt"
EPOCH_1950 = -631152000                      # 1950-01-01T00:00:00Z in unix seconds
GOOD_QC = (1, 2)                             # good, probably good (OceanSITES/Copernicus flags)
MAX_FILES = 8000                             # a month of daily files for ~250 platforms
# the variables, best first (Copernicus In Situ names; the standard names are checked too)
HS = ("VHM0", "VAVH", "VGHS")
TP = ("VTPK",)
DIR = ("VPED", "VMDR", "VDIR")               # all "from" directions
TM = ("VTM02", "VTM10", "VGTA", "VTZA")
WSPD, WDIR = ("WSPD",), ("WDIR",)
ENV_USER, ENV_PASS = "COPERNICUSMARINE_SERVICE_USERNAME", "COPERNICUSMARINE_SERVICE_PASSWORD"


class NoCredentials(Exception):
    pass


def credentials():
    u, p = os.environ.get(ENV_USER, "").strip(), os.environ.get(ENV_PASS, "").strip()
    return (u, p) if u and p else None


def parse_index(text, near, since, have=None):
    """index_latest.txt -> {platform: [file path]} of the wave files ending after `since` whose box
    centre is near the regions (near(lat, lon)) and not within 1 km of a station another source
    already gives (have(lat, lon) -> bool)."""
    out = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        c = line.split(",")
        if len(c) < 12:
            continue
        params = set(c[11].split())
        if not params & set(HS):
            continue
        try:
            lat = (float(c[2]) + float(c[3])) / 2
            lon = (float(c[4]) + float(c[5])) / 2
            end = calendar.timegm(time.strptime(c[7][:19], "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            continue
        if end < since or not near(lat, lon) or (have and have(lat, lon)):
            continue
        name = c[1].rsplit("/", 1)[-1]
        m = re.match(r"^[A-Z]{2}_[A-Z]{2}_([A-Z]{2})_(.+)_\d{8}\.nc$", name)
        if not m or m.group(1) not in ("MO", "TG"):          # moorings (and tide gauges with waves)
            continue
        out.setdefault(m.group(2), []).append(c[1])
    return out


def _one(f, n, qc=True):
    """Variable n of the file per time, as floats (None where missing or with a bad QC flag)."""
    import numpy as np
    v = f.variables[n]
    x = np.asarray(v[...], dtype=float)
    q = np.asarray(f.variables[n + "_QC"][...]) if qc and n + "_QC" in f.variables else None
    if x.ndim == 2:                                          # (TIME, DEPTH): the first level with data
        col = next((j for j in range(x.shape[1]) if (np.isfinite(x[:, j]) & (np.abs(x[:, j]) < 1e30)).any()), 0)
        x = x[:, col]
        q = q[:, col] if q is not None and q.ndim == 2 else q
    bad = ~np.isfinite(x) | (np.abs(x) >= 1e30)
    fill = v.attrs.get("_FillValue")
    if fill is not None:
        bad |= x == float(np.asarray(fill).ravel()[0])
    if q is not None:
        bad |= ~np.isin(q.astype(int).ravel(), GOOD_QC)
    return [None if b else float(val) for val, b in zip(x.ravel(), bad.ravel())]


def _values(f, names, n):
    """Per time, the first of names with a value there (files interleave two message streams: VAVH
    on the hour, VGHS and VDIR ten minutes later), or None if the file has none of them."""
    cols = [_one(f, x) for x in names if x in f.variables]
    if not cols:
        return None
    return [next((c[i] for c in cols if c[i] is not None), None) for i in range(n)]


def _fill_near(t, col, within=1200.0):
    """A missing value takes the one of the nearest record within `within` seconds that has it."""
    have = [i for i, v in enumerate(col) if v is not None]
    if not have:
        return col
    out = list(col)
    j = 0
    for i, v in enumerate(col):
        if v is not None:
            continue
        while j + 1 < len(have) and abs(t[have[j + 1]] - t[i]) <= abs(t[have[j]] - t[i]):
            j += 1
        if abs(t[have[j]] - t[i]) <= within:
            out[i] = col[have[j]]
    return out


def read_file(path):
    """A daily file -> (platform code, name, lat, lon, [(t, hs, tp, dp, tm)], [(t, wspd, wdir)])."""
    import h5netcdf
    import numpy as np
    with h5netcdf.File(path, "r") as f:
        code = str(f.attrs.get("platform_code", "")) or os.path.basename(path).split("_")[3]
        name = str(f.attrs.get("platform_name", "") or code)
        t = np.asarray(f.variables["TIME"][...], dtype=float) * 86400.0 + EPOCH_1950
        n = t.size
        tq = np.asarray(f.variables["TIME_QC"][...]).astype(int) if "TIME_QC" in f.variables else np.ones(n, int)
        lat = np.asarray(f.variables["LATITUDE"][...], dtype=float).ravel()
        lon = np.asarray(f.variables["LONGITUDE"][...], dtype=float).ravel()
        lat, lon = lat[np.abs(lat) <= 90], lon[np.abs(lon) <= 360]
        if not lat.size or not lon.size:
            return None
        cols = [_values(f, names, n) or [None] * n for names in (HS, TP, DIR, TM)]
        wind = [_values(f, names, n) for names in (WSPD, WDIR)]
    order = np.argsort(t)
    t, tq = t[order], tq[order]
    cols = [[c[i] for i in order] for c in cols]
    cols = [cols[0]] + [_fill_near(t, c) for c in cols[1:]]
    wind = [[w[i] for i in order] if w else None for w in wind]
    if wind[1]:
        wind[1] = _fill_near(t, wind[1])
    ok = [bool(q in GOOD_QC) for q in tq]
    recs = [(float(t[i]),) + tuple(c[i] for c in cols) for i in range(n) if ok[i] and cols[0][i] is not None]
    wrecs = []
    if wind[0]:
        wd = wind[1] or [None] * n
        wrecs = [(float(t[i]), wind[0][i], wd[i]) for i in range(n) if ok[i] and wind[0][i] is not None]
    return code, name, float(np.median(lat)), float(np.median(lon)), recs, wrecs


def download(paths, directory, log):
    """The files (paths as in the index) into directory with the Toolbox; returns the local paths."""
    import copernicusmarine
    user, pw = credentials()
    os.makedirs(directory, exist_ok=True)
    todo = [p for p in paths if not os.path.exists(os.path.join(directory, p.rsplit("/", 1)[-1]))]
    if todo:
        lst = os.path.join(directory, "files.txt")
        with open(lst, "w") as f:
            f.write("\n".join(todo) + "\n")
        copernicusmarine.get(dataset_id=DATASET, file_list=lst, output_directory=directory, no_directories=True,
                             skip_existing=True, disable_progress_bar=True, username=user, password=pw)
        log("  cmems: %d files downloaded" % len(todo))
    return [os.path.join(directory, p.rsplit("/", 1)[-1]) for p in paths]


def fetch(near, since, log, station_cls, finish, cache_dir, have=None):
    """The Copernicus In Situ stations near the regions (Station objects, finished)."""
    if not credentials():
        raise NoCredentials("sin credenciales (secretos %s y %s)" % (ENV_USER, ENV_PASS))
    d = os.path.join(cache_dir, "cmems")
    idx = download([INDEX], d, log)[0]
    with open(idx, encoding="utf-8", errors="replace") as f:
        plats = parse_index(f.read(), near, since, have)
    files = [p for ps in plats.values() for p in ps]
    log("cmems: %d wave platforms near the regions, %d daily files" % (len(plats), len(files)))
    if len(files) > MAX_FILES:
        files = sorted(files, key=lambda p: p.rsplit("_", 1)[-1], reverse=True)[:MAX_FILES]
        log("  cmems: only the newest %d files" % MAX_FILES)
    local = download(files, d, log)
    by = {}
    for p in local:
        try:
            r = read_file(p)
        except Exception as e:                    # noqa: BLE001 - one bad file does not stop the rest
            log("  cmems %s: %s" % (os.path.basename(p), str(e)[:120]))
            continue
        if r:
            by.setdefault(r[0], []).append(r)
    out = []
    for code, rs in by.items():
        recs = [x for r in rs for x in r[4]]
        wrecs = [x for r in rs for x in r[5]]
        lat = sorted(r[2] for r in rs)[len(rs) // 2]
        lon = sorted(r[3] for r in rs)[len(rs) // 2]
        out.append(finish(station_cls("cmems", code, rs[0][1], lat, lon, recs, wind_records=wrecs), since))
    return out


if __name__ == "__main__":                       # python3 validate/cmems.py FILE.nc ...: what read_file sees
    for p in sys.argv[1:]:
        r = read_file(p)
        print(p, r and (r[0], r[1], r[2], r[3], len(r[4]), r[4][:2], len(r[5]), r[5][:2]))
