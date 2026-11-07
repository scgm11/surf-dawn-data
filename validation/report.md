# Validación de los modelos de olas y viento

Ventana: **2026-10-08 a 2026-11-07** (UTC), hora a hora. Generado el 2026-11-07 11:25 UTC por `validate/run.py` (ver `validate/README.md`).

**Olas.** Cada región se compara con hasta 3 boyas a menos de 150 km de alguno de sus picos (la más cercana primero). Todos los modelos se miden sobre las mismas horas. Se elige sólo entre los modelos que dan **período pico** (el reloj muestra el período y puntúa las horas con él): ECMWF WAM, GFS-Wave 0,16°, GFS-Wave 0,25° (GFS-Wave 0,16° sólo entre 15°S y 52,5°N). MFWAM y DWD EWAM sólo dan período medio en Open-Meteo: se miden para informar y no se eligen. El mejor es el de menor `hs_rmse` con |sesgo| ≤ 15 % (empates de 0.01 m: menor error de período pico `tp_mae`, después menor error de dirección). La confianza mira las horas (≥ 480 alta, ≥ 240 media), cuánto peor es el modelo de hoy (≥ 10 % alta, ≥ 5 % media), que la mayoría de las boyas coincida y que la boya más cercana esté a ≤ 100 km (alta). Sólo se sugiere cambiar con confianza alta o media; las regiones sin boyas siguen con la regla por defecto (GFS-Wave 0,16° en su dominio, si no 0,25°).

**Viento.** Igual, con hasta 3 estaciones (boyas y estaciones costeras) a menos de 150 km: viento a 10 m de los modelos de Open-Meteo contra la estación llevada a 10 m. El mejor es el de menor rmse de velocidad con |sesgo| ≤ 20 %; se cambia de `gfs_seamless` sólo con confianza alta o media (mismas reglas).

## Resumen

- Regiones: **213**; con boyas de olas: **77**; con estaciones de viento: **48**.
- Olas, regiones con boyas por fuente: Copernicus Marine In Situ 46, CDIP 21, NOAA NDBC 13, AODN / IMOS 13, Marine Institute 4.
- Olas, mejor modelo elegible: ECMWF WAM 57, GFS-Wave 0,25° 11, GFS-Wave 0,16° 6, ninguno 3.
- Olas, confianza: alta 54, media 3, baja 20.
- Viento, regiones con estaciones por fuente: Copernicus Marine In Situ 27, NOAA NDBC 23, Marine Institute 4.
- Viento, mejor modelo: GFS 17, Météo-France 11, GEM 7, ECMWF IFS 7, UKMO 3, ICON 2, JMA 1.
- Viento, confianza: alta 28, media 11, baja 9.
- Sugerencias (`models-suggested.csv`): **40** regiones (37 cambian olas, 23 cambian viento).
- Open-Meteo: 0 pedidos, 0 ubicaciones, ~0 llamadas ponderadas como las cuenta la API (todo de la caché del día; límite gratuito 10.000/día).

## Fuentes

| Fuente | Datos | Licencia | Esta corrida |
|---|---|---|---|
| CDIP | Coastal Data Information Program, Scripps Institution of Oceanography (UCSD); ERDDAP `wave_agg` | uso libre, se agradece el crédito a CDIP | 82 estaciones, 81 con ≥ 72 h de Hs, 0 con ≥ 72 h de viento |
| AODN / IMOS | Boyas de olas de Australia (IMOS, estados y universidades), parquet `wave_buoy_realtime_nonqc` | CC BY 4.0 | 77 estaciones, 46 con ≥ 72 h de Hs, 0 con ≥ 72 h de viento |
| Marine Institute | Irish Wave Buoy Network, ERDDAP `IWaveBNetwork30Min`, y boyas meteorológicas M2–M6 (`IWBNetwork`, con viento) | CC BY 4.0 | 4 estaciones, 4 con ≥ 72 h de Hs, 4 con ≥ 72 h de viento |
| NOAA NDBC | National Data Buoy Center, `realtime2` (boyas, C-MAN y estaciones costeras con viento; incluye socios: PNBOIA, Canadá, etc.) | dominio público | 482 estaciones, 126 con ≥ 72 h de Hs, 291 con ≥ 72 h de viento |
| Copernicus Marine In Situ | `INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030`, archivos diarios `latest`: boyas de Europa (CANDHIS, Puertos del Estado, Cefas…), Marruecos, Canarias y del GTS; necesita cuenta (secretos `COPERNICUSMARINE_SERVICE_USERNAME` y `_PASSWORD`) | licencia de Copernicus Marine (libre, con crédito) | 260 estaciones, 243 con ≥ 72 h de Hs, 59 con ≥ 72 h de viento |

Boyas publicadas por dos fuentes (se usa una): cdip:132 = ndbc:41112, cdip:240 = ndbc:44087, cdip:192 = ndbc:44095, cdip:147 = ndbc:44099, cdip:036 = ndbc:46211, cdip:029 = ndbc:46214, cdip:076 = ndbc:46215, cdip:067 = ndbc:46219, cdip:028 = ndbc:46221, cdip:092 = ndbc:46222, cdip:045 = ndbc:46224, cdip:100 = ndbc:46225, cdip:139 = ndbc:46229, cdip:191 = ndbc:46232, cdip:179 = ndbc:46248, cdip:213 = ndbc:46253, cdip:215 = ndbc:46256, cdip:220 = ndbc:46258, cdip:284 = ndbc:46285, cdip:285 = ndbc:46286, cdip:106 = ndbc:51201, cdip:098 = ndbc:51202, cdip:188 = ndbc:51206, cdip:143 = ndbc:41113, cdip:134 = ndbc:41114, cdip:194 = ndbc:41117, cdip:250 = ndbc:41120, cdip:168 = ndbc:46244, cdip:153 = ndbc:46266, cdip:189 = ndbc:51209, cdip:252 = ndbc:42092, cdip:260 = ndbc:44085, cdip:154 = ndbc:44097, cdip:160 = ndbc:44098, cdip:142 = ndbc:46237, cdip:201 = ndbc:46254, cdip:262 = ndbc:46274, cdip:238 = ndbc:51212, cdip:150 = ndbc:41110, cdip:265 = ndbc:41122, cdip:279 = ndbc:42354, cdip:243 = ndbc:44086, cdip:171 = ndbc:44088, cdip:209 = ndbc:44091, cdip:430 = ndbc:44100, cdip:094 = ndbc:46213, cdip:156 = ndbc:46236, cdip:270 = ndbc:46278, cdip:233 = ndbc:51211, cdip:249 = ndbc:41121, cdip:071 = ndbc:46218, cdip:162 = ndbc:46243, cdip:248 = ndbc:46267, cdip:271 = ndbc:46277, cdip:433 = ndbc:44056, cdip:201 = ndbc:LJPC1, cdip:273 = ndbc:51214, cdip:171 = ndbc:44014, cdip:103 = ndbc:46268, cdip:221 = ndbc:44090, cdip:217 = ndbc:41159, cdip:264 = ndbc:46275, cdip:263 = ndbc:44084, cdip:222 = ndbc:46259, cdip:181 = ndbc:41115, cdip:203 = ndbc:46251, ndbc:42033 = ndbc:42034, cmems:Europlatform2 = cmems:Europlatform3, cmems:IJmuidenMunitiestort = cmems:IJmuidenMunitiestort2, cmems:K13a = cmems:K13a3, cmems:LichteilandGoeree1 = cmems:LichteilandGoeree2, cmems:Schouwenbank = cmems:Schouwenbank2, cmems:MaeslantkeringZeezijdeNoordMeetpaal = cmems:MaeslantkeringZeezijdeZuidMeetpaal, cmems:K13a = cmems:K13a2, cmems:4400258 = cmems:44258, cmems:4600207 = cmems:46207, cmems:4600304 = cmems:46304, cmems:4600131 = cmems:46131.

Estaciones de viento repetidas (se usa una): ndbc:CPMW1 = ndbc:CPNW1, ndbc:44080 = ndbc:FSKM2, ndbc:LJPC1 = ndbc:LJAC1, ndbc:MZXC1 = ndbc:UPBC1, ndbc:NAXR1 = ndbc:PTCR1, ndbc:DILA1 = ndbc:DPHA1, ndbc:42034 = ndbc:42033, cmems:4400258 = cmems:44258, cmems:4600207 = cmems:46207, cmems:4600304 = cmems:46304, cmems:4600131 = cmems:46131.

## Olas

### Por país

| País | Regiones con boyas | Gana |
|---|---|---|
| Estados Unidos | 20 | ECMWF WAM 14, GFS-Wave 0,16° 3, GFS-Wave 0,25° 2, ninguno 1 |
| Australia | 17 | ECMWF WAM 10, GFS-Wave 0,25° 6, ninguno 1 |
| Reino Unido | 7 | ECMWF WAM 7 |
| Portugal | 7 | ECMWF WAM 6, ninguno 1 |
| España | 6 | ECMWF WAM 6 |
| Francia | 5 | ECMWF WAM 3, GFS-Wave 0,16° 1, GFS-Wave 0,25° 1 |
| Canadá | 2 | ECMWF WAM 1, GFS-Wave 0,16° 1 |
| Irlanda | 2 | ECMWF WAM 2 |
| Puerto Rico | 2 | ECMWF WAM 2 |
| Alemania | 1 | ECMWF WAM 1 |
| Dinamarca | 1 | ECMWF WAM 1 |
| Guadalupe | 1 | ECMWF WAM 1 |
| Islandia | 1 | GFS-Wave 0,25° 1 |
| Italia | 1 | ECMWF WAM 1 |
| Corea del Sur | 1 | ECMWF WAM 1 |
| Martinica | 1 | GFS-Wave 0,25° 1 |
| México | 1 | GFS-Wave 0,16° 1 |
| Países Bajos | 1 | ECMWF WAM 1 |

### Regiones con boyas

Métricas del mejor modelo elegible (o del de hoy si ninguno califica). `Tp` es el sesgo de período del modelo contra el período pico de la boya: ECMWF WAM con su `wave_peak_period`; ᵖ: GFS-Wave no da período pico en Open-Meteo y se usa su `wave_period`, que es el del sistema de olas principal (se comporta como un pico). *No elegible*: MFWAM o EWAM cuando tienen menos error de altura que el elegido (sólo dan período medio, así que no se usan). ⇐ = se sugiere cambiar (en `models-suggested.csv`). Las regiones fijas (issue #7) se validan sólo para informar.

| Región | Boyas | Mejor | n | rmse m | sesgo | SI | Tp s | dir ° | Hoy | rmse hoy | No elegible | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MX-BCN | cdip:191 (28 km)<br>cdip:201 (40 km)<br>cdip:220 (43 km) | GFS-Wave 0,16° | 2163 | 0.30 | -12 % | 0.23 | 1.3ᵖ | 35 | ECMWF WAM | 0.27 | MFWAM 0.25 | baja |
| PR-NW | cdip:181 (1 km)<br>cdip:249 (38 km)<br>ndbc:41053 (102 km) | ECMWF WAM | 2022 | 0.17 | +3 % | 0.15 | 0.1 | 9 | GFS-Wave 0,16° | 0.17 | — | baja |
| PR-N | ndbc:41053 (5 km)<br>cdip:249 (19 km)<br>cdip:181 (81 km) | ECMWF WAM | 2022 | 0.17 | +3 % | 0.15 | 0.1 | 9 | GFS-Wave 0,16° | 0.17 | — | baja |
| GP-ALL | cmems:4100134 (17 km) | ECMWF WAM | 206 | 0.09 | -1 % | 0.06 | — | — | GFS-Wave 0,16° | 0.32 | — | baja |
| MQ-ALL | cmems:4100098 (1 km)<br>cmems:4100099 (43 km) | GFS-Wave 0,25° | 1354 | 0.17 | -10 % | 0.12 | —ᵖ | — | GFS-Wave 0,16° | 0.21 | MFWAM 0.15 | baja |
| US-CA-SD | cdip:262 (1 km)<br>cdip:153 (1 km)<br>cdip:201 (1 km) | GFS-Wave 0,16° | 2160 | 0.21 | -3 % | 0.24 | 1.1ᵖ | 50 | GFS-Wave 0,16° | 0.21 | — | baja |
| US-CA-OC | cdip:284 (1 km)<br>cdip:271 (8 km)<br>cdip:264 (11 km) | ECMWF WAM | 2120 | 0.16 | +4 % | 0.14 | -0.5 | 13 | ECMWF WAM | 0.16 | — | alta |
| US-CA-LA | cdip:103 (2 km)<br>cdip:028 (20 km)<br>ndbc:46025 (34 km) | ECMWF WAM | 2138 | 0.15 | +9 % | 0.12 | 0.1 | 21 | ECMWF WAM | 0.15 | — | alta |
| US-CA-SB | cdip:071 (26 km)<br>ndbc:46025 (34 km)<br>cdip:028 (37 km) | ECMWF WAM | 2133 | 0.21 | +7 % | 0.12 | -0.3 | 28 | ECMWF WAM | 0.21 | MFWAM 0.18 | alta |
| US-CA-CEN | cdip:076 (6 km)<br>cdip:157 (19 km)<br>cmems:46011 (28 km) | ECMWF WAM | 1820 | 0.35 | +2 % | 0.18 | -0.7 | 25 | ECMWF WAM | 0.35 | MFWAM 0.33 | alta |
| US-CA-SC | cdip:156 (14 km)<br>cdip:157 (26 km)<br>ndbc:46042 (30 km) | ECMWF WAM | 1830 | 0.33 | -3 % | 0.16 | -0.2 | 19 | ECMWF WAM | 0.33 | — | alta |
| US-CA-SF | cdip:142 (9 km)<br>ndbc:46026 (22 km)<br>cmems:46012 (36 km) | GFS-Wave 0,25° | 2132 | 0.38 | -2 % | 0.23 | 1.0ᵖ | 19 | ECMWF WAM | 0.44 | — | baja |
| US-CA-NOR | cdip:168 (16 km)<br>ndbc:46014 (18 km)<br>ndbc:46022 (24 km) | ECMWF WAM | 2120 | 0.23 | -2 % | 0.10 | -0.5 | 17 | ECMWF WAM | 0.23 | MFWAM 0.22 | alta |
| US-PNW | cdip:270 (7 km)<br>cdip:036 (10 km)<br>cdip:162 (10 km) | ECMWF WAM | 2159 | 0.28 | +0 % | 0.15 | -0.1 | 11 | ECMWF WAM | 0.28 | MFWAM 0.25 | alta |
| US-GULF | ndbc:42033 (5 km)<br>cdip:252 (21 km)<br>ndbc:42035 (35 km) | ECMWF WAM | 1496 | 0.15 | -8 % | 0.12 | -0.4 | 15 | ECMWF WAM | 0.15 | — | alta |
| US-FL | cdip:265 (2 km)<br>cdip:143 (6 km)<br>cdip:134 (13 km) | ninguno | 2162 | 0.39 | +17 % | 0.27 | -0.1ᵖ | 19 | GFS-Wave 0,16° | 0.39 | — | baja |
| US-FL-PAN | ndbc:42357 (20 km)<br>ndbc:42012 (24 km)<br>cdip:256 (42 km) | GFS-Wave 0,16° | 1936 | 0.21 | -9 % | 0.24 | -0.4ᵖ | 28 | ECMWF WAM | 0.26 | — | baja |
| US-SE | cdip:433 (5 km)<br>cdip:150 (10 km)<br>ndbc:SSBN7 (13 km) | GFS-Wave 0,16° ⇐ | 2018 | 0.18 | -6 % | 0.14 | -0.1ᵖ | 10 | GFS-Wave 0,25° | 0.21 | — | alta |
| US-SC-GA | ndbc:41067 (12 km)<br>ndbc:41065 (16 km)<br>ndbc:41076 (29 km) | ECMWF WAM | 1946 | 0.24 | -1 % | 0.20 | -1.5 | 25 | GFS-Wave 0,16° | 0.24 | — | baja |
| US-MID | cdip:263 (1 km)<br>cdip:147 (23 km)<br>cdip:430 (60 km) | GFS-Wave 0,25° | 2085 | 0.23 | -7 % | 0.16 | -0.4ᵖ | 14 | GFS-Wave 0,25° | 0.23 | — | baja |
| US-NE | ndbc:44007 (7 km)<br>ndbc:44029 (10 km)<br>ndbc:44030 (14 km) | ECMWF WAM | 1608 | 0.20 | -4 % | 0.22 | 0.4 | 24 | ECMWF WAM | 0.20 | — | alta |
| US-HI-OAN | cdip:106 (6 km) | ECMWF WAM ⇐ | 721 | 0.21 | +6 % | 0.10 | -0.5 | 29 | GFS-Wave 0,16° | 0.38 | MFWAM 0.21 | alta |
| US-HI-OAS | cdip:238 (4 km)<br>cdip:233 (10 km) | ECMWF WAM | 1439 | 0.25 | -1 % | 0.22 | 0.7 | 25 | ECMWF WAM | 0.25 | — | alta |
| US-HI-MAU | cdip:187 (10 km)<br>cdip:233 (138 km)<br>cdip:188 (148 km) | ECMWF WAM | 1581 | 0.19 | +3 % | 0.12 | 0.6 | 25 | ECMWF WAM | 0.19 | — | alta |
| US-HI-BIG | cdip:187 (116 km) | ECMWF WAM | 140 | 0.15 | +3 % | 0.09 | 0.4 | 40 | ECMWF WAM | 0.15 | — | baja |
| CA-BC-VI | ndbc:46087 (31 km)<br>cmems:4600207 (114 km) | ECMWF WAM | 1253 | 0.30 | -0 % | 0.13 | 0.3 | 19 | ECMWF WAM | 0.30 | MFWAM 0.30 | baja |
| CA-NS | cmems:4400258 (12 km) | GFS-Wave 0,16° | 713 | 0.20 | +5 % | 0.17 | 0.0ᵖ | 23 | GFS-Wave 0,16° | 0.20 | — | alta |
| AU-QLD-SC | cmems:55045 (5 km)<br>cmems:55030 (8 km)<br>cmems:55027 (17 km) | ECMWF WAM ⇐ | 1646 | 0.18 | +12 % | 0.15 | -0.9 | 21 | GFS-Wave 0,25° | 0.23 | MFWAM 0.14 | alta |
| AU-QLD-GC | cmems:55050 (1 km)<br>cmems:55036 (2 km)<br>cmems:55037 (3 km) | GFS-Wave 0,25° | 1671 | 0.24 | +10 % | 0.23 | -0.1ᵖ | 27 | GFS-Wave 0,25° | 0.24 | — | alta |
| AU-NSW-NR | cmems:55037 (4 km)<br>cmems:55017 (9 km)<br>cmems:55057 (11 km) | ECMWF WAM ⇐ | 1524 | 0.24 | +7 % | 0.17 | -0.5 | 24 | GFS-Wave 0,25° | 0.32 | — | alta |
| AU-NSW-MN | cmems:55018 (14 km)<br>cmems:55019 (14 km)<br>aodn:wooli (17 km) | ECMWF WAM ⇐ | 1549 | 0.28 | +10 % | 0.16 | -0.3 | 20 | GFS-Wave 0,25° | 0.34 | — | alta |
| AU-NSW-NC | aodn:collaroy-narrabeen (20 km)<br>cmems:55024 (24 km)<br>cmems:55022 (106 km) | ECMWF WAM | 1487 | 0.47 | +7 % | 0.33 | -0.9 | 28 | GFS-Wave 0,25° | 0.50 | MFWAM 0.42 | baja |
| AU-NSW-SYD | aodn:collaroy-narrabeen (1 km)<br>cmems:55024 (8 km)<br>cmems:55022 (30 km) | ECMWF WAM | 1487 | 0.47 | +7 % | 0.33 | -0.9 | 28 | GFS-Wave 0,25° | 0.50 | MFWAM 0.42 | baja |
| AU-NSW-SC | aodn:bengello (3 km)<br>cmems:55014 (9 km)<br>cmems:55022 (12 km) | GFS-Wave 0,25° | 1419 | 0.30 | +4 % | 0.24 | -0.8ᵖ | 29 | GFS-Wave 0,25° | 0.30 | — | alta |
| AU-VIC-SC | aodn:apollo-bay (32 km)<br>aodn:inverloch (114 km)<br>aodn:bob (146 km) | GFS-Wave 0,25° | 2184 | 0.30 | -7 % | 0.15 | 0.5ᵖ | 17 | GFS-Wave 0,25° | 0.30 | — | baja |
| AU-VIC-PI | aodn:inverloch (44 km)<br>aodn:apollo-bay (97 km)<br>aodn:wilsons-prom (147 km) | GFS-Wave 0,25° | 2184 | 0.30 | -11 % | 0.16 | 0.5ᵖ | 20 | GFS-Wave 0,25° | 0.30 | — | alta |
| AU-VIC-W | aodn:port-fairy (3 km)<br>aodn:cape-bridgewater (11 km)<br>aodn:apollo-bay (16 km) | ECMWF WAM ⇐ | 2185 | 0.33 | +13 % | 0.11 | 0.1 | 20 | GFS-Wave 0,25° | 0.50 | — | alta |
| AU-TAS | aodn:storm-bay (24 km) | ECMWF WAM ⇐ | 697 | 0.22 | -10 % | 0.20 | -1.8 | 53 | GFS-Wave 0,25° | 0.34 | — | alta |
| AU-SA | cmems:55040 (51 km) | ECMWF WAM | 217 | 0.23 | +1 % | 0.09 | 0.1 | 21 | ECMWF WAM | 0.23 | — | baja |
| AU-SA-EYR | aodn:ceduna (68 km) | ECMWF WAM ⇐ | 731 | 0.19 | -8 % | 0.10 | 0.2 | 7 | GFS-Wave 0,25° | 1.28 | — | alta |
| AU-WA-MR | aodn:bunbury (43 km) | GFS-Wave 0,25° | 728 | 0.16 | -1 % | 0.11 | 1.0ᵖ | 8 | GFS-Wave 0,25° | 0.16 | — | alta |
| AU-WA-PER | aodn:hillarys (9 km)<br>aodn:jurien-bay-inshore (144 km)<br>aodn:jurien-bay-offshore (146 km) | GFS-Wave 0,25° | 2188 | 0.32 | -6 % | 0.14 | 0.6ᵖ | 11 | GFS-Wave 0,25° | 0.32 | MFWAM 0.29 | alta |
| AU-WA-NW | aodn:dongara-inshore (51 km)<br>aodn:dongara-offshore (51 km) | ninguno | 1452 | 0.39 | +16 % | 0.16 | 0.1ᵖ | 10 | GFS-Wave 0,25° | 0.39 | — | baja |
| AU-WA-GAS | aodn:coral-bay-0-2 (85 km) | ECMWF WAM ⇐ | 731 | 0.23 | +0 % | 0.13 | 0.1 | 24 | GFS-Wave 0,25° | 0.46 | — | alta |
| KR-ALL | cmems:2200310 (33 km)<br>cmems:2200107 (40 km)<br>cmems:2200187 (57 km) | ECMWF WAM ⇐ | 2033 | 0.23 | -4 % | 0.18 | -0.6 | 28 | GFS-Wave 0,16° | 0.31 | — | alta |
| FR-PBA | cmems:6200079 (1 km)<br>cmems:6200066 (6 km)<br>cmems:PasaiaII-coast-buoy (9 km) | ECMWF WAM ⇐ | 1937 | 0.26 | -2 % | 0.14 | 0.1 | 4 | GFS-Wave 0,16° | 0.40 | — | alta |
| FR-HOS | cmems:6200066 (12 km)<br>cmems:6200079 (25 km)<br>cmems:Donostia-buoy (43 km) | ECMWF WAM ⇐ | 1937 | 0.28 | -0 % | 0.15 | -0.0 | 10 | GFS-Wave 0,16° | 0.53 | — | alta |
| FR-GIR | cmems:6200064 (14 km)<br>cmems:6200066 (32 km)<br>cmems:6200024 (131 km) | ECMWF WAM ⇐ | 1938 | 0.25 | +4 % | 0.13 | -0.1 | 9 | GFS-Wave 0,16° | 0.44 | — | alta |
| FR-VEN | cmems:6200067 (11 km)<br>cmems:6200251 (44 km)<br>cmems:6200078 (66 km) | GFS-Wave 0,25° ⇐ | 1731 | 0.24 | -2 % | 0.19 | —ᵖ | — | GFS-Wave 0,16° | 0.28 | — | alta |
| FR-BRE | cmems:6200069 (17 km)<br>cmems:6200074 (32 km)<br>cmems:6200078 (44 km) | GFS-Wave 0,16° | 1788 | 0.37 | -3 % | 0.22 | —ᵖ | — | GFS-Wave 0,16° | 0.37 | — | baja |
| ES-PV | cmems:Bilbao-coast-buoy (5 km)<br>cmems:Bilbao-station (5 km)<br>cmems:PasaiaII-coast-buoy (8 km) | ECMWF WAM ⇐ | 2094 | 0.38 | -9 % | 0.19 | 0.5 | 7 | GFS-Wave 0,16° | 0.56 | — | alta |
| ES-CAN | cmems:Bilbao-coast-buoy (28 km)<br>cmems:Bilbao-station (32 km)<br>cmems:6200024 (40 km) | ECMWF WAM ⇐ | 2094 | 0.38 | -7 % | 0.18 | 0.5 | 9 | GFS-Wave 0,16° | 0.60 | — | alta |
| ES-AST | cmems:Gijon-coast-buoy (8 km)<br>cmems:6200025 (22 km)<br>cmems:6200082 (84 km) | ECMWF WAM ⇐ | 2129 | 0.28 | -4 % | 0.11 | -0.1 | 13 | GFS-Wave 0,16° | 0.55 | — | alta |
| ES-GAL | cmems:6201070 (3 km)<br>cmems:6200083 (33 km)<br>cmems:6200084 (50 km) | ECMWF WAM ⇐ | 2160 | 0.32 | -5 % | 0.12 | -0.1 | 11 | GFS-Wave 0,16° | 0.49 | — | alta |
| ES-AND | cmems:6200085 (55 km) | ECMWF WAM ⇐ | 720 | 0.14 | -12 % | 0.15 | 0.1 | 30 | GFS-Wave 0,16° | 0.19 | — | alta |
| ES-CN-W | cmems:1300130 (11 km) | ECMWF WAM ⇐ | 720 | 0.13 | +4 % | 0.09 | -0.1 | 12 | GFS-Wave 0,16° | 0.26 | MFWAM 0.12 | alta |
| PT-NOR | cmems:Leixoes-coast-buoy (19 km)<br>cmems:6200084 (55 km) | ECMWF WAM ⇐ | 1400 | 0.24 | -2 % | 0.11 | -0.2 | 10 | GFS-Wave 0,16° | 0.43 | — | alta |
| PT-CEN | cmems:6200199 (7 km)<br>cmems:Leixoes-coast-buoy (48 km)<br>cmems:6200084 (144 km) | ECMWF WAM ⇐ | 2087 | 0.24 | -3 % | 0.11 | -0.1 | 9 | GFS-Wave 0,16° | 0.48 | — | alta |
| PT-PEN | cmems:6200199 (14 km)<br>cmems:Sines-coast-buoy (140 km) | ECMWF WAM ⇐ | 1365 | 0.22 | -6 % | 0.12 | 0.1 | 7 | GFS-Wave 0,16° | 0.45 | MFWAM 0.21 | alta |
| PT-ERI | cmems:6200199 (63 km)<br>cmems:Sines-coast-buoy (118 km) | ECMWF WAM ⇐ | 1365 | 0.22 | -6 % | 0.12 | 0.1 | 7 | GFS-Wave 0,16° | 0.45 | MFWAM 0.21 | alta |
| PT-LIS | cmems:Sines-coast-buoy (67 km)<br>cmems:6200199 (84 km) | ECMWF WAM ⇐ | 1365 | 0.22 | -6 % | 0.12 | 0.1 | 7 | GFS-Wave 0,16° | 0.45 | MFWAM 0.21 | alta |
| PT-ALG | cmems:Sines-coast-buoy (12 km)<br>cmems:Faro-coast-buoy (88 km) | ECMWF WAM ⇐ | 993 | 0.19 | -9 % | 0.13 | -0.2 | 14 | GFS-Wave 0,16° | 0.24 | MFWAM 0.18 | alta |
| PT-AZO | cmems:6202400 (82 km) | ninguno | 697 | 0.81 | +36 % | 0.34 | —ᵖ | 91 | GFS-Wave 0,16° | 0.81 | — | baja |
| GB-CON | cmems:6201001 (1 km)<br>cmems:6200107 (28 km)<br>cmems:6201024 (31 km) | ECMWF WAM ⇐ | 2154 | 0.43 | +10 % | 0.20 | -0.8 | 25 | GFS-Wave 0,16° | 0.47 | — | media |
| GB-DEV | cmems:6201562 (76 km)<br>cmems:6200103 (78 km)<br>cmems:6201001 (91 km) | ECMWF WAM ⇐ | 2157 | 0.36 | -0 % | 0.17 | -0.6 | 20 | GFS-Wave 0,16° | 0.44 | — | alta |
| GB-SOU | cmems:6201008 (1 km)<br>cmems:6200290 (13 km)<br>cmems:6201009 (14 km) | ECMWF WAM ⇐ | 2150 | 0.34 | +11 % | 0.35 | -2.6 | 33 | GFS-Wave 0,16° | 0.36 | DWD EWAM 0.30 | media |
| GB-WAL | cmems:6201562 (24 km)<br>mi:m5 (99 km)<br>cmems:6201006 (112 km) | ECMWF WAM ⇐ | 2159 | 0.27 | -5 % | 0.13 | -1.3 | 22 | GFS-Wave 0,16° | 0.37 | — | alta |
| GB-SCO | cmems:6200045 (21 km)<br>cmems:6204816 (26 km)<br>cmems:6200047 (48 km) | ECMWF WAM ⇐ | 2163 | 0.24 | -0 % | 0.14 | -0.6 | 22 | GFS-Wave 0,25° | 0.43 | — | alta |
| GB-NE | cmems:6201047 (1 km)<br>cmems:6201046 (2 km)<br>cmems:6201045 (6 km) | ECMWF WAM ⇐ | 2037 | 0.25 | +1 % | 0.22 | -1.8 | 34 | GFS-Wave 0,25° | 0.28 | DWD EWAM 0.24 | alta |
| GB-NIR | mi:m2 (86 km)<br>cmems:6200047 (98 km) | ECMWF WAM | 1442 | 0.43 | -7 % | 0.16 | -0.2 | 30 | ECMWF WAM | 0.43 | — | alta |
| IE-SW | mi:m3 (102 km) | ECMWF WAM | 721 | 0.30 | -2 % | 0.08 | -0.6 | 10 | ECMWF WAM | 0.30 | MFWAM 0.30 | media |
| IE-SE | mi:m3 (58 km)<br>cmems:IL4-Splaugh (60 km)<br>mi:m5 (60 km) | ECMWF WAM ⇐ | 2161 | 0.32 | -8 % | 0.11 | -0.8 | 11 | GFS-Wave 0,16° | 0.46 | — | alta |
| DK-ALL | cmems:Fjaltring (12 km)<br>cmems:Nymindegab (64 km)<br>cmems:Fanoebugt (115 km) | ECMWF WAM ⇐ | 2137 | 0.22 | +3 % | 0.16 | -1.3 | 25 | GFS-Wave 0,25° | 0.34 | — | alta |
| NL-ALL | cmems:DomburgerRassen (9 km)<br>cmems:WielingenNoord (15 km)<br>cmems:Deurlo (18 km) | ECMWF WAM ⇐ | 1539 | 0.16 | +1 % | 0.17 | -0.2 | 18 | GFS-Wave 0,16° | 0.40 | — | alta |
| DE-ALL | cmems:6202602 (13 km)<br>cmems:6201067 (34 km)<br>cmems:Fanoebugt (44 km) | ECMWF WAM ⇐ | 2119 | 0.28 | +12 % | 0.17 | -1.8 | 32 | GFS-Wave 0,25° | 0.34 | — | alta |
| IT-ALL | cmems:6100219 (27 km)<br>cmems:6100216 (53 km)<br>cmems:6100214 (111 km) | ECMWF WAM ⇐ | 1816 | 0.19 | -5 % | 0.22 | -0.1 | 26 | GFS-Wave 0,16° | 0.29 | — | alta |
| IS-ALL | cmems:Thorlakshafnardufl (5 km)<br>cmems:Grindavikurdufl (12 km)<br>cmems:Surtseyjardufl (65 km) | GFS-Wave 0,25° | 1921 | 0.53 | +1 % | 0.17 | —ᵖ | — | GFS-Wave 0,25° | 0.53 | MFWAM 0.46 | alta |

### Regiones sin boyas (136)

Dispersión entre modelos de la altura de ola en el pico central de la región (desvío / media, promedio de las horas). Más de 0.30 ⇒ confianza baja: los modelos no coinciden y conviene buscar boyas.

| Región | Dispersión | Hs media por modelo (m) | Confianza |
|---|---|---|---|
| VE-ALL | 0.46 | GFS-Wave 0,16° 0.42, GFS-Wave 0,25° 0.68, MFWAM 0.85, ECMWF WAM 0.22 | baja |
| FJ-MAM | 0.37 | GFS-Wave 0,25° 0.47, MFWAM 1.31, ECMWF WAM 1.17 | baja |
| EC-COS | 0.37 | GFS-Wave 0,16° 0.67, GFS-Wave 0,25° 0.91, MFWAM 1.23, ECMWF WAM 0.43 | baja |
| ES-CN-E | 0.32 | GFS-Wave 0,16° 1.23, GFS-Wave 0,25° 0.83, MFWAM 1.38, ECMWF WAM 0.60 | baja |
| ZA-WC-CPT | 0.30 | GFS-Wave 0,25° 1.84, MFWAM 1.62, ECMWF WAM 0.84 | media |
| ID-JAV-W | 0.30 | GFS-Wave 0,16° 1.26, MFWAM 0.83, ECMWF WAM 0.61 | media |
| PF-ISL | 0.29 | GFS-Wave 0,25° 1.90, MFWAM 2.09, ECMWF WAM 0.99 | media |
| CR-OSA | 0.23 | GFS-Wave 0,16° 1.13, GFS-Wave 0,25° 0.77, MFWAM 1.39, ECMWF WAM 0.91 | media |
| BS-ALL | 0.22 | GFS-Wave 0,16° 1.47, GFS-Wave 0,25° 1.29, MFWAM 0.91, ECMWF WAM 0.87 | media |
| BR-SC-NOR | 0.22 | GFS-Wave 0,25° 0.76, MFWAM 0.52, ECMWF WAM 0.91 | media |
| TO-ALL | 0.21 | GFS-Wave 0,25° 1.61, MFWAM 1.80, ECMWF WAM 1.10 | media |
| PF-TAH | 0.21 | GFS-Wave 0,25° 1.29, MFWAM 2.14, ECMWF WAM 1.73 | media |
| BR-RJ | 0.21 | GFS-Wave 0,25° 0.88, MFWAM 1.32, ECMWF WAM 0.88 | media |
| NZ-BOP | 0.21 | GFS-Wave 0,25° 0.73, MFWAM 0.56, ECMWF WAM 0.45 | media |
| MX-NAY | 0.20 | GFS-Wave 0,16° 0.51, MFWAM 0.76, ECMWF WAM 0.78 | media |
| NO-S | 0.19 | GFS-Wave 0,25° 1.69, MFWAM 1.21, ECMWF WAM 1.17, DWD EWAM 1.77 | media |
| CN-HAI | 0.19 | GFS-Wave 0,16° 1.03, GFS-Wave 0,25° 1.04, MFWAM 0.65, ECMWF WAM 1.11 | media |
| VN-ALL | 0.19 | GFS-Wave 0,16° 0.77, MFWAM 0.84, ECMWF WAM 0.54 | media |
| JP-IZU | 0.19 | GFS-Wave 0,16° 1.09, GFS-Wave 0,25° 1.57, MFWAM 1.70, ECMWF WAM 1.74 | media |
| PH-SIA | 0.18 | GFS-Wave 0,16° 1.21, GFS-Wave 0,25° 1.16, MFWAM 0.73, ECMWF WAM 1.13 | media |
| MZ-INH | 0.18 | GFS-Wave 0,25° 0.96, MFWAM 1.07, ECMWF WAM 1.43 | media |
| MX-CAR | 0.18 | GFS-Wave 0,16° 0.55, GFS-Wave 0,25° 0.38, MFWAM 0.44, ECMWF WAM 0.49 | media |
| NI-NW | 0.17 | GFS-Wave 0,16° 1.13, GFS-Wave 0,25° 1.23, MFWAM 0.84, ECMWF WAM 1.36 | media |
| PE-NOR | 0.17 | GFS-Wave 0,16° 0.99, GFS-Wave 0,25° 1.47, MFWAM 1.35, ECMWF WAM 1.05 | media |
| PA-PAC | 0.17 | GFS-Wave 0,16° 0.81, MFWAM 1.24, ECMWF WAM 1.11 | media |
| MV-NMA | 0.17 | GFS-Wave 0,16° 0.89, GFS-Wave 0,25° 0.68, MFWAM 0.89, ECMWF WAM 1.07 | media |
| BR-SP | 0.17 | GFS-Wave 0,25° 0.85, MFWAM 1.27, ECMWF WAM 1.05 | media |
| TW-E | 0.16 | GFS-Wave 0,16° 1.44, GFS-Wave 0,25° 1.94, MFWAM 2.05, ECMWF WAM 2.17 | media |
| PA-BDT | 0.15 | GFS-Wave 0,16° 0.76, GFS-Wave 0,25° 0.75, MFWAM 0.55, ECMWF WAM 0.57 | media |
| TT-ALL | 0.15 | GFS-Wave 0,16° 0.95, GFS-Wave 0,25° 1.02, MFWAM 1.01, ECMWF WAM 0.68 | media |
| MV-CEN | 0.15 | GFS-Wave 0,16° 0.87, GFS-Wave 0,25° 0.74, MFWAM 0.97, ECMWF WAM 1.09 | media |
| CO-PAC | 0.15 | GFS-Wave 0,16° 0.70, GFS-Wave 0,25° 0.97, MFWAM 0.81, ECMWF WAM 0.69 | media |
| MV-SOU | 0.15 | GFS-Wave 0,16° 0.99, GFS-Wave 0,25° 0.85, MFWAM 1.25, ECMWF WAM 1.13 | media |
| ID-ROT | 0.14 | GFS-Wave 0,16° 0.94, GFS-Wave 0,25° 0.97, MFWAM 1.25, ECMWF WAM 0.92 | media |
| NZ-GIS | 0.14 | GFS-Wave 0,25° 1.29, MFWAM 1.45, ECMWF WAM 1.72 | media |
| IT-SAR | 0.14 | GFS-Wave 0,16° 0.85, GFS-Wave 0,25° 0.94, MFWAM 1.04, ECMWF WAM 1.06, DWD EWAM 0.91 | media |
| UY-CAN | 0.14 | GFS-Wave 0,25° 0.93, MFWAM 0.76, ECMWF WAM 0.73 | media |
| CO-CAR | 0.13 | GFS-Wave 0,16° 0.85, MFWAM 1.00, ECMWF WAM 0.78 | media |
| LK-E | 0.13 | GFS-Wave 0,16° 1.08, GFS-Wave 0,25° 1.34, MFWAM 0.98, ECMWF WAM 1.24 | media |
| CV-ALL | 0.13 | GFS-Wave 0,16° 1.03, GFS-Wave 0,25° 0.95, MFWAM 1.19, ECMWF WAM 0.87 | media |
| MU-ALL | 0.13 | GFS-Wave 0,25° 1.23, MFWAM 1.65, ECMWF WAM 1.42 | media |
| RE-ALL | 0.13 | GFS-Wave 0,25° 1.36, MFWAM 1.47, ECMWF WAM 1.11 | media |
| CR-PAC | 0.12 | GFS-Wave 0,16° 1.12, GFS-Wave 0,25° 1.01, MFWAM 1.37, ECMWF WAM 1.28 | media |
| ID-BAL-E | 0.12 | GFS-Wave 0,16° 1.15, GFS-Wave 0,25° 1.50, MFWAM 1.16, ECMWF WAM 1.37 | media |
| UY-MAL | 0.12 | GFS-Wave 0,25° 1.36, MFWAM 1.11, ECMWF WAM 1.46 | media |
| MX-BCS-N | 0.12 | GFS-Wave 0,16° 1.07, GFS-Wave 0,25° 1.07, MFWAM 1.37, ECMWF WAM 1.25 | media |
| NZ-AKL | 0.12 | GFS-Wave 0,25° 1.83, MFWAM 1.89, ECMWF WAM 1.45 | media |
| ID-SBW | 0.12 | GFS-Wave 0,16° 1.21, MFWAM 1.48, ECMWF WAM 1.18 | media |
| IN-E | 0.12 | GFS-Wave 0,16° 0.80, GFS-Wave 0,25° 0.86, MFWAM 0.64, ECMWF WAM 0.78 | media |
| MA-TAG | 0.12 | GFS-Wave 0,16° 1.15, GFS-Wave 0,25° 1.33, MFWAM 1.53, ECMWF WAM 1.47, DWD EWAM 1.55 | media |
| UY-ROC | 0.12 | GFS-Wave 0,25° 1.52, MFWAM 1.17, ECMWF WAM 1.48 | media |
| IN-W | 0.12 | GFS-Wave 0,16° 0.79, GFS-Wave 0,25° 0.83, MFWAM 1.02, ECMWF WAM 0.95 | media |
| ID-BAL-BUK | 0.12 | GFS-Wave 0,16° 1.69, GFS-Wave 0,25° 1.50, MFWAM 2.00, ECMWF WAM 1.87 | media |
| JP-SHO | 0.11 | GFS-Wave 0,16° 0.84, GFS-Wave 0,25° 0.85, MFWAM 0.90, ECMWF WAM 0.93 | media |
| CL-NOR | 0.11 | GFS-Wave 0,25° 1.30, MFWAM 1.58, ECMWF WAM 1.24 | media |
| EC-GAL | 0.11 | GFS-Wave 0,16° 1.16, GFS-Wave 0,25° 1.33, MFWAM 1.53, ECMWF WAM 1.49 | media |
| NZ-WEL | 0.11 | GFS-Wave 0,25° 1.29, MFWAM 1.18, ECMWF WAM 1.07 | media |
| ID-NIA | 0.11 | GFS-Wave 0,16° 1.28, GFS-Wave 0,25° 1.42, MFWAM 1.68, ECMWF WAM 1.64 | media |
| BR-RJL | 0.11 | GFS-Wave 0,25° 1.15, MFWAM 1.39, ECMWF WAM 1.18 | media |
| CR-NIC | 0.11 | GFS-Wave 0,16° 1.05, GFS-Wave 0,25° 1.09, MFWAM 1.26, ECMWF WAM 1.36 | media |
| SV-ORI | 0.11 | GFS-Wave 0,16° 1.10, GFS-Wave 0,25° 1.06, MFWAM 1.03, ECMWF WAM 1.33 | media |
| JP-KYU | 0.11 | GFS-Wave 0,16° 1.33, GFS-Wave 0,25° 1.46, MFWAM 1.74, ECMWF WAM 1.52 | media |
| JP-CHI | 0.11 | GFS-Wave 0,16° 1.62, GFS-Wave 0,25° 1.80, MFWAM 1.44, ECMWF WAM 1.43 | media |
| VU-ALL | 0.11 | GFS-Wave 0,25° 1.42, MFWAM 1.82, ECMWF WAM 1.73 | media |
| BR-NE-RN | 0.10 | GFS-Wave 0,16° 0.95, GFS-Wave 0,25° 1.26, MFWAM 1.17, ECMWF WAM 1.11 | media |
| AR-BAN | 0.10 | GFS-Wave 0,25° 1.29, MFWAM 1.33, ECMWF WAM 1.07 | media |
| ID-MEN | 0.10 | GFS-Wave 0,16° 1.26, GFS-Wave 0,25° 1.55, MFWAM 1.56, ECMWF WAM 1.62 | media |
| BR-NOR | 0.10 | GFS-Wave 0,16° 1.29, GFS-Wave 0,25° 1.37, MFWAM 1.54, ECMWF WAM 1.18 | media |
| CL-MAU | 0.10 | GFS-Wave 0,25° 1.19, MFWAM 0.97, ECMWF WAM 1.08 | media |
| GH-ALL | 0.10 | GFS-Wave 0,16° 0.86, MFWAM 0.92, ECMWF WAM 1.08 | media |
| MA-S | 0.10 | GFS-Wave 0,16° 1.10, GFS-Wave 0,25° 1.20, MFWAM 1.41, ECMWF WAM 1.28 | media |
| BB-ALL | 0.10 | GFS-Wave 0,16° 0.81, GFS-Wave 0,25° 1.02, MFWAM 0.97, ECMWF WAM 0.92 | media |
| BR-NE-CE | 0.09 | GFS-Wave 0,16° 1.16, GFS-Wave 0,25° 1.16, MFWAM 1.12, ECMWF WAM 0.94 | media |
| WS-ALL | 0.09 | GFS-Wave 0,25° 2.03, MFWAM 2.46, ECMWF WAM 2.50 | media |
| PT-MAD | 0.09 | GFS-Wave 0,16° 0.97, GFS-Wave 0,25° 0.97, MFWAM 1.03, ECMWF WAM 0.85 | media |
| FJ-SOU | 0.09 | GFS-Wave 0,25° 1.25, MFWAM 1.53, ECMWF WAM 1.36 | media |
| MV-SMA | 0.09 | GFS-Wave 0,16° 0.83, GFS-Wave 0,25° 0.84, MFWAM 0.73, ECMWF WAM 0.89 | media |
| DO-ALL | 0.09 | GFS-Wave 0,16° 1.18, GFS-Wave 0,25° 1.08, MFWAM 1.24, ECMWF WAM 1.19 | media |
| PG-ALL | 0.09 | GFS-Wave 0,16° 0.81, GFS-Wave 0,25° 0.87, MFWAM 0.85, ECMWF WAM 0.92 | media |
| JP-SHK | 0.09 | GFS-Wave 0,16° 1.35, GFS-Wave 0,25° 1.49, MFWAM 1.57, ECMWF WAM 1.42 | media |
| BR-RS-SUL | 0.08 | GFS-Wave 0,25° 1.20, MFWAM 1.12, ECMWF WAM 1.35 | media |
| BR-BA | 0.08 | GFS-Wave 0,25° 1.18, MFWAM 1.13, ECMWF WAM 0.97 | media |
| MZ-S | 0.08 | GFS-Wave 0,25° 1.49, MFWAM 1.30, ECMWF WAM 1.25 | media |
| MA-N | 0.08 | GFS-Wave 0,16° 1.37, GFS-Wave 0,25° 1.37, MFWAM 1.53, ECMWF WAM 1.39, DWD EWAM 1.33 | media |
| PH-EAS | 0.08 | GFS-Wave 0,16° 1.18, MFWAM 1.31, ECMWF WAM 1.30 | media |
| IE-NW | 0.08 | GFS-Wave 0,25° 2.40, MFWAM 2.82, ECMWF WAM 2.82, DWD EWAM 2.71 | media |
| NZ-RAG | 0.08 | GFS-Wave 0,25° 1.60, MFWAM 1.74, ECMWF WAM 1.92 | media |
| ZA-KZN-N | 0.08 | GFS-Wave 0,25° 1.54, MFWAM 1.66, ECMWF WAM 1.41 | media |
| MX-BCS | 0.08 | GFS-Wave 0,16° 1.32, GFS-Wave 0,25° 1.33, MFWAM 1.56, ECMWF WAM 1.41 | media |
| BR-ES | 0.08 | GFS-Wave 0,25° 1.04, MFWAM 1.09, ECMWF WAM 0.97 | media |
| CL-SUR | 0.08 | GFS-Wave 0,25° 1.90, MFWAM 1.61, ECMWF WAM 1.81 | media |
| PE-LLB | 0.07 | GFS-Wave 0,16° 1.33, GFS-Wave 0,25° 1.44, MFWAM 1.41, ECMWF WAM 1.59 | media |
| CR-CAR | 0.07 | GFS-Wave 0,16° 0.73, GFS-Wave 0,25° 0.72, MFWAM 0.81, ECMWF WAM 0.76 | media |
| NZ-KAI | 0.07 | GFS-Wave 0,25° 0.99, MFWAM 0.99, ECMWF WAM 0.98 | media |
| PH-LUZ | 0.07 | GFS-Wave 0,16° 0.81, GFS-Wave 0,25° 0.78, MFWAM 0.82, ECMWF WAM 0.83 | media |
| ZA-EC-PE | 0.07 | GFS-Wave 0,25° 2.15, MFWAM 1.84, ECMWF WAM 1.97 | media |
| ID-JAV-E | 0.07 | GFS-Wave 0,16° 1.60, GFS-Wave 0,25° 1.72, MFWAM 1.71, ECMWF WAM 1.87 | media |
| CL-CEN | 0.07 | GFS-Wave 0,25° 1.85, MFWAM 2.13, ECMWF WAM 2.16 | media |
| SN-ALL | 0.07 | GFS-Wave 0,16° 1.34, GFS-Wave 0,25° 1.30, MFWAM 1.33, ECMWF WAM 1.16 | media |
| ID-BAL-W | 0.07 | GFS-Wave 0,16° 1.39, GFS-Wave 0,25° 1.58, MFWAM 1.56, ECMWF WAM 1.47 | media |
| ID-LOM | 0.07 | GFS-Wave 0,16° 1.73, GFS-Wave 0,25° 1.70, MFWAM 1.65, ECMWF WAM 1.91 | media |
| JP-IBA | 0.07 | GFS-Wave 0,16° 1.33, GFS-Wave 0,25° 1.45, MFWAM 1.39, ECMWF WAM 1.36 | media |
| BR-RS | 0.07 | GFS-Wave 0,25° 1.56, MFWAM 1.47, ECMWF WAM 1.70 | media |
| NZ-WC | 0.07 | GFS-Wave 0,25° 1.71, MFWAM 1.76, ECMWF WAM 1.90 | media |
| AR-SUR | 0.07 | GFS-Wave 0,25° 1.02, MFWAM 0.95, ECMWF WAM 0.94 | media |
| TW-NE | 0.07 | GFS-Wave 0,16° 1.85, GFS-Wave 0,25° 1.85, MFWAM 1.73, ECMWF WAM 1.75 | media |
| US-HI-KAU | 0.07 | GFS-Wave 0,16° 1.94, MFWAM 1.99, ECMWF WAM 1.77 | media |
| CR-GUA | 0.07 | GFS-Wave 0,16° 1.30, GFS-Wave 0,25° 1.31, MFWAM 1.36, ECMWF WAM 1.17 | media |
| NI-RIV | 0.07 | GFS-Wave 0,16° 1.01, GFS-Wave 0,25° 1.04, MFWAM 1.14, ECMWF WAM 1.11 | media |
| AR-MDP | 0.07 | GFS-Wave 0,25° 1.25, MFWAM 1.15, ECMWF WAM 1.28 | media |
| BR-SC-SUL | 0.06 | GFS-Wave 0,25° 1.36, MFWAM 1.20, ECMWF WAM 1.23 | media |
| NZ-NTL | 0.06 | GFS-Wave 0,25° 2.16, MFWAM 2.04, ECMWF WAM 1.94 | media |
| ZA-KZN-S | 0.06 | GFS-Wave 0,25° 1.73, MFWAM 1.73, ECMWF WAM 1.90 | media |
| CL-PIC | 0.06 | GFS-Wave 0,25° 1.82, MFWAM 2.01, ECMWF WAM 2.07 | media |
| PE-LIM | 0.06 | GFS-Wave 0,16° 1.77, GFS-Wave 0,25° 1.77, MFWAM 2.01, ECMWF WAM 1.97 | media |
| NZ-OTA | 0.06 | GFS-Wave 0,25° 1.38, MFWAM 1.47, ECMWF WAM 1.42 | media |
| ZA-EC-JB | 0.06 | GFS-Wave 0,25° 2.26, MFWAM 2.27, ECMWF WAM 2.49 | media |
| ZA-KZN-DBN | 0.06 | GFS-Wave 0,25° 1.59, MFWAM 1.61, ECMWF WAM 1.48 | media |
| GT-PAC | 0.06 | GFS-Wave 0,16° 1.26, GFS-Wave 0,25° 1.33, MFWAM 1.44, ECMWF WAM 1.30 | media |
| MX-OAX | 0.06 | GFS-Wave 0,16° 1.45, GFS-Wave 0,25° 1.54, MFWAM 1.51, ECMWF WAM 1.41 | media |
| ZA-WC-GR | 0.06 | GFS-Wave 0,25° 1.94, MFWAM 2.14, ECMWF WAM 2.12 | media |
| MX-PAC | 0.06 | GFS-Wave 0,16° 1.68, MFWAM 1.79, ECMWF WAM 1.63 | media |
| NO-N | 0.06 | GFS-Wave 0,25° 2.39, MFWAM 2.31, ECMWF WAM 2.37 | media |
| BR-SC-FLN | 0.05 | GFS-Wave 0,25° 1.47, MFWAM 1.49, ECMWF WAM 1.61 | media |
| BR-NE-PE | 0.05 | GFS-Wave 0,16° 0.97, GFS-Wave 0,25° 1.03, MFWAM 1.06, ECMWF WAM 0.99 | media |
| ZA-EC-WLD | 0.05 | GFS-Wave 0,25° 1.83, MFWAM 1.90, ECMWF WAM 1.96 | media |
| ID-KRU | 0.05 | GFS-Wave 0,16° 1.74, MFWAM 1.88, ECMWF WAM 1.71 | media |
| LK-S | 0.05 | GFS-Wave 0,16° 1.39, GFS-Wave 0,25° 1.39, MFWAM 1.49, ECMWF WAM 1.44 | media |
| ID-SMB | 0.05 | GFS-Wave 0,16° 1.42, MFWAM 1.38, ECMWF WAM 1.51 | media |
| NA-ERO | 0.05 | GFS-Wave 0,25° 1.19, MFWAM 1.18, ECMWF WAM 1.25 | media |
| MG-ALL | 0.05 | GFS-Wave 0,25° 1.88, MFWAM 1.73, ECMWF WAM 1.78 | media |
| ZA-WC-WCO | 0.05 | GFS-Wave 0,25° 2.01, MFWAM 2.16, ECMWF WAM 2.15 | media |
| SV-LIB | 0.04 | GFS-Wave 0,16° 1.19, MFWAM 1.28, ECMWF WAM 1.28 | media |
| LR-ALL | 0.04 | GFS-Wave 0,16° 0.86, MFWAM 0.86, ECMWF WAM 0.84 | media |
| NZ-TAR | 0.04 | GFS-Wave 0,25° 1.60, MFWAM 1.60, ECMWF WAM 1.58 | media |
| PE-SUR | 0.03 | GFS-Wave 0,25° 1.66, MFWAM 1.77, ECMWF WAM 1.72 | media |

### Control de convenciones por fuente

Promedios ponderados por horas sobre todas las boyas de cada fuente. `Tp` = modelo − período pico de la boya; `Tm` = `wave_period` del modelo − período medio de la boya (NDBC APD, CDIP Ta, AODN WPFM, MI EnergyPeriod: no son el mismo momento espectral); `dir` = error medio absoluto de dirección (de dónde vienen); `sesgo dir` = media circular de modelo − boya (cerca de ±180° indicaría una boya en convención "hacia").

| Fuente | Modelo | horas | Tp s | Tm s | dir ° | sesgo dir ° |
|---|---|---|---|---|---|---|
| AODN / IMOS | ECMWF WAM | 16002 | -0.1 | 2.6 | 21 | 5 |
| AODN / IMOS | MFWAM | 16002 | -2.2 | 2.3 | 20 | 3 |
| AODN / IMOS | GFS-Wave 0,25° | 16002 | -0.2 | 4.3 | 22 | 6 |
| CDIP | ECMWF WAM | 28615 | -0.1 | 2.7 | 19 | 2 |
| CDIP | MFWAM | 26007 | -1.8 | 3.0 | 21 | 0 |
| CDIP | GFS-Wave 0,16° | 28615 | 0.4 | 5.0 | 22 | -8 |
| CDIP | GFS-Wave 0,25° | 18432 | 0.1 | 3.9 | 19 | -1 |
| Copernicus Marine In Situ | DWD EWAM | 47534 | -1.6 | 2.2 | 17 | -1 |
| Copernicus Marine In Situ | ECMWF WAM | 66085 | -0.5 | 1.8 | 21 | 0 |
| Copernicus Marine In Situ | MFWAM | 66085 | -1.4 | 2.2 | 21 | 0 |
| Copernicus Marine In Situ | GFS-Wave 0,16° | 46909 | 0.2 | 3.8 | 19 | 2 |
| Copernicus Marine In Situ | GFS-Wave 0,25° | 53875 | -0.1 | 3.3 | 21 | 1 |
| Marine Institute | DWD EWAM | 1442 | -1.1 | 1.1 | 29 | -9 |
| Marine Institute | ECMWF WAM | 3605 | -0.7 | 1.4 | 18 | -5 |
| Marine Institute | MFWAM | 3605 | -1.6 | 1.7 | 19 | -7 |
| Marine Institute | GFS-Wave 0,16° | 2163 | 0.2 | 3.9 | 32 | -2 |
| Marine Institute | GFS-Wave 0,25° | 3605 | -0.2 | 3.2 | 34 | -5 |
| NOAA NDBC | ECMWF WAM | 12479 | -0.4 | 2.1 | 23 | -5 |
| NOAA NDBC | MFWAM | 11043 | -1.5 | 2.4 | 26 | -6 |
| NOAA NDBC | GFS-Wave 0,16° | 12479 | 0.2 | 4.4 | 20 | -6 |
| NOAA NDBC | GFS-Wave 0,25° | 11779 | 0.1 | 4.0 | 19 | -8 |

## Viento

Modelos de Open-Meteo (API Forecast, `wind_speed_10m` y `wind_direction_10m` en m/s) y dónde se comparan: GFS (`gfs_seamless`): todas partes (hoy); ECMWF IFS (`ecmwf_ifs`): todas partes; Météo-France (`meteofrance_seamless`): Europa (ARPEGE Europa, AROME); UKMO (`ukmo_seamless`): Islas Británicas (UKV); GEM (`cmc_gem_seamless`): Norteamérica (RDPS, HRDPS); JMA (`jma_seamless`): Japón, Corea y Taiwán (MSM); BOM ACCESS-G (`bom_access_global`): Australia, Nueva Zelanda y Pacífico sudoeste; ICON (`icon_seamless`): Europa (ICON-EU, D2). En las boyas se pide la celda de mar más cercana (`cell_selection=sea`); en las estaciones en tierra, la más cercana (`nearest`).

Observaciones: NDBC (`WSPD` m/s, promedio de 8 min en boyas y 2 min en C-MAN; `WDIR`), Marine Institute (boyas M2–M6, convertido a m/s según la unidad del dataset) y AODN si su parquet trae viento. La velocidad se lleva a 10 m con la ley de potencia U₁₀ = U(z)·(10/z)^0.11 (sobre el mar, casi neutral) cuando la estación publica la altura del anemómetro (NDBC: página de la estación): **36** de **68** estaciones usadas tienen altura (de 2.7 a 38.0 m); sin altura se usa como viene (una boya de ~4 m subestima ~10 % el viento a 10 m). La dirección se compara con viento observado ≥ 3 m/s.

| Región | Estaciones (distancia, altura) | Mejor | n | rmse m/s | sesgo | sesgo m/s | dir ° | rmse hoy | sesgo hoy | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|
| MX-BCN | ndbc:LJPC1 (40 km, 20 m)<br>ndbc:46086 (85 km, 3 m) | GFS | 1433 | 1.36 | -2 % | -0.1 | 13 | 1.36 | -2 % | baja |
| PR-NW | ndbc:41053 (102 km, 4 m) | GEM | 721 | 1.68 | +7 % | 0.3 | 21 | 1.68 | +7 % | media |
| PR-N | ndbc:41053 (5 km, 4 m) | GEM | 721 | 1.68 | +7 % | 0.3 | 21 | 1.68 | +7 % | media |
| US-CA-SD | ndbc:LJPC1 (0 km, 20 m)<br>ndbc:46086 (76 km, 3 m) | GFS | 1433 | 1.36 | -2 % | -0.1 | 13 | 1.36 | -2 % | baja |
| US-CA-OC | ndbc:46025 (90 km, 4 m)<br>ndbc:46086 (106 km, 3 m) | GFS | 1431 | 1.21 | -13 % | -0.6 | 11 | 1.21 | -13 % | alta |
| US-CA-LA | ndbc:46025 (34 km, 4 m)<br>ndbc:46069 (127 km, 4 m)<br>ndbc:LJPC1 (133 km, 20 m) | GFS | 2140 | 1.28 | -3 % | -0.1 | 12 | 1.28 | -3 % | alta |
| US-CA-SB | ndbc:46025 (34 km, 4 m)<br>ndbc:46011 (66 km, 4 m)<br>ndbc:46069 (89 km, 4 m) | GFS | 2140 | 1.17 | -8 % | -0.5 | 10 | 1.17 | -8 % | alta |
| US-CA-CEN | cmems:46011 (28 km, z ?)<br>ndbc:46011 (34 km, 4 m)<br>ndbc:46092 (36 km, 4 m) | GFS | 2100 | 1.32 | -4 % | -0.2 | 15 | 1.32 | -4 % | alta |
| US-CA-SC | ndbc:46092 (16 km, 4 m)<br>ndbc:46042 (30 km, 4 m)<br>cmems:46012 (61 km, z ?) | GFS | 2099 | 1.36 | -8 % | -0.4 | 18 | 1.36 | -8 % | media |
| US-CA-SF | ndbc:46026 (22 km, 4 m)<br>cmems:46012 (36 km, z ?)<br>ndbc:46013 (44 km, 4 m) | GFS | 2133 | 1.19 | -7 % | -0.4 | 14 | 1.19 | -7 % | media |
| US-CA-NOR | ndbc:46014 (18 km, 4 m)<br>ndbc:46022 (24 km, 4 m)<br>cmems:46022 (24 km, z ?) | GFS | 2125 | 1.11 | -4 % | -0.2 | 9 | 1.11 | -4 % | alta |
| US-PNW | ndbc:NWPO3 (1 km, 16 m)<br>ndbc:46097 (19 km, 4 m)<br>ndbc:46087 (22 km, 4 m) | GFS | 2113 | 1.29 | -8 % | -0.4 | 14 | 1.29 | -8 % | alta |
| US-GULF | ndbc:ANPT2 (1 km, 14 m)<br>ndbc:42034 (5 km, z ?)<br>ndbc:42043 (23 km, 3 m) | GFS | 1390 | 1.23 | -6 % | -0.3 | 26 | 1.23 | -6 % | alta |
| US-FL | ndbc:SIPF1 (0 km, 11 m)<br>ndbc:LKWF1 (0 km, 12 m)<br>ndbc:41068 (17 km, 3 m) | GFS | 2099 | 1.85 | +0 % | 0.0 | 13 | 1.85 | +0 % | media |
| US-FL-PAN | ndbc:PCBF1 (6 km, 16 m)<br>ndbc:42012 (24 km, 4 m)<br>ndbc:BURL1 (64 km, 38 m) | GFS | 2145 | 1.34 | -5 % | -0.3 | 10 | 1.34 | -5 % | alta |
| US-SE | ndbc:MBNN7 (2 km, 6 m)<br>ndbc:DUKN7 (2 km, 16 m)<br>ndbc:41038 (10 km, 3 m) | ECMWF IFS | 2121 | 1.61 | +5 % | 0.3 | 12 | 1.61 | +5 % | baja |
| US-SC-GA | ndbc:41033 (11 km, 3 m)<br>ndbc:41029 (16 km, 3 m)<br>ndbc:41066 (29 km, 3 m) | GEM | 2146 | 1.72 | -11 % | -0.9 | 11 | 1.79 | -11 % | baja |
| US-MID | ndbc:44009 (31 km, 4 m)<br>ndbc:DUKN7 (62 km, 16 m)<br>ndbc:41082 (112 km, 4 m) | GEM ⇐ | 2147 | 1.22 | -2 % | -0.2 | 10 | 1.35 | -6 % | alta |
| US-NE | ndbc:44007 (7 km, 4 m)<br>ndbc:44029 (10 km, 4 m)<br>ndbc:IOSN3 (11 km, 32 m) | GFS | 1664 | 1.58 | -11 % | -0.7 | 11 | 1.58 | -11 % | baja |
| US-HI-OAN | ndbc:51WH0 (112 km, 3 m) | GEM | 565 | 1.43 | -1 % | -0.1 | 13 | 1.49 | +0 % | baja |
| US-HI-OAS | ndbc:51WH0 (100 km, 3 m) | GEM | 565 | 1.43 | -1 % | -0.1 | 13 | 1.49 | +0 % | baja |
| US-HI-MAU | ndbc:51WH0 (116 km, 3 m) | GEM | 565 | 1.43 | -1 % | -0.1 | 13 | 1.49 | +0 % | baja |
| CA-BC-VI | cmems:46206 (30 km, z ?)<br>ndbc:46087 (31 km, 4 m)<br>ndbc:LAPW1 (70 km, 11 m) | GFS | 2122 | 1.59 | +3 % | 0.1 | 14 | 1.59 | +3 % | alta |
| CA-NS | cmems:4400258 (12 km, z ?) | GFS | 713 | 1.22 | +4 % | 0.3 | 8 | 1.22 | +4 % | alta |
| KR-ALL | cmems:2200310 (33 km, z ?)<br>cmems:2200107 (40 km, z ?)<br>cmems:2200187 (57 km, z ?) | JMA ⇐ | 2038 | 1.84 | +4 % | 0.3 | 19 | 2.02 | +1 % | media |
| FR-PBA | cmems:Bilbao-station (106 km, z ?)<br>cmems:6200024 (106 km, z ?) | Météo-France ⇐ | 1331 | 1.61 | +17 % | 0.7 | 17 | 1.80 | +12 % | media |
| FR-HOS | cmems:6200024 (125 km, z ?)<br>cmems:Bilbao-station (131 km, z ?) | Météo-France ⇐ | 1331 | 1.61 | +17 % | 0.7 | 17 | 1.80 | +12 % | media |
| FR-GIR | cmems:6200024 (131 km, z ?)<br>cmems:Bilbao-station (141 km, z ?) | Météo-France ⇐ | 1331 | 1.61 | +17 % | 0.7 | 17 | 1.80 | +12 % | media |
| ES-PV | cmems:Bilbao-station (5 km, z ?)<br>cmems:6200024 (26 km, z ?) | Météo-France ⇐ | 1331 | 1.61 | +17 % | 0.7 | 17 | 1.80 | +12 % | alta |
| ES-CAN | cmems:Bilbao-station (32 km, z ?)<br>cmems:6200024 (40 km, z ?) | Météo-France ⇐ | 1331 | 1.61 | +17 % | 0.7 | 17 | 1.80 | +12 % | alta |
| ES-AST | cmems:6200025 (22 km, z ?)<br>cmems:6200082 (84 km, z ?)<br>cmems:6201070 (132 km, z ?) | Météo-France ⇐ | 2142 | 1.72 | +7 % | 0.4 | 50 | 2.06 | +27 % | alta |
| ES-GAL | cmems:6201070 (3 km, z ?)<br>cmems:6200083 (33 km, z ?)<br>cmems:6200084 (50 km, z ?) | ECMWF IFS ⇐ | 2124 | 1.63 | +13 % | 0.7 | 14 | 2.12 | +25 % | alta |
| ES-AND | cmems:6200085 (55 km, z ?) | Météo-France ⇐ | 690 | 1.52 | +19 % | 0.7 | 14 | 2.03 | +36 % | alta |
| ES-CN-W | cmems:1300130 (11 km, z ?) | Météo-France ⇐ | 720 | 1.43 | +7 % | 0.4 | 14 | 1.79 | +15 % | alta |
| PT-NOR | cmems:6200084 (55 km, z ?) | ECMWF IFS ⇐ | 704 | 1.44 | +14 % | 0.8 | 16 | 1.64 | +15 % | alta |
| PT-CEN | cmems:6200199 (7 km, z ?)<br>cmems:6200084 (144 km, z ?) | ECMWF IFS ⇐ | 1391 | 1.37 | +12 % | 0.6 | 14 | 1.71 | +17 % | alta |
| PT-PEN | cmems:6200199 (14 km, z ?) | ECMWF IFS ⇐ | 687 | 1.30 | +8 % | 0.3 | 11 | 1.77 | +21 % | alta |
| PT-ERI | cmems:6200199 (63 km, z ?) | ECMWF IFS ⇐ | 687 | 1.30 | +8 % | 0.3 | 11 | 1.77 | +21 % | alta |
| PT-LIS | cmems:6200199 (84 km, z ?) | ECMWF IFS ⇐ | 687 | 1.30 | +8 % | 0.3 | 11 | 1.77 | +21 % | alta |
| GB-DEV | cmems:6200103 (78 km, z ?) | Météo-France ⇐ | 720 | 0.99 | -0 % | -0.1 | 6 | 1.30 | -2 % | alta |
| GB-SOU | cmems:6200103 (96 km, z ?)<br>cmems:6200305 (105 km, z ?) | Météo-France | 1440 | 1.41 | -3 % | -0.3 | 8 | 1.45 | -4 % | baja |
| GB-WAL | mi:m5 (99 km, z ?) | UKMO ⇐ | 721 | 1.44 | +8 % | 0.7 | 8 | 2.15 | +16 % | alta |
| GB-NE | cmems:6200165 (93 km, z ?)<br>cmems:6200149 (106 km, z ?) | UKMO ⇐ | 1432 | 1.71 | +5 % | 0.4 | 9 | 2.09 | +12 % | alta |
| GB-NIR | mi:m2 (86 km, z ?) | ICON ⇐ | 721 | 1.05 | +0 % | 0.0 | 9 | 1.26 | +4 % | alta |
| IE-SW | mi:m3 (102 km, z ?) | ICON ⇐ | 721 | 1.14 | +2 % | 0.2 | 11 | 1.37 | +3 % | media |
| IE-SE | mi:m3 (58 km, z ?)<br>cmems:IL4-Splaugh (60 km, z ?)<br>mi:m5 (60 km, z ?) | UKMO ⇐ | 2161 | 1.41 | -1 % | -0.1 | 10 | 1.81 | +8 % | alta |
| NL-ALL | cmems:6200170 (109 km, z ?)<br>cmems:6200145 (128 km, z ?) | GFS | 1393 | 1.41 | -3 % | -0.3 | 9 | 1.41 | -3 % | media |
| IT-ALL | cmems:6100219 (27 km, z ?)<br>cmems:6100216 (53 km, z ?)<br>cmems:6100214 (111 km, z ?) | Météo-France ⇐ | 1815 | 1.75 | -6 % | -0.3 | 62 | 2.23 | -12 % | alta |

Sin estaciones de viento (165 regiones, siguen con `gfs_seamless`): UY-CAN UY-MAL UY-ROC AR-MDP AR-BAN AR-SUR BR-RS BR-RS-SUL BR-SC-FLN BR-SC-SUL BR-SC-NOR BR-SP BR-RJ BR-RJL BR-ES BR-BA BR-NE-CE BR-NE-RN BR-NE-PE BR-NOR CL-NOR CL-CEN CL-PIC CL-MAU CL-SUR PE-NOR PE-LLB PE-LIM PE-SUR EC-COS EC-GAL CO-PAC CO-CAR VE-ALL PA-PAC PA-BDT CR-GUA CR-NIC CR-PAC CR-OSA CR-CAR NI-RIV NI-NW SV-LIB SV-ORI GT-PAC MX-OAX MX-PAC MX-NAY MX-BCS MX-BCS-N MX-CAR BB-ALL DO-ALL GP-ALL MQ-ALL BS-ALL TT-ALL US-HI-KAU US-HI-BIG AU-QLD-SC AU-QLD-GC AU-NSW-NR AU-NSW-MN AU-NSW-NC AU-NSW-SYD AU-NSW-SC AU-VIC-SC AU-VIC-PI AU-VIC-W AU-TAS AU-SA AU-SA-EYR AU-WA-MR AU-WA-PER AU-WA-NW AU-WA-GAS NZ-NTL NZ-AKL NZ-RAG NZ-TAR NZ-BOP NZ-GIS NZ-WEL NZ-KAI NZ-OTA NZ-WC FJ-MAM FJ-SOU PF-TAH PF-ISL WS-ALL TO-ALL VU-ALL PG-ALL ID-BAL-BUK ID-BAL-W ID-BAL-E ID-JAV-E ID-JAV-W ID-LOM ID-SBW ID-SMB ID-ROT ID-MEN ID-NIA ID-KRU PH-SIA PH-LUZ PH-EAS LK-E LK-S MV-NMA MV-SMA MV-SOU MV-CEN JP-CHI JP-SHO JP-IZU JP-IBA JP-SHK JP-KYU TW-E TW-NE IN-W IN-E VN-ALL CN-HAI ZA-WC-CPT ZA-WC-WCO ZA-WC-GR ZA-EC-JB ZA-EC-PE ZA-EC-WLD ZA-KZN-DBN ZA-KZN-N ZA-KZN-S NA-ERO MA-TAG MA-N MA-S SN-ALL LR-ALL GH-ALL MZ-S MZ-INH MG-ALL RE-ALL MU-ALL CV-ALL FR-VEN FR-BRE ES-CN-E PT-ALG PT-AZO PT-MAD GB-CON GB-SCO IE-NW NO-S NO-N DK-ALL DE-ALL IT-SAR IS-ALL.

### Control de unidades y convenciones por fuente

Promedios ponderados por horas sobre todas las estaciones de cada fuente: velocidad media observada (a 10 m), sesgo y rmse de velocidad del modelo, error medio absoluto de dirección y sesgo circular (cerca de ±180° indicaría una convención "hacia"; un sesgo de velocidad cerca de ×1,9 o ×0,5, nudos por m/s).

| Fuente | Modelo | horas | obs m/s | sesgo m/s | rmse m/s | dir ° | sesgo dir ° |
|---|---|---|---|---|---|---|---|
| Copernicus Marine In Situ | GEM | 4236 | 5.7 | 0.25 | 1.44 | 18 | 6 |
| Copernicus Marine In Situ | UKMO | 4311 | 9.7 | -0.45 | 1.63 | 8 | 3 |
| Copernicus Marine In Situ | ECMWF IFS | 30280 | 5.9 | 0.29 | 1.65 | 20 | 8 |
| Copernicus Marine In Situ | Météo-France | 24006 | 5.8 | 0.43 | 1.72 | 20 | 9 |
| Copernicus Marine In Situ | ICON | 23286 | 5.9 | -0.00 | 1.75 | 21 | 8 |
| Copernicus Marine In Situ | GFS | 30280 | 5.9 | 0.45 | 1.78 | 21 | 9 |
| Copernicus Marine In Situ | JMA | 2038 | 7.1 | 0.30 | 1.84 | 19 | 1 |
| Marine Institute | UKMO | 3605 | 9.2 | 0.04 | 1.29 | 9 | 2 |
| Marine Institute | ECMWF IFS | 3605 | 9.2 | 0.48 | 1.42 | 9 | 1 |
| Marine Institute | ICON | 3605 | 9.2 | 0.65 | 1.54 | 9 | 1 |
| Marine Institute | GFS | 3605 | 9.2 | 0.77 | 1.71 | 9 | 2 |
| Marine Institute | Météo-France | 3605 | 9.2 | 1.04 | 1.97 | 10 | 2 |
| NOAA NDBC | GFS | 34595 | 5.8 | -0.25 | 1.50 | 13 | -0 |
| NOAA NDBC | GEM | 34595 | 5.8 | -0.32 | 1.70 | 16 | 3 |
| NOAA NDBC | ECMWF IFS | 34595 | 5.8 | -0.29 | 1.73 | 15 | 1 |

## Próximos pasos

- Fuentes con cuenta o clave que faltan: **Copernicus Marine** (In Situ TAC: boyas de Europa, Brasil, Sudáfrica, Japón, con viento), **CANDHIS** (Francia), **Channel Coastal Observatory** (Inglaterra), **Puertos del Estado** (España), **IH Portugal**, **SIMCOSTA/PNBOIA** directo (Brasil), **CMEMS** para Uruguay y Argentina.
- Los meses cambian el ganador (verano/invierno, swell/viento): mirar varias corridas mensuales antes de pasar una sugerencia a `models.csv` por PR.
- Las boyas lejos de la costa validan el modelo en mar abierto, no el punto de olas del pico: preferir boyas someras (CDIP, AODN, MI) cuando haya.
- Viento: casi todas las estaciones son de EE. UU. (NDBC) e Irlanda; las costeras miden efectos locales (muelles, edificios, brisa) y las que todos los modelos erran por más de 35 % se descartan. Fuera de ahí sigue `gfs_seamless`.
