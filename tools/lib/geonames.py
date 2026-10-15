"""GeoNames (https://www.geonames.org, CC BY 4.0) as a source of positions for named places: the
country dumps (download.geonames.org/export/dump/<CC>.zip, no account), downloaded once into
tools/.cache/geonames/ and searched by name (tools/lib/names.py) around a point. Used by
tools/check_spots.py (a source for the flagship spots) and tools/resolve_seeds.py (candidates).
"""
import csv
import io
import os
import sys
import time
import urllib.request
import zipfile

from . import geo
from .names import fold

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", ".cache", "geonames"))
URL = "https://download.geonames.org/export/dump/%s.zip"
UA = {"User-Agent": "surf-dawn-data/1.0 (https://github.com/scgm11/surf-dawn-data)"}
# the feature codes worth a surf spot's name, best first (www.geonames.org/export/codes.html)
RANK = {"BCH": 0, "BCHS": 0, "RF": 0, "RFC": 0, "PT": 1, "PTS": 1, "CAPE": 1, "HDLD": 1, "BAY": 1, "BAYS": 1,
        "COVE": 1, "INLT": 1, "ISL": 2, "PPL": 2, "PPLX": 2, "PPLL": 2, "PPLA4": 2, "PPLA3": 2, "LCTY": 2, "AREA": 3}
_rows = {}


def _download(cc):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "%s.txt" % cc)
    if os.path.exists(path):
        return path
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL % cc, headers=UA)
            data = urllib.request.urlopen(req, timeout=300).read()
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                with open(path + ".part", "wb") as f:
                    f.write(z.read("%s.txt" % cc))
            os.replace(path + ".part", path)
            return path
        except Exception as e:  # noqa: BLE001 - retried, then the country has no GeoNames rows here
            print("  geonames %s failed (%s), retrying" % (cc, str(e)[:80]), file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return None


def rows(cc):
    """[(name, lat, lon, feature code, geonameid, folded names)] of a country's useful places."""
    cc = cc.upper()
    if cc in _rows:
        return _rows[cc]
    out = []
    path = _download(cc)
    if path:
        with open(path, encoding="utf-8", newline="") as f:
            for r in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
                if len(r) < 9 or r[7] not in RANK:
                    continue
                names = {fold(r[1]), fold(r[2])} | {fold(a) for a in r[3].split(",") if a}
                out.append((r[1], float(r[4]), float(r[5]), r[7], r[0], names))
    _rows[cc] = out
    return out


def named_near(lat, lon, variants, cc, km):
    """Places of country cc within km of (lat, lon) named like one of the variants (accents and case
    aside: a name containing the variant, or contained in it): candidates {lat, lon, name, kind, src}."""
    want = [fold(v) for v in variants if len(v) >= 3]
    out = []
    for name, la, lo, code, gid, names in rows(cc):
        if abs(la - lat) > km / 100.0 or geo.km((lat, lon), (la, lo)) > km:
            continue
        if any(w in n or (len(n) >= 4 and n in w) for w in want for n in names):
            out.append({"lat": la, "lon": lo, "name": name, "kind": code, "rank": RANK[code],
                        "src": "geonames:%s" % gid})
    out.sort(key=lambda c: (c["rank"], geo.km((lat, lon), (c["lat"], c["lon"]))))
    return out
