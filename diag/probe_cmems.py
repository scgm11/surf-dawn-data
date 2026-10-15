"""Diagnostic: layout of the Copernicus In Situ native dataset (public STAC/S3) to write the parser against."""
import os, re, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import get, OUT, UA
B = "https://s3.waw3-1.cloudferro.com/mdl-native-01"
D = "native/INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030/cmems_obs-ins_glo_phybgcwav_mynrt_na_irr_202311/"
out = open(os.path.join(OUT, "cmems2.txt"), "w")
def ls(prefix, n=200):
    t = get("%s?list-type=2&prefix=%s&delimiter=/&max-keys=%d" % (B, urllib.parse.quote(prefix), n)) or ""
    return re.findall(r"<Prefix>([^<]+)</Prefix>", t)[1:], re.findall(r"<Key>([^<]+)</Key>", t), re.findall(r"<Size>(\d+)</Size>", t)
p, k, s = ls(D)
out.write("TOP prefixes %s\nkeys %s\n" % (p, list(zip(k, s))))
for sub in p:
    pp, kk, ss = ls(sub, 60)
    out.write("\n%s prefixes(%d) %s\nkeys(%d) %s\n" % (sub, len(pp), pp[:30], len(kk), list(zip(kk, ss))[:30]))
# the index files, head
for key in k:
    if "index" in key:
        req = urllib.request.Request("%s/%s" % (B, key), headers=dict(UA, Range="bytes=0-6000"))
        try:
            out.write("\n=== %s\n%s\n" % (key, urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")))
        except Exception as e:
            out.write("\n=== %s failed %s\n" % (key, e))
