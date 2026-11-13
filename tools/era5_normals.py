#!/usr/bin/env python3
"""ERA5's waves and wind at each region, for what is normal there in the iPhone's Cómo viene
(normals/normals.json, docs/formatos.md).

The normal of a region is worked out in the apps' repo, with the apps' own ranking (surf-dawn:
`Normals` in SurfDawnKit/Outlook.swift and its tool, `swift run normals --answers`): of each month,
how many days in 30 gave waves at some spot of the region from 2016 to 2024. That takes nine years of
hourly waves and wind at one point, some 480 calls of Open-Meteo's free API (10,000 a day) a region:
too many to ask from the user's connection, which the phone shares. This tool only asks, on GitHub's
runners, the same seven requests the Swift tool would, at the region's reference spot (the one whose wave
point most of its spots share, Normals.reference; ties the first):

- ERA5's wind (archive API, 0.25°) at the spot: wind_speed_10m and wind_direction_10m in km/h, sunrise,
  sunset and the air's daily max and min, from START to END (the end of ERA5-Ocean's peak period,
  Normals.lastDay), timezone=auto;
- ERA5-Ocean's waves (marine API, 0.5°) at its wave point: wave_height, wave_peak_period and
  wave_direction (Normals.keys), the same days, in the wind's time zone;
- the region's wave model's last 92 days and ERA5-Ocean's at the same point (wave_height, GMT): ERA5's
  heights are taken times the model's mean over them (Normals.factor);
- the water at the spot (the marine API's sea_surface_temperature, the one the forecast gives: it has no
  history before 2023), its whole years from WATER_START to WATER_END, in the wind's time zone;
- the air's daily max and min of the region's wind model over the last 92 days and ERA5's (Normals.offset).

Each region's answers go into one gzip (tools/.cache/era5/<REGION>.json.gz) and, with --upload, to
the release "era5" of this repo, with index.json: each region's reference spot, so that a region whose
reference spot moved is asked again and the rest never. BUDGET calls a run, a region every PACE s at
least (5,000 an hour, 600 a minute), the rest in the next runs (Action era5.yml, daily); a 429 for the
day ends the run with what it got.

    python3 tools/era5_normals.py [--budget N] [--upload] [REGION ...]
"""
import argparse
import datetime
import gzip
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)
from tools.lib import openmeteo  # noqa: E402

REGIONS = os.path.join(ROOT, "spots", "r")
CACHE = os.path.join(ROOT, "tools", ".cache", "era5")
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
MARINE = openmeteo.MARINE
START, END = "2016-01-01", "2024-11-17"          # ERA5-Ocean's peak period ends there (Normals.lastDay)
WAVES = "wave_height,wave_peak_period,wave_direction"   # Normals.keys: the total sea, as ECMWF WAM's
WIND = "wind_speed_10m,wind_direction_10m"
AIR = "temperature_2m_max,temperature_2m_min"   # Normals.airKeys
WATER_START, WATER_END = "2023-01-01", "2025-12-31"   # Normals.waterStart, waterEnd
FORECAST = "https://api.open-meteo.com/v1/forecast"
FACTOR_DAYS = 92                                 # the model's past days against ERA5's (Normals.factor)
BUDGET = 9000                                    # calls a run: the free API's 10,000 a day, a margin left
PACE = 440                                       # s a region at least: ~570 calls each, under 5,000 an hour
RELEASE = "era5"
VERSION = 2                                      # 2: with the water and the air (13/11/2026); a region asked before, again
FACTORY = ("UY-CAN", "UY-MAL", "UY-ROC")         # the apps bring theirs (Normals' normals.json): last
MIN_SHARE = 0.5                                  # of the hours with a peak period, or the point has no sea


class Stop(Exception):
    """The day's calls are over (a 429 for the day): the rest in the next run."""


def wave_point(s):
    """A spot row's wave point: its offshore point, else its own position (Spot.wavePoint)."""
    return (s[5], s[6]) if len(s) >= 7 else (s[1], s[2])


def reference(z):
    """The spot whose waves and wind stand for the region's: the one with the wave point most of its
    spots share, ties the first in the region's order (Normals.reference)."""
    points = [wave_point(s) for s in z["s"]]
    best, most = 0, 0
    for i, p in enumerate(points):
        n = points.count(p)
        if n > most:
            best, most = i, n
    return best


def coord(v):
    return "%.4f" % v                            # OpenMeteo.coord


def day(days_ago, today):
    return (today - datetime.timedelta(days=days_ago)).isoformat()


def plan(z, today):
    """The region's four requests as the Swift tool asks them (OpenMeteo.url: latitude, longitude,
    timeformat, timezone=auto unless one is given, cell_selection=sea on the marine API, then the
    request's own): {name: (url, [(key, value)])}. The waves' time zone is the wind's answer's, filled
    in by fetch(), and so are the air's. Plus the reference spot, to know later whether it moved."""
    s = z["s"][reference(z)]
    at = (coord(s[1]), coord(s[2]))
    wp = wave_point(s)
    wave = (coord(wp[0]), coord(wp[1]))
    head = [("timeformat", "unixtime")]
    sea = head + [("cell_selection", "sea")]
    return {
        "spot": s[0], "at": [s[1], s[2]], "wave": list(wp), "model": z["m"][0],
        "wind": (ARCHIVE, [("latitude", at[0]), ("longitude", at[1])] + head + [
            ("timezone", "auto"), ("hourly", WIND), ("daily", "sunrise,sunset," + AIR), ("models", "era5"),
            ("wind_speed_unit", "kmh"), ("start_date", START), ("end_date", END)]),
        "marine": (MARINE, [("latitude", wave[0]), ("longitude", wave[1])] + sea + [
            ("hourly", WAVES), ("models", "era5_ocean"), ("start_date", START), ("end_date", END),
            ("timezone", None)]),
        "factor_model": (MARINE, [("latitude", wave[0]), ("longitude", wave[1])] + sea + [
            ("hourly", "wave_height"), ("models", z["m"][0]), ("past_days", str(FACTOR_DAYS)),
            ("forecast_days", "1"), ("timezone", "GMT")]),
        "factor_era5": (MARINE, [("latitude", wave[0]), ("longitude", wave[1])] + sea + [
            ("hourly", "wave_height"), ("models", "era5_ocean"), ("start_date", day(FACTOR_DAYS, today)),
            ("end_date", day(1, today)), ("timezone", "GMT")]),
        "water": (MARINE, [("latitude", at[0]), ("longitude", at[1])] + sea + [
            ("hourly", "sea_surface_temperature"), ("start_date", WATER_START), ("end_date", WATER_END), ("timezone", None)]),
        "air_model": (FORECAST, [("latitude", at[0]), ("longitude", at[1])] + head + [("cell_selection", "nearest"),
            ("daily", AIR), ("models", z["m"][1]), ("past_days", str(FACTOR_DAYS)), ("forecast_days", "1"), ("timezone", None)]),
        "air_era5": (ARCHIVE, [("latitude", at[0]), ("longitude", at[1])] + head + [
            ("daily", AIR), ("models", "era5"), ("start_date", day(FACTOR_DAYS, today)), ("end_date", day(1, today)),
            ("timezone", None)]),
    }


def weight(params):
    """What a request costs of the day's calls (openmeteo.call_weight)."""
    p = dict(params)
    n_vars = sum(len(p[k].split(",")) for k in ("hourly", "daily") if p.get(k))
    if "start_date" in p:
        a, b = (datetime.date.fromisoformat(p[k]) for k in ("start_date", "end_date"))
        n_days = (b - a).days + 1
    else:
        n_days = int(p.get("past_days", 0)) + int(p.get("forecast_days", 7))
    return openmeteo.call_weight(1, n_vars, n_days)


def cost(z, today):
    pl = plan(z, today)
    return sum(weight(pl[k][1]) for k in ("wind", "marine", "factor_model", "factor_era5", "water", "air_model", "air_era5"))


def get(url, params, tries=6):
    """GET url?params, decoded. A 429 waits out the minute or the hour, and for the day raises Stop;
    a 400 raises ValueError with the API's reason; the rest (503 when it is busy, timeouts) retried."""
    q = urllib.parse.urlencode(params, safe=",")
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url + "?" + q, timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try:
                reason = str(json.load(e).get("reason", ""))
            except (ValueError, AttributeError):
                reason = ""
            if e.code == 400:
                raise ValueError(reason or "HTTP 400")
            if e.code == 429 and "aily" in reason:
                raise Stop(reason)
            if e.code == 429 and "ourly" in reason:
                wait = 3600 - time.time() % 3600 + 60
            elif e.code == 429:
                wait = 65
            else:
                wait = 30 * (attempt + 1)
            print("  open-meteo %d %s: %d s" % (e.code, reason[:60], wait), file=sys.stderr, flush=True)
        except (urllib.error.URLError, OSError, ValueError) as e:
            wait = 30 * (attempt + 1)
            print("  open-meteo: %s: %d s" % (str(e)[:80], wait), file=sys.stderr, flush=True)
        time.sleep(wait)
    raise RuntimeError("Open-Meteo unavailable")


def sea_hours(marine):
    h = marine.get("hourly") or {}
    tp = h.get("wave_peak_period") or []
    return sum(1 for v in tp if v is not None), len(tp)


def fetch(z, today):
    """The region's bundle: its reference spot and the four answers (the waves in the wind's time zone)."""
    pl = plan(z, today)
    out = {"v": VERSION, "region": z["id"], "spot": pl["spot"], "at": pl["at"], "wave": pl["wave"],
           "model": pl["model"], "fetched": today.isoformat(), "asked": {}}

    def ask(name, params, fail=None):
        url = pl[name][0]
        out["asked"][name] = urllib.parse.urlencode(params, safe=",")   # the Swift tool checks it is its request
        try:
            out[name] = get(url, params)
        except ValueError as e:
            if fail is None:
                raise
            out[name] = fail(e)

    ask("wind", pl["wind"][1])
    tz = out["wind"].get("timezone") or "auto"
    ask("marine", [(k, tz if k == "timezone" else v) for k, v in pl["marine"][1]])
    for k in ("factor_model", "factor_era5", "water", "air_model", "air_era5"):
        # a model without the point: the heights as ERA5's (k = 1); no water or air there: Cómo viene without them
        ask(k, [(p, tz if p == "timezone" and v is None else v) for p, v in pl[k][1]],
            fail=lambda e: {"error": True, "reason": str(e)})
    return out


def entry(b):
    """A bundle's line of index.json: what it was asked at, so a region whose reference spot moved is
    asked again."""
    n, total = sea_hours(b["marine"])
    return {"v": VERSION, "spot": b["spot"], "at": b["at"], "wave": b["wave"], "model": b["model"], "fetched": b["fetched"],
            "hours": n, "of": total}


def current(e, pl):
    """Asked already, at the same reference spot and with this version's requests (an error stays as it is)."""
    return e is not None and e.get("spot") == pl["spot"] and e.get("at") == pl["at"] and e.get("wave") == pl["wave"] \
        and (e.get("v") == VERSION or "error" in e)


def gh(*args, check=True):
    return subprocess.run(["gh", *args], check=check, capture_output=True, text=True)


def release_index():
    """index.json of the release, created when there is none yet."""
    if gh("release", "view", RELEASE, check=False).returncode != 0:
        gh("release", "create", RELEASE, "--prerelease", "--title", "ERA5 para lo normal (Cómo viene)",
           "--notes", "Las olas y el viento de ERA5 (2016-2024) en el pico de referencia de cada región, como "
           "los pide la app de iPhone para calcular lo normal (tools/era5_normals.py). Datos de Open-Meteo "
           "(CC BY 4.0) con ERA5 y ERA5-Ocean de Copernicus (ECMWF). Lo que bajan las apps es "
           "normals/normals.json.")
        return {}
    with tempfile.TemporaryDirectory() as d:
        r = gh("release", "download", RELEASE, "-p", "index.json", "-D", d, check=False)
        if r.returncode != 0:
            return {}
        with open(os.path.join(d, "index.json")) as f:
            return json.load(f).get("regions", {})


def upload(paths):
    gh("release", "upload", RELEASE, *paths, "--clobber")


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path + ".tmp", "wt", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    os.replace(path + ".tmp", path)              # whole or not at all


def write_index(index):
    path = os.path.join(CACHE, "index.json")
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "w") as f:
        json.dump({"v": VERSION, "regions": dict(sorted(index.items()))}, f, indent=0, separators=(",", ":"))
    return path


def local_index():
    try:
        with open(os.path.join(CACHE, "index.json")) as f:
            return json.load(f).get("regions", {})
    except (OSError, ValueError):
        return {}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("regions", nargs="*")
    ap.add_argument("--budget", type=float, default=BUDGET)
    ap.add_argument("--upload", action="store_true", help="to the release era5 (gh, GH_TOKEN)")
    a = ap.parse_args()
    today = datetime.datetime.now(datetime.timezone.utc).date()
    codes = a.regions or sorted(f[:-5] for f in os.listdir(REGIONS) if f.endswith(".json"))
    codes.sort(key=lambda c: (c in FACTORY, c))
    index = release_index() if a.upload else local_index()
    zones = {}
    for c in codes:
        with open(os.path.join(REGIONS, c + ".json"), encoding="utf-8") as f:
            zones[c] = json.load(f)
    todo = [c for c in codes if not current(index.get(c), plan(zones[c], today))]
    print("%d regiones, %d por bajar (~%.0f llamadas cada una)" % (len(codes), len(todo), cost(zones[todo[0]], today) if todo else 0),
          flush=True)
    spent = 0.0
    done = 0
    for c in todo:
        w = cost(zones[c], today)
        if spent + w > a.budget:
            break
        t0 = time.time()
        spent += w
        try:
            b = fetch(zones[c], today)
            e = entry(b)
            if e["hours"] < MIN_SHARE * max(1, e["of"]):
                e["error"] = "sin olas en el punto"
            else:
                path = os.path.join(CACHE, c + ".json.gz")
                save(path, b)
                if a.upload:
                    upload([path])
        except Stop as err:
            print("%s: se acabaron las llamadas del día (%s)" % (c, err), flush=True)
            break
        except ValueError as err:                # the API refuses the request: so it will tomorrow
            pl = plan(zones[c], today)
            e = {k: pl[k] for k in ("spot", "at", "wave", "model")}
            e.update(v=VERSION, fetched=today.isoformat(), hours=0, of=0, error=str(err)[:120])
        except RuntimeError as err:              # Open-Meteo down: the next run asks again
            print("%s: %s" % (c, err), file=sys.stderr, flush=True)
            continue
        # an error stays in the index: the region is not asked again until its reference spot moves
        index[c] = e
        idx = write_index(index)
        if a.upload:
            upload([idx])
        done += 1
        print("%3d/%d %-11s %-18s %6d horas de olas  %5.0f llamadas  %s" % (
            done, len(todo), c, e["spot"], e["hours"], spent, e.get("error", "")), flush=True)
        if c != todo[-1]:
            time.sleep(max(0, PACE - (time.time() - t0)))
    print("bajadas %d, faltan %d, %.0f llamadas" % (done, len(todo) - done, spent), flush=True)


if __name__ == "__main__":
    main()
