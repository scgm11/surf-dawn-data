#!/usr/bin/env python3
"""The wind of the iPhone's weather map (Mapa del tiempo), and which layer of Copernicus Marine has its waves.

The wind is GFS's at 10 m (NOAA, public domain), the same model as the spots' wind (the zones' "m",
gfs_seamless), so the map and a spot's page say the same. Every run takes the newest complete cycle on
AWS (noaa-gfs-bdp-pds), only the two fields of each hour it keeps (UGRD and VGRD at 10 m, by the byte
ranges of the .idx), and writes them as tiles in one file, viento-<RUN>.bin, in the release "viento"
of this repo; the phone asks only for the bytes of its tiles (an HTTP Range). mapa.json says where
everything is (docs/formatos.md, "Mapa del tiempo"):

- the wind: the run, the hours (0 to 120 every 3), the scale and the two levels of tiles: 10 degrees
  with a point every 0.25 (the coasts) and 40 degrees with one every degree (the ocean);
- the waves: the layer of Copernicus Marine's WMTS that is current (its name carries the product's
  version, which changes about once a year) and its last hour, read from the product's GetCapabilities;
  the phone takes it from here, so that a new version needs nothing by hand.

A run whose cycle is already in the release only checks the waves' layer.

The wind of every past day stays too, for the map's "Hace un año" (a year ago): one picture a day, each
place at its midday (the 3-hourly GFS time nearest noon at the tile's longitude, from the cycles' first
hours), the 10-degree tiles that hold a spot and all the 40-degree ones, some 490 KB a day, as
<DAY>.bin in the release "viento-historia" (the last KEEP_DAYS days). Each run adds the days missing
up to yesterday (at most --history of them: the first run filled the year before, from AWS's archive);
mapa.json says which days there are.

Nothing is committed: no queue of data-commit (Action viento.yml, every 6 hours). Needs eccodes (pip install
eccodes) for GRIB2.

    python3 tools/wind.py [--upload] [--run YYYYMMDDHH] [--history DAYS]
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

import numpy as np

RELEASE = "viento"
HISTORY = "viento-historia"
KEEP_DAYS = 400
MAGIC = b"SDV1"
GFS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.%s/%s/atmos/gfs.t%sz.pgrb2.0p25.f%03d"
HOURS = list(range(0, 121, 3))
K = 0.3                                   # m/s a unit: int8 holds ±38 m/s
N = 41                                    # points a side of a tile
LEVELS = [(10, 1), (40, 4)]               # degrees a tile, and a point every that many of 0.25 deg: 10 at 0.25, 40 at 1
WMTS = "https://wmts.marine.copernicus.eu/teroWmts"
WAVES = "GLOBAL_ANALYSISFORECAST_WAV_001_027"
WAVES_DATASET = re.compile(r"^%s/(cmems_mod_glo_wav_anfc_0\.083deg_PT3H-i_(\d{6}))/VHM0$" % WAVES)
UA = {"User-Agent": "surf-dawn-data (github.com/scgm11/surf-dawn-data)"}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache", "wind")


def get(url, rng=None, timeout=120):
    headers = dict(UA, Range="bytes=%d-%d" % rng) if rng else UA
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
        return r.read()


def exists(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA, method="HEAD"), timeout=30):
            return True
    except Exception:
        return False


def newest_cycle(now=None):
    """The newest GFS cycle whose last hour kept is on AWS (YYYYMMDDHH)."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    t = now.replace(minute=0, second=0, microsecond=0, hour=now.hour // 6 * 6)
    for _ in range(8):
        run = t.strftime("%Y%m%d%H")
        if exists(GFS % (run[:8], run[8:], run[8:], HOURS[-1]) + ".idx"):
            return run
        t -= datetime.timedelta(hours=6)
    raise SystemExit("no hay un ciclo de GFS completo en las últimas 48 h")


def fields(run, fh):
    """u and v at 10 m of one hour, lat 90 to -90 and lon 0 to 359.75 (721 x 1440)."""
    import eccodes
    url = GFS % (run[:8], run[8:], run[8:], fh)
    idx = get(url + ".idx").decode().splitlines()
    out = {}
    for i, line in enumerate(idx):
        p = line.split(":")
        if p[3] in ("UGRD", "VGRD") and p[4] == "10 m above ground":
            msg = get(url, (int(p[1]), int(idx[i + 1].split(":")[1]) - 1))
            h = eccodes.codes_new_from_message(msg)
            try:
                ni, nj = eccodes.codes_get(h, "Ni"), eccodes.codes_get(h, "Nj")
                out[p[3]] = eccodes.codes_get_values(h).reshape(nj, ni)
            finally:
                eccodes.codes_release(h)
    if set(out) != {"UGRD", "VGRD"}:
        raise RuntimeError("f%03d sin viento a 10 m" % fh)
    return out["UGRD"], out["VGRD"]


def world(a):
    """A GFS field as the tiles want it: lat -90 to 90 (721 rows), lon -180 to 180 with both ends (1441)."""
    a = np.flipud(a)
    a = np.roll(a, 720, axis=1)
    return np.concatenate([a, a[:, :1]], axis=1)


def quantize(a):
    return np.clip(np.round(a / K), -127, 127).astype(np.int8)


def tiles(u, v):
    """Every tile of every level as bytes, in the file's order: level by level, rows from the south, columns
    from the west; in a tile, hour by hour, u then v, N x N points from the south-west corner by rows."""
    out = []
    for deg, step in LEVELS:
        rows, cols = -(-180 // deg), 360 // deg
        for r in range(rows):
            lat_i = np.minimum((r * deg * 4) + np.arange(N) * step, 720)          # 0.25 degree indices, clamped at 90
            for c in range(cols):
                lon_i = (c * deg * 4) + np.arange(N) * step
                block = np.stack([u[:, lat_i][:, :, lon_i], v[:, lat_i][:, :, lon_i]], axis=1)   # hours, 2, N, N
                out.append(block.tobytes())
    return out


def tile_offset(levels, lat, lon, level=0):
    """Where the tile that holds (lat, lon) begins in the file, and its size (the phone does the same)."""
    size = len(HOURS) * 2 * N * N
    deg = levels[level]["deg"]
    r = min(int((lat + 90) // deg), levels[level]["rows"] - 1)
    c = min(int((lon + 180) // deg), levels[level]["cols"] - 1)
    return levels[level]["offset"] + (r * levels[level]["cols"] + c) * size, size


def waves_layer():
    """The current dataset of the waves (the newest version) and its last hour, from GetCapabilities."""
    xml = get("%s/%s?SERVICE=WMTS&REQUEST=GetCapabilities" % (WMTS, WAVES), timeout=180).decode()
    found = []
    for m in re.finditer(r"<ows:Identifier>([^<]+)</ows:Identifier>", xml):
        w = WAVES_DATASET.match(m.group(1))
        if w:
            block = xml[m.end():xml.find("</Layer>", m.end())]
            span = re.search(r"<Value>([^<]+)</Value>", block)
            found.append((w.group(2), "%s/%s" % (WAVES, w.group(1)), span.group(1).split("/")[1] if span else None))
    if not found:
        raise RuntimeError("Copernicus no tiene la capa de olas (%s)" % WAVES_DATASET.pattern)
    version, layer, last = max(found)
    return {"layer": layer, "last": last}


def noon(lon):
    """The UTC hour, 0 to 24 every 3, nearest midday at longitude `lon` (a tile's middle)."""
    return int(max(0, min(24, round((12 - lon / 15) / 3) * 3)))


def spot_tiles(root=None):
    """The 10-degree tiles (row, col) that hold a spot of spots/r/."""
    root = root or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spots", "r")
    out = set()
    for name in os.listdir(root):
        if name.endswith(".json"):
            for s in json.load(open(os.path.join(root, name))).get("s", []):
                out.add((min(17, int((s[1] + 90) // 10)), min(35, int((s[2] + 180) // 10))))
    return sorted(out)


def day_layout(fine):
    """A day's tiles, (level, row, col, hour): the fine ones given, then every coarse one, each at its midday."""
    out = [(0, r, c, noon(-180 + c * 10 + 5)) for r, c in fine]
    deg = LEVELS[1][0]
    out += [(1, r, c, noon(-180 + c * deg + deg / 2)) for r in range(-(-180 // deg)) for c in range(360 // deg)]
    return out


def one_tile(u, v, level, r, c):
    """One tile of one hour: u then v, N x N from its south-west corner (u, v as world() gives them)."""
    deg, step = LEVELS[level]
    lat_i = np.minimum(r * deg * 4 + np.arange(N) * step, 720)
    lon_i = c * deg * 4 + np.arange(N) * step
    return np.stack([u[lat_i][:, lon_i], v[lat_i][:, lon_i]]).tobytes()


def header(layout):
    """SDV1, version, N, K in hundredths, how many tiles (2 bytes, little-endian), and each tile's level, row,
    column and hour: the tiles follow in that order, 2 x N x N bytes each."""
    return MAGIC + bytes([1, N, int(round(K * 100))]) + len(layout).to_bytes(2, "little") + b"".join(bytes(e) for e in layout)


def gfs_time(t):
    """The cycle and hour that give UTC time t (a multiple of 3 h): the cycle's own analysis or its 3rd hour."""
    return t.replace(hour=t.hour // 6 * 6).strftime("%Y%m%d%H"), t.hour % 6


def history_day(day, layout):
    """The day's file: header() and the tiles, each at its hour of that day (24: 00 of the next)."""
    hours = sorted({e[3] for e in layout})
    t0 = datetime.datetime(day.year, day.month, day.day, tzinfo=datetime.timezone.utc)

    def at(h):
        run, fh = gfs_time(t0 + datetime.timedelta(hours=h))
        uu, vv = fields(run, fh)
        return h, (quantize(world(uu)), quantize(world(vv)))

    with cf.ThreadPoolExecutor(5) as ex:
        got = dict(ex.map(at, hours))
    return header(layout) + b"".join(one_tile(*got[e[3]], e[0], e[1], e[2]) for e in layout)


def history(days, upload):
    """Adds the days missing up to yesterday (at most `days`, the newest first) and drops the oldest; the days there are."""
    have = set()
    if upload:
        if gh("release", "view", HISTORY, check=False).returncode != 0:
            gh("release", "create", HISTORY, "--prerelease", "--title", "Mapa del tiempo: el viento de cada día",
               "--notes", "Una foto por día del viento de GFS (NOAA) a 10 m, cada lugar al mediodía, para el \"Hace un año\" "
               "del mapa del tiempo de la app de iPhone (tools/wind.py, docs/formatos.md).")
        have = {a["name"][:-4] for a in assets(HISTORY) if a["name"].endswith(".bin")}
    today = datetime.datetime.now(datetime.timezone.utc).date()
    layout = day_layout(spot_tiles())
    todo = [today - datetime.timedelta(days=i) for i in range(1, min(days, KEEP_DAYS) + 1)]
    todo = [d for d in todo if d.isoformat() not in have]
    nxt = datetime.datetime(today.year, today.month, today.day, tzinfo=datetime.timezone.utc)
    if todo and todo[0] == today - datetime.timedelta(days=1) and not exists(GFS % (nxt.strftime("%Y%m%d"), "00", "00", 0) + ".idx"):
        todo = todo[1:]                                          # yesterday needs today's 00 UTC: the next run
    batch = []

    def send():
        if upload and batch:                                     # one release lookup for many files: fewer API calls
            gh("release", "upload", HISTORY, *batch, "--clobber")
            for f in batch:
                os.remove(f)
        batch.clear()

    for d in todo:
        try:
            data = history_day(d, layout)
        except Exception as e:                                   # a day the archive lacks stays out
            print("sin", d, e)
            continue
        path = os.path.join(CACHE, "%s.bin" % d.isoformat())
        open(path, "wb").write(data)
        batch.append(path)
        if len(batch) >= 20:
            send()
        have.add(d.isoformat())
        print("día", d, "%d KB" % (len(data) // 1024), flush=True)
    send()
    old = (today - datetime.timedelta(days=KEEP_DAYS)).isoformat()
    for name in sorted(have):
        if name < old:
            if upload:
                gh("release", "delete-asset", HISTORY, name + ".bin", "-y")
            have.discard(name)
            print("borrado", name)
    return sorted(have)


def assets(release):
    """Every asset of a release, all pages ({"name": ...} each)."""
    rid = gh("api", "repos/{owner}/{repo}/releases/tags/%s" % release, "--jq", ".id", check=False).stdout.strip()
    if not rid:
        return []
    out = gh("api", "--paginate", "repos/{owner}/{repo}/releases/%s/assets?per_page=100" % rid, "--jq", ".[] | {name: .name}").stdout
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def gh(*args, check=True):
    return subprocess.run(["gh", *args], check=check, capture_output=True, text=True)


def published():
    """mapa.json of the release, or None."""
    if gh("release", "view", RELEASE, check=False).returncode != 0:
        gh("release", "create", RELEASE, "--prerelease", "--title", "Mapa del tiempo (viento y olas)",
           "--notes", "El viento de GFS (NOAA) a 10 m en baldosas para el mapa del tiempo de la app de iPhone, y la "
           "capa de olas de Copernicus Marine vigente (tools/wind.py, docs/formatos.md). Se pisa cada 6 horas.")
        return None
    with tempfile.TemporaryDirectory() as d:
        if gh("release", "download", RELEASE, "-p", "mapa.json", "-D", d, check=False).returncode != 0:
            return None
        return json.load(open(os.path.join(d, "mapa.json")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--run", help="GFS cycle YYYYMMDDHH (default: the newest complete)")
    ap.add_argument("--history", type=int, default=3, help="days of the wind's history to add at most (default 3)")
    a = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    old = published() if a.upload else None
    waves = waves_layer()
    run = a.run or newest_cycle()
    print("olas:", waves["layer"], "hasta", waves["last"])
    index = dict(old) if old else {"v": 1}
    name = "viento-%s.bin" % run
    path = os.path.join(CACHE, name)
    if old and old.get("wind", {}).get("file") == name:
        print("el ciclo", run, "ya está publicado")
        path = None
    else:
        print("GFS", run, "f%03d-f%03d" % (HOURS[0], HOURS[-1]))

        def hour(fh):
            uu, vv = fields(run, fh)
            return quantize(world(uu)), quantize(world(vv))

        with cf.ThreadPoolExecutor(8) as ex:
            got = list(ex.map(hour, HOURS))
        u = np.stack([g[0] for g in got])
        v = np.stack([g[1] for g in got])
        parts = tiles(u, v)
        size = len(HOURS) * 2 * N * N
        levels, offset = [], 0
        for deg, step in LEVELS:
            rows, cols = -(-180 // deg), 360 // deg
            levels.append({"deg": deg, "rows": rows, "cols": cols, "offset": offset})
            offset += rows * cols * size
        with open(path, "wb") as f:
            for p in parts:
                f.write(p)
        assert os.path.getsize(path) == offset
        t0 = datetime.datetime.strptime(run, "%Y%m%d%H").replace(tzinfo=datetime.timezone.utc)
        index["wind"] = {"file": name, "run": t0.strftime("%Y-%m-%dT%H:%M:%SZ"), "hours": HOURS, "k": K, "n": N,
                         "size": size, "levels": levels}
        print(name, "%.1f MB" % (offset / 1e6), "·", sum(l["rows"] * l["cols"] for l in levels), "baldosas")
        if a.upload:
            gh("release", "upload", RELEASE, path, "--clobber")
    index["waves"] = waves
    days = history(a.history, a.upload)
    if days:
        index["history"] = {"release": HISTORY, "first": days[0], "last": days[-1], "count": len(days)}
    ipath = os.path.join(CACHE, "mapa.json")
    json.dump(index, open(ipath, "w"), separators=(",", ":"))
    if not a.upload:
        return
    if index != old:
        gh("release", "upload", RELEASE, ipath, "--clobber")  # after its file: the phone never reads an index without it
        print("mapa.json subido")
    if path is None:
        return
    keep = {name, old["wind"]["file"] if old and "wind" in old else name, "mapa.json"}   # the cycle before, for an index read before
    for asset in assets(RELEASE):
        if asset["name"] not in keep:
            gh("release", "delete-asset", RELEASE, asset["name"], "-y")
            print("borrado", asset["name"])
    for f in os.listdir(CACHE):
        if f.startswith("viento-") and f != name:
            os.remove(os.path.join(CACHE, f))


if __name__ == "__main__":
    sys.exit(main())
