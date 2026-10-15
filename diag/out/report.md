# Validación de los modelos de olas y viento

Ventana: **2026-09-15 a 2026-10-15** (UTC), hora a hora. Generado el 2026-10-15 04:08 UTC por `validate/run.py` (ver `validate/README.md`).

**Olas.** Cada región se compara con hasta 3 boyas a menos de 150 km de alguno de sus picos (la más cercana primero). Todos los modelos se miden sobre las mismas horas. Se elige sólo entre los modelos que dan **período pico** (el reloj muestra el período y puntúa las horas con él): ECMWF WAM, GFS-Wave 0,16°, GFS-Wave 0,25° (GFS-Wave 0,16° sólo entre 15°S y 52,5°N). MFWAM y DWD EWAM sólo dan período medio en Open-Meteo: se miden para informar y no se eligen. El mejor es el de menor `hs_rmse` con |sesgo| ≤ 15 % (empates de 0.01 m: menor error de período pico `tp_mae`, después menor error de dirección). La confianza mira las horas (≥ 480 alta, ≥ 240 media), cuánto peor es el modelo de hoy (≥ 10 % alta, ≥ 5 % media), que la mayoría de las boyas coincida y que la boya más cercana esté a ≤ 100 km (alta). Sólo se sugiere cambiar con confianza alta o media; las regiones sin boyas siguen con la regla por defecto (GFS-Wave 0,16° en su dominio, si no 0,25°).

**Viento.** Igual, con hasta 3 estaciones (boyas y estaciones costeras) a menos de 150 km: viento a 10 m de los modelos de Open-Meteo contra la estación llevada a 10 m. El mejor es el de menor rmse de velocidad con |sesgo| ≤ 20 %; se cambia de `gfs_seamless` sólo con confianza alta o media (mismas reglas).

## Resumen

- Regiones: **6**; con boyas de olas: **6**; con estaciones de viento: **5**.
- Olas, regiones con boyas por fuente: Copernicus Marine In Situ 6.
- Olas, mejor modelo elegible: ECMWF WAM 6.
- Olas, confianza: alta 5, media 1, baja 0.
- Viento, regiones con estaciones por fuente: Copernicus Marine In Situ 5.
- Viento, mejor modelo: Météo-France 4, ICON 1.
- Viento, confianza: alta 1, media 4, baja 0.
- Sugerencias (`models-suggested.csv`): **6** regiones (6 cambian olas, 5 cambian viento).
- Open-Meteo: 12 pedidos, 35 ubicaciones, ~97 llamadas ponderadas como las cuenta la API (Forecast 9 pedidos, 15 llamadas; Marine 3 pedidos, 82 llamadas; límite gratuito 10.000/día).

## Fuentes

| Fuente | Datos | Licencia | Esta corrida |
|---|---|---|---|
| CDIP | Coastal Data Information Program, Scripps Institution of Oceanography (UCSD); ERDDAP `wave_agg` | uso libre, se agradece el crédito a CDIP | no se pidió |
| AODN / IMOS | Boyas de olas de Australia (IMOS, estados y universidades), parquet `wave_buoy_realtime_nonqc` | CC BY 4.0 | no se pidió |
| Marine Institute | Irish Wave Buoy Network, ERDDAP `IWaveBNetwork30Min`, y boyas meteorológicas M2–M6 (`IWBNetwork`, con viento) | CC BY 4.0 | 4 estaciones, 4 con ≥ 72 h de Hs, 4 con ≥ 72 h de viento |
| NOAA NDBC | National Data Buoy Center, `realtime2` (boyas, C-MAN y estaciones costeras con viento; incluye socios: PNBOIA, Canadá, etc.) | dominio público | no se pidió |
| Copernicus Marine In Situ | `INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030`, archivos diarios `latest`: boyas de Europa (CANDHIS, Puertos del Estado, Cefas…), Marruecos, Canarias y del GTS; necesita cuenta (secretos `COPERNICUSMARINE_SERVICE_USERNAME` y `_PASSWORD`) | licencia de Copernicus Marine (libre, con crédito) | 34 estaciones, 32 con ≥ 72 h de Hs, 5 con ≥ 72 h de viento |

## Olas

### Por país

| País | Regiones con boyas | Gana |
|---|---|---|
| España | 2 | ECMWF WAM 2 |
| Francia | 2 | ECMWF WAM 2 |
| Reino Unido | 1 | ECMWF WAM 1 |
| Portugal | 1 | ECMWF WAM 1 |

### Regiones con boyas

Métricas del mejor modelo elegible (o del de hoy si ninguno califica). `Tp` es el sesgo de período del modelo contra el período pico de la boya: ECMWF WAM con su `wave_peak_period`; ᵖ: GFS-Wave no da período pico en Open-Meteo y se usa su `wave_period`, que es el del sistema de olas principal (se comporta como un pico). *No elegible*: MFWAM o EWAM cuando tienen menos error de altura que el elegido (sólo dan período medio, así que no se usan). ⇐ = se sugiere cambiar (en `models-suggested.csv`). Las regiones fijas (issue #7) se validan sólo para informar.

| Región | Boyas | Mejor | n | rmse m | sesgo | SI | Tp s | dir ° | Hoy | rmse hoy | No elegible | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-HOS | cmems:6200066 (12 km)<br>cmems:6200079 (25 km)<br>cmems:Donostia-buoy (43 km) | ECMWF WAM ⇐ | 1839 | 0.22 | -0 % | 0.14 | 0.0 | 9 | GFS-Wave 0,16° | 0.35 | MFWAM 0.21 | alta |
| FR-GIR | cmems:6200064 (14 km)<br>cmems:6200066 (32 km)<br>cmems:6200024 (131 km) | ECMWF WAM ⇐ | 1838 | 0.24 | +6 % | 0.14 | -0.0 | 8 | GFS-Wave 0,16° | 0.33 | — | alta |
| ES-PV | cmems:Bilbao-coast-buoy (5 km)<br>cmems:Bilbao-station (5 km)<br>cmems:PasaiaII-coast-buoy (8 km) | ECMWF WAM ⇐ | 2142 | 0.26 | -7 % | 0.16 | 0.5 | 8 | GFS-Wave 0,16° | 0.43 | — | alta |
| ES-CAN | cmems:Bilbao-coast-buoy (28 km)<br>cmems:Bilbao-station (32 km)<br>cmems:6200024 (40 km) | ECMWF WAM ⇐ | 2167 | 0.27 | -4 % | 0.16 | 0.4 | 8 | GFS-Wave 0,16° | 0.44 | — | alta |
| PT-CEN | cmems:6200199 (7 km)<br>cmems:Leixoes-coast-buoy (48 km)<br>cmems:6200084 (144 km) | ECMWF WAM ⇐ | 2124 | 0.23 | -2 % | 0.12 | -0.1 | 7 | GFS-Wave 0,16° | 0.45 | — | alta |
| GB-CON | cmems:6201001 (1 km)<br>cmems:6200107 (28 km)<br>cmems:6201024 (31 km) | ECMWF WAM ⇐ | 2143 | 0.29 | +9 % | 0.16 | -0.4 | 15 | GFS-Wave 0,16° | 0.31 | — | media |

### Regiones sin boyas (0)

Dispersión entre modelos de la altura de ola en el pico central de la región (desvío / media, promedio de las horas). Más de 0.30 ⇒ confianza baja: los modelos no coinciden y conviene buscar boyas.

| Región | Dispersión | Hs media por modelo (m) | Confianza |
|---|---|---|---|

### Control de convenciones por fuente

Promedios ponderados por horas sobre todas las boyas de cada fuente. `Tp` = modelo − período pico de la boya; `Tm` = `wave_period` del modelo − período medio de la boya (NDBC APD, CDIP Ta, AODN WPFM, MI EnergyPeriod: no son el mismo momento espectral); `dir` = error medio absoluto de dirección (de dónde vienen); `sesgo dir` = media circular de modelo − boya (cerca de ±180° indicaría una boya en convención "hacia").

| Fuente | Modelo | horas | Tp s | Tm s | dir ° | sesgo dir ° |
|---|---|---|---|---|---|---|
| Copernicus Marine In Situ | DWD EWAM | 12253 | -1.4 | 2.1 | 14 | 4 |
| Copernicus Marine In Situ | ECMWF WAM | 12253 | 0.1 | 2.1 | 14 | 4 |
| Copernicus Marine In Situ | MFWAM | 12253 | -1.3 | 2.3 | 14 | 4 |
| Copernicus Marine In Situ | GFS-Wave 0,16° | 12253 | 0.0 | 3.5 | 13 | 2 |
| Copernicus Marine In Situ | GFS-Wave 0,25° | 4291 | 0.1 | 4.2 | 8 | -2 |

## Viento

Modelos de Open-Meteo (API Forecast, `wind_speed_10m` y `wind_direction_10m` en m/s) y dónde se comparan: GFS (`gfs_seamless`): todas partes (hoy); ECMWF IFS (`ecmwf_ifs`): todas partes; Météo-France (`meteofrance_seamless`): Europa (ARPEGE Europa, AROME); UKMO (`ukmo_seamless`): Islas Británicas (UKV); GEM (`cmc_gem_seamless`): Norteamérica (RDPS, HRDPS); JMA (`jma_seamless`): Japón, Corea y Taiwán (MSM); BOM ACCESS-G (`bom_access_global`): Australia, Nueva Zelanda y Pacífico sudoeste; ICON (`icon_seamless`): Europa (ICON-EU, D2). En las boyas se pide la celda de mar más cercana (`cell_selection=sea`); en las estaciones en tierra, la más cercana (`nearest`).

Observaciones: NDBC (`WSPD` m/s, promedio de 8 min en boyas y 2 min en C-MAN; `WDIR`), Marine Institute (boyas M2–M6, convertido a m/s según la unidad del dataset) y AODN si su parquet trae viento. La velocidad se lleva a 10 m con la ley de potencia U₁₀ = U(z)·(10/z)^0.11 (sobre el mar, casi neutral) cuando la estación publica la altura del anemómetro (NDBC: página de la estación): **0** de **4** estaciones usadas tienen altura (—); sin altura se usa como viene (una boya de ~4 m subestima ~10 % el viento a 10 m). La dirección se compara con viento observado ≥ 3 m/s.

| Región | Estaciones (distancia, altura) | Mejor | n | rmse m/s | sesgo | sesgo m/s | dir ° | rmse hoy | sesgo hoy | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|
| FR-HOS | cmems:6200024 (125 km, z ?)<br>cmems:Bilbao-station (131 km, z ?) | Météo-France ⇐ | 1418 | 1.69 | +17 % | 0.6 | 19 | 1.86 | +7 % | media |
| FR-GIR | cmems:6200024 (131 km, z ?)<br>cmems:Bilbao-station (141 km, z ?) | Météo-France ⇐ | 1418 | 1.69 | +17 % | 0.6 | 19 | 1.86 | +7 % | media |
| ES-PV | cmems:Bilbao-station (5 km, z ?)<br>cmems:6200024 (26 km, z ?) | Météo-France ⇐ | 1418 | 1.69 | +17 % | 0.6 | 19 | 1.86 | +7 % | media |
| ES-CAN | cmems:Bilbao-station (32 km, z ?)<br>cmems:6200024 (40 km, z ?) | Météo-France ⇐ | 1418 | 1.69 | +17 % | 0.6 | 19 | 1.86 | +7 % | media |
| PT-CEN | cmems:6200199 (7 km, z ?)<br>cmems:6200084 (144 km, z ?) | ICON ⇐ | 1437 | 1.68 | +15 % | 0.7 | 10 | 2.39 | +36 % | alta |

Sin estaciones de viento (1 regiones, siguen con `gfs_seamless`): GB-CON.

### Control de unidades y convenciones por fuente

Promedios ponderados por horas sobre todas las estaciones de cada fuente: velocidad media observada (a 10 m), sesgo y rmse de velocidad del modelo, error medio absoluto de dirección y sesgo circular (cerca de ±180° indicaría una convención "hacia"; un sesgo de velocidad cerca de ×1,9 o ×0,5, nudos por m/s).

| Fuente | Modelo | horas | obs m/s | sesgo m/s | rmse m/s | dir ° | sesgo dir ° |
|---|---|---|---|---|---|---|---|
| Copernicus Marine In Situ | Météo-France | 7109 | 3.8 | 0.73 | 1.80 | 17 | 0 |
| Copernicus Marine In Situ | ECMWF IFS | 7109 | 3.8 | 0.74 | 1.90 | 22 | 6 |
| Copernicus Marine In Situ | ICON | 7109 | 3.8 | -0.05 | 1.92 | 20 | 1 |
| Copernicus Marine In Situ | GFS | 7109 | 3.8 | 0.54 | 1.98 | 25 | 8 |

## Próximos pasos

- Fuentes con cuenta o clave que faltan: **Copernicus Marine** (In Situ TAC: boyas de Europa, Brasil, Sudáfrica, Japón, con viento), **CANDHIS** (Francia), **Channel Coastal Observatory** (Inglaterra), **Puertos del Estado** (España), **IH Portugal**, **SIMCOSTA/PNBOIA** directo (Brasil), **CMEMS** para Uruguay y Argentina.
- Los meses cambian el ganador (verano/invierno, swell/viento): mirar varias corridas mensuales antes de pasar una sugerencia a `models.csv` por PR.
- Las boyas lejos de la costa validan el modelo en mar abierto, no el punto de olas del pico: preferir boyas someras (CDIP, AODN, MI) cuando haya.
- Viento: casi todas las estaciones son de EE. UU. (NDBC) e Irlanda; las costeras miden efectos locales (muelles, edificios, brisa) y las que todos los modelos erran por más de 35 % se descartan. Fuera de ahí sigue `gfs_seamless`.
