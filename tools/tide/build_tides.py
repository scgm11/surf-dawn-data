#!/usr/bin/env python3
"""Builds tide/ (docs/formatos.md, "Mareas") for every region of seeds/regions.csv.

1. Ports. For each spot (seeds/spots/<REGION>.csv) the candidate stations, by tiers:
     1  official station <= 60 km on the same coast (NOAA CO-OPS harmonic stations, JMA, Marine
        Institute, LINZ)
     2  TICON-3 Coastal gauge <= 120 km on the same coast, record >= 1 year
     3  official station <= 60 km across land
     4  TICON-3 gauge <= 60 km across land, record >= 1 year
     5  TICON-3 gauge <= 120 km on the same coast, record >= 180 days
   "Across land": the straight line between spot and station runs over land (global-land-mask) for
   more than max(4 km, 15 % of the distance). A region keeps the set of at most 3 ports that
   serves its spots best (score per spot: tier weight minus distance/100, minus 0.5 per port);
   every spot goes to its best port of the set, or none (the watch then uses Open-Meteo's
   sea_level_height_msl). Radius = farthest assigned spot + 10 km.
2. Heights. Hourly, UTC, cm, for every month of the current and the next year: NOAA predictions
   (MLLW), JMA tables (JST -> UTC, datum DL), Marine Institute predictions (5 min -> hour), LINZ
   highs and lows (half cosines, chart datum), TICON-3 constants predicted with pyTMD's nodal
   corrections (MSL + sum of amplitudes, always >= 0). Hours an official source has not published
   yet (JMA's last 9 hours of next year, Marine Institute's next year) come from a harmonic
   analysis of the published ones (tools/tide/harmonic.py), and the month's src says so.
3. harmonics.json: the watch's 30-period fit of the current year (t0 = Jan 1, 00:00 UTC).
4. ports.json, regions.json, report.md. The ports of Uruguay and Brazil (punta-del-este,
   la-paloma, imbituba: tools/sohma_tide.py, tools/ciram_tide.py) and the regions UY-MAL, UY-ROC,
   BR-SC-FLN and BR-SC-SUL are left exactly as they are.

Validation: TICON-3 predictions against NOAA's own at NOAA stations that are also TICON gauges,
for each set of nodal corrections; the best set is the one used.

Usage: python3 tools/tide/build_tides.py [--regions CODE ...] [--years 2026 2027]
"""
import argparse
import datetime as dt
import hashlib
import itertools
import json
import math
import os
import shutil
import sys
import time
import unicodedata

import numpy as np
from global_land_mask import globe

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from tools.lib import geo, seeds  # noqa: E402
from tools.lib import tide as tidelib  # noqa: E402
from tools.tide import harmonic as H  # noqa: E402
from tools.tide import sources as S  # noqa: E402

ROOT = seeds.ROOT
OUT = os.path.join(ROOT, "tide")
CACHE = os.path.join(ROOT, "tools", ".tide_cache")
MAX_BYTES = 6144
OFFICIAL_KM = 60.0
TICON_KM = 120.0
CROSS_KM = 60.0                   # tiers 3 and 4: across land, only this close
MIN_DAYS, SHORT_DAYS = 365, 180
MAX_PORTS = 3
PORT_COST = 0.5
TIER_W = {1: 10.0, 2: 8.0, 3: 6.0, 4: 5.0, 5: 4.0}
TIER_TXT = {1: "oficial, misma costa", 2: "TICON-3, misma costa", 3: "oficial, cruzando tierra",
            4: "TICON-3, cruzando tierra", 5: "TICON-3, registro corto"}
FROZEN = ["UY-MAL", "UY-ROC", "BR-SC-FLN", "BR-SC-SUL"]
LEGACY = [
    {"key": "imbituba", "name": "Porto de Imbituba (DHN)", "lat": -28.2297, "lon": -48.6525, "utc_offset": -3,
     "src": "dhn:Imbituba (Epagri/CIRAM)", "datum": "nível de redução da DHN",
     "license": "sin licencia abierta declarada", "credit": "DHN/Marinha do Brasil, vía Epagri/CIRAM"},
    {"key": "la-paloma", "name": "La Paloma (SOHMA)", "lat": -34.6533, "lon": -54.1417, "utc_offset": -3,
     "src": "sohma:La Paloma", "datum": "cero del puerto (SOHMA)",
     "license": "sin licencia abierta declarada", "credit": "SOHMA, Armada Nacional (Uruguay)"},
    {"key": "punta-del-este", "name": "Punta del Este (SOHMA)", "lat": -34.9617, "lon": -54.9517, "utc_offset": -3,
     "src": "sohma:Punta del Este", "datum": "cero del puerto (SOHMA)",
     "license": "sin licencia abierta declarada", "credit": "SOHMA, Armada Nacional (Uruguay)"},
]
LEGACY_KEYS = {p["key"] for p in LEGACY}
# NOAA stations that are also TICON-3 gauges, tried first for the validation
VALIDATION = ["9410230", "1612340", "9414290", "8518750", "8724580", "9447130", "1910000", "9755371", "8443970",
              "1617760", "8665530", "9411340"]

LIC = {
    "noaa": ("dominio público (EE. UU.)", "NOAA/NOS/CO-OPS"),
    "jma": ("Public Data License 1.0 (compatible CC BY 4.0)", "気象庁 Japan Meteorological Agency, 潮位表 (procesado)"),
    "imi": ("CC BY 4.0", "Marine Institute (Ireland)"),
    "linz": ("CC BY 4.0", "Land Information New Zealand (LINZ), Crown copyright"),
    "ticon": ("CC BY 4.0", "TICON-3, Hart-Davis et al. 2022 (doi:10.1594/PANGAEA.951610), datos GESLA-3"),
}


def log(*a):
    print(*a, flush=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    out = "".join(c if c.isalnum() else "-" for c in s)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


# ---------------------------------------------------------------- catalogs

def load_catalogs(year, ticon_zip, rep):
    """All candidate stations: official ones and TICON-3 Coastal gauges (one per spot within 1 km)."""
    st = []
    keys = set(LEGACY_KEYS)

    def add(s):
        k = s["key"]
        n = 2
        while s["key"] in keys:
            s["key"] = "%s-%d" % (k, n)
            n += 1
        keys.add(s["key"])
        s["license"], s["credit"] = LIC[s["kind"]]
        st.append(s)

    noaa = S.noaa_stations()
    log("NOAA: %d harmonic stations" % len(noaa))
    for s in noaa:
        add({"key": "noaa-" + s["id"], "kind": "noaa", "official": True, "lat": s["lat"], "lon": s["lon"],
             "name": s["name"], "ref": s["id"], "src": "noaa:" + s["id"], "datum": "MLLW"})
    jma = S.jma_stations(year)
    log("JMA: %d stations" % len(jma))
    for s in jma:
        add({"key": "jma-" + s["code"].lower(), "kind": "jma", "official": True, "lat": s["lat"], "lon": s["lon"],
             "name": "%s (JMA %s)" % (s["name"], s["code"]), "ref": s["code"], "src": "jma:" + s["code"],
             "datum": "DL (潮位表基準面, JMA)"})
    info = S.imi_info()
    var = "Water_Level_LAT" if "Water_Level_LAT" in info else "Water_Level"
    wl = info.get(var, {})
    log("IMI: variable %s, attributes %s; time coverage %s .. %s" % (
        var, json.dumps(wl, ensure_ascii=False)[:600], info.get("NC_GLOBAL", {}).get("time_coverage_start"),
        info.get("NC_GLOBAL", {}).get("time_coverage_end")))
    txt = " ".join(wl.values()).lower()
    imi_datum = "LAT" if ("lat" in var.lower() or "lowest astronomical" in txt or " lat" in txt) else \
        ("OD Malin" if "malin" in txt else "datum del Marine Institute")
    rep["imi_datum"] = imi_datum
    rep["imi_coverage"] = info.get("NC_GLOBAL", {}).get("time_coverage_end", "?")
    imi = S.imi_stations()
    log("IMI: %d stations (datum %s)" % (len(imi), imi_datum))
    for s in imi:
        add({"key": "imi-" + slug(s["name"]), "kind": "imi", "official": True, "lat": s["lat"], "lon": s["lon"],
             "name": s["name"] + (" (modelado)" if s["modelled"] else ""), "ref": s["id"], "var": var,
             "src": "imi:" + s["id"], "datum": imi_datum})
    linz = S.linz_ports(year)
    n = 0
    for name, years in sorted(linz.items()):
        y = year if year in years else min(years)
        try:
            lat, lon = S.linz_position(name, y)
        except S.SourceError as e:
            rep["warnings"].append("LINZ %s: %s" % (name, e))
            continue
        n += 1
        add({"key": "linz-" + slug(name), "kind": "linz", "official": True, "lat": lat, "lon": lon,
             "name": name, "ref": name, "years": sorted(years), "src": "linz:" + name, "datum": "Chart Datum (LINZ)"})
    log("LINZ: %d ports with CSV" % n)

    gauges = S.ticon_gauges(ticon_zip)
    types = {}
    for g in gauges:
        types[g["type"]] = types.get(g["type"], 0) + 1
    log("TICON-3: %d gauges %s" % (len(gauges), types))
    coastal = [g for g in gauges if g["type"] == "Coastal" and "M2" in g["cons"]]
    coastal.sort(key=lambda g: (-g["days"], g["source"]))
    kept = []
    for g in coastal:                         # the longest record of the gauges within 1 km
        if any(abs(k["lat"] - g["lat"]) < 0.01 and geo.km((k["lat"], k["lon"]), (g["lat"], g["lon"])) < 1.0
               for k in kept):
            continue
        kept.append(g)
    log("TICON-3: %d Coastal gauges, %d after merging duplicates within 1 km" % (len(coastal), len(kept)))
    for g in kept:
        h = hashlib.sha1(("%.3f,%.3f" % (g["lat"], g["lon"])).encode()).hexdigest()[:6]
        add({"key": "ticon-" + h, "kind": "ticon", "official": False, "lat": g["lat"], "lon": g["lon"],
             "name": "TICON-3 %.3f%s %.3f%s (%s)" % (abs(g["lat"]), "N" if g["lat"] >= 0 else "S", abs(g["lon"]),
                                                    "E" if g["lon"] >= 0 else "W", g["source"]),
             "ref": "%.3f,%.3f" % (g["lat"], g["lon"]), "src": "ticon3:%.3f,%.3f" % (g["lat"], g["lon"]),
             "datum": "MSL+ΣA", "gauge": g, "days": g["days"]})
    return st, coastal


# ---------------------------------------------------------------- selection

def dist_km(lat, lon, lats, lons):
    """geo.km vectorised: equirectangular, longitudes wrapped."""
    dlon = (lons - lon + 540.0) % 360.0 - 180.0
    dx = dlon * np.cos(np.radians((lats + lat) / 2))
    return np.hypot(lats - lat, dx) * geo.KM_PER_DEG


def land_run(a, b, d):
    """Longest stretch (km) over land on the straight line a -> b, leaving out 1.5 km at each end."""
    if d < 3.5:
        return 0.0
    n = max(8, int(d / 0.5))
    f = np.linspace(0.0, 1.0, n + 1)
    lat = a[0] + (b[0] - a[0]) * f
    lon = a[1] + geo.dlon(a[1], b[1]) * f
    lon = (lon + 540.0) % 360.0 - 180.0
    land = globe.is_land(lat, lon)
    k = int(math.ceil(1.5 / (d / n)))
    land = land[k:len(land) - k]
    best = run = 0
    for x in land:
        run = run + 1 if x else 0
        best = max(best, run)
    return best * d / n


def crosses(run, d):
    return run > max(4.0, 0.15 * d)


def spot_candidates(spot, st, lats, lons, excluded):
    """[(station index, km, tier, land run)] eligible for the spot, and [(index, km, reason)] rejected."""
    d = dist_km(spot["lat"], spot["lon"], lats, lons)
    ok, rej = [], []
    for i in np.nonzero(d <= TICON_KM)[0]:
        s = st[i]
        di = float(d[i])
        if s["key"] in excluded:
            rej.append((i, di, excluded[s["key"]]))
            continue
        if s["official"] and di > OFFICIAL_KM:
            continue
        run = land_run((spot["lat"], spot["lon"]), (s["lat"], s["lon"]), di)
        x = crosses(run, di)
        if s["official"]:
            ok.append((i, di, 3 if x else 1, run))
            continue
        days = s["days"]
        if days >= MIN_DAYS and not x:
            ok.append((i, di, 2, run))
        elif days >= MIN_DAYS and di <= CROSS_KM:
            ok.append((i, di, 4, run))
        elif days >= SHORT_DAYS and not x:
            ok.append((i, di, 5, run))
        elif days < SHORT_DAYS:
            rej.append((i, di, "registro de %d días" % days))
        else:
            rej.append((i, di, "cruza %.0f km de tierra" % run))
    return ok, rej


def score(tier, d):
    return TIER_W[tier] - d / 100.0


def choose_ports(spots, cands):
    """The set of at most MAX_PORTS stations that maximises the region's score."""
    pool = {}
    for c in cands:
        for i, d, tier, run in sorted(c, key=lambda x: -score(x[2], x[1]))[:6]:
            pool[i] = pool.get(i, 0.0) + score(tier, d)
    pool = sorted(pool, key=lambda i: -pool[i])[:24]
    if not pool:
        return []
    col = {p: j for j, p in enumerate(pool)}
    M = np.zeros((len(spots), len(pool)))
    for r, c in enumerate(cands):
        for i, d, tier, run in c:
            if i in col:
                M[r, col[i]] = max(M[r, col[i]], score(tier, d))
    best, best_set = -1e9, []
    for k in range(1, min(MAX_PORTS, len(pool)) + 1):
        for comb in itertools.combinations(range(len(pool)), k):
            v = M[:, comb].max(axis=1).sum() - PORT_COST * k
            if v > best + 1e-9:
                best, best_set = v, [pool[j] for j in comb]
    return best_set


def select_region(code, spots, st, lats, lons, excluded):
    cands, rejs = [], []
    for s in spots:
        ok, rej = spot_candidates(s, st, lats, lons, excluded)
        cands.append(ok)
        rejs.append(rej)
    chosen = choose_ports(spots, cands)
    assign = {}
    nop = []
    for s, c in zip(spots, cands):
        mine = [x for x in c if x[0] in chosen]
        if not mine:
            nop.append(s)
            continue
        i, d, tier, run = max(mine, key=lambda x: score(x[2], x[1]))
        assign.setdefault(i, []).append((s, d, tier, run))
    ports = []
    for i in chosen:
        if i not in assign:
            continue
        a = assign[i]
        ports.append({"i": i, "spots": a, "radius": int(math.ceil(max(x[1] for x in a))) + 10,
                      "tier": min(x[2] for x in a)})
    ports.sort(key=lambda p: (-len(p["spots"]), p["i"]))
    # what was left out, for the report
    left = {}
    for c, rej in zip(cands, rejs):
        for i, d, tier, run in c:
            if i not in chosen:
                left.setdefault(i, (d, "fuera por el tope de %d puertos (nivel %d)" % (MAX_PORTS, tier)))
                left[i] = min(left[i], (d, left[i][1]))
        for i, d, why in rej:
            if i not in left or d < left[i][0]:
                left[i] = (d, why)
    nearest = {}                              # why a spot has no port
    for s, c, rej in zip(spots, cands, rejs):
        if any(s is x for x in nop):
            if c:
                i, d, tier, run = min(c, key=lambda x: x[1])
                nearest[s["name"]] = (i, d, "fuera por el tope de %d puertos" % MAX_PORTS)
            elif rej:
                nearest[s["name"]] = min(rej, key=lambda x: x[1])
            else:
                nearest[s["name"]] = None
    return {"ports": ports, "nop": nop, "left": left, "nearest": nearest}


# ---------------------------------------------------------------- heights

class Heights:
    """Hourly UTC series per port (both years), fetched once."""

    def __init__(self, years, corrections):
        self.years = years
        self.corr = corrections
        self.cache = {}
        self.noaa_cache = {}

    def noaa(self, sid, year):
        k = (sid, year)
        if k not in self.noaa_cache:
            try:
                self.noaa_cache[k] = (S.noaa_year(sid, year, "MLLW"), "MLLW")
            except S.SourceError as e:
                log("  noaa %s %d MLLW: %s; trying MSL" % (sid, year, e))
                self.noaa_cache[k] = (S.noaa_year(sid, year, "MSL"), "MSL")
        return self.noaa_cache[k]

    def series(self, s):
        """{"y": {year: array cm}, "datum", "filled": {year: hours}, "rms_fill"}; raises SourceError."""
        if s["key"] in self.cache:
            return self.cache[s["key"]]
        kind = s["kind"]
        y, datum = {}, s["datum"]
        for yr in self.years:
            if kind == "noaa":
                y[yr], datum = self.noaa(s["ref"], yr)
            elif kind == "jma":
                y[yr] = S.jma_year(s["ref"], yr)
            elif kind == "imi":
                y[yr] = S.imi_year(s["ref"], yr, s["var"])
            elif kind == "linz":
                try:
                    y[yr] = S.linz_year(s["ref"], yr, set(s["years"]))
                except S.SourceError as e:
                    log("  %s: %s" % (s["key"], e))
                    y[yr] = np.full(len(S.year_hours(yr)), np.nan)
            elif kind == "ticon":
                g = s["gauge"]
                names = [H.pytmd_name(c) for c in g["cons"]]
                amp = [g["cons"][c][0] for c in g["cons"]]
                pha = [g["cons"][c][1] for c in g["cons"]]
                y[yr] = H.predict(S.year_hours(yr), names, amp, pha, self.corr)
        out = {"y": y, "datum": datum, "filled": {}, "mask": {}, "rms_fill": 0.0}
        if kind == "ticon":
            g = s["gauge"]
            names = [H.pytmd_name(c) for c in g["cons"]]
            fmax = H.max_nodal(names, self.corr)
            off = int(math.ceil(sum(g["cons"][c][0] * f for c, f in zip(g["cons"], fmax))))
            hi = max(float(np.max(v)) for v in y.values()) + off
            if hi <= 999:
                for yr in y:
                    y[yr] = y[yr] + off
                out["datum"] = "MSL+ΣA (MSL+%d cm)" % off
            else:
                out["datum"] = "MSL"
            out["offset"] = off
        else:
            t = np.concatenate([S.year_hours(yr) for yr in self.years]).astype(float)
            v = np.concatenate([y[yr] for yr in self.years])
            good = int(np.isfinite(v).sum())
            if good < 300 * 24:
                raise S.SourceError("%s: only %d hours published" % (s["key"], good))
            if good < len(v):
                v2, n, rms = H.fill(t, v, self.corr)
                k = 0
                for yr in self.years:
                    m = len(y[yr])
                    out["mask"][yr] = ~np.isfinite(y[yr])
                    out["filled"][yr] = int(out["mask"][yr].sum())
                    y[yr] = v2[k:k + m]
                    k += m
                out["rms_fill"] = rms
        lo = min(float(np.min(v)) for v in y.values())
        hi = max(float(np.max(v)) for v in y.values())
        if lo < -999 or hi > 999:
            raise S.SourceError("%s: heights %.0f..%.0f cm outside ±999" % (s["key"], lo, hi))
        out["lo"], out["hi"] = lo, hi
        self.cache[s["key"]] = out
        return out


def have_files(key, years):
    d = os.path.join(OUT, key)
    if not os.path.exists(os.path.join(d, "harmonics.json")):
        return False
    return all(os.path.exists(os.path.join(d, "%d-%02d.json" % (y, m))) for y in years for m in range(1, 13))


# ---------------------------------------------------------------- validation

def validate(st, coastal, heights, year, rep):
    """TICON-3 vs NOAA at NOAA stations that are TICON gauges too; returns the best corrections."""
    noaa = {s["ref"]: s for s in st if s["kind"] == "noaa"}
    order = [k for k in VALIDATION if k in noaa] + sorted(k for k in noaa if k not in VALIDATION)
    clat = np.array([g["lat"] for g in coastal])
    clon = np.array([g["lon"] for g in coastal])
    rows = []
    hours = S.year_hours(year)
    for sid in order:
        if len(rows) >= 6 or (len(rows) >= 3 and sid not in VALIDATION):
            break
        s = noaa[sid]
        d = dist_km(s["lat"], s["lon"], clat, clon)
        near = [j for j in np.argsort(d)[:5] if d[j] <= 1.5 and coastal[j]["days"] >= 730]
        if not near:
            continue
        g = coastal[near[0]]
        try:
            obs, datum = heights.noaa(sid, year)
        except S.SourceError as e:
            rep["warnings"].append("validación %s: %s" % (sid, e))
            continue
        if np.isnan(obs).any():
            continue
        names = [H.pytmd_name(c) for c in g["cons"]]
        amp = [g["cons"][c][0] for c in g["cons"]]
        pha = [g["cons"][c][1] for c in g["cons"]]
        r = {"id": sid, "name": s["name"], "km": float(d[near[0]]), "source": g["source"], "days": g["days"],
             "range": float(obs.max() - obs.min()), "rms": {}, "rms_nosa": {}}
        for corr in H.CORRECTIONS:
            p = H.predict(hours, names, amp, pha, corr)
            e = (p - p.mean()) - (obs - obs.mean())
            r["rms"][corr] = float(np.sqrt(np.mean(e ** 2)))
            keep = [k for k, c in enumerate(g["cons"]) if c not in ("SA", "SSA")]
            p2 = H.predict(hours, [names[k] for k in keep], [amp[k] for k in keep], [pha[k] for k in keep], corr)
            # NOAA keeps its own Sa/Ssa: compare the tide without both annual terms on each side
            e2 = (p2 - p2.mean()) - (obs - obs.mean() - (p - p2 - (p - p2).mean()))
            r["rms_nosa"][corr] = float(np.sqrt(np.mean(e2 ** 2)))
        rows.append(r)
        log("validación %s %s: TICON %s a %.2f km, %d días; RMS %s" % (
            sid, s["name"], g["source"], r["km"], g["days"],
            " ".join("%s %.1f" % (c, v) for c, v in r["rms"].items())))
    rep["validation"] = rows
    if len(rows) < 3:
        rep["warnings"].append("validación: sólo %d estaciones NOAA comparables" % len(rows))
    if not rows:
        return "FES"
    best = min(H.CORRECTIONS, key=lambda c: np.mean([r["rms"][c] for r in rows]))
    rep["corrections"] = best
    return best


# ---------------------------------------------------------------- output

def month_json(key, year, month, h, src, datum):
    return {"port": key, "month": "%d-%02d" % (year, month), "days": tidelib.days_in(year, month), "utc_offset": 0,
            "unit": "cm", "src": src, "datum": datum, "h": [int(round(v)) for v in h]}


def write_port(s, ser, years):
    """Month files and harmonics.json of a new port; returns (files written, bytes, fit rms)."""
    key = s["key"]
    nfiles = nbytes = 0
    for yr in years:
        y = ser["y"][yr]
        mask = ser["mask"].get(yr)
        for m in range(1, 13):
            a = (dt.date(yr, m, 1) - dt.date(yr, 1, 1)).days * 24
            n = tidelib.days_in(yr, m) * 24
            src = s["src"]
            if mask is not None and mask[a:a + n].any():
                src += " +armónicos (%d h)" % int(mask[a:a + n].sum())
            obj = month_json(key, yr, m, y[a:a + n], src, ser["datum"])
            path = os.path.join(OUT, key, "%d-%02d.json" % (yr, m))
            tidelib.write_json(path, obj)
            size = os.path.getsize(path)
            if size > MAX_BYTES:
                raise SystemExit("%s: %d bytes > %d" % (path, size, MAX_BYTES))
            nfiles += 1
            nbytes += size
    yr = years[0]
    t = S.year_hours(yr)
    mean, c, sn, rms = H.fit30((t - t[0]) / 3600.0, ser["y"][yr], tidelib.PERIODS)
    obj = tidelib.harm_json(key, int(t[0]), mean, c, sn, rms)
    path = os.path.join(OUT, key, "harmonics.json")
    tidelib.write_json(path, obj)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("%s: %d bytes > %d" % (path, size, MAX_BYTES))
    return nfiles + 1, nbytes + size, rms


def write_regions(rows):
    """One region per line, like the file always was."""
    items = []
    for code, ports in rows:
        items.append('"%s":%s' % (code, json.dumps(ports, separators=(",", ":"), ensure_ascii=False)))
    text = "{" + ",\n ".join(items) + "}\n"
    path = os.path.join(OUT, "regions.json")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


def write_ports(ports):
    items = [json.dumps(p, separators=(",", ":"), ensure_ascii=False) for p in sorted(ports, key=lambda p: p["key"])]
    text = "[" + ",\n ".join(items) + "]\n"
    path = os.path.join(OUT, "ports.json")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


def fmt_km(x):
    return "%.0f" % x if x >= 9.5 else "%.1f" % x


def report_md(rep, regions, sel, st, used, years):
    L = ["# Mareas: reporte del último build", "",
         "Generado %s por `tools/tide/build_tides.py`. Años: %s. Correcciones nodales: pyTMD `%s`." % (
             dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), ", ".join(map(str, years)),
             rep.get("corrections", "FES")), ""]
    kinds = {}
    for k, u in used.items():
        kinds[u["kind"]] = kinds.get(u["kind"], 0) + 1
    with_p = [c for c in sel if sel[c]["ports"]]
    L += ["## Resumen", "",
          "- Puertos nuevos: %d (%s); más los 3 de Uruguay y Brasil, sin cambios." % (
              len(used), ", ".join("%s %d" % (k, v) for k, v in sorted(kinds.items()))),
          "- Regiones con puerto: %d de %d (más UY-MAL, UY-ROC, BR-SC-FLN y BR-SC-SUL, congeladas); sin puerto: %d." % (
              len(with_p), len(sel), len(sel) - len(with_p)),
          "- Picos con puerto: %d de %d." % (rep["spots_with"], rep["spots_total"]),
          "- Archivos: %d, %.1f MB (cada mes ≤ %d bytes; el mayor: %d)." % (
              rep["files"], rep["bytes"] / 1e6, MAX_BYTES, rep.get("max_month", 0)),
          "- Marine Institute: datum `%s`; predicciones hasta %s." % (rep.get("imi_datum"), rep.get("imi_coverage")), ""]
    if rep["warnings"]:
        L += ["## Avisos", ""] + ["- " + w for w in rep["warnings"]] + [""]
    L += ["## Validación TICON-3 vs NOAA", "",
          "Predicción horaria %d de las constantes de TICON-3 (pyTMD, cada juego de correcciones nodales) contra "
          "las predicciones de NOAA en la misma estación; RMS en cm de la diferencia, cada serie sin su media. "
          "\"sin Sa/Ssa\": sin los términos anual y semianual de TICON (son en parte meteorológicos)." % years[0], "",
          "| Estación NOAA | Gauge TICON-3 | Registro | Rango NOAA | " + " | ".join(H.CORRECTIONS) + " | sin Sa/Ssa (%s) |" %
          rep.get("corrections", "FES"), "|---|---|---|---|" + "---|" * len(H.CORRECTIONS) + "---|"]
    for r in rep.get("validation", []):
        L.append("| %s %s | %s, a %.2f km | %d días | %.0f cm | %s | %.1f |" % (
            r["id"], r["name"], r["source"], r["km"], r["days"], r["range"],
            " | ".join("%.1f" % r["rms"][c] for c in H.CORRECTIONS), r["rms_nosa"][rep.get("corrections", "FES")]))
    L += ["", "## Puertos", "",
          "| Clave | Fuente | Nombre | Datum | Rango (cm) | Horas completadas | Ajuste 30 períodos (RMS cm) |",
          "|---|---|---|---|---|---|---|"]
    for k in sorted(used):
        u = used[k]
        L.append("| %s | %s | %s | %s | %.0f..%.0f | %s | %.1f |" % (
            k, u["src"], u["name"], u["datum"], u["lo"], u["hi"],
            ", ".join("%d: %d" % (y, n) for y, n in sorted(u["filled"].items()) if n) or "—", u["rms"]))
    L += ["", "## Regiones", ""]
    for code in sel:
        r = sel[code]
        n = sum(len(p["spots"]) for p in r["ports"]) + len(r["nop"])
        L.append("### %s — %s (%d picos)" % (code, regions[code]["name_es"], n))
        L.append("")
        if not r["ports"]:
            L.append("Sin puerto: el reloj usa `sea_level_height_msl` de Open-Meteo.")
        for p in r["ports"]:
            s = st[p["i"]]
            ds = [x[1] for x in p["spots"]]
            L.append("- `%s` %s — %s: %d picos a %s–%s km, radio %d km%s" % (
                s["key"], s["name"], TIER_TXT[p["tier"]], len(p["spots"]), fmt_km(min(ds)), fmt_km(max(ds)),
                p["radius"], "" if all(x[2] == p["tier"] for x in p["spots"]) else
                " (niveles %s)" % ",".join(sorted(set(str(x[2]) for x in p["spots"])))))
        if r["ports"] and r["nop"]:
            L.append("- Sin puerto (Open-Meteo): " + ", ".join(
                s["name"] + ("" if not r["nearest"].get(s["name"]) else " (%s a %s km: %s)" % (
                    st[r["nearest"][s["name"]][0]]["key"], fmt_km(r["nearest"][s["name"]][1]),
                    r["nearest"][s["name"]][2])) for s in r["nop"]))
        if r.get("conflicts"):
            L.append("- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): " + ", ".join(r["conflicts"]))
        left = sorted(r["left"].items(), key=lambda x: x[1][0])[:4]
        if left:
            L.append("- Descartadas: " + "; ".join("`%s` %s km, %s" % (st[i]["key"], fmt_km(d), why) for i, (d, why) in left))
        L.append("")
    L += ["## Fuentes y licencias", "",
          "- NOAA/NOS/CO-OPS (dominio público): predicciones horarias sobre MLLW, estaciones armónicas.",
          "- 気象庁 JMA, 潮位表 (Public Data License 1.0): alturas horarias, JST → UTC, datum DL.",
          "- Marine Institute, Ireland (CC BY 4.0): ERDDAP `IMI-TidePrediction`, de 5 min a la hora.",
          "- LINZ (CC BY 4.0, Crown copyright): pleamares y bajamares → horarias con medios cosenos.",
          "- TICON-3 (CC BY 4.0): Hart-Davis, M. G., Dettmering, D., Seitz, F. (2022). TICON-3: Tidal Constants "
          "based on GESLA-3 sea-level records from globally distributed tide gauges including gauge type "
          "information (data). PANGAEA, https://doi.org/10.1594/PANGAEA.951610", ""]
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", nargs="*")
    ap.add_argument("--years", nargs="*", type=int)
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    years = a.years or [now.year, now.year + 1]
    os.makedirs(CACHE, exist_ok=True)
    rep = {"warnings": []}

    ticon_zip = os.path.join(CACHE, "TICON_3.zip")
    if not os.path.exists(ticon_zip):
        log("TICON-3: downloading %s" % S.TICON_ZIP)
        data = S.get(S.TICON_ZIP, timeout=600)
        with open(ticon_zip + ".part", "wb") as f:
            f.write(data)
        os.replace(ticon_zip + ".part", ticon_zip)
    man = S.ticon_manual(ticon_zip)
    if man:
        log("TICON-3 user manual (columns):\n" + man)

    t0 = time.time()
    st, coastal = load_catalogs(years[0], ticon_zip, rep)
    lats = np.array([s["lat"] for s in st])
    lons = np.array([s["lon"] for s in st])
    log("catalogs: %d stations in %.0f s" % (len(st), time.time() - t0))

    regions = seeds.regions()
    codes = [c for c in (a.regions or list(regions)) if c not in FROZEN]
    spots = {c: seeds.spots(c) for c in codes}

    heights = Heights(years, "FES")
    heights.corr = validate(st, coastal, heights, years[0], rep)
    log("nodal corrections: %s" % heights.corr)

    excluded = {}
    stale = set()
    for it in range(6):
        sel = {c: select_region(c, spots[c], st, lats, lons, excluded) for c in codes}
        need = sorted({p["i"] for r in sel.values() for p in r["ports"]})
        log("pass %d: %d ports for %d regions" % (it + 1, len(need), sum(1 for r in sel.values() if r["ports"])))
        new_fail = False
        for i in need:
            s = st[i]
            if s["key"] in heights.cache or s["key"] in stale:
                continue
            try:
                ser = heights.series(s)
                log("  %-16s %-5s %5.0f..%4.0f cm  %s" % (s["key"], s["kind"], ser["lo"], ser["hi"], s["name"]))
            except S.SourceError as e:
                if have_files(s["key"], years):
                    stale.add(s["key"])
                    rep["warnings"].append("%s: %s; quedan los archivos de la corrida anterior" % (s["key"], e))
                else:
                    excluded[s["key"]] = "descarga fallida"
                    rep["warnings"].append("%s: %s; descartado" % (s["key"], e))
                    new_fail = True
                log("  %s: %s" % (s["key"], e))
        if not new_fail:
            break

    # radius conflicts: a spot that the watch (nearest covering port) would give to another port
    for c, r in sel.items():
        conf = []
        for p in r["ports"]:
            for sp, d, tier, run in p["spots"]:
                for q in r["ports"]:
                    if q is p:
                        continue
                    s2 = st[q["i"]]
                    d2 = geo.km((sp["lat"], sp["lon"]), (s2["lat"], s2["lon"]))
                    if d2 <= q["radius"] and d2 < d:
                        conf.append("%s → %s" % (sp["name"], s2["key"]))
        r["conflicts"] = conf

    # write
    used = {}
    rep["files"] = rep["bytes"] = 0
    for c in codes:
        for p in sel[c]["ports"]:
            s = st[p["i"]]
            if s["key"] in used or s["key"] in stale:
                continue
            ser = heights.cache[s["key"]]
            nf, nb, rms = write_port(s, ser, years)
            rep["files"] += nf
            rep["bytes"] += nb
            used[s["key"]] = {"kind": s["kind"], "src": s["src"], "name": s["name"], "datum": ser["datum"],
                              "lo": ser["lo"], "hi": ser["hi"], "filled": ser["filled"], "rms": rms}
    for k in stale:
        s = next(x for x in st if x["key"] == k)
        with open(os.path.join(OUT, k, "%d-01.json" % years[0]), encoding="utf-8") as f:
            datum = json.load(f).get("datum", s["datum"])
        used[k] = {"kind": s["kind"], "src": s["src"], "name": s["name"], "datum": datum, "lo": 0, "hi": 0,
                   "filled": {}, "rms": float("nan")}

    # regions.json: frozen rows as they were, then every region with ports, in regions.csv order
    old = {}
    path = os.path.join(OUT, "regions.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
    rows = []
    for code in regions:
        if code in FROZEN:
            if code in old:
                rows.append((code, old[code]))
        elif code in sel and sel[code]["ports"]:
            rows.append((code, [[st[p["i"]]["key"], round(st[p["i"]]["lat"], 4), round(st[p["i"]]["lon"], 4),
                                 p["radius"], 0] for p in sel[code]["ports"]]))
        elif a.regions and code in old and code not in sel:
            rows.append((code, old[code]))
    write_regions(rows)

    ports = [dict(p) for p in LEGACY]
    by_key = {s["key"]: s for s in st}
    for k, u in used.items():
        s = by_key[k]
        ports.append({"key": k, "name": s["name"], "lat": round(s["lat"], 4), "lon": round(s["lon"], 4),
                      "utc_offset": 0, "src": s["src"], "datum": u["datum"], "license": s["license"],
                      "credit": s["credit"]})
    if a.regions and os.path.exists(os.path.join(OUT, "ports.json")):
        with open(os.path.join(OUT, "ports.json"), encoding="utf-8") as f:
            keep = {p["key"]: p for p in json.load(f)}
        keep.update({p["key"]: p for p in ports})
        ports = list(keep.values())
    write_ports(ports)

    # remove the folders of ports no longer used (full runs only)
    if not a.regions:
        for d in sorted(os.listdir(OUT)):
            full = os.path.join(OUT, d)
            if os.path.isdir(full) and d not in LEGACY_KEYS and d not in used:
                log("removing tide/%s (no region uses it)" % d)
                shutil.rmtree(full)

    rep["spots_total"] = sum(len(spots[c]) for c in codes)
    rep["spots_with"] = sum(len(p["spots"]) for c in codes for p in sel[c]["ports"])
    sizes = [os.path.getsize(os.path.join(OUT, k, f)) for k in used for f in os.listdir(os.path.join(OUT, k))
             if os.path.exists(os.path.join(OUT, k))]
    rep["max_month"] = max(sizes) if sizes else 0
    with open(os.path.join(OUT, "report.md"), "w", encoding="utf-8") as f:
        f.write(report_md(rep, regions, sel, st, used, years))
    log("done: %d ports, %d regions with ports, %d/%d spots, %d files %.1f MB, %.0f s" % (
        len(used), sum(1 for r in sel.values() if r["ports"]), rep["spots_with"], rep["spots_total"],
        rep["files"], rep["bytes"] / 1e6, time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
