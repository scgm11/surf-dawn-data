"""Open-Meteo hourly series of the candidate models for the last 30 days plus today:

  waves  Marine API, at buoy positions (full variables) and at one spot per region (wave height
         only, for the inter-model spread)
  wind   Forecast API, wind at 10 m at the wind stations (buoys: cell_selection=sea; stations
         ashore: nearest), with the models of the regions each station validates

Requests are grouped by the models a point can have, batched and paced well under the free API
limits (weight(): the API's own count), and cached for the day.
"""
import hashlib
import os
import sys
import time

import cache

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from tools.lib import openmeteo  # noqa: E402

FORECAST = "https://api.open-meteo.com/v1/forecast"
VARS = ["wave_height", "wave_period", "wave_peak_period", "wave_direction"]
WIND_VARS = ["wind_speed_10m", "wind_direction_10m"]
PAST_DAYS, FORECAST_DAYS = 30, 1
BATCH = 10                      # locations per request
PER_MINUTE = 250                # weighted calls per minute we allow ourselves (the API allows 600)
LABEL = {"ncep_gfswave016": "GFS-Wave 0,16°", "ncep_gfswave025": "GFS-Wave 0,25°", "meteofrance_wave": "MFWAM",
         "ecmwf_wam": "ECMWF WAM", "dwd_ewam": "DWD EWAM",
         "gfs_seamless": "GFS", "ecmwf_ifs": "ECMWF IFS", "meteofrance_seamless": "Météo-France",
         "ukmo_seamless": "UKMO", "cmc_gem_seamless": "GEM", "jma_seamless": "JMA", "bom_access_global": "BOM ACCESS-G",
         "icon_seamless": "ICON"}
# Wave models that can be chosen: the watch shows and scores the peak period, and only these give
# one in Open-Meteo (ECMWF WAM wave_peak_period; GFS-Wave the period of the primary system, which
# behaves as a peak). MFWAM and DWD EWAM only give a mean period: measured, never chosen.
ELIGIBLE = ("ecmwf_wam", "ncep_gfswave016", "ncep_gfswave025")
# Wind models compared and where (lat0, lat1, lon0, lon1): GFS and ECMWF IFS everywhere, the national
# models in their own high-resolution domain (their global run elsewhere is not a candidate).
WIND_DOMAINS = {
    "gfs_seamless": None,
    "ecmwf_ifs": None,
    "meteofrance_seamless": (20.0, 72.0, -32.0, 42.0),      # ARPEGE Europe (+ AROME France)
    "ukmo_seamless": (48.0, 62.0, -14.0, 4.0),              # UKV: British Isles
    "cmc_gem_seamless": (18.0, 72.0, -170.0, -50.0),         # RDPS / HRDPS: North America
    "jma_seamless": (20.0, 48.0, 118.0, 150.0),             # MSM: Japan, Korea, Taiwan
    "bom_access_global": (-50.0, 0.0, 100.0, 180.0),         # BoM's own region: Australia, NZ, SW Pacific
    "icon_seamless": (29.5, 70.5, -23.5, 62.5),             # ICON-EU (+ D2)
}
USED = {"weight": 0.0, "requests": 0, "locations": 0, "by_api": {}}
REFUSED = {}                    # wind model -> reason, when the API does not know it (probe_wind)


def models_for(lat, lon):
    """The candidate wave models whose domain covers (lat, lon)."""
    ms = []
    if -15.0 <= lat <= 52.5:
        ms.append("ncep_gfswave016")
    ms += ["ncep_gfswave025", "meteofrance_wave", "ecmwf_wam"]
    if 30.0 <= lat <= 66.0 and -10.5 <= lon <= 42.0:
        ms.append("dwd_ewam")
    return ms


def wind_models_for(lat, lon):
    """The wind models compared at (lat, lon): WIND_DOMAINS, less the ones the API refused."""
    out = []
    for m, box in WIND_DOMAINS.items():
        if m in REFUSED:
            continue
        if box is None or (box[0] <= lat <= box[1] and box[2] <= lon <= box[3]):
            out.append(m)
    return out


def weight(n_points, n_columns, n_days):
    """The calls of the daily allowance a request costs, as the API counts them (ForecastApiResult
    calculateQueryWeight): per location max(1, columns / 10 * max(1, days / 14)), where columns are
    variables x models."""
    v = n_columns / 10.0
    return n_points * max(1.0, v * max(1.0, n_days / 14.0))


class Pacer:
    """Keeps the weighted calls per minute under a ceiling."""
    def __init__(self, per_minute=PER_MINUTE, clock=time.monotonic, sleep=time.sleep):
        self.per_minute, self.clock, self.sleep = per_minute, clock, sleep
        self.log = []                      # [(time, weight)]

    def wait(self, weight):
        now = self.clock()
        self.log = [(t, w) for t, w in self.log if now - t < 60]
        while self.log and sum(w for _, w in self.log) + weight > self.per_minute:
            self.sleep(max(0.5, 60 - (now - self.log[0][0])))
            now = self.clock()
            self.log = [(t, w) for t, w in self.log if now - t < 60]
        self.log.append((now, weight))


PACER = Pacer()


def _name(kind, lat, lon, models, variables):
    h = hashlib.sha1((",".join(models) + "|" + ",".join(variables)).encode()).hexdigest()[:8]
    return "%s_%.4f_%.4f_%s.json" % (kind, lat, lon, h)


def _account(api, w, n):
    USED["weight"] += w
    USED["requests"] += 1
    USED["locations"] += n
    a = USED["by_api"].setdefault(api, {"weight": 0.0, "requests": 0, "locations": 0})
    a["weight"] += w
    a["requests"] += 1
    a["locations"] += n


def _request(points, models, variables, api="marine", extra=None, days=(PAST_DAYS, FORECAST_DAYS)):
    params = {"latitude": ",".join("%.4f" % p[0] for p in points),
              "longitude": ",".join("%.4f" % p[1] for p in points),
              "hourly": ",".join(variables), "models": ",".join(models),
              "past_days": days[0], "forecast_days": days[1],
              "timezone": "GMT", "timeformat": "unixtime", "cell_selection": "sea"}
    params.update(extra or {})
    w = weight(len(points), len(variables) * len(models), days[0] + days[1])
    PACER.wait(w)
    _account(api, w, len(points))
    return openmeteo.get_json(params, url=FORECAST if api == "forecast" else openmeteo.MARINE)


def _fetch(points, models, variables, log, api="marine", extra=None):
    """Blocks for each point, splitting a refused request until the refused point is alone."""
    res = _request(points, models, variables, api, extra)
    if isinstance(res, dict) or len(res) != len(points):
        if len(points) == 1:
            log("  open-meteo refused %.4f,%.4f (%s): %s" % (points[0][0], points[0][1], ",".join(models),
                                                            res.get("reason") if isinstance(res, dict) else "bad answer"))
            return [None]
        half = len(points) // 2
        return _fetch(points[:half], models, variables, log, api, extra) + _fetch(points[half:], models, variables, log, api, extra)
    return res


def _series(todo, out, variables, log, kind, api, extra=None):
    """Fetch {(models tuple): [points]} in batches into out (and the day's cache)."""
    for ms, group in todo.items():
        ms = list(ms)
        for i in range(0, len(group), BATCH):
            part = group[i:i + BATCH]
            blocks = _fetch(part, ms, variables, log, api, extra)
            for p, b in zip(part, blocks):
                times, cols = openmeteo.split_models(b, ms, variables) if b else ([], {})
                cache.save_json("om", _name(kind, p[0], p[1], ms, variables), {"t": times, "m": cols})
                out[p] = (times, cols)


def series(points, log, kind="buoy", variables=VARS):
    """{(lat, lon): (times, {model: {variable: [values]}})} for each point (rounded to 4 decimals),
    with the wave models of models_for(); a point the API refuses gets (times=[], {})."""
    pts = list(dict.fromkeys((round(p[0], 4), round(p[1], 4)) for p in points))
    out, todo = {}, {}
    for p in pts:
        ms = models_for(*p)
        hit = cache.load_json("om", _name(kind, p[0], p[1], ms, variables))
        if hit is not None:
            out[p] = (hit["t"], hit["m"])
        else:
            todo.setdefault(tuple(ms), []).append(p)
    n = sum(len(v) for v in todo.values())
    if n:
        log("open-meteo: %d %s points to fetch (%d cached)" % (n, kind, len(pts) - n))
    _series(todo, out, variables, log, kind, "marine")
    return out


def probe_wind(log, models=None):
    """Ask once for each wind model at one point (weight 1 each): a model the API does not know goes
    to REFUSED and is left out everywhere (instead of every batch failing point by point)."""
    for m in models or list(WIND_DOMAINS):
        hit = cache.load_json("om", "probe_%s.json" % m)
        if hit is None:
            res = _request([(0.0, 0.0)], [m], ["wind_speed_10m"], "forecast", {"cell_selection": "nearest"}, (0, 1))
            hit = {"reason": res.get("reason", "refused")} if isinstance(res, dict) else {"ok": True}
            cache.save_json("om", "probe_%s.json" % m, hit)
        if not hit.get("ok"):
            REFUSED[m] = hit.get("reason")
            log("open-meteo: wind model %s refused (%s): left out" % (m, str(hit.get("reason"))[:120]))


def wind_series(stations, log):
    """stations: [(lat, lon, kind, [models])] -> {(lat, lon): (times, {model: {variable: [values]}})},
    wind at 10 m in m/s. Buoys ask for the nearest sea cell, stations ashore for the nearest cell."""
    out, todo = {}, {}
    seen = set()
    for lat, lon, kind, ms in stations:
        p = (round(lat, 4), round(lon, 4))
        if p in seen:
            continue
        seen.add(p)
        ms = [m for m in dict.fromkeys(ms) if m not in REFUSED]
        cell = "sea" if kind == "buoy" else "nearest"
        name = "wind-%s" % cell
        hit = cache.load_json("om", _name(name, p[0], p[1], ms, WIND_VARS))
        if hit is not None:
            out[p] = (hit["t"], hit["m"])
        else:
            todo.setdefault(cell, {}).setdefault(tuple(ms), []).append(p)
    n = sum(len(g) for c in todo.values() for g in c.values())
    if n:
        log("open-meteo: %d wind points to fetch (%d cached)" % (n, len(seen) - n))
    for cell, groups in todo.items():
        _series(groups, out, WIND_VARS, log, "wind-%s" % cell, "forecast", {"cell_selection": cell, "wind_speed_unit": "ms"})
    return out
