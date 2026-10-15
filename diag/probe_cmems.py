"""Diagnostic: is Copernicus Marine In Situ readable without an account (STAC + S3 listing)?"""
import json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discover import get, OUT
P = "INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030"
out = open(os.path.join(OUT, "cmems.txt"), "w")
cat = get("https://stac.marine.copernicus.eu/metadata/%s/product.stac.json" % P)
out.write("product.stac.json: %s\n" % (cat[:3000] if cat else None))
if cat:
    try:
        j = json.loads(cat)
        for l in j.get("links", []):
            out.write("link %s %s\n" % (l.get("rel"), l.get("href")))
            if l.get("rel") == "item":
                it = get("https://stac.marine.copernicus.eu/metadata/%s/%s" % (P, l["href"]))
                out.write("ITEM %s: %s\n" % (l["href"], (it or "")[:4000]))
    except Exception as e:
        out.write("parse error %s\n" % e)
for bucket in ("mdl-native-01", "mdl-native-12", "mdl-native-13", "mdl-native-14"):
    for host in ("https://s3.waw3-1.cloudferro.com",):
        u = "%s/%s?list-type=2&prefix=%s&delimiter=/&max-keys=50" % (host, bucket, urllib.parse.quote("native/%s/" % P))
        t = get(u)
        out.write("LIST %s: %s\n" % (u, (t or "")[:3000]))
