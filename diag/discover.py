"""Diagnostic (temporary branch): which open ERDDAP servers have European wave buoys without an account."""
import csv, io, json, os, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "surf-dawn-validation/1.0 (+https://github.com/scgm11/surf-dawn-data)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
SERVERS = ["https://erddap.emodnet-physics.eu/erddap/", "https://er1.s4oceanice.eu/erddap/",
           "https://erddap.emodnet.eu/erddap/", "https://coastwatch.pfeg.noaa.gov/erddap/"]
log = open(os.path.join(OUT, "log.txt"), "w")

def get(url, timeout=120):
    t = time.time()
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
        log.write("OK %.1fs %d bytes %s\n" % (time.time() - t, len(data), url)); log.flush()
        return data
    except Exception as e:
        log.write("FAIL %.1fs %s: %s\n" % (time.time() - t, url, str(e)[:200])); log.flush()
        return None

for base in SERVERS:
    tag = urllib.parse.urlparse(base).netloc
    for term in ("VHM0", "significant wave height", "wave buoy"):
        q = urllib.parse.urlencode({"page": 1, "itemsPerPage": 300, "searchFor": term})
        txt = get(base + "search/index.csv?" + q)
        if not txt:
            continue
        rows = list(csv.reader(io.StringIO(txt)))
        hdr = rows[0]
        idx = {h: i for i, h in enumerate(hdr)}
        with open(os.path.join(OUT, "%s-search-%s.txt" % (tag, term.replace(" ", "_"))), "w") as f:
            for r in rows[1:]:
                if len(r) > idx.get("Dataset ID", 0):
                    f.write("%s | %s | tabledap=%s\n" % (r[idx["Dataset ID"]], r[idx.get("Title", 0)][:120], r[idx.get("tabledap", 0)][:10] if "tabledap" in idx else "?"))
