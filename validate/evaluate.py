"""A region's validation: its buoys' hourly observations against the model series at each buoy,
pooled over the buoys on the hours every compared model has (the same sample for all).
Pure: takes the matched stations and the model series, returns the validation/<REGION>.json body."""
import score
from models import models_for
from regions import MAX_BUOYS

MIN_PAIRS = 72              # below this (3 days of hourly pairs) a region gets no best
COVER = 0.8                 # a model with fewer hours than this share of the best-covered one is left out
NOT_REPR = 0.5              # a buoy where every model is off by more than this (relative Hs bias) is
                            # not representative of the open coast (a bay, a harbour, a sheltered reef)


def region_result(region, matched, series, window, spread_pt=None, blocked=()):
    """matched: [(Station, km, shared)] nearest first (more than MAX_BUOYS: the unrepresentative ones are
    skipped and the next ones used); series: {(lat, lon): (times, {model: cols})} at the buoys;
    window: (from, to) dates; spread_pt: (times, {model: cols}) at the region's middle spot;
    blocked: [(Station, km, shared)] near but facing another sea (regions.match), only recorded.
    Returns (body, info) where info has what the report needs beyond the JSON."""
    body = {"region": region.code, "from": window[0], "to": window[1], "buoys": []}
    info = {"region": region, "matched": [], "dropped_models": []}
    cands = models_for(region.lat, region.lon)
    usable = []
    for st, d, sh in blocked:
        body.setdefault("excluded", []).append({"id": st.id, "km": round(d, 1), "why": "otro mar o abrigada: ve %.0f %% de las direcciones abiertas de los picos" % (100 * sh)})
    for st, d, _ in matched:
        times, cols = series.get((round(st.lat, 4), round(st.lon, 4)), ([], {}))
        have = [m for m in cands if m in cols]
        cur = region.current[0]
        if not times or not have or (cur in cands and cur not in have):   # a buoy must show today's model
            body.setdefault("excluded", []).append({"id": st.id, "km": round(d, 1), "why": "sin serie de %s en Open-Meteo" % (
                cur if have else "ningún modelo")})
            continue
        usable.append((st, d, times, cols, have))
    cur = region.current[0]
    if usable:
        # a model counts at a buoy if it has most of the hours the best-covered model has there
        cover = []
        for st, d, times, cols, have in usable:
            obs = set(st.hourly)
            n = {m: len(obs & score.model_hours(times, cols[m])) for m in have}
            top = max(n.values()) if n else 0
            ok = [m for m in have if top and n[m] >= COVER * top]
            info["coverage"] = info.get("coverage", []) + [(st.id, n)]
            cover.append(ok)
        keep = [(u, ok) for u, ok in zip(usable, cover) if cur not in cands or cur in ok]
        for u, ok in zip(usable, cover):
            if (u, ok) not in keep:
                body.setdefault("excluded", []).append({"id": u[0].id, "km": round(u[1], 1),
                                                        "why": "pocas horas de %s en Open-Meteo" % cur})
        usable = [u for u, _ in keep]
        common = [m for m in cands if keep and all(m in ok for _, ok in keep)]
        info["dropped_models"] = [m for m in cands if m not in common]
        pooled = {m: [] for m in common}
        per_buoy = {}
        for st, d, times, cols, _ in usable:
            hours = set(st.hourly)
            for m in common:
                hours &= score.model_hours(times, cols[m])
            ps = {m: score.pairs(st.hourly, times, cols[m], hours) for m in common}
            sc = {m: score.metrics(p) for m, p in ps.items() if p}
            if not sc:
                body.setdefault("excluded", []).append({"id": st.id, "km": round(d, 1),
                                                        "why": "sin horas en común entre la boya y los modelos"})
                continue
            if all(s["hs_bias"] is None or abs(s["hs_bias"]) > NOT_REPR for s in sc.values()):
                body.setdefault("excluded", []).append(
                    {"id": st.id, "km": round(d, 1), "why": "sesgo de Hs %s en todos los modelos" % ", ".join(
                        "%+.0f%%" % (100 * s["hs_bias"]) for s in sc.values() if s["hs_bias"] is not None)})
                continue
            if len(body["buoys"]) >= MAX_BUOYS:
                continue
            for m in common:
                pooled[m] += ps[m]
            per_buoy[st.id] = {"n": max(s["n"] for s in sc.values()), "best": score.best(sc), "km": round(d, 1)}
            body["buoys"].append(st.id)
            info["matched"].append((st, d, sc))
        scores = {m: score.metrics(p) for m, p in pooled.items() if p}
    else:
        scores, per_buoy = {}, {}
    if body["buoys"] and scores:
        tp_type = {}
        for st, d, times, cols, _ in usable:
            for m in scores:
                tp_type.setdefault(m, score.model_columns(cols[m], m)[2])
        wave = {}
        for m in score.rank(scores):
            s = dict(scores[m])
            s["tp_type"] = tp_type.get(m, "mean")
            wave[m] = s
        body["wave"] = wave
        n = max(s["n"] for s in scores.values())
        win = score.best(scores) if n >= MIN_PAIRS else None
        if win:
            body["best"] = {"wave": win}
            rival = region.current[0] if region.current[0] != win and region.current[0] in scores else \
                next((m for m in score.rank(scores) if m != win), None)
            wins = sum(1 for _, _, sc in info["matched"]
                       if win in sc and (rival not in sc or sc[win]["hs_rmse"] <= sc[rival]["hs_rmse"]))
            nearest = min(b["km"] for b in per_buoy.values())
            conf, margin = score.confidence(scores, win, rival, n, wins, len(per_buoy), nearest)
            body["confidence"] = conf
            body["vs"] = rival
            body["margin"] = margin
        else:
            body["confidence"] = "baja"
        body["per_buoy"] = per_buoy
    body["current"] = region.current[0]
    body["fixed"] = region.fixed
    if spread_pt is not None:
        times, cols = spread_pt
        sp, hours, means = score.spread(times, {m: c for m, c in cols.items()})
        body["spread"] = {"hs": sp, "hours": hours, "point": [round(region.mid[0], 4), round(region.mid[1], 4)],
                          "mean_hs": means}
    if not body["buoys"]:
        body["confidence"] = score.spread_confidence(body.get("spread", {}).get("hs"))
    return body, info
