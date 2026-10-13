# Validación de los modelos de olas

Ventana: **2026-09-13 a 2026-10-13** (UTC), hora a hora. Generado el 2026-10-13 03:22 UTC por `validate/run.py` (ver `validate/README.md`).

Cada región se compara con hasta 3 boyas a menos de 150 km de alguno de sus picos (la más cercana primero). Todos los modelos se miden sobre las mismas horas. El mejor es el de menor `hs_rmse` con |sesgo| ≤ 15 % (empates de 0.01 m: menor error de dirección). La confianza mira las horas (≥ 480 alta, ≥ 240 media), cuánto peor es el modelo de hoy (≥ 10 % alta, ≥ 5 % media), que la mayoría de las boyas coincida y que la boya más cercana esté a ≤ 100 km (alta).

## Resumen

- Regiones: **212**; con boyas: **44**; sin boyas: **168**.
- Regiones con boyas por fuente: CDIP 23, AODN / IMOS 15, NOAA NDBC 14, Marine Institute 4.
- Mejor modelo (regiones con boyas): ECMWF WAM 18, MFWAM 12, GFS-Wave 0,25° 7, GFS-Wave 0,16° 3, ninguno 3, DWD EWAM 1.
- Confianza: alta 19, media 6, baja 19.
- Open-Meteo: 6 pedidos, 10 ubicaciones, ~22 llamadas ponderadas (límite gratuito 10.000/día).

## Fuentes

| Fuente | Datos | Licencia | Esta corrida |
|---|---|---|---|
| CDIP | Coastal Data Information Program, Scripps Institution of Oceanography (UCSD); ERDDAP `wave_agg` | uso libre, se agradece el crédito a CDIP | 80 estaciones, 80 con ≥ 72 h de Hs |
| AODN / IMOS | Boyas de olas de Australia (IMOS, estados y universidades), parquet `wave_buoy_realtime_nonqc` | CC BY 4.0 | 77 estaciones, 48 con ≥ 72 h de Hs |
| Marine Institute | Irish Wave Buoy Network, ERDDAP `IWaveBNetwork30Min` | CC BY 4.0 | 4 estaciones, 4 con ≥ 72 h de Hs |
| NOAA NDBC | National Data Buoy Center, `realtime2` (incluye socios: PNBOIA, Canadá, etc.) | dominio público | 159 estaciones, 123 con ≥ 72 h de Hs |

Boyas publicadas por dos fuentes (se usa una): cdip:201 = cdip:073, cdip:150 = ndbc:41110, cdip:132 = ndbc:41112, cdip:143 = ndbc:41113, cdip:194 = ndbc:41117, cdip:250 = ndbc:41120, cdip:249 = ndbc:41121, cdip:256 = ndbc:42084, cdip:252 = ndbc:42092, cdip:171 = ndbc:44014, cdip:433 = ndbc:44056, cdip:260 = ndbc:44085, cdip:243 = ndbc:44086, cdip:240 = ndbc:44087, cdip:209 = ndbc:44091, cdip:192 = ndbc:44095, cdip:154 = ndbc:44097, cdip:160 = ndbc:44098, cdip:147 = ndbc:44099, cdip:430 = ndbc:44100, cdip:094 = ndbc:46213, cdip:029 = ndbc:46214, cdip:071 = ndbc:46218, cdip:067 = ndbc:46219, cdip:028 = ndbc:46221, cdip:092 = ndbc:46222, cdip:045 = ndbc:46224, cdip:100 = ndbc:46225, cdip:139 = ndbc:46229, cdip:156 = ndbc:46236, cdip:157 = ndbc:46239, cdip:162 = ndbc:46243, cdip:179 = ndbc:46248, cdip:213 = ndbc:46253, cdip:201 = ndbc:46254, cdip:215 = ndbc:46256, cdip:220 = ndbc:46258, cdip:222 = ndbc:46259, cdip:153 = ndbc:46266, cdip:248 = ndbc:46267, cdip:271 = ndbc:46277, cdip:270 = ndbc:46278, cdip:284 = ndbc:46285, cdip:106 = ndbc:51201, cdip:098 = ndbc:51202, cdip:187 = ndbc:51205, cdip:188 = ndbc:51206, cdip:189 = ndbc:51209, cdip:233 = ndbc:51211, cdip:238 = ndbc:51212, cdip:036 = ndbc:46211, cdip:076 = ndbc:46215, cdip:262 = ndbc:46274, cdip:264 = ndbc:46275, cdip:273 = ndbc:51214, cdip:265 = ndbc:41122, cdip:171 = ndbc:44088, cdip:103 = ndbc:46268, cdip:217 = ndbc:41159, cdip:263 = ndbc:44084, cdip:221 = ndbc:44090, cdip:201 = ndbc:LJPC1, cdip:191 = ndbc:46232, cdip:134 = ndbc:41114, cdip:285 = ndbc:46286, cdip:279 = ndbc:42354, cdip:142 = ndbc:46237, cdip:168 = ndbc:46244.

## Por país

| País | Regiones con boyas | Gana |
|---|---|---|
| Estados Unidos | 21 | ECMWF WAM 12, MFWAM 5, GFS-Wave 0,16° 3, GFS-Wave 0,25° 1 |
| Australia | 15 | ECMWF WAM 4, GFS-Wave 0,25° 4, MFWAM 4, ninguno 3 |
| Reino Unido | 2 | DWD EWAM 1, ECMWF WAM 1 |
| Irlanda | 2 | MFWAM 2 |
| Puerto Rico | 2 | GFS-Wave 0,25° 2 |
| Canadá | 1 | MFWAM 1 |
| México | 1 | ECMWF WAM 1 |

## Regiones con boyas

Métricas del mejor modelo (o del de hoy si ninguno califica). `Tp` es el sesgo de período del modelo contra el período pico de la boya; ᵖ: GFS-Wave no da período pico en Open-Meteo y se usa su `wave_period`, que es el del sistema de olas principal (se comporta como un pico); ᵐ: MFWAM y EWAM tampoco lo dan y su `wave_period` es un período medio, así que su `Tp` sale negativo por construcción. ⇐ = se sugiere cambiar (en `models-suggested.csv`). Las regiones fijas (issue #7) se validan sólo para informar.

| Región | Boyas | Mejor | n | rmse m | sesgo | SI | Tp s | dir ° | Hoy | rmse hoy | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MX-BCN | cdip:191 (28 km)<br>cdip:201 (40 km)<br>cdip:220 (43 km) | ECMWF WAM ⇐ | 2056 | 0.19 | +8 % | 0.16 | 0.3 | 31 | GFS-Wave 0,16° | 0.26 | alta |
| PR-NW | cdip:249 (29 km)<br>ndbc:41053 (92 km) | GFS-Wave 0,25° | 1411 | 0.14 | +4 % | 0.16 | 0.5ᵖ | 12 | GFS-Wave 0,16° | 0.14 | baja |
| PR-N | ndbc:41053 (5 km)<br>cdip:249 (19 km) | GFS-Wave 0,25° | 1411 | 0.14 | +4 % | 0.16 | 0.5ᵖ | 12 | GFS-Wave 0,16° | 0.14 | baja |
| US-CA-SD | cdip:262 (1 km)<br>cdip:153 (1 km)<br>cdip:201 (1 km) | ECMWF WAM | 2168 | 0.18 | +11 % | 0.18 | -0.4 | 22 | GFS-Wave 0,16° | 0.17 | baja |
| US-CA-OC | cdip:284 (1 km)<br>cdip:271 (8 km)<br>cdip:264 (11 km) | ECMWF WAM ⇐ | 2168 | 0.15 | +7 % | 0.15 | -1.4 | 16 | GFS-Wave 0,16° | 0.23 | alta |
| US-CA-LA | cdip:103 (2 km)<br>cdip:028 (20 km)<br>ndbc:46025 (34 km) | ECMWF WAM ⇐ | 2168 | 0.15 | +9 % | 0.13 | -0.6 | 25 | GFS-Wave 0,16° | 0.31 | alta |
| US-CA-SB | cdip:071 (26 km)<br>ndbc:46025 (34 km)<br>cdip:028 (37 km) | MFWAM ⇐ | 2169 | 0.20 | +3 % | 0.14 | -2.7ᵐ | 28 | GFS-Wave 0,16° | 0.35 | alta |
| US-CA-CEN | cdip:076 (6 km)<br>cdip:157 (20 km)<br>ndbc:46011 (34 km) | ECMWF WAM ⇐ | 2168 | 0.31 | +0 % | 0.17 | -1.1 | 21 | GFS-Wave 0,16° | 0.41 | alta |
| US-CA-SC | cdip:156 (14 km)<br>cdip:157 (26 km)<br>ndbc:46042 (30 km) | ECMWF WAM ⇐ | 2168 | 0.27 | -2 % | 0.15 | -0.2 | 16 | GFS-Wave 0,16° | 0.44 | alta |
| US-CA-SF | cdip:142 (9 km)<br>ndbc:46026 (22 km)<br>ndbc:46013 (44 km) | MFWAM ⇐ | 1692 | 0.20 | +6 % | 0.10 | -1.4ᵐ | 14 | GFS-Wave 0,16° | 0.42 | alta |
| US-CA-NOR | cdip:168 (16 km)<br>ndbc:46014 (18 km)<br>ndbc:46022 (24 km) | MFWAM ⇐ | 2026 | 0.20 | -0 % | 0.10 | -0.8ᵐ | 12 | GFS-Wave 0,16° | 0.28 | alta |
| US-PNW | cdip:270 (7 km)<br>cdip:036 (10 km)<br>cdip:162 (10 km) | MFWAM ⇐ | 2169 | 0.20 | +2 % | 0.13 | -1.4ᵐ | 13 | GFS-Wave 0,16° | 0.34 | alta |
| US-GULF | cdip:252 (21 km)<br>ndbc:42035 (35 km) | MFWAM ⇐ | 1446 | 0.15 | -8 % | 0.13 | -0.9ᵐ | 12 | GFS-Wave 0,16° | 0.21 | alta |
| US-FL | cdip:265 (2 km)<br>cdip:143 (6 km)<br>cdip:134 (13 km) | GFS-Wave 0,16° | 1961 | 0.20 | +7 % | 0.29 | 0.4ᵖ | 26 | GFS-Wave 0,16° | 0.20 | baja |
| US-FL-PAN | ndbc:42357 (20 km)<br>ndbc:42012 (24 km)<br>cdip:256 (42 km) | ECMWF WAM ⇐ | 1853 | 0.18 | +4 % | 0.24 | -0.1 | 29 | GFS-Wave 0,16° | 0.19 | media |
| US-SE | cdip:433 (5 km)<br>cdip:150 (10 km)<br>ndbc:SSBN7 (13 km) | GFS-Wave 0,16° | 1894 | 0.16 | -7 % | 0.15 | 0.1ᵖ | 12 | GFS-Wave 0,16° | 0.16 | baja |
| US-SC-GA | ndbc:41067 (12 km)<br>ndbc:41076 (29 km)<br>cdip:132 (45 km) | ECMWF WAM | 2157 | 0.19 | -6 % | 0.19 | -1.9 | 19 | GFS-Wave 0,16° | 0.20 | baja |
| US-MID | cdip:263 (1 km)<br>cdip:147 (23 km)<br>cdip:430 (60 km) | GFS-Wave 0,25° ⇐ | 2153 | 0.20 | -3 % | 0.16 | -0.5ᵖ | 15 | GFS-Wave 0,16° | 0.27 | alta |
| US-NE | ndbc:44007 (7 km)<br>ndbc:44029 (10 km)<br>ndbc:44030 (14 km) | ECMWF WAM ⇐ | 1609 | 0.18 | +0 % | 0.18 | 0.3 | 20 | GFS-Wave 0,16° | 0.21 | alta |
| US-HI-OAN | cdip:106 (6 km) | GFS-Wave 0,16° | 723 | 0.24 | -14 % | 0.11 | 0.6ᵖ | 24 | GFS-Wave 0,16° | 0.24 | alta |
| US-HI-OAS | cdip:238 (4 km)<br>cdip:233 (10 km) | ECMWF WAM ⇐ | 1446 | 0.19 | +2 % | 0.17 | 0.0 | 18 | GFS-Wave 0,16° | 0.42 | alta |
| US-HI-MAU | cdip:187 (10 km)<br>cdip:233 (138 km)<br>cdip:188 (148 km) | ECMWF WAM ⇐ | 2169 | 0.21 | +5 % | 0.12 | -0.2 | 20 | GFS-Wave 0,16° | 0.51 | alta |
| US-HI-KAU | cdip:238 (143 km) | ECMWF WAM ⇐ | 723 | 0.18 | -8 % | 0.13 | -0.7 | 20 | GFS-Wave 0,16° | 0.31 | media |
| US-HI-BIG | cdip:187 (116 km) | ECMWF WAM ⇐ | 723 | 0.26 | +9 % | 0.11 | -0.8 | 26 | GFS-Wave 0,16° | 0.47 | media |
| CA-BC-VI | ndbc:46087 (31 km)<br>ndbc:46041 (130 km) | MFWAM ⇐ | 1319 | 0.25 | -2 % | 0.15 | -0.9ᵐ | 12 | GFS-Wave 0,16° | 0.37 | alta |
| AU-NSW-NR | aodn:wooli (28 km) | ECMWF WAM | 194 | 0.32 | +8 % | 0.19 | -1.0 | 20 | GFS-Wave 0,25° | 0.33 | baja |
| AU-NSW-MN | aodn:crowdy (4 km)<br>aodn:wooli (17 km) | GFS-Wave 0,25° | 408 | 0.30 | -9 % | 0.16 | -1.2ᵖ | 26 | GFS-Wave 0,25° | 0.30 | baja |
| AU-NSW-NC | aodn:collaroy-narrabeen (20 km)<br>aodn:crowdy (113 km) | MFWAM ⇐ | 407 | 0.29 | +9 % | 0.21 | -1.4ᵐ | 31 | GFS-Wave 0,25° | 0.83 | media |
| AU-NSW-SYD | aodn:collaroy-narrabeen (1 km) | ninguno | 193 | 1.17 | +98 % | 0.97 | -1.6ᵖ | 58 | GFS-Wave 0,25° | 1.17 | baja |
| AU-NSW-SC | aodn:bengello (3 km)<br>aodn:collaroy-narrabeen (63 km) | ninguno | 387 | 0.87 | +46 % | 0.79 | -2.2ᵖ | 47 | GFS-Wave 0,25° | 0.87 | baja |
| AU-VIC-SC | aodn:apollo-bay (32 km)<br>aodn:inverloch (114 km)<br>aodn:bob (145 km) | GFS-Wave 0,25° | 1109 | 0.40 | -14 % | 0.14 | 0.5ᵖ | 12 | GFS-Wave 0,25° | 0.40 | baja |
| AU-VIC-PI | aodn:inverloch (44 km)<br>aodn:apollo-bay (97 km)<br>aodn:wilsons-prom (147 km) | ninguno | 1043 | 0.39 | -16 % | 0.15 | 0.5ᵖ | 12 | GFS-Wave 0,25° | 0.39 | baja |
| AU-VIC-W | aodn:port-fairy (3 km)<br>aodn:cape-bridgewater (11 km)<br>aodn:apollo-bay (16 km) | MFWAM ⇐ | 1109 | 0.46 | +12 % | 0.17 | -2.6ᵐ | 21 | GFS-Wave 0,25° | 0.60 | alta |
| AU-TAS | aodn:storm-bay (24 km) | ECMWF WAM | 193 | 0.22 | +1 % | 0.17 | -1.2 | 46 | GFS-Wave 0,25° | 0.34 | baja |
| AU-SA | aodn:victor-harbouroffshore (9 km)<br>aodn:brighton (14 km)<br>aodn:west-beach (22 km) | MFWAM | 1633 | 0.30 | -0 % | 0.29 | -2.7ᵐ | 16 | GFS-Wave 0,25° | 0.35 | baja |
| AU-SA-EYR | aodn:ceduna (68 km) | ECMWF WAM | 194 | 0.15 | -7 % | 0.10 | 0.2 | 9 | GFS-Wave 0,25° | 1.07 | baja |
| AU-WA-MR | aodn:augusta-offshore (43 km)<br>aodn:bunbury (47 km) | GFS-Wave 0,25° | 387 | 0.22 | -5 % | 0.08 | 0.8ᵖ | 8 | GFS-Wave 0,25° | 0.22 | media |
| AU-WA-PER | aodn:hillarys (10 km)<br>aodn:jurien-bay-inshore (144 km)<br>aodn:jurien-bay-offshore (146 km) | MFWAM ⇐ | 1639 | 0.33 | +10 % | 0.09 | -2.4ᵐ | 16 | GFS-Wave 0,25° | 0.38 | alta |
| AU-WA-NW | aodn:dongara-inshore (51 km)<br>aodn:dongara-offshore (51 km) | GFS-Wave 0,25° | 1445 | 0.36 | +14 % | 0.14 | 0.2ᵖ | 7 | GFS-Wave 0,25° | 0.36 | baja |
| AU-WA-GAS | aodn:coral-bay-0-2 (85 km) | ECMWF WAM | 194 | 0.18 | +2 % | 0.10 | -0.0 | 28 | GFS-Wave 0,25° | 0.47 | baja |
| GB-WAL | mi:m5 (99 km) | DWD EWAM | 723 | 0.24 | -2 % | 0.13 | -1.4ᵐ | 9 | GFS-Wave 0,16° | 0.24 | baja |
| GB-NIR | mi:m2 (86 km) | ECMWF WAM ⇐ | 723 | 0.20 | -6 % | 0.15 | -0.4 | 19 | GFS-Wave 0,25° | 0.26 | alta |
| IE-SW | mi:m3 (102 km) | MFWAM ⇐ | 723 | 0.26 | -2 % | 0.08 | -1.9ᵐ | 9 | GFS-Wave 0,25° | 0.42 | media |
| IE-SE | mi:m3 (58 km)<br>mi:m5 (60 km) | MFWAM | 1446 | 0.25 | -4 % | 0.09 | -1.6ᵐ | 9 | GFS-Wave 0,16° | 0.34 | baja |

## Regiones sin boyas (168)

Dispersión entre modelos de la altura de ola en el pico central de la región (desvío / media, promedio de las horas). Más de 0.30 ⇒ confianza baja: los modelos no coinciden y conviene buscar boyas.

| Región | Dispersión | Hs media por modelo (m) | Confianza |
|---|---|---|---|
| VE-ALL | 0.45 | GFS-Wave 0,16° 0.39, GFS-Wave 0,25° 0.64, MFWAM 0.78, ECMWF WAM 0.20 | baja |
| FJ-MAM | 0.36 | GFS-Wave 0,25° 0.66, MFWAM 1.68, ECMWF WAM 1.53 | baja |
| EC-COS | 0.34 | GFS-Wave 0,16° 0.66, GFS-Wave 0,25° 0.86, MFWAM 1.09, ECMWF WAM 0.40 | baja |
| PT-LIS | 0.33 | GFS-Wave 0,16° 1.07, GFS-Wave 0,25° 1.63, MFWAM 1.37, ECMWF WAM 0.78, DWD EWAM 0.70 | baja |
| GB-SOU | 0.31 | GFS-Wave 0,16° 0.57, GFS-Wave 0,25° 0.90, MFWAM 0.49, ECMWF WAM 0.47, DWD EWAM 0.49 | baja |
| ES-CN-E | 0.30 | GFS-Wave 0,16° 1.20, GFS-Wave 0,25° 0.81, MFWAM 1.33, ECMWF WAM 0.62 | media |
| IE-NW | 0.29 | MFWAM 1.91, ECMWF WAM 1.06, DWD EWAM 1.09 | media |
| DE-ALL | 0.28 | GFS-Wave 0,25° 1.17, MFWAM 1.22, ECMWF WAM 1.20, DWD EWAM 0.51 | media |
| BS-ALL | 0.28 | GFS-Wave 0,16° 0.86, GFS-Wave 0,25° 0.99, MFWAM 0.57, ECMWF WAM 0.50 | media |
| NZ-BOP | 0.28 | GFS-Wave 0,25° 0.68, MFWAM 0.39, ECMWF WAM 0.40 | media |
| PF-ISL | 0.27 | GFS-Wave 0,25° 1.91, MFWAM 1.72, ECMWF WAM 0.95 | media |
| BR-SC-FLN | 0.27 | MFWAM 0.85, ECMWF WAM 1.46 | media |
| ID-JAV-W | 0.25 | GFS-Wave 0,16° 1.33, MFWAM 0.92, ECMWF WAM 0.76 | media |
| ZA-WC-CPT | 0.24 | GFS-Wave 0,25° 1.88, MFWAM 1.67, ECMWF WAM 1.03 | media |
| CR-OSA | 0.24 | GFS-Wave 0,16° 0.99, GFS-Wave 0,25° 0.65, MFWAM 1.19, ECMWF WAM 0.74 | media |
| ES-AND | 0.24 | GFS-Wave 0,16° 0.62, GFS-Wave 0,25° 0.80, MFWAM 0.68, ECMWF WAM 0.50, DWD EWAM 0.44 | media |
| MV-SOU | 0.23 | GFS-Wave 0,16° 0.58, GFS-Wave 0,25° 0.51, MFWAM 0.60, ECMWF WAM 0.89 | media |
| VN-ALL | 0.23 | GFS-Wave 0,16° 0.57, MFWAM 0.63, ECMWF WAM 0.38 | media |
| BR-SC-NOR | 0.22 | GFS-Wave 0,25° 0.84, MFWAM 0.55, ECMWF WAM 0.96 | media |
| BR-RJ | 0.21 | GFS-Wave 0,25° 0.94, MFWAM 1.40, ECMWF WAM 0.93 | media |
| MX-NAY | 0.20 | GFS-Wave 0,16° 0.62, MFWAM 0.89, ECMWF WAM 1.04 | media |
| ES-PV | 0.20 | GFS-Wave 0,16° 0.77, GFS-Wave 0,25° 1.15, MFWAM 1.16, ECMWF WAM 1.46, DWD EWAM 1.18 | media |
| MV-CEN | 0.20 | GFS-Wave 0,16° 0.78, GFS-Wave 0,25° 0.78, MFWAM 0.74, ECMWF WAM 1.15 | media |
| MX-CAR | 0.20 | GFS-Wave 0,16° 0.55, GFS-Wave 0,25° 0.36, MFWAM 0.45, ECMWF WAM 0.43 | media |
| IT-ALL | 0.20 | GFS-Wave 0,16° 0.45, GFS-Wave 0,25° 0.46, MFWAM 0.40, ECMWF WAM 0.39, DWD EWAM 0.35 | media |
| TO-ALL | 0.19 | GFS-Wave 0,25° 1.63, MFWAM 2.00, ECMWF WAM 1.35 | media |
| ID-ROT | 0.19 | GFS-Wave 0,16° 1.09, GFS-Wave 0,25° 0.80, MFWAM 1.22, ECMWF WAM 0.88 | media |
| TT-ALL | 0.18 | GFS-Wave 0,16° 0.98, GFS-Wave 0,25° 1.05, MFWAM 1.01, ECMWF WAM 0.64 | media |
| MV-NMA | 0.18 | GFS-Wave 0,16° 0.92, GFS-Wave 0,25° 0.71, MFWAM 0.77, ECMWF WAM 1.09 | media |
| NI-NW | 0.18 | GFS-Wave 0,16° 1.05, GFS-Wave 0,25° 1.15, MFWAM 0.73, ECMWF WAM 1.13 | media |
| IT-SAR | 0.18 | GFS-Wave 0,16° 0.52, GFS-Wave 0,25° 0.59, MFWAM 0.66, ECMWF WAM 0.65, DWD EWAM 0.57 | media |
| NO-S | 0.18 | GFS-Wave 0,25° 1.76, MFWAM 1.75, ECMWF WAM 1.16, DWD EWAM 1.73 | media |
| EC-GAL | 0.18 | GFS-Wave 0,16° 1.04, GFS-Wave 0,25° 1.23, MFWAM 1.33, ECMWF WAM 0.83 | media |
| MZ-INH | 0.18 | GFS-Wave 0,25° 1.03, MFWAM 1.33, ECMWF WAM 1.58 | media |
| JP-IZU | 0.17 | GFS-Wave 0,16° 1.19, GFS-Wave 0,25° 1.60, MFWAM 1.62, ECMWF WAM 1.83 | media |
| DK-ALL | 0.17 | GFS-Wave 0,25° 0.97, MFWAM 1.31, ECMWF WAM 1.53, DWD EWAM 1.49 | media |
| GB-DEV | 0.17 | GFS-Wave 0,16° 1.22, MFWAM 1.10, ECMWF WAM 0.81, DWD EWAM 1.18 | media |
| TW-E | 0.17 | GFS-Wave 0,16° 0.97, GFS-Wave 0,25° 1.38, MFWAM 1.38, ECMWF WAM 1.42 | media |
| ES-CN-W | 0.17 | GFS-Wave 0,16° 0.55, GFS-Wave 0,25° 0.81, MFWAM 0.74, ECMWF WAM 0.63 | media |
| PE-NOR | 0.16 | GFS-Wave 0,16° 0.93, GFS-Wave 0,25° 1.34, MFWAM 1.16, ECMWF WAM 0.95 | media |
| NL-ALL | 0.16 | GFS-Wave 0,25° 0.93, MFWAM 0.88, ECMWF WAM 0.67, DWD EWAM 0.85 | media |
| FR-VEN | 0.16 | GFS-Wave 0,16° 0.83, GFS-Wave 0,25° 0.90, MFWAM 1.02, ECMWF WAM 0.67, DWD EWAM 0.74 | media |
| BR-SP | 0.16 | GFS-Wave 0,25° 0.92, MFWAM 1.35, ECMWF WAM 1.11 | media |
| AU-QLD-GC | 0.16 | GFS-Wave 0,25° 0.99, MFWAM 0.88, ECMWF WAM 1.25 | media |
| CV-ALL | 0.15 | GFS-Wave 0,16° 1.24, GFS-Wave 0,25° 1.22, MFWAM 1.27, ECMWF WAM 0.86 | media |
| GB-SCO | 0.15 | GFS-Wave 0,25° 0.72, MFWAM 0.71, ECMWF WAM 0.63, DWD EWAM 0.70 | media |
| GB-NE | 0.14 | GFS-Wave 0,25° 0.56, MFWAM 0.60, ECMWF WAM 0.69, DWD EWAM 0.56 | media |
| ID-BAL-E | 0.14 | GFS-Wave 0,16° 1.09, GFS-Wave 0,25° 1.48, MFWAM 1.06, ECMWF WAM 1.25 | media |
| ZA-WC-WCO | 0.14 | MFWAM 2.07, ECMWF WAM 1.57 | media |
| LK-E | 0.14 | GFS-Wave 0,16° 1.20, GFS-Wave 0,25° 1.44, MFWAM 0.99, ECMWF WAM 1.28 | media |
| KR-ALL | 0.14 | GFS-Wave 0,16° 0.87, GFS-Wave 0,25° 0.90, MFWAM 0.69, ECMWF WAM 0.91 | media |
| PA-BDT | 0.14 | GFS-Wave 0,16° 0.87, GFS-Wave 0,25° 0.86, MFWAM 0.63, ECMWF WAM 0.68 | media |
| RE-ALL | 0.14 | GFS-Wave 0,25° 1.75, MFWAM 1.91, ECMWF WAM 1.41 | media |
| BB-ALL | 0.13 | GFS-Wave 0,16° 0.77, GFS-Wave 0,25° 1.10, MFWAM 0.97, ECMWF WAM 0.94 | media |
| CN-HAI | 0.13 | GFS-Wave 0,16° 0.92, GFS-Wave 0,25° 0.85, MFWAM 0.71, ECMWF WAM 0.97 | media |
| UY-ROC | 0.13 | GFS-Wave 0,25° 1.56, MFWAM 1.16, ECMWF WAM 1.49 | media |
| CL-NOR | 0.13 | GFS-Wave 0,25° 1.10, MFWAM 1.32, ECMWF WAM 1.00 | media |
| CO-PAC | 0.13 | GFS-Wave 0,16° 0.63, GFS-Wave 0,25° 0.84, MFWAM 0.75, ECMWF WAM 0.66 | media |
| GP-ALL | 0.13 | GFS-Wave 0,16° 1.11, GFS-Wave 0,25° 0.95, MFWAM 0.85, ECMWF WAM 1.16 | media |
| IS-ALL | 0.13 | GFS-Wave 0,25° 2.59, MFWAM 2.65, ECMWF WAM 2.02 | media |
| FR-BRE | 0.13 | GFS-Wave 0,16° 0.85, MFWAM 1.08, ECMWF WAM 0.91, DWD EWAM 0.84 | media |
| UY-MAL | 0.12 | GFS-Wave 0,25° 1.38, MFWAM 1.11, ECMWF WAM 1.47 | media |
| AR-BAN | 0.12 | GFS-Wave 0,25° 1.33, MFWAM 1.30, ECMWF WAM 1.01 | media |
| IN-E | 0.12 | GFS-Wave 0,16° 0.74, GFS-Wave 0,25° 0.79, MFWAM 0.59, ECMWF WAM 0.68 | media |
| JP-SHO | 0.12 | GFS-Wave 0,16° 0.90, GFS-Wave 0,25° 0.90, MFWAM 0.85, ECMWF WAM 0.91 | media |
| JP-KYU | 0.12 | GFS-Wave 0,16° 1.38, GFS-Wave 0,25° 1.50, MFWAM 1.78, ECMWF WAM 1.48 | media |
| PT-MAD | 0.12 | GFS-Wave 0,16° 0.79, GFS-Wave 0,25° 0.79, MFWAM 0.88, ECMWF WAM 0.66 | media |
| MA-TAG | 0.11 | GFS-Wave 0,16° 1.16, GFS-Wave 0,25° 1.36, MFWAM 1.52, ECMWF WAM 1.44, DWD EWAM 1.48 | media |
| ES-GAL | 0.11 | GFS-Wave 0,16° 1.49, GFS-Wave 0,25° 1.87, MFWAM 1.55, ECMWF WAM 1.63, DWD EWAM 1.85 | media |
| NZ-AKL | 0.11 | GFS-Wave 0,25° 2.27, MFWAM 2.43, ECMWF WAM 1.88 | media |
| BR-NE-CE | 0.11 | GFS-Wave 0,16° 1.25, GFS-Wave 0,25° 1.25, MFWAM 1.19, ECMWF WAM 0.96 | media |
| BR-NE-RN | 0.11 | GFS-Wave 0,16° 1.07, GFS-Wave 0,25° 1.42, MFWAM 1.33, ECMWF WAM 1.24 | media |
| MU-ALL | 0.11 | GFS-Wave 0,25° 1.61, MFWAM 2.07, ECMWF WAM 1.89 | media |
| BR-RJL | 0.10 | GFS-Wave 0,25° 1.27, MFWAM 1.47, ECMWF WAM 1.23 | media |
| BR-NOR | 0.10 | GFS-Wave 0,16° 1.40, GFS-Wave 0,25° 1.48, MFWAM 1.71, ECMWF WAM 1.30 | media |
| IN-W | 0.10 | GFS-Wave 0,16° 0.92, GFS-Wave 0,25° 0.97, MFWAM 1.18, ECMWF WAM 1.10 | media |
| MA-S | 0.10 | GFS-Wave 0,16° 1.12, GFS-Wave 0,25° 1.22, MFWAM 1.41, ECMWF WAM 1.36 | media |
| ID-BAL-BUK | 0.10 | GFS-Wave 0,16° 1.69, GFS-Wave 0,25° 1.48, MFWAM 1.91, ECMWF WAM 1.83 | media |
| NZ-KAI | 0.10 | GFS-Wave 0,25° 0.77, MFWAM 0.78, ECMWF WAM 0.86 | media |
| ID-SBW | 0.10 | GFS-Wave 0,16° 1.18, MFWAM 1.41, ECMWF WAM 1.17 | media |
| BR-RS | 0.10 | MFWAM 1.17, ECMWF WAM 1.42 | media |
| JP-CHI | 0.10 | GFS-Wave 0,16° 1.77, GFS-Wave 0,25° 1.97, MFWAM 1.56, ECMWF WAM 1.61 | media |
| FR-GIR | 0.10 | GFS-Wave 0,16° 1.34, MFWAM 1.48, ECMWF WAM 1.20, DWD EWAM 1.40 | media |
| CL-MAU | 0.10 | GFS-Wave 0,25° 1.35, MFWAM 1.11, ECMWF WAM 1.22 | media |
| MX-BCS-N | 0.09 | GFS-Wave 0,16° 1.26, GFS-Wave 0,25° 1.26, MFWAM 1.52, ECMWF WAM 1.36 | media |
| PH-LUZ | 0.09 | GFS-Wave 0,16° 0.52, GFS-Wave 0,25° 0.50, MFWAM 0.54, ECMWF WAM 0.52 | media |
| ZA-WC-GR | 0.09 | MFWAM 2.01, ECMWF WAM 1.69 | media |
| GH-ALL | 0.09 | GFS-Wave 0,16° 0.98, MFWAM 1.06, ECMWF WAM 1.22 | media |
| NZ-WEL | 0.09 | GFS-Wave 0,25° 1.81, MFWAM 2.02, ECMWF WAM 1.94 | media |
| PH-EAS | 0.09 | GFS-Wave 0,16° 0.85, MFWAM 1.00, ECMWF WAM 0.98 | media |
| FR-PBA | 0.09 | GFS-Wave 0,16° 1.37, MFWAM 1.32, ECMWF WAM 1.55, DWD EWAM 1.56 | media |
| SV-ORI | 0.09 | GFS-Wave 0,16° 1.06, GFS-Wave 0,25° 1.02, MFWAM 0.91, ECMWF WAM 1.14 | media |
| JP-SHK | 0.09 | GFS-Wave 0,16° 1.42, GFS-Wave 0,25° 1.52, MFWAM 1.53, ECMWF WAM 1.37 | media |
| BR-RS-SUL | 0.09 | GFS-Wave 0,25° 1.23, MFWAM 1.09, ECMWF WAM 1.33 | media |
| ID-MEN | 0.09 | GFS-Wave 0,16° 1.38, GFS-Wave 0,25° 1.69, MFWAM 1.66, ECMWF WAM 1.72 | media |
| ES-CAN | 0.09 | GFS-Wave 0,16° 1.44, GFS-Wave 0,25° 1.44, MFWAM 1.61, ECMWF WAM 1.44, DWD EWAM 1.71 | media |
| PT-AZO | 0.09 | GFS-Wave 0,16° 1.42, GFS-Wave 0,25° 1.57, MFWAM 1.38, ECMWF WAM 1.66 | media |
| CR-CAR | 0.09 | GFS-Wave 0,16° 0.84, GFS-Wave 0,25° 0.84, MFWAM 0.98, ECMWF WAM 0.96 | media |
| PT-ALG | 0.09 | GFS-Wave 0,16° 1.36, GFS-Wave 0,25° 1.50, MFWAM 1.41, ECMWF WAM 1.30, DWD EWAM 1.53 | media |
| CL-PIC | 0.09 | MFWAM 1.74, ECMWF WAM 1.47 | media |
| NZ-RAG | 0.09 | GFS-Wave 0,25° 1.97, MFWAM 2.18, ECMWF WAM 2.42 | media |
| MV-SMA | 0.09 | GFS-Wave 0,16° 0.85, GFS-Wave 0,25° 0.86, MFWAM 0.74, ECMWF WAM 0.88 | media |
| PF-TAH | 0.09 | GFS-Wave 0,25° 1.92, MFWAM 2.13, ECMWF WAM 1.78 | media |
| VU-ALL | 0.09 | MFWAM 1.69, ECMWF WAM 1.44 | media |
| PT-ERI | 0.09 | GFS-Wave 0,16° 1.58, GFS-Wave 0,25° 1.58, MFWAM 1.83, ECMWF WAM 1.63, DWD EWAM 1.76 | media |
| CA-NS | 0.08 | GFS-Wave 0,16° 1.29, MFWAM 1.10, ECMWF WAM 1.13 | media |
| MX-OAX | 0.08 | GFS-Wave 0,16° 1.54, GFS-Wave 0,25° 1.68, MFWAM 1.54, ECMWF WAM 1.38 | media |
| TW-NE | 0.08 | GFS-Wave 0,16° 1.05, GFS-Wave 0,25° 1.05, MFWAM 1.07, ECMWF WAM 1.05 | media |
| PT-NOR | 0.08 | GFS-Wave 0,16° 1.22, MFWAM 1.34, ECMWF WAM 1.37, DWD EWAM 1.36 | media |
| AU-QLD-SC | 0.08 | GFS-Wave 0,25° 1.18, MFWAM 1.11, ECMWF WAM 1.22 | media |
| MA-N | 0.08 | GFS-Wave 0,16° 1.33, GFS-Wave 0,25° 1.33, MFWAM 1.45, ECMWF WAM 1.33, DWD EWAM 1.22 | media |
| PT-PEN | 0.08 | GFS-Wave 0,16° 1.59, GFS-Wave 0,25° 1.57, MFWAM 1.74, ECMWF WAM 1.67, DWD EWAM 1.80 | media |
| MX-BCS | 0.08 | GFS-Wave 0,16° 1.57, GFS-Wave 0,25° 1.58, MFWAM 1.70, ECMWF WAM 1.44 | media |
| BR-SC-SUL | 0.08 | GFS-Wave 0,25° 1.47, MFWAM 1.27, ECMWF WAM 1.29 | media |
| PG-ALL | 0.08 | GFS-Wave 0,16° 1.43, GFS-Wave 0,25° 1.36, MFWAM 1.18, ECMWF WAM 1.30 | media |
| CR-PAC | 0.08 | GFS-Wave 0,16° 1.09, GFS-Wave 0,25° 0.97, MFWAM 1.19, ECMWF WAM 1.08 | media |
| GB-CON | 0.08 | GFS-Wave 0,16° 1.53, MFWAM 1.63, ECMWF WAM 1.43, DWD EWAM 1.51 | media |
| DO-ALL | 0.08 | GFS-Wave 0,16° 1.00, GFS-Wave 0,25° 0.87, MFWAM 0.94, ECMWF WAM 0.92 | media |
| NZ-WC | 0.08 | GFS-Wave 0,25° 1.90, MFWAM 2.00, ECMWF WAM 2.17 | media |
| ES-AST | 0.08 | GFS-Wave 0,16° 1.46, GFS-Wave 0,25° 1.56, MFWAM 1.65, ECMWF WAM 1.70, DWD EWAM 1.63 | media |
| SN-ALL | 0.07 | GFS-Wave 0,16° 1.35, GFS-Wave 0,25° 1.34, MFWAM 1.37, ECMWF WAM 1.16 | media |
| CL-SUR | 0.07 | GFS-Wave 0,25° 2.09, MFWAM 1.78, ECMWF WAM 2.01 | media |
| MZ-S | 0.07 | GFS-Wave 0,25° 1.78, MFWAM 1.53, ECMWF WAM 1.75 | media |
| GT-PAC | 0.07 | GFS-Wave 0,16° 1.21, GFS-Wave 0,25° 1.28, MFWAM 1.34, ECMWF WAM 1.17 | media |
| ID-SMB | 0.07 | GFS-Wave 0,16° 1.64, MFWAM 1.47, ECMWF WAM 1.69 | media |
| AR-MDP | 0.07 | GFS-Wave 0,25° 1.56, MFWAM 1.43, ECMWF WAM 1.58 | media |
| FJ-SOU | 0.07 | GFS-Wave 0,25° 1.58, MFWAM 1.84, ECMWF WAM 1.81 | media |
| ZA-KZN-N | 0.07 | GFS-Wave 0,25° 1.74, MFWAM 1.90, ECMWF WAM 1.65 | media |
| CO-CAR | 0.07 | GFS-Wave 0,16° 1.10, MFWAM 0.99, ECMWF WAM 0.97 | media |
| BR-ES | 0.07 | GFS-Wave 0,25° 1.10, MFWAM 1.14, ECMWF WAM 1.03 | media |
| ID-BAL-W | 0.07 | GFS-Wave 0,16° 1.38, GFS-Wave 0,25° 1.57, MFWAM 1.56, ECMWF WAM 1.53 | media |
| PA-PAC | 0.07 | GFS-Wave 0,16° 0.85, GFS-Wave 0,25° 0.92, MFWAM 0.91, ECMWF WAM 0.88 | media |
| NI-RIV | 0.07 | GFS-Wave 0,16° 1.00, GFS-Wave 0,25° 1.02, MFWAM 1.03, ECMWF WAM 0.97 | media |
| FR-HOS | 0.07 | GFS-Wave 0,16° 1.39, GFS-Wave 0,25° 1.42, MFWAM 1.53, ECMWF WAM 1.50, DWD EWAM 1.54 | media |
| CR-NIC | 0.07 | GFS-Wave 0,16° 1.02, GFS-Wave 0,25° 1.06, MFWAM 1.11, ECMWF WAM 1.19 | media |
| NZ-OTA | 0.07 | GFS-Wave 0,25° 1.55, MFWAM 1.61, ECMWF WAM 1.56 | media |
| AR-SUR | 0.06 | GFS-Wave 0,25° 1.20, MFWAM 1.14, ECMWF WAM 1.13 | media |
| ID-JAV-E | 0.06 | GFS-Wave 0,16° 1.61, GFS-Wave 0,25° 1.74, MFWAM 1.66, ECMWF WAM 1.82 | media |
| ID-LOM | 0.06 | GFS-Wave 0,16° 1.78, GFS-Wave 0,25° 1.76, MFWAM 1.59, ECMWF WAM 1.83 | media |
| PH-SIA | 0.06 | GFS-Wave 0,16° 0.95, GFS-Wave 0,25° 0.96, MFWAM 0.92, ECMWF WAM 0.94 | media |
| NA-ERO | 0.06 | GFS-Wave 0,25° 1.10, MFWAM 1.11, ECMWF WAM 1.19 | media |
| PT-CEN | 0.06 | GFS-Wave 0,16° 1.65, GFS-Wave 0,25° 1.67, MFWAM 1.59, ECMWF WAM 1.68, DWD EWAM 1.64 | media |
| PE-LLB | 0.06 | GFS-Wave 0,16° 1.17, GFS-Wave 0,25° 1.26, MFWAM 1.15, ECMWF WAM 1.29 | media |
| MX-PAC | 0.06 | GFS-Wave 0,16° 1.88, MFWAM 1.92, ECMWF WAM 1.73 | media |
| JP-IBA | 0.06 | GFS-Wave 0,16° 1.58, GFS-Wave 0,25° 1.70, MFWAM 1.63, ECMWF WAM 1.61 | media |
| ZA-EC-WLD | 0.06 | GFS-Wave 0,25° 1.95, MFWAM 2.10, ECMWF WAM 2.15 | media |
| BR-BA | 0.06 | GFS-Wave 0,25° 1.17, MFWAM 1.13, ECMWF WAM 1.03 | media |
| CR-GUA | 0.06 | GFS-Wave 0,16° 1.24, GFS-Wave 0,25° 1.25, MFWAM 1.27, ECMWF WAM 1.17 | media |
| NZ-GIS | 0.06 | MFWAM 1.03, ECMWF WAM 1.11 | media |
| ID-NIA | 0.06 | GFS-Wave 0,16° 1.79, GFS-Wave 0,25° 1.75, MFWAM 1.97, ECMWF WAM 1.96 | media |
| ZA-EC-PE | 0.06 | GFS-Wave 0,25° 2.18, MFWAM 1.99, ECMWF WAM 2.15 | media |
| NO-N | 0.06 | GFS-Wave 0,25° 1.82, MFWAM 1.73, ECMWF WAM 1.76 | media |
| ZA-KZN-DBN | 0.06 | GFS-Wave 0,25° 1.80, MFWAM 1.83, ECMWF WAM 1.70 | media |
| ZA-KZN-S | 0.05 | GFS-Wave 0,25° 1.93, MFWAM 1.95, ECMWF WAM 2.08 | media |
| BR-NE-PE | 0.05 | GFS-Wave 0,16° 1.01, GFS-Wave 0,25° 1.10, MFWAM 1.14, ECMWF WAM 1.09 | media |
| LK-S | 0.05 | GFS-Wave 0,16° 1.63, GFS-Wave 0,25° 1.65, MFWAM 1.74, ECMWF WAM 1.59 | media |
| PE-LIM | 0.05 | GFS-Wave 0,16° 1.45, MFWAM 1.35, ECMWF WAM 1.38 | media |
| NZ-NTL | 0.05 | GFS-Wave 0,25° 2.72, MFWAM 2.62, ECMWF WAM 2.55 | media |
| SV-LIB | 0.04 | GFS-Wave 0,16° 1.15, MFWAM 1.20, ECMWF WAM 1.15 | media |
| ZA-EC-JB | 0.04 | MFWAM 1.62, ECMWF WAM 1.57 | media |
| CL-CEN | 0.04 | MFWAM 1.65, ECMWF WAM 1.77 | media |
| MG-ALL | 0.04 | GFS-Wave 0,25° 2.04, MFWAM 1.98, ECMWF WAM 2.04 | media |
| ID-KRU | 0.04 | GFS-Wave 0,16° 1.86, MFWAM 1.96, ECMWF WAM 1.89 | media |
| LR-ALL | 0.04 | GFS-Wave 0,16° 1.14, GFS-Wave 0,25° 1.18, MFWAM 1.16, ECMWF WAM 1.13 | media |
| NZ-TAR | 0.04 | GFS-Wave 0,25° 1.84, MFWAM 1.87, ECMWF WAM 1.82 | media |
| MQ-ALL | 0.03 | GFS-Wave 0,16° 1.21, GFS-Wave 0,25° 1.22, MFWAM 1.21, ECMWF WAM 1.20 | media |
| PE-SUR | 0.02 | MFWAM 1.42, ECMWF WAM 1.36 | media |
| WS-ALL | 0.01 | MFWAM 2.27, ECMWF WAM 2.23 | media |

## Control de convenciones por fuente

Promedios ponderados por horas sobre todas las boyas de cada fuente. `Tp` = modelo − período pico de la boya; `Tm` = `wave_period` del modelo − período medio de la boya (NDBC APD, CDIP Ta, AODN WPFM, MI EnergyPeriod: no son el mismo momento espectral); `dir` = error medio absoluto de dirección (de dónde vienen); `sesgo dir` = media circular de modelo − boya (cerca de ±180° indicaría una boya en convención "hacia").

| Fuente | Modelo | horas | Tp s | Tm s | dir ° | sesgo dir ° |
|---|---|---|---|---|---|---|
| AODN / IMOS | ECMWF WAM | 10535 | 0.2 | 2.9 | 18 | 4 |
| AODN / IMOS | MFWAM | 10535 | -2.4 | 2.3 | 19 | 3 |
| AODN / IMOS | GFS-Wave 0,25° | 10535 | -0.5 | 4.3 | 19 | 4 |
| CDIP | ECMWF WAM | 30127 | -0.4 | 2.4 | 20 | 2 |
| CDIP | MFWAM | 28681 | -1.7 | 2.8 | 21 | -2 |
| CDIP | GFS-Wave 0,16° | 30127 | 0.7 | 5.2 | 23 | -8 |
| CDIP | GFS-Wave 0,25° | 19398 | 0.4 | 4.1 | 22 | -5 |
| Marine Institute | DWD EWAM | 1446 | -1.1 | 1.1 | 14 | -3 |
| Marine Institute | ECMWF WAM | 3615 | -0.5 | 1.3 | 10 | -2 |
| Marine Institute | MFWAM | 3615 | -1.5 | 1.6 | 12 | -2 |
| Marine Institute | GFS-Wave 0,16° | 2169 | 0.0 | 3.4 | 12 | 3 |
| Marine Institute | GFS-Wave 0,25° | 3615 | -0.3 | 2.8 | 14 | 1 |
| NOAA NDBC | ECMWF WAM | 13823 | -0.6 | 1.9 | 19 | -3 |
| NOAA NDBC | MFWAM | 12447 | -1.2 | 2.2 | 20 | -3 |
| NOAA NDBC | GFS-Wave 0,16° | 13823 | 0.6 | 4.2 | 22 | -10 |
| NOAA NDBC | GFS-Wave 0,25° | 13100 | 0.5 | 3.9 | 20 | -10 |

## Próximos pasos

- Fuentes con cuenta o clave que faltan: **Copernicus Marine** (In Situ TAC: boyas de Europa, Brasil, Sudáfrica, Japón), **CANDHIS** (Francia), **Channel Coastal Observatory** (Inglaterra), **Puertos del Estado** (España), **IH Portugal**, **SIMCOSTA/PNBOIA** directo (Brasil), **CMEMS** para Uruguay y Argentina.
- Los meses cambian el ganador (verano/invierno, swell/viento): mirar varias corridas mensuales antes de pasar una sugerencia a `models.csv` por PR.
- Las boyas lejos de la costa validan el modelo en mar abierto, no el punto de olas del pico: preferir boyas someras (CDIP, AODN, MI) cuando haya.
- Viento: sin validar (sigue `gfs_seamless`).
