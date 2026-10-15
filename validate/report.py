"""validation/report.md and models-suggested.csv from the regions' results (pure)."""
import time

from buoys import WIND_EXP
from models import ELIGIBLE, LABEL, REFUSED, WIND_DOMAINS
from regions import DEFAULT_WIND, MATCH_KM
import score

SOURCES = {
    "cdip": ("CDIP", "Coastal Data Information Program, Scripps Institution of Oceanography (UCSD); ERDDAP `wave_agg`",
             "uso libre, se agradece el crédito a CDIP"),
    "aodn": ("AODN / IMOS", "Boyas de olas de Australia (IMOS, estados y universidades), parquet `wave_buoy_realtime_nonqc`",
             "CC BY 4.0"),
    "mi": ("Marine Institute", "Irish Wave Buoy Network, ERDDAP `IWaveBNetwork30Min`, y boyas meteorológicas M2–M6 "
           "(`IWBNetwork`, con viento)", "CC BY 4.0"),
    "ndbc": ("NOAA NDBC", "National Data Buoy Center, `realtime2` (boyas, C-MAN y estaciones costeras con viento; incluye "
             "socios: PNBOIA, Canadá, etc.)", "dominio público"),
    "cmems": ("Copernicus Marine In Situ", "`INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030`, archivos diarios `latest`: boyas "
              "de Europa (CANDHIS, Puertos del Estado, Cefas…), Marruecos, Canarias y del GTS; necesita cuenta (secretos "
              "`COPERNICUSMARINE_SERVICE_USERNAME` y `_PASSWORD`)", "licencia de Copernicus Marine (libre, con crédito)"),
}
WIND_WHERE = {"gfs_seamless": "todas partes (hoy)", "ecmwf_ifs": "todas partes", "meteofrance_seamless": "Europa (ARPEGE Europa, AROME)",
              "ukmo_seamless": "Islas Británicas (UKV)", "cmc_gem_seamless": "Norteamérica (RDPS, HRDPS)",
              "jma_seamless": "Japón, Corea y Taiwán (MSM)", "bom_access_global": "Australia, Nueva Zelanda y Pacífico sudoeste",
              "icon_seamless": "Europa (ICON-EU, D2)"}


def f(x, k=2, pct=False):
    if x is None:
        return "—"
    if pct:
        return "%+.0f %%" % (100 * x)
    return ("%." + str(k) + "f") % x


def L_(m):
    return LABEL.get(m, m)


def suggestions(results):
    """[region, wave, wind, why] for the regions whose confident ('alta' or 'media') best wave or wind
    model is not the one they use today; the other column keeps today's model. Never the fixed
    regions (issue #7)."""
    rows = []
    for body, info in results:
        r = info["region"]
        if r.fixed:
            continue
        cur_wave = r.current[0]
        cur_wind = r.current[1] if len(r.current) > 1 else DEFAULT_WIND
        wave, wind, why = cur_wave, cur_wind, []
        win = body.get("best", {}).get("wave")
        if win and win != cur_wave and body.get("confidence") in ("alta", "media"):
            w, c = body["wave"][win], body["wave"].get(cur_wave)
            wave = win
            why.append("olas (%s): Hs rmse %.2f m vs %s de %s, sesgo %s, %d h, %s" % (
                body["confidence"], w["hs_rmse"], f(c["hs_rmse"]) if c else "—", cur_wave,
                f(w["hs_bias"], pct=True), w["n"], " ".join(body["buoys"])))
        wb = body.get("wind") or {}
        ww = wb.get("best")
        if ww and ww != cur_wind and wb.get("confidence") in ("alta", "media"):
            w, c = wb["models"][ww], wb["models"].get(cur_wind)
            wind = ww
            why.append("viento (%s): rmse %.2f m/s vs %s de %s, sesgo %s, %d h, %s" % (
                wb["confidence"], w["spd_rmse"], f(c["spd_rmse"]) if c else "—", cur_wind,
                f(w["spd_bias"], pct=True), w["n"], " ".join(wb["stations"])))
        if why:
            rows.append([r.code, wave, wind, "validación %s: %s" % (body["to"], "; ".join(why))])
    return rows


def _other(body, win):
    """The best wave model that cannot be chosen (MFWAM, EWAM) when it beats the chosen one."""
    w = body["wave"].get(win) if win else None
    for m, s in body["wave"].items():
        if m in ELIGIBLE or not score.qualifies(s):
            continue
        if w is None or s["hs_rmse"] < w["hs_rmse"]:
            return "%s %s" % (L_(m), f(s["hs_rmse"]))
        return ""
    return ""


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
    return "| %s%s | %s | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        r.code, tag, "<br>".join("%s (%.0f km)" % (b, body["per_buoy"][b]["km"]) for b in body["buoys"]),
        L_(name), flag, shown["n"], f(shown["hs_rmse"]), f(shown["hs_bias"], pct=True), f(shown["hs_si"]),
        f(shown["tp_bias"], 1) + {"mean": "ᵐ", "primary": "ᵖ"}.get(shown.get("tp_type"), ""), f(shown["dir_mae"], 0),
        L_(r.current[0]), f(cur.get("hs_rmse")), _other(body, win) or "—", body["confidence"])


def _wind_row(body, info):
    r = info["region"]
    wb = body["wind"]
    win = wb.get("best")
    cur = wb.get("models", {}).get(wb["current"], {})
    shown = wb["models"].get(win) if win else (cur or next(iter(wb["models"].values())))
    tag = " (fija)" if r.fixed else ""
    flag = " ⇐" if win and win != wb["current"] and not r.fixed and wb.get("confidence") in ("alta", "media") else ""

    def st(sid):
        p = wb["per_station"][sid]
        return "%s (%.0f km, %s)" % (sid, p["km"], ("%.0f m" % p["z"]) if p.get("z") is not None else "z ?")
    return "| %s%s | %s | %s%s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        r.code, tag, "<br>".join(st(s) for s in wb["stations"]), L_(win or "ninguno"), flag, shown["n"],
        f(shown["spd_rmse"]), f(shown["spd_bias"], pct=True), f(shown["spd_bias_ms"], 1), f(shown["dir_mae"], 0),
        f(cur.get("spd_rmse")), f(cur.get("spd_bias"), pct=True), wb.get("confidence", "—"))


def _count(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return sorted(out.items(), key=lambda kv: (-kv[1], kv[0]))


def markdown(results, window, status, checks, used, twins, wchecks=None, wtwins=()):
    from tools.lib import seeds
    countries = seeds.countries()
    wchecks = wchecks or {}
    withb = [(b, i) for b, i in results if b["buoys"]]
    without = [(b, i) for b, i in results if not b["buoys"]]
    withw = [(b, i) for b, i in results if b.get("wind", {}).get("stations")]
    by_src = {}
    for b, _ in withb:
        for s in {x.split(":")[0] for x in b["buoys"]}:
            by_src[s] = by_src.get(s, 0) + 1
    wby_src = {}
    for b, _ in withw:
        for s in {x.split(":")[0] for x in b["wind"]["stations"]}:
            wby_src[s] = wby_src.get(s, 0) + 1
    wins = _count(b.get("best", {}).get("wave", "ninguno") for b, _ in withb)
    conf = dict(_count(b["confidence"] for b, _ in withb))
    wwins = _count(b["wind"].get("best", "ninguno") for b, _ in withw)
    wconf = dict(_count(b["wind"].get("confidence", "baja") for b, _ in withw))
    sugg = suggestions(results)
    n_wave = sum(1 for row in sugg for b, i in results if b["region"] == row[0] and row[1] != i["region"].current[0])
    n_wind = sum(1 for row in sugg for b, i in results if b["region"] == row[0] and row[2] != (
        i["region"].current[1] if len(i["region"].current) > 1 else DEFAULT_WIND))
    zs = {}
    for b, i in withw:
        for sid in b["wind"]["stations"]:
            zs[sid] = b["wind"]["per_station"][sid].get("z")
    with_z = [z for z in zs.values() if z is not None]
    el = ", ".join(L_(m) for m in ELIGIBLE)
    L = ["# Validación de los modelos de olas y viento", "",
         "Ventana: **%s a %s** (UTC), hora a hora. Generado el %s por `validate/run.py` (ver `validate/README.md`)."
         % (window[0], window[1], time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())), "",
         "**Olas.** Cada región se compara con hasta 3 boyas a menos de %d km de alguno de sus picos (la más cercana primero). "
         "Todos los modelos se miden sobre las mismas horas. Se elige sólo entre los modelos que dan **período pico** "
         "(el reloj muestra el período y puntúa las horas con él): %s (GFS-Wave 0,16° sólo entre 15°S y 52,5°N). "
         "MFWAM y DWD EWAM sólo dan período medio en Open-Meteo: se miden para informar y no se eligen. "
         "El mejor es el de menor `hs_rmse` con |sesgo| ≤ %d %% (empates de %.2f m: menor error de período pico `tp_mae`, "
         "después menor error de dirección). La confianza mira las horas (≥ %d alta, ≥ %d media), cuánto "
         "peor es el modelo de hoy (≥ %d %% alta, ≥ %d %% media), que la mayoría de las boyas coincida y que la boya "
         "más cercana esté a ≤ %d km (alta). Sólo se sugiere cambiar con confianza alta o media; las regiones sin boyas "
         "siguen con la regla por defecto (GFS-Wave 0,16° en su dominio, si no 0,25°)."
         % (MATCH_KM, el, score.BIAS_MAX * 100, score.TIE_M, score.N_ALTA, score.N_MEDIA, score.MARGIN_ALTA * 100,
            score.MARGIN_MEDIA * 100, score.FAR_KM), "",
         "**Viento.** Igual, con hasta 3 estaciones (boyas y estaciones costeras) a menos de %d km: viento a 10 m "
         "de los modelos de Open-Meteo contra la estación llevada a 10 m. El mejor es el de menor rmse de velocidad con "
         "|sesgo| ≤ %d %%; se cambia de `%s` sólo con confianza alta o media (mismas reglas)." %
         (MATCH_KM, score.WIND_BIAS_MAX * 100, DEFAULT_WIND), "",
         "## Resumen", "",
         "- Regiones: **%d**; con boyas de olas: **%d**; con estaciones de viento: **%d**." % (len(results), len(withb), len(withw)),
         "- Olas, regiones con boyas por fuente: %s." % ", ".join("%s %d" % (SOURCES[s][0], n) for s, n in sorted(by_src.items(), key=lambda x: -x[1])),
         "- Olas, mejor modelo elegible: %s." % ", ".join("%s %d" % (L_(m), n) for m, n in wins),
         "- Olas, confianza: %s." % ", ".join("%s %d" % (k, conf.get(k, 0)) for k in ("alta", "media", "baja")),
         "- Viento, regiones con estaciones por fuente: %s." % (", ".join(
             "%s %d" % (SOURCES[s][0], n) for s, n in sorted(wby_src.items(), key=lambda x: -x[1])) or "ninguna"),
         "- Viento, mejor modelo: %s." % (", ".join("%s %d" % (L_(m), n) for m, n in wwins) or "—"),
         "- Viento, confianza: %s." % ", ".join("%s %d" % (k, wconf.get(k, 0)) for k in ("alta", "media", "baja")),
         "- Sugerencias (`models-suggested.csv`): **%d** regiones (%d cambian olas, %d cambian viento)." % (len(sugg), n_wave, n_wind)]
    by_api = used.get("by_api", {})
    L.append("- Open-Meteo: %d pedidos, %d ubicaciones, ~%.0f llamadas ponderadas como las cuenta la API (%s; límite "
             "gratuito 10.000/día)." % (used["requests"], used["locations"], used["weight"], "; ".join(
                 "%s %d pedidos, %.0f llamadas" % ({"marine": "Marine", "forecast": "Forecast"}.get(a, a), u["requests"], u["weight"])
                 for a, u in sorted(by_api.items())) or "todo de la caché del día"))
    L.append("")
    L += ["## Fuentes", "", "| Fuente | Datos | Licencia | Esta corrida |", "|---|---|---|---|"]
    for s, (name, what, lic) in SOURCES.items():
        L.append("| %s | %s | %s | %s |" % (name, what, lic, status.get(s, "no se pidió")))
    if twins:
        L += ["", "Boyas publicadas por dos fuentes (se usa una): %s." % ", ".join("%s = %s" % (k.id, s.id) for s, k in twins)]
    if wtwins:
        L += ["", "Estaciones de viento repetidas (se usa una): %s." % ", ".join("%s = %s" % (k.id, s.id) for s, k in wtwins)]

    # --- waves ---
    L += ["", "## Olas", "", "### Por país", "", "| País | Regiones con boyas | Gana |", "|---|---|---|"]
    byc = {}
    for b, i in withb:
        byc.setdefault(i["region"].country, []).append(b.get("best", {}).get("wave", "ninguno"))
    for c, ws in sorted(byc.items(), key=lambda x: (-len(x[1]), x[0])):
        L.append("| %s | %d | %s |" % (countries.get(c, {}).get("name_es", c), len(ws),
                                       ", ".join("%s %d" % (L_(m), n) for m, n in _count(ws))))
    L += ["", "### Regiones con boyas", "",
          "Métricas del mejor modelo elegible (o del de hoy si ninguno califica). `Tp` es el sesgo de período del modelo "
          "contra el período pico de la boya: ECMWF WAM con su `wave_peak_period`; ᵖ: GFS-Wave no da período pico en "
          "Open-Meteo y se usa su `wave_period`, que es el del sistema de olas principal (se comporta como un pico). "
          "*No elegible*: MFWAM o EWAM cuando tienen menos error de altura que el elegido (sólo dan período medio, "
          "así que no se usan). ⇐ = se sugiere cambiar (en `models-suggested.csv`). Las regiones fijas (issue #7) se "
          "validan sólo para informar.", "",
          "| Región | Boyas | Mejor | n | rmse m | sesgo | SI | Tp s | dir ° | Hoy | rmse hoy | No elegible | Confianza |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b, i in withb:
        L.append(_row(b, i))
    L += ["", "### Regiones sin boyas (%d)" % len(without), "",
          "Dispersión entre modelos de la altura de ola en el pico central de la región (desvío / media, promedio de "
          "las horas). Más de %.2f ⇒ confianza baja: los modelos no coinciden y conviene buscar boyas."
          % score.SPREAD_BAJA, "",
          "| Región | Dispersión | Hs media por modelo (m) | Confianza |", "|---|---|---|---|"]
    for b, i in sorted(without, key=lambda x: -(x[0].get("spread", {}).get("hs") or 0)):
        sp = b.get("spread", {})
        L.append("| %s | %s | %s | %s |" % (b["region"], f(sp.get("hs")),
                                            ", ".join("%s %.2f" % (L_(m), v) for m, v in sp.get("mean_hs", {}).items()),
                                            b["confidence"]))
    L += ["", "### Control de convenciones por fuente", "",
          "Promedios ponderados por horas sobre todas las boyas de cada fuente. `Tp` = modelo − período pico de la boya; "
          "`Tm` = `wave_period` del modelo − período medio de la boya (NDBC APD, CDIP Ta, AODN WPFM, MI EnergyPeriod: no son "
          "el mismo momento espectral); `dir` = error medio absoluto de dirección (de dónde vienen); `sesgo dir` = media "
          "circular de modelo − boya (cerca de ±180° indicaría una boya en convención \"hacia\").", "",
          "| Fuente | Modelo | horas | Tp s | Tm s | dir ° | sesgo dir ° |", "|---|---|---|---|---|---|---|"]
    for s, ms in sorted(checks.items()):
        for m, c in sorted(ms.items()):
            L.append("| %s | %s | %d | %s | %s | %s | %s |" % (SOURCES.get(s, (s,))[0], L_(m), c["n"], f(c["tp_bias"], 1),
                                                             f(c["tm_bias"], 1), f(c["dir_mae"], 0), f(c.get("dir_bias"), 0)))

    # --- wind ---
    L += ["", "## Viento", "",
          "Modelos de Open-Meteo (API Forecast, `wind_speed_10m` y `wind_direction_10m` en m/s) y dónde se comparan: %s. "
          "En las boyas se pide la celda de mar más cercana (`cell_selection=sea`); en las estaciones en tierra, la más "
          "cercana (`nearest`)."
          % "; ".join("%s (`%s`): %s" % (L_(m), m, WIND_WHERE.get(m, "")) for m in WIND_DOMAINS), ""]
    if REFUSED:
        L += ["Modelos que la API no aceptó y quedaron afuera: %s." % ", ".join("`%s` (%s)" % (m, str(r)[:80]) for m, r in REFUSED.items()), ""]
    L += ["Observaciones: NDBC (`WSPD` m/s, promedio de 8 min en boyas y 2 min en C-MAN; `WDIR`), Marine Institute "
          "(boyas M2–M6, convertido a m/s según la unidad del dataset) y AODN si su parquet trae viento. La velocidad se "
          "lleva a 10 m con la ley de potencia U₁₀ = U(z)·(10/z)^%.2f (sobre el mar, casi neutral) cuando la estación "
          "publica la altura del anemómetro (NDBC: página de la estación): **%d** de **%d** estaciones usadas tienen altura "
          "(%s); sin altura se usa como viene (una boya de ~4 m subestima ~10 %% el viento a 10 m). La dirección se compara "
          "con viento observado ≥ %.0f m/s." % (
              WIND_EXP, len(with_z), len(zs), ("de %.1f a %.1f m" % (min(with_z), max(with_z))) if with_z else "—",
              score.WIND_DIR_MIN), "",
          "| Región | Estaciones (distancia, altura) | Mejor | n | rmse m/s | sesgo | sesgo m/s | dir ° | rmse hoy | sesgo hoy | Confianza |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for b, i in withw:
        if b["wind"].get("models"):
            L.append(_wind_row(b, i))
    nowind = [b["region"] for b, _ in results if not b.get("wind", {}).get("stations")]
    L += ["", "Sin estaciones de viento (%d regiones, siguen con `%s`): %s." % (len(nowind), DEFAULT_WIND, " ".join(nowind)), "",
          "### Control de unidades y convenciones por fuente", "",
          "Promedios ponderados por horas sobre todas las estaciones de cada fuente: velocidad media observada (a 10 m), "
          "sesgo y rmse de velocidad del modelo, error medio absoluto de dirección y sesgo circular (cerca de ±180° "
          "indicaría una convención \"hacia\"; un sesgo de velocidad cerca de ×1,9 o ×0,5, nudos por m/s).", "",
          "| Fuente | Modelo | horas | obs m/s | sesgo m/s | rmse m/s | dir ° | sesgo dir ° |", "|---|---|---|---|---|---|---|---|"]
    for s, ms in sorted(wchecks.items()):
        for m, c in sorted(ms.items(), key=lambda kv: (kv[1]["rmse"] or 99)):
            L.append("| %s | %s | %d | %s | %s | %s | %s | %s |" % (SOURCES.get(s, (s,))[0], L_(m), c["n"], f(c["obs_spd"], 1),
                                                                  f(c["bias_ms"], 2), f(c["rmse"], 2), f(c["dir_mae"], 0),
                                                                  f(c["dir_bias"], 0)))
    L += ["", "## Próximos pasos", "",
          "- Fuentes con cuenta o clave que faltan: **Copernicus Marine** (In Situ TAC: boyas de Europa, Brasil, Sudáfrica, "
          "Japón, con viento), **CANDHIS** (Francia), **Channel Coastal Observatory** (Inglaterra), **Puertos del Estado** "
          "(España), **IH Portugal**, **SIMCOSTA/PNBOIA** directo (Brasil), **CMEMS** para Uruguay y Argentina.",
          "- Los meses cambian el ganador (verano/invierno, swell/viento): mirar varias corridas mensuales antes de pasar "
          "una sugerencia a `models.csv` por PR.",
          "- Las boyas lejos de la costa validan el modelo en mar abierto, no el punto de olas del pico: preferir boyas "
          "someras (CDIP, AODN, MI) cuando haya.",
          "- Viento: casi todas las estaciones son de EE. UU. (NDBC) e Irlanda; las costeras miden efectos locales (muelles, "
          "edificios, brisa) y las que todos los modelos erran por más de 35 %% se descartan. Fuera de ahí sigue `%s`."
          % DEFAULT_WIND, ""]
    return "\n".join(L)
