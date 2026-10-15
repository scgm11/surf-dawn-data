"""The seed tables (seeds/README.md), read with the csv module (pandas reads Namibia's "NA" as empty)."""
import csv
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEEDS = os.path.join(ROOT, "seeds")
TYPES = {"": 0, "B": 1, "P": 2, "R": 3}


def table(name):
    with open(os.path.join(SEEDS, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def continents():
    return {r["code"]: r for r in table("continents.csv")}


def countries():
    return {r["code"]: r for r in table("countries.csv")}


def regions():
    return {r["code"]: r for r in table("regions.csv")}


def flags(s):
    """'top nosnap facing=120 wave=-27.5;-48.25' -> {'top': True, 'nosnap': True, 'facing': 120, 'wave': (-27.5, -48.25)}"""
    out = {}
    for tok in s.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = int(v) if k == "facing" else tuple(float(x) for x in v.split(";"))
        else:
            out[tok] = True
    return out


def spots(code):
    """The region's seed rows, each with lat/lon as floats, its type as 0-3 and its flags parsed."""
    path = os.path.join(SEEDS, "spots", code + ".csv")
    if not os.path.exists(path):
        return []
    out = []
    for r in table(os.path.join("spots", code + ".csv")):
        if not r["name"].strip():
            continue
        r = dict(r)
        r["lat"], r["lon"] = float(r["lat"]), float(r["lon"])
        r["kind"] = TYPES.get(r["type"], 0)
        r["f"] = flags(r["flags"])
        out.append(r)
    return out
