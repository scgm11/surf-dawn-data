"""Diagnostic (temporary branch): which open ERDDAP servers have European wave buoys without an account."""
import csv, io, os, re, time, urllib.parse, urllib.request
UA = {"User-Agent": "surf-dawn-validation/1.0 (+https://github.com/scgm11/surf-dawn-data)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
SERVERS = ["https://erddap.emodnet-physics.eu/erddap/", "https://prod-erddap.emodnet-physics.eu/erddap/",
           "https://erddap.ifremer.fr/erddap/", "https://erddap.socib.es/erddap/"]
log = open(os.path.join(OUT, "log.txt"), "a")

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

if __name__ == "__main__":
    for base in SERVERS:
        tag = urllib.parse.urlparse(base).netloc
        txt = get(base + "tabledap/index.csv?page=1&itemsPerPage=5000")
        if not txt:
            continue
        rows = list(csv.reader(io.StringIO(txt)))
        idx = {h: i for i, h in enumerate(rows[0])}
        with open(os.path.join(OUT, "%s-tabledap.txt" % tag), "w") as f:
            f.write("%d datasets\n" % (len(rows) - 1))
            for r in rows[1:]:
                if len(r) < len(rows[0]):
                    continue
                title = r[idx.get("Title", 0)]
                ds = r[idx.get("Dataset ID", 0)]
                f.write("ALL %s | %s\n" % (ds, title[:110]))
                if re.search(r"wave|VHM0|swell|buoy|boya|bou[ée]e|moor|CANDHIS|WaveNet|Puertos|SIMAR|REDEXT|Cefas", title + " " + ds, re.I):
                    f.write("%s | %s\n" % (ds, title[:150]))
