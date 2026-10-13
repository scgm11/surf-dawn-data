"""validation/report.md and models-suggested.csv from the regions' results (pure)."""
import time

from models import LABEL
from regions import DEFAULT_WIND, MATCH_KM
import score

SOURCES = {
    "cdip": ("CDIP", "Coastal Data Information Program, Scripps Institution of Oceanography (UCSD); ERDDAP `wave_agg`",
             "uso libre, se agradece el crédito a CDIP"),
    "aodn": ("AODN / IMOS", "Boyas de olas de Australia (IMOS, estados y universidades), parquet `wave_buoy_realtime_nonqc`",
             "CC BY 4.0"),
    "mi": ("Marine Institute", "Irish Wave Buoy Network, ERDDAP `IWaveBNetwork30Min`", "CC BY 4.0"),
    "ndbc": ("NOAA NDBC", "National Data Buoy Center, `realtime2` (incluye socios: PNBOIA, Canadá, etc.)", "dominio público"),
}


def f(x, k=2, pct=False):
    if x is None:
        return "—"
    if pct:
        return "%+.0f %%" % (100 * x)
    return ("%." + str(k) + "f") % x


def suggestions(results):
    """[region, wave, wind, why] for regions with a confident ('alta' or 'media') best model that is
    not the one they use today; never the fixed regions (issue #7)."""
    rows = []
    for body, info in results:
        r = info["region"]
        win = body.get("best", {}).get("wave")
        if r.fixed or not win or body.get("confidence") not in ("alta", "media") or win == r.current[0]:
            continue
        w, c = body["wave"][win], body["wave"].get(r.current[0])
        why = "validación %s (%s): Hs rmse %.2f m vs %.2f de %s, sesgo %s, %d h, %s" % (
            body["to"], body["confidence"], w["hs_rmse"], c["hs_rmse"] if c else float("nan"), r.current[0],
            f(w["hs_bias"], pct=True), w["n"], " ".join(body["buoys"]))
        rows.append([r.code, win, r.current[1] if len(r.current) > 1 else DEFAULT_WIND, why])
    return rows


def _row(body, info):
    r = info["region"]
    win = body.get("best", {}).get("wave")
    cur = body["wave"].get(r.current[0], {})
    w = body["wave"].get(win) if win else None
    shown = w or cur or next(iter(body["wave"].values()))
    name = win or "ninguno"
    tag = " (fija)" if r.fixed else ""
    flag = ""
    if win and win != r.current[0]:
        flag = " ⇐" if not r.fixed and body["confidence"] in ("alta", "media") else ""
    return "| %s%s | %s | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        r.code, tag, "<br>".join("%s (%.0f km)" % (b, body["per_buoy"][b]["km"]) for b in body["buoys"]),
        LABEL.get(name, name), flag, shown["n"], f(shown["hs_rmse"]), f(shown["hs_bias"], pct=True), f(shown["hs_si"]),
        f(shown["tp_bias"], 1) + {"mean": "ᵐ", "primary": "ᵖ"}.get(shown.get("tp_type"), ""), f(shown["dir_mae"], 0),
        LABEL.get(r.current[0], r.current[0]), f(cur.get("hs_rmse")), body["confidence"])


def markdown(results, window, status, checks, used, twins):
    from tools.lib import seeds
    countries = seeds.countries()
    withb = [(b, i) for b, i in results if b["buoys"]]
    without = [(b, i) for b, i in results if not b["buoys"]]
    by_src = {}
    for b, _ in withb:
        for s in {x.split(":")[0] for x in b["buoys"]}:
            by_src[s] = by_src.get(s, 0) + 1
    wins = {}
    for b, _ in withb:
        w = b.get("best", {}).get("wave", "ninguno")
        wins[w] = wins.get(w, 0) + 1
    conf = {}
    for b, _ in withb:
        conf[b["confidence"]] = conf.get(b["confidence"], 0) + 1
    L = ["# Validación de los modelos de olas", "",
         "Ventana: **%s a %s** (UTC), hora a hora. Generado el %s por `validate/run.py` (ver `validate/README.md`)."
         % (window[0], window[1], time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())), "",
         "Cada región se compara con hasta 3 boyas a menos de %d km de alguno de sus picos (la más cercana primero). "
         "Todos los modelos se miden sobre las mismas horas. El mejor es el de menor `hs_rmse` con |sesgo| ≤ %d %% "
         "(empates de %.2f m: menor error de dirección). La confianza mira las horas (≥ %d alta, ≥ %d media), cuánto "
         "peor es el modelo de hoy (≥ %d %% alta, ≥ %d %% media), que la mayoría de las boyas coincida y que la boya "
         "más cercana esté a ≤ %d km (alta)."
         % (MATCH_KM, score.BIAS_MAX * 100, score.TIE_M, score.N_ALTA, score.N_MEDIA, score.MARGIN_ALTA * 100,
            score.MARGIN_MEDIA * 100, score.FAR_KM), "",
         "## Resumen", "",
         "- Regiones: **%d**; con boyas: **%d**; sin boyas: **%d**." % (len(results), len(withb), len(without)),
         "- Regiones con boyas por fuente: %s." % ", ".join("%s %d" % (SOURCES[s][0], n) for s, n in sorted(by_src.items(), key=lambda x: -x[1])),
         "- Mejor modelo (regiones con boyas): %s." % ", ".join("%s %d" % (LABEL.get(m, m), n) for m, n in sorted(wins.items(), key=lambda x: -x[1])),
         "- Confianza: %s." % ", ".join("%s %d" % (k, conf.get(k, 0)) for k in ("alta", "media", "baja")),
         "- Open-Meteo: %d pedidos, %d ubicaciones, ~%.0f llamadas ponderadas (límite gratuito 10.000/día)."
         % (used["requests"], used["locations"], used["weight"]), ""]
    L += ["## Fuentes", "", "| Fuente | Datos | Licencia | Esta corrida |", "|---|---|---|---|"]
    for s, (name, what, lic) in SOURCES.items():
        L.append("| %s | %s | %s | %s |" % (name, what, lic, status.get(s, "no se pidió")))
    if twins:
        L += ["", "Boyas publicadas por dos fuentes (se usa una): %s." % ", ".join("%s = %s" % (k.id, s.id) for s, k in twins)]
    L += ["", "## Por país", "", "| País | Regiones con boyas | Gana |", "|---|---|---|"]
    byc = {}
    for b, i in withb:
        byc.setdefault(i["region"].country, []).append(b.get("best", {}).get("wave", "ninguno"))
    for c, ws in sorted(byc.items(), key=lambda x: (-len(x[1]), x[0])):
        cnt = {}
        for w in ws:
            cnt[w] = cnt.get(w, 0) + 1
        L.append("| %s | %d | %s |" % (countries.get(c, {}).get("name_es", c), len(ws),
                                       ", ".join("%s %d" % (LABEL.get(m, m), n) for m, n in sorted(cnt.items(), key=lambda x: -x[1]))))
    L += ["", "## Regiones con boyas", "",
          "Métricas del mejor modelo (o del de hoy si ninguno califica). `Tp` es el sesgo de período del modelo contra el "
          "período pico de la boya; ᵖ: GFS-Wave no da período pico en Open-Meteo y se usa su `wave_period`, que es el del "
          "sistema de olas principal (se comporta como un pico); ᵐ: MFWAM y EWAM tampoco lo dan y su `wave_period` es un "
          "período medio, así que su `Tp` sale negativo por construcción. "
          "⇐ = se sugiere cambiar (en `models-suggested.csv`). Las regiones fijas (issue #7) se validan sólo para informar.", "",
          "| Región | Boyas | Mejor | n | rmse m | sesgo | SI | Tp s | dir ° | Hoy | rmse hoy | Confianza |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b, i in withb:
        L.append(_row(b, i))
    L += ["", "## Regiones sin boyas (%d)" % len(without), "",
          "Dispersión entre modelos de la altura de ola en el pico central de la región (desvío / media, promedio de "
          "las horas). Más de %.2f ⇒ confianza baja: los modelos no coinciden y conviene buscar boyas."
          % score.SPREAD_BAJA, "",
          "| Región | Dispersión | Hs media por modelo (m) | Confianza |", "|---|---|---|---|"]
    for b, i in sorted(without, key=lambda x: -(x[0].get("spread", {}).get("hs") or 0)):
        sp = b.get("spread", {})
        L.append("| %s | %s | %s | %s |" % (b["region"], f(sp.get("hs")),
                                            ", ".join("%s %.2f" % (LABEL.get(m, m), v) for m, v in sp.get("mean_hs", {}).items()),
                                            b["confidence"]))
    L += ["", "## Control de convenciones por fuente", "",
          "Promedios ponderados por horas sobre todas las boyas de cada fuente. `Tp` = modelo − período pico de la boya; "
          "`Tm` = `wave_period` del modelo − período medio de la boya (NDBC APD, CDIP Ta, AODN WPFM, MI EnergyPeriod: no son "
          "el mismo momento espectral); `dir` = error medio absoluto de dirección (de dónde vienen); `sesgo dir` = media "
          "circular de modelo − boya (cerca de ±180° indicaría una boya en convención \"hacia\").", "",
          "| Fuente | Modelo | horas | Tp s | Tm s | dir ° | sesgo dir ° |", "|---|---|---|---|---|---|---|"]
    for s, ms in sorted(checks.items()):
        for m, c in sorted(ms.items()):
            L.append("| %s | %s | %d | %s | %s | %s | %s |" % (SOURCES.get(s, (s,))[0], LABEL.get(m, m), c["n"], f(c["tp_bias"], 1),
                                                             f(c["tm_bias"], 1), f(c["dir_mae"], 0), f(c.get("dir_bias"), 0)))
    L += ["", "## Próximos pasos", "",
          "- Fuentes con cuenta o clave que faltan: **Copernicus Marine** (In Situ TAC: boyas de Europa, Brasil, Sudáfrica, "
          "Japón), **CANDHIS** (Francia), **Channel Coastal Observatory** (Inglaterra), **Puertos del Estado** (España), "
          "**IH Portugal**, **SIMCOSTA/PNBOIA** directo (Brasil), **CMEMS** para Uruguay y Argentina.",
          "- Los meses cambian el ganador (verano/invierno, swell/viento): mirar varias corridas mensuales antes de pasar "
          "una sugerencia a `models.csv` por PR.",
          "- Las boyas lejos de la costa validan el modelo en mar abierto, no el punto de olas del pico: preferir boyas "
          "someras (CDIP, AODN, MI) cuando haya.",
          "- Viento: sin validar (sigue `gfs_seamless`).", ""]
    return "\n".join(L)
