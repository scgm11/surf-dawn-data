#!/usr/bin/env python3
"""Diagnostics: saves the first bytes of every source to validation/probe/ (formats check)."""
import json
import os
import sys
import time
import traceback
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "validation", "probe")
UA = {"User-Agent": "surf-dawn-validation/1.0 (github.com/scgm11/surf-dawn-data)"}


def get(url, n=4000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    return "%d bytes\n" % len(b) + b[:n].decode("utf-8", "replace") + ("\n...\n" + b[-n // 2:].decode("utf-8", "replace") if len(b) > n else "")


def save(name, text):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".txt"), "w") as f:
        f.write(text)


def probe(name, fn):
    t = time.time()
    try:
        save(name, fn())
        print("ok  %-24s %.1fs" % (name, time.time() - t))
    except Exception:                            # noqa: BLE001
        save(name, "FAILED\n" + traceback.format_exc())
        print("ERR %-24s %s" % (name, traceback.format_exc().splitlines()[-1]))


def aodn():
    import pyarrow.dataset as ds
    import pyarrow.fs as pfs
    fs = pfs.S3FileSystem(anonymous=True, region="ap-southeast-2")
    out = []
    sel = fs.get_file_info(pfs.FileSelector("aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet", recursive=False))
    out.append("top: %d entries" % len(sel))
    out += [i.path for i in sel[:30]]
    d = ds.dataset("aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet", filesystem=fs, format="parquet", partitioning="hive")
    out.append(str(d.schema))
    out.append("partitioning: %s" % d.partitioning)
    files = d.files
    out.append("files: %d" % len(files))
    out += files[-20:]
    return "\n".join(out)


def aodn_rows():
    import datetime
    import pyarrow.dataset as ds
    import pyarrow.fs as pfs
    fs = pfs.S3FileSystem(anonymous=True, region="ap-southeast-2")
    d = ds.dataset("aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet", filesystem=fs, format="parquet", partitioning="hive")
    files = sorted(d.files)
    # the last files by name: what one looks like
    import pyarrow.parquet as pq
    out = []
    for f in files[-3:]:
        t = pq.read_table(f, filesystem=fs)
        out.append("%s: %d rows" % (f, t.num_rows))
        out.append(t.slice(max(0, t.num_rows - 5), 5).to_pandas().to_string())
    cut = datetime.datetime.utcnow() - datetime.timedelta(days=2)
    return "\n".join(out) + "\ncut %s" % cut


def openmeteo(models, lat, lon):
    q = ("https://marine-api.open-meteo.com/v1/marine?latitude=%s&longitude=%s&hourly=wave_height,wave_period,"
         "wave_peak_period,wave_direction&models=%s&past_days=1&forecast_days=1&timezone=GMT&timeformat=unixtime&cell_selection=sea"
         % (lat, lon, models))
    try:
        return get(q, 3000)
    except urllib.error.HTTPError as e:
        return "HTTP %s\n%s" % (e.code, e.read()[:2000].decode())


import urllib.error  # noqa: E402

P = [
    ("ndbc_active", lambda: get("https://www.ndbc.noaa.gov/activestations.xml")),
    ("ndbc_listing", lambda: get("https://www.ndbc.noaa.gov/data/realtime2/", 6000)),
    ("ndbc_46225", lambda: get("https://www.ndbc.noaa.gov/data/realtime2/46225.txt", 2000)),
    ("ndbc_31260", lambda: get("https://www.ndbc.noaa.gov/data/realtime2/31260.txt", 2000)),
    ("cdip_catalog", lambda: get("https://thredds.cdip.ucsd.edu/thredds/catalog/cdip/realtime/catalog.xml", 5000)),
    ("cdip_das", lambda: get("https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/100p1_rt.nc.das", 8000)),
    ("cdip_dds", lambda: get("https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/100p1_rt.nc.dds", 6000)),
    ("cdip_ascii", lambda: get("https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/100p1_rt.nc.ascii?waveTime[0:1:3],waveHs[0:1:3],metaDeployLatitude,metaDeployLongitude,metaStationName", 3000)),
    ("cdip_erddap_info", lambda: get("https://erddap.cdip.ucsd.edu/erddap/info/wave_agg/index.csv", 6000)),
    ("cdip_erddap_list", lambda: get("https://erddap.cdip.ucsd.edu/erddap/tabledap/allDatasets.csv?datasetID,title", 4000)),
    ("mi_info", lambda: get("https://erddap.marine.ie/erddap/info/IWaveBNetwork30Min/index.csv", 6000)),
    ("mi_rows", lambda: get("https://erddap.marine.ie/erddap/tabledap/IWaveBNetwork30Min.csv?&time>=now-1day", 4000)),
    ("aodn_schema", aodn),
    ("aodn_rows", aodn_rows),
    ("om_all", lambda: openmeteo("ncep_gfswave016,ncep_gfswave025,meteofrance_wave,ecmwf_wam,dwd_ewam", 32.93, -117.39)),
    ("om_ewam_eu", lambda: openmeteo("dwd_ewam,ecmwf_wam,meteofrance_wave", 43.5, -1.6)),
    ("om_ewam_out", lambda: openmeteo("dwd_ewam", 32.93, -117.39)),
    ("om_wam025", lambda: openmeteo("ecmwf_wam025", 32.93, -117.39)),
]

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, fn in P:
        if not only or name in only:
            probe(name, fn)
