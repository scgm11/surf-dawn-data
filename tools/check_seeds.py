"""Checks the seed tables (seeds/README.md): columns, names, positions, types and flags,
and that every region has its file and every file its region. Offline; exits 1 on errors.

Usage: python3 tools/check_seeds.py [--present] [REGION ...]   (no regions: every region;
       --present: a region without its file yet is a warning, not an error)
"""
import csv
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(HERE, "..", "seeds")
COLS = ["name", "lat", "lon", "type", "conf", "src", "flags", "note"]
NAME_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÁÉÍÓÚÑÜÃÕÂÊÔÇÀ '.-")
NAME_MAX = 18
MAX_SPOTS = 60
SPREAD_KM = 400                   # a spot this far from its region's median is in the wrong region


def read(name):
    with open(os.path.join(SEEDS, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def km(a, b):
    dlon = (a[1] - b[1] + 540) % 360 - 180
    return math.hypot(a[0] - b[0], dlon * math.cos(math.radians((a[0] + b[0]) / 2))) * 111.2


def check_region(code, errors, warnings, present=False):
    path = os.path.join(SEEDS, "spots", code + ".csv")
    if not os.path.exists(path):
        (warnings if present else errors).append("%s: no seeds/spots/%s.csv" % (code, code))
        return 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        head = next(reader, None)
        if head != COLS:
            errors.append("%s: header must be %s" % (code, ",".join(COLS)))
            return 0
        rows = [r for r in reader if any(c.strip() for c in r)]
    names, pts = set(), []
    for i, r in enumerate(rows, 2):
        where = "%s line %d" % (code, i)
        if len(r) != len(COLS):
            errors.append("%s: %d columns, expected %d" % (where, len(r), len(COLS)))
            continue
        d = dict(zip(COLS, r))
        n = d["name"]
        if not n or n != n.strip() or len(n) > NAME_MAX or set(n) - NAME_CHARS:
            errors.append("%s: name %r (uppercase, max %d, letters of the font)" % (where, n, NAME_MAX))
        if n in names:
            errors.append("%s: name %r twice" % (where, n))
        names.add(n)
        try:
            lat, lon = float(d["lat"]), float(d["lon"])
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError
            pts.append((lat, lon, n))
        except ValueError:
            errors.append("%s: bad lat/lon %r %r" % (where, d["lat"], d["lon"]))
        if d["type"] not in ("", "B", "P", "R"):
            errors.append("%s: type %r (B, P, R or empty)" % (where, d["type"]))
        if d["conf"] not in ("V", "K", "L"):
            errors.append("%s: conf %r (V, K or L)" % (where, d["conf"]))
        if not d["src"]:
            errors.append("%s: no src" % where)
        for fl in d["flags"].split():
            if fl in ("top", "nosnap"):
                continue
            m = re.fullmatch(r"facing=(\d{1,3})", fl)
            if m and int(m.group(1)) < 360:
                continue
            m = re.fullmatch(r"wave=(-?\d+(?:\.\d+)?);(-?\d+(?:\.\d+)?)", fl)
            if m:
                continue
            errors.append("%s: flag %r" % (where, fl))
        if "top" in d["flags"].split() and not d["type"]:
            errors.append("%s: top spot %r without type" % (where, n))
    if len(rows) > MAX_SPOTS:
        errors.append("%s: %d spots (max %d: split the region)" % (code, len(rows), MAX_SPOTS))
    if len(rows) == 0:
        errors.append("%s: no spots" % code)
    if pts:
        mlat = sorted(p[0] for p in pts)[len(pts) // 2]
        mlon = sorted(p[1] for p in pts)[len(pts) // 2]
        for lat, lon, n in pts:
            if km((lat, lon), (mlat, mlon)) > SPREAD_KM:
                warnings.append("%s: %r is %.0f km from the region's middle" % (code, n, km((lat, lon), (mlat, mlon))))
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if km(pts[i], pts[j]) < 0.05:
                    warnings.append("%s: %r and %r are under 50 m apart" % (code, pts[i][2], pts[j][2]))
    return len(rows)


def main():
    regions = read("regions.csv")
    countries = {c["code"]: c for c in read("countries.csv")}
    continents = {c["code"] for c in read("continents.csv")}
    errors, warnings = [], []
    for c in countries.values():
        if c["continent"] not in continents:
            errors.append("country %s: continent %r" % (c["code"], c["continent"]))
    codes = [r["code"] for r in regions]
    for r in regions:
        if not re.fullmatch(r"[A-Z]{2}(-[A-Z0-9]{1,4}){1,2}", r["code"]):
            errors.append("region code %r" % r["code"])
        if r["country"] not in countries:
            errors.append("region %s: country %r" % (r["code"], r["country"]))
        if not r["code"].startswith(r["country"] + "-"):
            errors.append("region %s does not start with its country %s" % (r["code"], r["country"]))
    if len(set(codes)) != len(codes):
        errors.append("repeated region codes")
    files = {f[:-4] for f in os.listdir(os.path.join(SEEDS, "spots")) if f.endswith(".csv")}
    for f in sorted(files - set(codes)):
        errors.append("seeds/spots/%s.csv has no row in regions.csv" % f)
    args = sys.argv[1:]
    present = "--present" in args
    want = [x for x in args if x != "--present"] or codes
    total = 0
    for code in want:
        if code not in codes:
            errors.append("%s is not in regions.csv" % code)
            continue
        total += check_region(code, errors, warnings, present)
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print("%d regions, %d spots, %d errors, %d warnings" % (len(want), total, len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
