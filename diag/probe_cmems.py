"""Diagnostic: the wave platforms in Copernicus In Situ 'latest' (index) and a few sample files for the parser."""
import collections, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import OUT, UA
B = "https://s3.waw3-1.cloudferro.com/mdl-native-01/native/"
IDX = "INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030/cmems_obs-ins_glo_phybgcwav_mynrt_na_irr_202311/index_latest.txt"
data = urllib.request.urlopen(urllib.request.Request(B + IDX, headers=UA), timeout=600).read().decode("utf-8", "replace")
rows = [l for l in data.splitlines() if l and not l.startswith("#")]
wave = [l for l in rows if " VHM0" in " " + l.split(",")[-1] or "VAVH" in l.split(",")[-1]]
with open(os.path.join(OUT, "index_latest_waves.txt"), "w") as f:
    f.write("\n".join(wave))
types = collections.Counter(l.split(",")[1].rsplit("/", 1)[-1].split("_")[2] for l in wave)
plats = {}
for l in wave:
    c = l.split(",")
    name = c[1].rsplit("/", 1)[-1]
    plats[name.split("_")[3]] = (name.split("_")[0], name.split("_")[2], c[2], c[4], c[11])
with open(os.path.join(OUT, "cmems_platforms.txt"), "w") as f:
    f.write("%d rows, %d wave rows, types %s, %d platforms\n" % (len(rows), len(wave), dict(types), len(plats)))
    for k, v in sorted(plats.items()):
        f.write("%s %s\n" % (k, v))
# samples: a Spanish, a French, an Irish/UK and a Moroccan/Canary mooring if any
want = ["_MO_", "_MO_", "_MO_"]
picked = []
for l in wave:
    c = l.split(",")
    lat, lon = float(c[2]), float(c[4])
    if "_MO_" in c[1] and 27 < lat < 50 and -20 < lon < 0 and not any(p.split("_")[3] == c[1].rsplit("/", 1)[-1].split("_")[3] for p in picked):
        picked.append(c[1].rsplit("/", 1)[-1]); paths = picked
        urllib.request.urlretrieve(B + c[1], os.path.join(OUT, c[1].rsplit("/", 1)[-1]))
    if len(picked) >= 4:
        break
