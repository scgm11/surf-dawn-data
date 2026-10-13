"""Open-Meteo marine hourly series of the candidate wave models, for the last 30 days plus today,
at buoy positions (full variables) and at one spot per region (wave height only, for the
inter-model spread). Requests are grouped by the models a point can have, batched and paced
well under the free API limits (tools/lib/openmeteo.py: call_weight), and cached for the day.
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

VARS = ["wave_height", "wave_period", "wave_peak_period", "wave_direction"]
PAST_DAYS, FORECAST_DAYS = 30, 1
BATCH = 10                      # locations per request
PER_MINUTE = 250                # weighted calls per minute we allow ourselves (the API allows 600)
LABEL = {"ncep_gfswave016": "GFS-Wave 0,16°", "ncep_gfswave025": "GFS-Wave 0,25°", "meteofrance_wave": "MFWAM",
         "ecmwf_wam": "ECMWF WAM", "dwd_ewam": "DWD EWAM"}
USED = {"weight": 0.0, "requests": 0, "locations": 0}


def models_for(lat, lon):
    """The candidate wave models whose domain covers (lat, lon)."""
    ms = []
    if -15.0 <= lat <= 52.5:
        ms.append("ncep_gfswave016")
    ms += ["ncep_gfswave025", "meteofrance_wave", "ecmwf_wam"]
    if 30.0 <= lat <= 66.0 and -10.5 <= lon <= 42.0:
        ms.append("dwd_ewam")
    return ms


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


def _request(points, models, variables):
    params = {"latitude": ",".join("%.4f" % p[0] for p in points),
              "longitude": ",".join("%.4f" % p[1] for p in points),
              "hourly": ",".join(variables), "models": ",".join(models),
              "past_days": PAST_DAYS, "forecast_days": FORECAST_DAYS,
              "timezone": "GMT", "timeformat": "unixtime", "cell_selection": "sea"}
    w = openmeteo.call_weight(len(points), len(variables) * len(models), PAST_DAYS + FORECAST_DAYS)
    PACER.wait(w)
    USED["weight"] += w
    USED["requests"] += 1
    USED["locations"] += len(points)
    return openmeteo.get_json(params)


def _fetch(points, models, variables, log):
    """Blocks for each point, splitting a refused request until the refused point is alone."""
    res = _request(points, models, variables)
    if isinstance(res, dict) or len(res) != len(points):
        if len(points) == 1:
            log("  open-meteo refused %.4f,%.4f (%s): %s" % (points[0][0], points[0][1], ",".join(models),
                                                            res.get("reason") if isinstance(res, dict) else "bad answer"))
            return [None]
        half = len(points) // 2
        return _fetch(points[:half], models, variables, log) + _fetch(points[half:], models, variables, log)
    return res


def series(points, log, kind="buoy", variables=VARS):
    """{(lat, lon): (times, {model: {variable: [values]}})} for each point (rounded to 4 decimals),
    with the models of models_for(); a point the API refuses gets (times=[], {})."""
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
    for ms, group in todo.items():
        ms = list(ms)
        for i in range(0, len(group), BATCH):
            part = group[i:i + BATCH]
            blocks = _fetch(part, ms, variables, log)
            for p, b in zip(part, blocks):
                times, cols = openmeteo.split_models(b, ms, variables) if b else ([], {})
                cache.save_json("om", _name(kind, p[0], p[1], ms, variables), {"t": times, "m": cols})
                out[p] = (times, cols)
    return out
