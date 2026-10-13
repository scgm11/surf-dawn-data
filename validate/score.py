"""Scores of a wave model against buoys, pure functions (tested offline).

Pairs are hourly: an observation (hs, tp, dp, tm) and the model's (hs, period, peak period,
direction) at the same hour. Definitions (docs/formatos.md, Validación):
  hs_bias   (mean(model) - mean(obs)) / mean(obs)                  relative, fraction
  hs_rmse   sqrt(mean((model - obs)^2))                            m
  hs_si     sqrt(mean((model - obs - mean bias)^2)) / mean(obs)    scatter index (bias removed)
  tp_bias   mean(model Tp - obs Tp)                                s; the model's peak period, or its
            wave_period when it has none (tp_type "primary" or "mean", see PERIOD_KIND)
  tm_bias   mean(model wave_period - obs mean period)              s (the buoys' mean periods differ by source)
  dir_mae   mean |circular(model dir - obs peak dir)|              deg, pairs with obs Hs >= DIR_MIN_HS
  dir_bias  circular mean of (model dir - obs peak dir)             deg (near ±180: a from/to mix-up)
"""
import math
import statistics

DIR_MIN_HS = 0.3            # below this a buoy's peak direction is mostly noise
BIAS_MAX = 0.15             # a model with a larger |hs_bias| cannot be the best
TIE_M = 0.01                # rmse difference that counts as a tie (then dir_mae decides)
N_ALTA, N_MEDIA = 480, 240  # hourly pairs: 20 and 10 days
MARGIN_ALTA, MARGIN_MEDIA = 0.10, 0.05
FAR_KM = 100.0              # a region whose nearest buoy is farther cannot reach "alta"
SPREAD_BAJA = 0.30          # inter-model Hs spread above which a region without buoys is "baja"


def circ(a, b):
    """b - a on the circle, in (-180, 180]."""
    d = (b - a + 540.0) % 360.0 - 180.0
    return 180.0 if d == -180.0 else d


def circ_mean(ds):
    """Circular mean of angle differences, in (-180, 180]."""
    x = sum(math.cos(math.radians(d)) for d in ds)
    y = sum(math.sin(math.radians(d)) for d in ds)
    return circ(0.0, math.degrees(math.atan2(y, x)))


# What wave_period is in Open-Meteo for the models without wave_peak_period. GFS-Wave's is the
# period of the primary (dominant) wave system, close to the peak period: against the buoys it is
# ~0.5 s off their peak period and ~4-5 s above their mean period (validation of 2026-10).
PERIOD_KIND = {"ncep_gfswave016": "primary", "ncep_gfswave025": "primary"}


def model_columns(cols, model=None):
    """A model's columns {'wave_height': [...], ...} -> (hs, tp, tp_type, per, dp) lists.
    tp is the peak period when the model has one (any non-null value), else its wave_period, with
    tp_type "primary" (PERIOD_KIND) or "mean"."""
    n = len(cols.get("wave_height") or [])
    nul = [None] * n
    hs = cols.get("wave_height") or nul
    per = cols.get("wave_period") or nul
    pk = cols.get("wave_peak_period") or nul
    dp = cols.get("wave_direction") or nul
    if any(x is not None for x in pk):
        return hs, pk, "peak", per, dp
    return hs, per, PERIOD_KIND.get(model, "mean"), per, dp


def pairs(obs_hourly, times, cols, hours=None):
    """Hourly pairs of a buoy and a model: [(o_hs, m_hs, o_tp, m_tp, o_dp, m_dp, o_tm, m_per)].
    `times` are the model's unix times; `hours`, if given, limits to that set of hours
    (the hours every compared model has, so the models are scored on the same sample)."""
    hs, tp, _, per, dp = model_columns(cols)
    out = []
    for i, t in enumerate(times):
        h = int(t) // 3600
        if hours is not None and h not in hours:
            continue
        o = obs_hourly.get(h)
        if o is None or o[0] is None or hs[i] is None or hs[i] <= 0:
            continue
        out.append((o[0], hs[i], o[1], tp[i], o[2], dp[i], o[3], per[i]))
    return out


def model_hours(times, cols):
    hs = cols.get("wave_height") or []
    return {int(t) // 3600 for t, h in zip(times, hs) if h is not None and h > 0}


def _r(x, k):
    return None if x is None else round(x, k)


def metrics(ps):
    """Scores of a list of pairs (see pairs()); None when there are no pairs."""
    if not ps:
        return None
    o = [p[0] for p in ps]
    m = [p[1] for p in ps]
    n = len(ps)
    mo, mm = sum(o) / n, sum(m) / n
    err = [b - a for a, b in zip(o, m)]
    bias = sum(err) / n
    rmse = math.sqrt(sum(e * e for e in err) / n)
    si = math.sqrt(sum((e - bias) ** 2 for e in err) / n) / mo if mo > 0 else None
    tp = [p[3] - p[2] for p in ps if p[2] is not None and p[3] is not None]
    tm = [p[7] - p[6] for p in ps if p[6] is not None and p[7] is not None]
    sd = [circ(p[4], p[5]) for p in ps if p[4] is not None and p[5] is not None and p[0] >= DIR_MIN_HS]
    dd = [abs(x) for x in sd]
    return {"n": n, "hs_bias": _r((mm - mo) / mo if mo > 0 else None, 3), "hs_rmse": _r(rmse, 3),
            "hs_si": _r(si, 3), "tp_bias": _r(sum(tp) / len(tp), 2) if tp else None,
            "dir_mae": _r(sum(dd) / len(dd), 1) if dd else None,
            "dir_bias": _r(circ_mean(sd), 1) if sd else None,
            "tm_bias": _r(sum(tm) / len(tm), 2) if tm else None, "obs_hs": _r(mo, 2)}


def qualifies(s):
    return s["hs_bias"] is not None and abs(s["hs_bias"]) <= BIAS_MAX


def rank(scores):
    """Models ordered best first: those with |hs_bias| <= BIAS_MAX by hs_rmse, where the ones within
    TIE_M of the lowest go first ordered by dir_mae; then the rest by hs_rmse."""
    ok = sorted((m for m in scores if qualifies(scores[m])), key=lambda m: (scores[m]["hs_rmse"], m))
    rest = sorted((m for m in scores if not qualifies(scores[m])), key=lambda m: (scores[m]["hs_rmse"], m))
    if not ok:
        return rest
    lead = scores[ok[0]]["hs_rmse"]
    tied = [m for m in ok if scores[m]["hs_rmse"] - lead <= TIE_M + 1e-9]
    tied.sort(key=lambda m: (scores[m]["dir_mae"] if scores[m]["dir_mae"] is not None else 999.0, scores[m]["hs_rmse"], m))
    return tied + [m for m in ok if m not in tied] + rest


def best(scores):
    """The best model: lowest hs_rmse among those with |hs_bias| <= BIAS_MAX (ties within TIE_M
    by dir_mae), None if no model qualifies."""
    if not scores:
        return None
    r = rank(scores)
    return r[0] if qualifies(scores[r[0]]) else None


def confidence(scores, winner, rival, n, wins, n_buoys, nearest_km):
    """alta / media / baja for a region's best model, and the margin it is judged by.
    rival: the model the region uses today, or the runner-up when the best already is that one;
    margin: how much worse the rival is (hs_rmse, relative to the best's); n: hourly pairs;
    wins: buoys where the best's hs_rmse is not worse than the rival's."""
    if winner is None or rival is None or rival not in scores:
        return "baja", None
    b = scores[winner]["hs_rmse"]
    margin = (scores[rival]["hs_rmse"] - b) / b if b > 0 else 0.0
    agree = wins * 2 > n_buoys
    if n >= N_ALTA and margin >= MARGIN_ALTA and agree and nearest_km <= FAR_KM:
        return "alta", round(margin, 3)
    if n >= N_MEDIA and margin >= MARGIN_MEDIA and agree:
        return "media", round(margin, 3)
    return "baja", round(margin, 3)


def spread(times, by_model):
    """Inter-model spread of Hs at one point: for each hour with at least two models, the
    population std / mean of their Hs; the mean over hours. Also each model's mean Hs."""
    names = list(by_model)
    vals = []
    for i in range(len(times)):
        hs = [by_model[m]["wave_height"][i] for m in names
              if by_model[m].get("wave_height") and by_model[m]["wave_height"][i] is not None and by_model[m]["wave_height"][i] > 0]
        if len(hs) >= 2:
            mu = sum(hs) / len(hs)
            if mu > 0:
                vals.append(statistics.pstdev(hs) / mu)
    means = {}
    for m in names:
        x = [v for v in (by_model[m].get("wave_height") or []) if v is not None and v > 0]
        if x:
            means[m] = round(sum(x) / len(x), 2)
    return (round(sum(vals) / len(vals), 3) if vals else None), len(vals), means


def spread_confidence(sp):
    """A region without buoys: 'baja' when the models disagree (spread > SPREAD_BAJA), else 'media'."""
    if sp is None:
        return "baja"
    return "baja" if sp > SPREAD_BAJA else "media"
