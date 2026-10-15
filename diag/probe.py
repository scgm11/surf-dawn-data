"""Second step: the variables of chosen datasets and a sample of recent European rows."""
import csv, io, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import get, OUT
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets.txt")):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    base, ds = line.split()
    info = get(base + "info/%s/index.csv" % ds)
    if not info:
        continue
    vars_ = {}
    for r in csv.reader(io.StringIO(info)):
        if len(r) >= 5 and r[0] == "variable":
            vars_.setdefault(r[1], {"type": r[3]})
        elif len(r) >= 5 and r[0] == "attribute" and r[1] != "NC_GLOBAL" and r[2] in ("standard_name", "units", "long_name"):
            vars_.setdefault(r[1], {})[r[2]] = r[4]
    with open(os.path.join(OUT, "info-%s.txt" % ds), "w") as f:
        for v, a in vars_.items():
            f.write("%s %s\n" % (v, a))
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 2 * 86400))
    want = [v for v in vars_ if v in ("platform_code", "platform_id", "station_id", "PLATFORMCODE", "time", "latitude", "longitude",
                                      "VHM0", "VTPK", "VMDR", "VPED", "VTM02", "VAVH")]
    q = ",".join(want) + "&time>=" + since + "&latitude>=27&latitude<=60&longitude>=-20&longitude<=10"
    txt = get(base + "tabledap/%s.csv?%s" % (ds, urllib.parse.quote(q, safe="&=,<>:")), timeout=300)
    if txt:
        rows = txt.splitlines()
        with open(os.path.join(OUT, "sample-%s.txt" % ds), "w") as f:
            f.write("%d rows\n" % len(rows))
            f.write("\n".join(rows[:40]))
