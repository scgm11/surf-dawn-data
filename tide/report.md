# Mareas: reporte del último build

Generado 2026-10-14 21:45 UTC por `tools/tide/build_tides.py`. Años: 2026, 2027. Correcciones nodales: pyTMD `FES`.

## Resumen

- Puertos nuevos: 425 (got 162, imi 10, jma 9, linz 20, noaa 57, ticon 167); más los 3 de Uruguay y Brasil, sin cambios.
- Regiones con puerto: 208 de 208 (más UY-MAL, UY-ROC, BR-SC-FLN y BR-SC-SUL, congeladas); sin puerto: 0.
- Picos con puerto: 2326 de 2437.
- Archivos: 10625, 28.2 MB (cada mes ≤ 6144 bytes; el mayor: 3343).
- Marine Institute: datum `LAT`; predicciones hasta 2029-01-01T00:20:00Z.

## Validación TICON-3 vs NOAA

Predicción horaria 2026 de las constantes de TICON-3 (pyTMD, cada juego de correcciones nodales) contra las predicciones de NOAA en la misma estación; RMS en cm de la diferencia, cada serie sin su media. "sin Sa/Ssa": sin los términos anual y semianual de TICON (son en parte meteorológicos).

| Estación NOAA | Gauge TICON-3 | Registro | Rango NOAA | FES | GOT | perth3 | OTIS | sin Sa/Ssa (FES) |
|---|---|---|---|---|---|---|---|---|
| 9410230 La Jolla (Scripps Institution Wharf), CA | gesla.usgs, a 0.02 km | 35428 días | 275 cm | 1.8 | 1.8 | 1.8 | 1.8 | 1.8 |
| 1612340 HONOLULU, HI | gesla.meds, a 0.48 km | 39293 días | 95 cm | 1.8 | 1.8 | 1.8 | 1.8 | 1.8 |
| 9414290 SAN FRANCISCO (Golden Gate), CA | gesla.jodc_jma, a 0.04 km | 45167 días | 278 cm | 3.5 | 3.5 | 3.6 | 3.6 | 3.5 |
| 8518750 NEW YORK (The Battery), NY | gesla.uhslc, a 0.05 km | 36981 días | 222 cm | 3.7 | 3.7 | 3.7 | 3.9 | 3.7 |
| 8724580 KEY WEST, FL | gesla.uhslc, a 0.30 km | 38697 días | 98 cm | 1.6 | 1.6 | 1.6 | 1.8 | 1.6 |
| 1910000 SUVA HARBOR, Viti Levu Island | gesla.jodc_jma, a 0.03 km | 1095 días | 190 cm | 2.4 | 2.4 | 2.4 | 2.5 | 2.4 |

## Validación GOT5.6 vs tablas oficiales

El modelo global (nivel 6, donde no hay mareógrafo cerca) predicho 2026 en la posición de estaciones con tabla oficial, contra esa tabla: RMS en cm de la diferencia horaria, cada serie sin su media, y cuánto del rango de la tabla da el modelo. En el mismo mareógrafo, el lugar más difícil para un modelo global (puertos, bahías, el Río de la Plata). Mediana del RMS: 7.3 cm.

| Estación | Rango oficial | RMS GOT5.6 | Rango modelo / oficial |
|---|---|---|---|
| noaa-9410230 La Jolla (Scripps Institution Wharf), CA | 275 cm | 6.6 | 0.95 |
| noaa-1612340 HONOLULU, HI | 95 cm | 5.5 | 1.05 |
| noaa-9414290 SAN FRANCISCO (Golden Gate), CA | 278 cm | 6.6 | 1.02 |
| noaa-8518750 NEW YORK (The Battery), NY | 222 cm | 19.6 | 0.85 |
| noaa-8724580 KEY WEST, FL | 98 cm | 11.3 | 0.96 |
| noaa-9447130 SEATTLE (Madison St.), Elliott Bay, WA | 522 cm | 137.1 | 0.84 |
| jma-wn 稚内 (JMA WN) | 49 cm | 7.0 | 0.74 |
| jma-ke 枝幸 (JMA KE) | 133 cm | 5.5 | 0.86 |
| jma-a0 紋別 (JMA A0) | 161 cm | 4.8 | 0.97 |
| linz-akaroa Akaroa | 230 cm | 8.4 | 1.01 |
| linz-anakakata-bay Anakakata Bay | 179 cm | 5.4 | 1.04 |
| linz-anawhata Anawhata | 300 cm | 7.3 | 1.05 |
| imi-achill-island Achill Island (modelado) | 441 cm | 11.3 | 0.96 |
| imi-aranmore Aranmore | 416 cm | 6.7 | 0.99 |
| imbituba Porto de Imbituba (DHN) | 100 cm | 7.7 | 0.97 |
| la-paloma La Paloma (SOHMA) | 74 cm | 10.4 | 1.03 |
| punta-del-este Punta del Este (SOHMA) | 61 cm | 7.3 | 0.84 |

## Puertos

| Clave | Fuente | Nombre | Datum | Rango (cm) | Horas completadas | Ajuste 30 períodos (RMS cm) |
|---|---|---|---|---|---|---|
| got-03f20d | got5.6:-32.181,152.524 | GOT5.6 32.181S 152.524E (AU-NSW-MN) | MSL+95 cm (modelo) | 5..210 | — | 1.1 |
| got-041b3c | got5.6:-32.682,28.383 | GOT5.6 32.682S 28.383E (ZA-EC-WLD) | MSL+106 cm (modelo) | 5..212 | — | 1.4 |
| got-043c05 | got5.6:32.643,-16.955 | GOT5.6 32.643N 16.955W (PT-MAD) | MSL+131 cm (modelo) | 6..264 | — | 1.4 |
| got-04911c | got5.6:-3.677,-80.670 | GOT5.6 3.677S 80.670W (PE-NOR) | MSL+127 cm (modelo) | 6..246 | — | 1.3 |
| got-04ac46 | got5.6:-35.344,-72.430 | GOT5.6 35.344S 72.430W (CL-MAU) | MSL+87 cm (modelo) | 5..191 | — | 1.1 |
| got-0548a0 | got5.6:18.630,110.222 | GOT5.6 18.630N 110.222E (CN-HAI) | MSL+102 cm (modelo) | 5..202 | — | 1.5 |
| got-06d168 | got5.6:9.876,-85.628 | GOT5.6 9.876N 85.628W (CR-NIC) | MSL+151 cm (modelo) | 6..301 | — | 1.5 |
| got-07bdb8 | got5.6:-33.605,26.922 | GOT5.6 33.605S 26.922E (ZA-EC-PE) | MSL+104 cm (modelo) | 6..209 | — | 1.4 |
| got-0a9164 | got5.6:-2.497,-44.248 | GOT5.6 2.497S 44.248W (BR-NE-CE) | MSL+277 cm (modelo) | 6..545 | — | 2.5 |
| got-0bc1cc | got5.6:43.564,-6.703 | GOT5.6 43.564N 6.703W (ES-AST) | MSL+226 cm (modelo) | 5..447 | — | 2.5 |
| got-0d6795 | got5.6:-39.390,-73.215 | GOT5.6 39.390S 73.215W (CL-SUR) | MSL+90 cm (modelo) | 5..199 | — | 1.2 |
| got-0e82ac | got5.6:33.245,126.412 | GOT5.6 33.245N 126.412E (KR-ALL) | MSL+160 cm (modelo) | 5..308 | — | 1.8 |
| got-0f94d8 | got5.6:-26.846,32.895 | GOT5.6 26.846S 32.895E (MZ-S) | MSL+136 cm (modelo) | 6..269 | — | 1.9 |
| got-11c637 | got5.6:-29.544,-49.875 | GOT5.6 29.544S 49.875W (BR-RS) | MSL+52 cm (modelo) | 6..95 | — | 1.2 |
| got-125cb8 | got5.6:-8.724,114.350 | GOT5.6 8.724S 114.350E (ID-JAV-E) | MSL+152 cm (modelo) | 6..304 | — | 2.1 |
| got-1426bf | got5.6:-18.426,-39.704 | GOT5.6 18.426S 39.704W (BR-ES) | MSL+167 cm (modelo) | 5..327 | — | 2.2 |
| got-1682f6 | got5.6:9.818,126.170 | GOT5.6 9.818N 126.170E (PH-SIA) | MSL+126 cm (modelo) | 6..226 | — | 1.4 |
| got-16f772 | got5.6:-28.957,31.780 | GOT5.6 28.957S 31.780E (ZA-KZN-N) | MSL+123 cm (modelo) | 6..245 | — | 1.7 |
| got-1940fc | got5.6:-40.812,-65.085 | GOT5.6 40.812S 65.085W (AR-SUR) | MSL+446 cm (modelo) | 6..873 | — | 4.8 |
| got-1a2bc4 | got5.6:30.640,-9.830 | GOT5.6 30.640N 9.830W (MA-TAG) | MSL+172 cm (modelo) | 5..350 | — | 1.9 |
| got-1a5319 | got5.6:-20.659,-40.488 | GOT5.6 20.659S 40.488W (BR-ES) | MSL+102 cm (modelo) | 6..188 | — | 1.3 |
| got-1afd1e | got5.6:-11.000,-37.040 | GOT5.6 11.000S 37.040W (BR-NE-PE) | MSL+135 cm (modelo) | 6..264 | — | 1.5 |
| got-1c5103 | got5.6:33.597,-7.679 | GOT5.6 33.597N 7.679W (MA-N) | MSL+178 cm (modelo) | 5..359 | — | 2.0 |
| got-1e8580 | got5.6:-19.532,169.268 | GOT5.6 19.532S 169.268E (VU-ALL) | MSL+93 cm (modelo) | 5..160 | — | 0.9 |
| got-210825 | got5.6:-34.169,115.030 | GOT5.6 34.169S 115.030E (AU-WA-MR) | MSL+61 cm (modelo) | 5..117 | — | 1.1 |
| got-2175da | got5.6:10.003,-83.027 | GOT5.6 10.003N 83.027W (CR-CAR) | MSL+34 cm (modelo) | 5..64 | — | 0.4 |
| got-22dcfd | got5.6:-30.092,-71.360 | GOT5.6 30.092S 71.360W (CL-CEN) | MSL+80 cm (modelo) | 6..177 | — | 1.0 |
| got-23237f | got5.6:-41.880,148.296 | GOT5.6 41.880S 148.296E (AU-TAS) | MSL+90 cm (modelo) | 6..168 | — | 1.0 |
| got-243beb | got5.6:-22.942,-42.359 | GOT5.6 22.942S 42.359W (BR-RJL) | MSL+83 cm (modelo) | 6..145 | — | 1.1 |
| got-260f66 | got5.6:-14.347,-38.980 | GOT5.6 14.347S 38.980W (BR-BA) | MSL+132 cm (modelo) | 5..255 | — | 1.5 |
| got-2613c9 | got5.6:-37.230,-56.948 | GOT5.6 37.230S 56.948W (AR-BAN) | MSL+78 cm (modelo) | 5..171 | — | 1.5 |
| got-26250e | got5.6:0.870,-79.850 | GOT5.6 0.870N 79.850W (EC-COS) | MSL+185 cm (modelo) | 5..366 | — | 1.9 |
| got-28a8b3 | got5.6:-9.738,119.314 | GOT5.6 9.738S 119.314E (ID-SMB) | MSL+180 cm (modelo) | 5..358 | — | 2.5 |
| got-295992 | got5.6:-18.162,177.504 | GOT5.6 18.162S 177.504E (FJ-SOU) | MSL+105 cm (modelo) | 5..199 | — | 0.9 |
| got-2c8cf0 | got5.6:-41.053,-62.823 | GOT5.6 41.053S 62.823W (AR-SUR) | MSL+245 cm (modelo) | 5..476 | — | 2.7 |
| got-2e40a2 | got5.6:-8.735,115.836 | GOT5.6 8.735S 115.836E (ID-LOM) | MSL+122 cm (modelo) | 6..243 | — | 1.8 |
| got-2ee07d | got5.6:18.271,109.723 | GOT5.6 18.271N 109.723E (CN-HAI) | MSL+104 cm (modelo) | 6..209 | — | 1.7 |
| got-2f1c38 | got5.6:-7.063,106.508 | GOT5.6 7.063S 106.508E (ID-JAV-W) | MSL+80 cm (modelo) | 5..169 | — | 1.2 |
| got-30731c | got5.6:-6.880,-79.950 | GOT5.6 6.880S 79.950W (PE-LLB) | MSL+91 cm (modelo) | 5..177 | — | 1.0 |
| got-332a05 | got5.6:-20.237,-70.140 | GOT5.6 20.237S 70.140W (CL-NOR) | MSL+66 cm (modelo) | 6..149 | — | 1.0 |
| got-3334f6 | got5.6:-25.932,153.189 | GOT5.6 25.932S 153.189E (AU-QLD-SC) | MSL+103 cm (modelo) | 6..228 | — | 1.3 |
| got-360725 | got5.6:30.198,-9.639 | GOT5.6 30.198N 9.639W (MA-S) | MSL+171 cm (modelo) | 5..347 | — | 1.9 |
| got-38e06a | got5.6:-34.078,22.954 | GOT5.6 34.078S 22.954E (ZA-WC-GR) | MSL+114 cm (modelo) | 5..233 | — | 1.6 |
| got-39b84c | got5.6:0.569,97.734 | GOT5.6 0.569N 97.734E (ID-NIA) | MSL+51 cm (modelo) | 6..111 | — | 0.8 |
| got-3ba912 | got5.6:6.753,-11.379 | GOT5.6 6.753N 11.379W (LR-ALL) | MSL+82 cm (modelo) | 6..166 | — | 0.9 |
| got-3cd5c4 | got5.6:34.257,-6.689 | GOT5.6 34.257N 6.689W (MA-N) | MSL+178 cm (modelo) | 5..359 | — | 2.0 |
| got-3d80b7 | got5.6:10.240,-85.842 | GOT5.6 10.240N 85.842W (CR-GUA) | MSL+147 cm (modelo) | 6..293 | — | 1.4 |
| got-439ad8 | got5.6:-22.115,14.268 | GOT5.6 22.115S 14.268E (NA-ERO) | MSL+97 cm (modelo) | 6..189 | — | 1.1 |
| got-441786 | got5.6:43.443,-4.048 | GOT5.6 43.443N 4.048W (ES-CAN) | MSL+235 cm (modelo) | 6..464 | — | 2.6 |
| got-47f025 | got5.6:-33.743,-53.370 | GOT5.6 33.743S 53.370W (BR-RS-SUL) | MSL+59 cm (modelo) | 5..119 | — | 1.1 |
| got-48d2ad | got5.6:14.752,-17.509 | GOT5.6 14.752N 17.509W (SN-ALL) | MSL+81 cm (modelo) | 6..164 | — | 0.9 |
| got-4b911c | got5.6:-34.055,24.925 | GOT5.6 34.055S 24.925E (ZA-EC-JB) | MSL+105 cm (modelo) | 6..212 | — | 1.4 |
| got-4e1d64 | got5.6:2.919,73.570 | GOT5.6 2.919N 73.570E (MV-CEN) | MSL+65 cm (modelo) | 6..121 | — | 1.0 |
| got-528c98 | got5.6:13.077,74.787 | GOT5.6 13.077N 74.787E (IN-W) | MSL+126 cm (modelo) | 6..213 | — | 1.4 |
| got-529ee2 | got5.6:15.765,121.574 | GOT5.6 15.765N 121.574E (PH-LUZ) | MSL+116 cm (modelo) | 6..211 | — | 1.3 |
| got-56aa18 | got5.6:-25.030,46.999 | GOT5.6 25.030S 46.999E (MG-ALL) | MSL+33 cm (modelo) | 6..64 | — | 0.6 |
| got-56d0a4 | got5.6:-2.410,99.855 | GOT5.6 2.410S 99.855E (ID-MEN) | MSL+66 cm (modelo) | 5..146 | — | 1.0 |
| got-56fcd4 | got5.6:15.861,-97.063 | GOT5.6 15.861N 97.063W (MX-OAX) | MSL+67 cm (modelo) | 6..143 | — | 0.8 |
| got-57076f | got5.6:-29.493,31.275 | GOT5.6 29.493S 31.275E (ZA-KZN-N) | MSL+117 cm (modelo) | 5..234 | — | 1.6 |
| got-5888b8 | got5.6:-36.070,-72.800 | GOT5.6 36.070S 72.800W (CL-MAU) | MSL+87 cm (modelo) | 6..192 | — | 1.1 |
| got-5c5f01 | got5.6:-22.752,-41.912 | GOT5.6 22.752S 41.912W (BR-RJL) | MSL+89 cm (modelo) | 5..159 | — | 1.1 |
| got-5e72ab | got5.6:7.619,-81.243 | GOT5.6 7.619N 81.243W (PA-PAC) | MSL+200 cm (modelo) | 6..397 | — | 2.0 |
| got-63d295 | got5.6:-33.023,27.919 | GOT5.6 33.023S 27.919E (ZA-EC-PE) | MSL+105 cm (modelo) | 6..210 | — | 1.4 |
| got-642556 | got5.6:-29.976,-50.121 | GOT5.6 29.976S 50.121W (BR-RS) | MSL+48 cm (modelo) | 6..91 | — | 1.2 |
| got-668790 | got5.6:-34.129,-71.998 | GOT5.6 34.129S 71.998W (CL-PIC) | MSL+84 cm (modelo) | 5..186 | — | 1.1 |
| got-684e80 | got5.6:-8.973,116.729 | GOT5.6 8.973S 116.729E (ID-SBW) | MSL+157 cm (modelo) | 5..314 | — | 2.3 |
| got-68a040 | got5.6:-27.720,114.151 | GOT5.6 27.720S 114.151E (AU-WA-NW) | MSL+56 cm (modelo) | 5..111 | — | 1.1 |
| got-6cb02d | got5.6:-37.995,-57.544 | GOT5.6 37.995S 57.544W (AR-MDP) | MSL+89 cm (modelo) | 6..187 | — | 1.6 |
| got-6d1313 | got5.6:23.400,-110.211 | GOT5.6 23.400N 110.211W (MX-BCS) | MSL+116 cm (modelo) | 5..220 | — | 1.6 |
| got-6f9c71 | got5.6:12.760,-87.450 | GOT5.6 12.760N 87.450W (NI-NW) | MSL+154 cm (modelo) | 6..310 | — | 1.5 |
| got-707910 | got5.6:9.382,-82.235 | GOT5.6 9.382N 82.235W (PA-BDT) | MSL+33 cm (modelo) | 6..64 | — | 0.5 |
| got-70a590 | got5.6:43.427,-4.893 | GOT5.6 43.427N 4.893W (ES-AST) | MSL+235 cm (modelo) | 5..464 | — | 2.7 |
| got-713511 | got5.6:20.214,-87.429 | GOT5.6 20.214N 87.429W (MX-CAR) | MSL+22 cm (modelo) | 5..38 | — | 0.4 |
| got-72b502 | got5.6:13.659,124.398 | GOT5.6 13.659N 124.398E (PH-EAS) | MSL+125 cm (modelo) | 5..223 | — | 1.4 |
| got-770eaa | got5.6:-7.148,-34.796 | GOT5.6 7.148S 34.796W (BR-NE-RN) | MSL+143 cm (modelo) | 6..283 | — | 1.5 |
| got-78d608 | got5.6:-38.780,143.400 | GOT5.6 38.780S 143.400E (AU-VIC-W) | MSL+94 cm (modelo) | 6..172 | — | 1.3 |
| got-798f17 | got5.6:-38.589,-58.740 | GOT5.6 38.589S 58.740W (AR-MDP) | MSL+103 cm (modelo) | 6..205 | — | 1.4 |
| got-799775 | got5.6:-10.893,122.812 | GOT5.6 10.893S 122.812E (ID-ROT) | MSL+193 cm (modelo) | 5..380 | — | 2.7 |
| got-7a487c | got5.6:-26.596,153.107 | GOT5.6 26.596S 153.107E (AU-QLD-SC) | MSL+101 cm (modelo) | 5..224 | — | 1.3 |
| got-7c798b | got5.6:11.196,-60.800 | GOT5.6 11.196N 60.800W (TT-ALL) | MSL+63 cm (modelo) | 6..116 | — | 0.7 |
| got-7d5db3 | got5.6:-38.270,-57.840 | GOT5.6 38.270S 57.840W (AR-MDP) | MSL+96 cm (modelo) | 6..193 | — | 1.5 |
| got-82a78a | got5.6:-8.816,118.376 | GOT5.6 8.816S 118.376E (ID-SBW) | MSL+176 cm (modelo) | 5..351 | — | 2.5 |
| got-87528f | got5.6:25.420,-76.623 | GOT5.6 25.420N 76.623W (BS-ALL) | MSL+65 cm (modelo) | 5..138 | — | 0.6 |
| got-8a708f | got5.6:-8.062,-79.123 | GOT5.6 8.062S 79.123W (PE-LLB) | MSL+83 cm (modelo) | 5..161 | — | 1.0 |
| got-8ae671 | got5.6:63.405,-19.071 | GOT5.6 63.405N 19.071W (IS-ALL) | MSL+151 cm (modelo) | 5..307 | — | 1.8 |
| got-8af89e | got5.6:-32.811,17.885 | GOT5.6 32.811S 17.885E (ZA-WC-WCO) | MSL+99 cm (modelo) | 5..202 | — | 1.3 |
| got-8bd957 | got5.6:11.300,-85.910 | GOT5.6 11.300N 85.910W (NI-RIV) | MSL+144 cm (modelo) | 6..288 | — | 1.4 |
| got-8d76ed | got5.6:26.704,-113.578 | GOT5.6 26.704N 113.578W (MX-BCS-N) | MSL+132 cm (modelo) | 6..258 | — | 1.8 |
| got-913e13 | got5.6:-31.643,29.550 | GOT5.6 31.643S 29.550E (ZA-EC-WLD) | MSL+108 cm (modelo) | 6..216 | — | 1.4 |
| got-91ed50 | got5.6:-24.366,113.406 | GOT5.6 24.366S 113.406E (AU-WA-GAS) | MSL+85 cm (modelo) | 6..161 | — | 1.2 |
| got-91f084 | got5.6:10.850,-85.801 | GOT5.6 10.850N 85.801W (CR-GUA) | MSL+147 cm (modelo) | 6..294 | — | 1.4 |
| got-94cadf | got5.6:6.800,81.820 | GOT5.6 6.800N 81.820E (LK-E) | MSL+21 cm (modelo) | 6..35 | — | 0.3 |
| got-95d729 | got5.6:9.634,-82.712 | GOT5.6 9.634N 82.712W (CR-CAR) | MSL+37 cm (modelo) | 6..67 | — | 0.4 |
| got-964843 | got5.6:5.998,80.269 | GOT5.6 5.998N 80.269E (LK-S) | MSL+41 cm (modelo) | 5..79 | — | 0.7 |
| got-9803e3 | got5.6:-23.760,-45.870 | GOT5.6 23.760S 45.870W (BR-SP) | MSL+90 cm (modelo) | 6..165 | — | 2.4 |
| got-9b0ee7 | got5.6:11.605,125.440 | GOT5.6 11.605N 125.440E (PH-EAS) | MSL+99 cm (modelo) | 5..183 | — | 1.1 |
| got-9decc4 | got5.6:-39.774,-73.400 | GOT5.6 39.774S 73.400W (CL-SUR) | MSL+91 cm (modelo) | 6..200 | — | 1.2 |
| got-a0b028 | got5.6:-28.125,32.558 | GOT5.6 28.125S 32.558E (ZA-KZN-N) | MSL+127 cm (modelo) | 6..253 | — | 1.8 |
| got-a0b2f5 | got5.6:-30.240,-50.230 | GOT5.6 30.240S 50.230W (BR-RS) | MSL+45 cm (modelo) | 6..87 | — | 1.2 |
| got-a1d318 | got5.6:22.900,121.233 | GOT5.6 22.900N 121.233E (TW-E) | MSL+113 cm (modelo) | 5..208 | — | 1.3 |
| got-a65a9d | got5.6:40.133,-8.874 | GOT5.6 40.133N 8.874W (PT-CEN) | MSL+185 cm (modelo) | 5..373 | — | 2.1 |
| got-a806af | got5.6:26.250,-112.480 | GOT5.6 26.250N 112.480W (MX-BCS-N) | MSL+134 cm (modelo) | 5..260 | — | 1.8 |
| got-a8e5b2 | got5.6:-5.877,-35.173 | GOT5.6 5.877S 35.173W (BR-NE-RN) | MSL+145 cm (modelo) | 5..286 | — | 1.6 |
| got-a905b1 | got5.6:-32.083,132.989 | GOT5.6 32.083S 132.989E (AU-SA-EYR) | MSL+83 cm (modelo) | 5..178 | — | 3.9 |
| got-a95390 | got5.6:24.027,121.627 | GOT5.6 24.027N 121.627E (TW-E) | MSL+108 cm (modelo) | 5..193 | — | 1.3 |
| got-a989b9 | got5.6:37.969,128.760 | GOT5.6 37.969N 128.760E (KR-ALL) | MSL+32 cm (modelo) | 6..52 | — | 0.3 |
| got-aa96f4 | got5.6:-9.667,-35.710 | GOT5.6 9.667S 35.710W (BR-NE-PE) | MSL+138 cm (modelo) | 5..269 | — | 1.5 |
| got-ab6d4c | got5.6:-23.650,43.635 | GOT5.6 23.650S 43.635E (MG-ALL) | MSL+158 cm (modelo) | 5..314 | — | 2.3 |
| got-addc69 | got5.6:20.955,-105.356 | GOT5.6 20.955N 105.356W (MX-NAY) | MSL+101 cm (modelo) | 6..185 | — | 1.4 |
| got-af9925 | got5.6:8.731,76.703 | GOT5.6 8.731N 76.703E (IN-W) | MSL+64 cm (modelo) | 6..115 | — | 0.9 |
| got-b07ca8 | got5.6:19.415,-155.909 | GOT5.6 19.415N 155.909W (US-HI-BIG) | MSL+49 cm (modelo) | 5..113 | — | 0.7 |
| got-b0dc74 | got5.6:-30.200,30.807 | GOT5.6 30.200S 30.807E (ZA-KZN-S) | MSL+113 cm (modelo) | 6..224 | — | 1.5 |
| got-b18ed4 | got5.6:-12.577,-38.003 | GOT5.6 12.577S 38.003W (BR-BA) | MSL+134 cm (modelo) | 6..259 | — | 1.5 |
| got-b2745e | got5.6:-38.999,-61.295 | GOT5.6 38.999S 61.295W (AR-SUR) | MSL+166 cm (modelo) | 6..308 | — | 1.9 |
| got-b32477 | got5.6:-8.915,116.355 | GOT5.6 8.915S 116.355E (ID-LOM) | MSL+157 cm (modelo) | 6..311 | — | 2.2 |
| got-b461dd | got5.6:5.713,-77.264 | GOT5.6 5.713N 77.264W (CO-PAC) | MSL+202 cm (modelo) | 5..401 | — | 2.1 |
| got-b495c3 | got5.6:12.787,80.255 | GOT5.6 12.787N 80.255E (IN-E) | MSL+66 cm (modelo) | 5..132 | — | 0.8 |
| got-b68b0a | got5.6:-32.312,18.324 | GOT5.6 32.312S 18.324E (ZA-WC-WCO) | MSL+105 cm (modelo) | 5..215 | — | 1.4 |
| got-b6d772 | got5.6:8.456,-79.966 | GOT5.6 8.456N 79.966W (PA-PAC) | MSL+263 cm (modelo) | 6..518 | — | 2.7 |
| got-b81c05 | got5.6:-40.575,-73.736 | GOT5.6 40.575S 73.736W (CL-SUR) | MSL+90 cm (modelo) | 6..199 | — | 1.2 |
| got-bbafe3 | got5.6:31.359,-9.809 | GOT5.6 31.359N 9.809W (MA-TAG) | MSL+176 cm (modelo) | 6..357 | — | 1.9 |
| got-bea209 | got5.6:-42.450,171.198 | GOT5.6 42.450S 171.198E (NZ-WC) | MSL+166 cm (modelo) | 5..327 | — | 1.5 |
| got-c1e848 | got5.6:-2.674,141.299 | GOT5.6 2.674S 141.299E (PG-ALL) | MSL+98 cm (modelo) | 5..150 | — | 1.1 |
| got-c38d4b | got5.6:16.062,108.249 | GOT5.6 16.062N 108.249E (VN-ALL) | MSL+76 cm (modelo) | 5..129 | — | 1.0 |
| got-c504a0 | got5.6:20.769,-105.526 | GOT5.6 20.769N 105.526W (MX-NAY) | MSL+100 cm (modelo) | 6..182 | — | 1.4 |
| got-c73835 | got5.6:10.500,-67.690 | GOT5.6 10.500N 67.690W (VE-ALL) | MSL+29 cm (modelo) | 5..60 | — | 0.4 |
| got-c774f7 | got5.6:-1.900,99.300 | GOT5.6 1.900S 99.300E (ID-MEN) | MSL+61 cm (modelo) | 6..135 | — | 0.9 |
| got-c939f5 | got5.6:-30.891,30.354 | GOT5.6 30.891S 30.354E (ZA-KZN-S) | MSL+110 cm (modelo) | 5..220 | — | 1.5 |
| got-c94e22 | got5.6:-26.630,-48.678 | GOT5.6 26.630S 48.678W (BR-SC-NOR) | MSL+75 cm (modelo) | 6..150 | — | 2.8 |
| got-c96e4a | got5.6:11.130,-63.850 | GOT5.6 11.130N 63.850W (VE-ALL) | MSL+37 cm (modelo) | 6..71 | — | 0.4 |
| got-ca232b | got5.6:33.790,-7.175 | GOT5.6 33.790N 7.175W (MA-N) | MSL+178 cm (modelo) | 6..359 | — | 2.0 |
| got-cb31f0 | got5.6:6.100,-77.420 | GOT5.6 6.100N 77.420W (CO-PAC) | MSL+204 cm (modelo) | 5..406 | — | 2.1 |
| got-cb786a | got5.6:29.430,-10.130 | GOT5.6 29.430N 10.130W (MA-S) | MSL+173 cm (modelo) | 6..350 | — | 1.9 |
| got-cff16a | got5.6:-0.939,-80.733 | GOT5.6 0.939S 80.733W (EC-COS) | MSL+159 cm (modelo) | 5..314 | — | 1.6 |
| got-d032d9 | got5.6:-23.881,113.488 | GOT5.6 23.881S 113.488E (AU-WA-GAS) | MSL+84 cm (modelo) | 5..162 | — | 1.2 |
| got-d2f680 | got5.6:11.243,-73.568 | GOT5.6 11.243N 73.568W (CO-CAR) | MSL+25 cm (modelo) | 6..57 | — | 0.5 |
| got-d30559 | got5.6:-5.305,103.992 | GOT5.6 5.305S 103.992E (ID-KRU) | MSL+69 cm (modelo) | 6..150 | — | 1.0 |
| got-d42e6d | got5.6:-36.580,-56.690 | GOT5.6 36.580S 56.690W (AR-BAN) | MSL+81 cm (modelo) | 5..164 | — | 1.4 |
| got-d43a78 | got5.6:-20.330,-40.285 | GOT5.6 20.330S 40.285W (BR-ES) | MSL+103 cm (modelo) | 6..189 | — | 1.2 |
| got-d5b42a | got5.6:-8.218,111.095 | GOT5.6 8.218S 111.095E (ID-JAV-E) | MSL+119 cm (modelo) | 5..244 | — | 1.7 |
| got-d6cb2e | got5.6:5.968,80.685 | GOT5.6 5.968N 80.685E (LK-S) | MSL+38 cm (modelo) | 6..72 | — | 0.6 |
| got-d76764 | got5.6:0.912,97.263 | GOT5.6 0.912N 97.263E (ID-NIA) | MSL+48 cm (modelo) | 6..105 | — | 0.8 |
| got-d8f761 | got5.6:-25.697,-48.467 | GOT5.6 25.697S 48.467W (BR-SC-NOR) | MSL+106 cm (modelo) | 5..219 | — | 4.4 |
| got-ddd9f6 | got5.6:-7.410,-79.580 | GOT5.6 7.410S 79.580W (PE-LLB) | MSL+88 cm (modelo) | 6..169 | — | 1.0 |
| got-def45c | got5.6:-34.923,-72.174 | GOT5.6 34.923S 72.174W (CL-MAU) | MSL+86 cm (modelo) | 5..189 | — | 1.1 |
| got-dfa80c | got5.6:-34.516,-72.041 | GOT5.6 34.516S 72.041W (CL-PIC) | MSL+86 cm (modelo) | 6..189 | — | 1.1 |
| got-dfbfb8 | got5.6:-27.115,-48.605 | GOT5.6 27.115S 48.605W (BR-SC-NOR) | MSL+70 cm (modelo) | 5..133 | — | 2.3 |
| got-e07ca7 | got5.6:-29.855,31.049 | GOT5.6 29.855S 31.049E (ZA-KZN-DBN) | MSL+114 cm (modelo) | 5..227 | — | 1.5 |
| got-e4029c | got5.6:-31.980,29.153 | GOT5.6 31.980S 29.153E (ZA-EC-WLD) | MSL+107 cm (modelo) | 5..215 | — | 1.4 |
| got-e49ea1 | got5.6:43.951,-64.818 | GOT5.6 43.951N 64.818W (CA-NS) | MSL+114 cm (modelo) | 5..219 | — | 1.0 |
| got-e51b06 | got5.6:-23.858,35.549 | GOT5.6 23.858S 35.549E (MZ-INH) | MSL+167 cm (modelo) | 6..330 | — | 2.4 |
| got-e5aa1d | got5.6:11.978,79.833 | GOT5.6 11.978N 79.833E (IN-E) | MSL+61 cm (modelo) | 5..120 | — | 0.7 |
| got-e7ff80 | got5.6:12.378,-87.042 | GOT5.6 12.378N 87.042W (NI-NW) | MSL+143 cm (modelo) | 6..288 | — | 1.4 |
| got-ec35aa | got5.6:-33.984,23.562 | GOT5.6 33.984S 23.562E (ZA-WC-GR) | MSL+110 cm (modelo) | 5..225 | — | 1.5 |
| got-ef40bc | got5.6:5.490,-0.405 | GOT5.6 5.490N 0.405W (GH-ALL) | MSL+100 cm (modelo) | 5..189 | — | 1.0 |
| got-f03581 | got5.6:-34.046,22.418 | GOT5.6 34.046S 22.418E (ZA-WC-GR) | MSL+117 cm (modelo) | 5..240 | — | 1.6 |
| got-f0b002 | got5.6:37.653,-8.801 | GOT5.6 37.653N 8.801W (PT-ALG) | MSL+182 cm (modelo) | 6..363 | — | 2.0 |
| got-f0c08b | got5.6:7.300,-80.380 | GOT5.6 7.300N 80.380W (PA-PAC) | MSL+208 cm (modelo) | 6..412 | — | 2.1 |
| got-f341c0 | got5.6:-22.938,14.418 | GOT5.6 22.938S 14.418E (NA-ERO) | MSL+98 cm (modelo) | 5..190 | — | 1.1 |
| got-f4a045 | got5.6:11.040,-74.910 | GOT5.6 11.040N 74.910W (CO-CAR) | MSL+24 cm (modelo) | 6..56 | — | 0.4 |
| got-f89309 | got5.6:-6.237,-35.046 | GOT5.6 6.237S 35.046W (BR-NE-RN) | MSL+144 cm (modelo) | 5..285 | — | 1.5 |
| got-f8b86d | got5.6:16.669,120.320 | GOT5.6 16.669N 120.320E (PH-LUZ) | MSL+63 cm (modelo) | 5..138 | — | 1.1 |
| imi-achill-island | imi:Achill_Island_MODELLED | Achill Island (modelado) | LAT | 9..467 | 2026: 1 | 0.3 |
| imi-castletownbere | imi:Castletownbere | Castletownbere | LAT | 11..374 | — | 2.2 |
| imi-dingle | imi:Dingle | Dingle | LAT | 8..440 | — | 2.7 |
| imi-dungarvan | imi:Dungarvan_MODELLED | Dungarvan (modelado) | LAT | 1..412 | 2026: 1 | 0.3 |
| imi-fenit | imi:Fenit | Fenit | LAT | 15..532 | — | 3.5 |
| imi-inishmore | imi:Inishmore | Inishmore | LAT | 15..537 | — | 3.3 |
| imi-killybegs | imi:Killybegs | Killybegs | LAT | 17..459 | — | 2.9 |
| imi-kinsale | imi:Kinsale_MODELLED | Kinsale (modelado) | LAT | -2..396 | 2026: 1 | 0.3 |
| imi-port-oriel | imi:Port_Oriel | Port Oriel | LAT | 8..564 | — | 5.2 |
| imi-sligo | imi:Sligo | Sligo | LAT | 16..465 | — | 2.9 |
| jma-cs | jma:CS | 銚子漁港 (JMA CS) | DL (潮位表基準面, JMA) | -19..160 | 2027: 9 | 1.6 |
| jma-d2 | jma:D2 | 鹿島 (JMA D2) | DL (潮位表基準面, JMA) | -21..156 | 2027: 9 | 1.6 |
| jma-d6 | jma:D6 | 下田 (JMA D6) | DL (潮位表基準面, JMA) | -25..181 | 2027: 9 | 1.6 |
| jma-d8 | jma:D8 | 湘南港 (JMA D8) | DL (潮位表基準面, JMA) | -20..161 | 2027: 9 | 2.0 |
| jma-hw | jma:HW | 日和佐 (JMA HW) | DL (潮位表基準面, JMA) | -23..204 | 2027: 9 | 1.7 |
| jma-mg | jma:MG | 宮崎 (JMA MG) | DL (潮位表基準面, JMA) | -37..221 | 2027: 9 | 2.0 |
| jma-ok | jma:OK | 岡田 (JMA OK) | DL (潮位表基準面, JMA) | -25..161 | 2027: 9 | 1.6 |
| jma-on | jma:ON | 小名浜 (JMA ON) | DL (潮位表基準面, JMA) | -20..151 | 2027: 9 | 1.5 |
| jma-zf | jma:ZF | 勝浦 (JMA ZF) | DL (潮位表基準面, JMA) | -24..165 | 2027: 9 | 1.6 |
| linz-anawhata | linz:Anawhata | Anawhata | Chart Datum (LINZ) | 20..340 | — | 3.1 |
| linz-ben-gunn-wharf | linz:Ben Gunn Wharf | Ben Gunn Wharf | Chart Datum (LINZ) | 10..259 | — | 3.4 |
| linz-castlepoint | linz:Castlepoint | Castlepoint | Chart Datum (LINZ) | 0..180 | — | 2.6 |
| linz-dargaville | linz:Dargaville | Dargaville | Chart Datum (LINZ) | 50..450 | — | 6.8 |
| linz-dog-island | linz:Dog Island | Dog Island | Chart Datum (LINZ) | 40..330 | — | 2.8 |
| linz-gisborne | linz:Gisborne | Gisborne | Chart Datum (LINZ) | 40..220 | — | 2.7 |
| linz-green-island | linz:Green Island | Green Island | Chart Datum (LINZ) | 0..227 | — | 2.7 |
| linz-huruhi-harbour | linz:Huruhi Harbour | Huruhi Harbour | Chart Datum (LINZ) | 20..260 | — | 2.6 |
| linz-kaikoura | linz:Kaikōura | Kaikōura | Chart Datum (LINZ) | 0..190 | — | 2.5 |
| linz-manu-bay | linz:Manu Bay | Manu Bay | Chart Datum (LINZ) | 30..379 | — | 2.6 |
| linz-marsden-point | linz:Marsden Point | Marsden Point | Chart Datum (LINZ) | 30..300 | — | 2.9 |
| linz-moturiki-island | linz:Moturiki Island | Moturiki Island | Chart Datum (LINZ) | 10..220 | — | 2.8 |
| linz-new-brighton-pier | linz:New Brighton Pier | New Brighton Pier | Chart Datum (LINZ) | 20..259 | — | 3.7 |
| linz-paratutae-island | linz:Paratutae Island | Paratutae Island | Chart Datum (LINZ) | 20..360 | — | 3.3 |
| linz-port-ohope-wharf | linz:Port Ōhope Wharf | Port Ōhope Wharf | Chart Datum (LINZ) | 0..210 | — | 2.9 |
| linz-port-taranaki | linz:Port Taranaki | Port Taranaki | Chart Datum (LINZ) | 10..390 | — | 3.4 |
| linz-rangatira-point | linz:Rangatira Point | Rangatira Point | Chart Datum (LINZ) | 10..200 | — | 3.7 |
| linz-spit-wharf | linz:Spit Wharf | Spit Wharf | Chart Datum (LINZ) | 20..210 | — | 2.7 |
| linz-wellington | linz:Wellington | Wellington | Chart Datum (LINZ) | 50..190 | — | 2.5 |
| linz-westport | linz:Westport | Westport | Chart Datum (LINZ) | 30..380 | — | 3.0 |
| noaa-1611347 | noaa:1611347 | Port Allen, Hanapepe Bay, HI | MLLW | -19..83 | — | 0.6 |
| noaa-1611400 | noaa:1611400 | NAWILIWILI, HI | MLLW | -15..79 | — | 0.5 |
| noaa-1612340 | noaa:1612340 | HONOLULU, HI | MLLW | -13..82 | — | 0.5 |
| noaa-1612401 | noaa:1612401 | Ford Island, Pearl Harbor, HI | MLLW | -13..84 | — | 0.6 |
| noaa-1613198 | noaa:1613198 | Kaunakakai, HI | MLLW | -14..88 | — | 0.9 |
| noaa-1615680 | noaa:1615680 | KAHULUI, HI | MLLW | -23..93 | — | 0.7 |
| noaa-1617433 | noaa:1617433 | Kawaihae, HI | MLLW | -15..91 | — | 0.5 |
| noaa-1617760 | noaa:1617760 | HILO, HI | MLLW | -22..99 | — | 0.6 |
| noaa-1732417 | noaa:1732417 | Papeete Harbor, Fare Ute Point | MLLW | -8..33 | — | 0.4 |
| noaa-1778000 | noaa:1778000 | APIA (Observatory), Upolu Island, AS | MLLW | 95..228 | — | 0.4 |
| noaa-8459338 | noaa:8459338 | Block Island (Old Harbor), RI | MLLW | -26..126 | — | 0.9 |
| noaa-8517137 | noaa:8517137 | Beach Channel (bridge), NY | MLLW | -37..218 | — | 1.8 |
| noaa-8534720 | noaa:8534720 | Atlantic City (Ocean), NJ | MLLW | -34..172 | — | 0.9 |
| noaa-8536110 | noaa:8536110 | Cape May, ferry terminal, NJ | MLLW | -30..197 | — | 1.1 |
| noaa-8570280 | noaa:8570280 | OCEAN CITY (FISHING PIER), MD | MLLW | -32..152 | — | 0.7 |
| noaa-8639207 | noaa:8639207 | Rudee Inlet, interior channel, VA | MLLW | -26..141 | — | 0.8 |
| noaa-8658163 | noaa:8658163 | Wrightsville Beach, NC | MLLW | -37..173 | — | 1.2 |
| noaa-8659897 | noaa:8659897 | Sunset Beach Pier, NC | MLLW | -36..212 | — | 2.0 |
| noaa-8665530 | noaa:8665530 | CHARLESTON (Customhouse Wharf), SC | MLLW | -44..209 | — | 1.8 |
| noaa-8668498 | noaa:8668498 | Fripps Inlet, Hunting Island Bridge, SC | MLLW | -46..242 | — | 1.8 |
| noaa-8677344 | noaa:8677344 | St. Simons Light, GA | MLLW | -54..267 | — | 1.9 |
| noaa-8721649 | noaa:8721649 | Cocoa Beach, FL | MLLW | -31..155 | — | 1.0 |
| noaa-8723080 | noaa:8723080 | Haulover Pier, N. Miami Beach, FL | MLLW | -25..112 | — | 0.4 |
| noaa-8729210 | noaa:8729210 | Panama City Beach, FL | MLLW | -31..68 | — | 1.0 |
| noaa-8731269 | noaa:8731269 | Gulf State Park Pier, AL | MLLW | -30..67 | — | 0.9 |
| noaa-8761724 | noaa:8761724 | EAST POINT, GRAND ISLE, LA | MLLW | -33..56 | — | 0.6 |
| noaa-8775270 | noaa:8775270 | Port Aransas (H. Caldwell Pier), TX | MLLW | -48..92 | — | 1.2 |
| noaa-8779770 | noaa:8779770 | Port Isabel, TX | MLLW | -30..66 | — | 0.7 |
| noaa-9410135 | noaa:9410135 | South San Diego Bay, CA | MLLW | -62..240 | — | 1.7 |
| noaa-9410196 | noaa:9410196 | Mission Bay, Campland, CA | MLLW | -58..224 | — | 1.7 |
| noaa-9410230 | noaa:9410230 | La Jolla (Scripps Institution Wharf), CA | MLLW | -57..218 | — | 1.3 |
| noaa-9410580 | noaa:9410580 | Newport Bay Entrance, Corona del Mar, CA | MLLW | -56..218 | — | 1.5 |
| noaa-9410660 | noaa:9410660 | LOS ANGELES (Outer Harbor), CA | MLLW | -58..221 | — | 1.5 |
| noaa-9410678 | noaa:9410678 | Long Beach Fire Boat Pier, CA | MLLW | -55..220 | — | 1.6 |
| noaa-9410840 | noaa:9410840 | Santa Monica, Municipal Pier, CA | MLLW | -59..222 | — | 1.5 |
| noaa-9411270 | noaa:9411270 | Rincon Island, Mussel Shoals, CA | MLLW | -58..220 | — | 1.4 |
| noaa-9411340 | noaa:9411340 | Santa Barbara, CA | MLLW | -59..220 | — | 1.4 |
| noaa-9411406 | noaa:9411406 | Oil Platform Harvest, CA | MLLW | -54..210 | — | 1.3 |
| noaa-9412110 | noaa:9412110 | PORT SAN LUIS, CA | MLLW | -57..214 | — | 1.4 |
| noaa-9413450 | noaa:9413450 | MONTEREY, MONTEREY BAY, CA | MLLW | -58..212 | — | 1.3 |
| noaa-9413631 | noaa:9413631 | Elkhorn, Elkhorn Slough, CA | MLLW | -50..203 | — | 1.7 |
| noaa-9414131 | noaa:9414131 | Pillar Point Harbor, Half Moon Bay, CA | MLLW | -64..219 | — | 1.6 |
| noaa-9414958 | noaa:9414958 | Bolinas Lagoon, CA | MLLW | -28..161 | — | 1.1 |
| noaa-9415020 | noaa:9415020 | Point Reyes, CA | MLLW | -65..226 | — | 1.3 |
| noaa-9416841 | noaa:9416841 | ARENA COVE, CA | MLLW | -66..232 | — | 1.4 |
| noaa-9418817 | noaa:9418817 | Samoa, CA | MLLW | -72..281 | — | 1.7 |
| noaa-9435380 | noaa:9435380 | Southbeach, OR | MLLW | -85..320 | — | 1.8 |
| noaa-9640507 | noaa:9640507 | La Union (Cutuco) | MLLW | -37..338 | — | 1.3 |
| noaa-9684403 | noaa:9684403 | Puntarenas | MLLW | -34..321 | — | 1.2 |
| noaa-9753766 | noaa:9753766 | Luquillo, PR | MLLW | -15..62 | — | 0.4 |
| noaa-9754986 | noaa:9754986 | Boca de Cangrejos, PR | MLLW | -14..57 | — | 0.4 |
| noaa-9756567 | noaa:9756567 | Boca del Cibuco, PR | MLLW | -15..74 | — | 0.5 |
| noaa-9757809 | noaa:9757809 | Arecibo, PR | MLLW | -16..70 | — | 0.4 |
| noaa-9759394 | noaa:9759394 | Mayaguez, PR | MLLW | -11..54 | — | 0.4 |
| noaa-9759412 | noaa:9759412 | Aguadilla, PR | MLLW | -16..58 | — | 0.4 |
| noaa-9991474 | noaa:9991474 | La Libertad, Bahia de Santa Elena | MLLW | -29..245 | — | 1.0 |
| noaa-9992401 | noaa:9992401 | San Cristobal, Galapagos islands | MLLW | -24..213 | — | 0.9 |
| ticon-00efc3 | ticon3:-42.549,147.928 | TICON-3 42.549S 147.928E (gesla.cmems) | MSL+ΣA (MSL+96 cm) | 26..167 | — | 0.7 |
| ticon-03a6be | ticon3:-32.924,151.789 | TICON-3 32.924S 151.789E (gesla.cmems) | MSL+ΣA (MSL+140 cm) | 51..247 | — | 1.0 |
| ticon-041ef0 | ticon3:34.655,129.478 | TICON-3 34.655N 129.478E (gesla.noaa) | MSL+ΣA (MSL+107 cm) | 30..188 | — | 1.6 |
| ticon-07792e | ticon3:50.714,-1.875 | TICON-3 50.714N 1.875W (gesla.noaa) | MSL+ΣA (MSL+183 cm) | 47..272 | — | 2.5 |
| ticon-079795 | ticon3:-35.705,150.178 | TICON-3 35.705S 150.178E (gesla.cmems) | MSL+ΣA (MSL+130 cm) | 48..228 | — | 1.0 |
| ticon-0a453c | ticon3:-20.153,57.490 | TICON-3 20.153S 57.490E (gesla.noaa) | MSL+ΣA (MSL+69 cm) | 22..111 | — | 1.0 |
| ticon-0ccd99 | ticon3:-8.747,115.212 | TICON-3 8.747S 115.212E (gesla.usgs) | MSL+ΣA (MSL+240 cm) | 87..393 | — | 2.3 |
| ticon-10c275 | ticon3:44.520,-64.000 | TICON-3 44.520N 64.000W (gesla.uhslc) | MSL+ΣA (MSL+165 cm) | 58..275 | — | 3.5 |
| ticon-16f890 | ticon3:48.641,-2.028 | TICON-3 48.641N 2.028W (gesla.bodc) | MSL | -651..632 | — | 10.8 |
| ticon-18a200 | ticon3:16.755,-22.983 | TICON-3 16.755N 22.983W (gesla.refmar) | MSL+ΣA (MSL+86 cm) | 34..151 | — | 0.7 |
| ticon-1af31e | ticon3:54.967,8.666 | TICON-3 54.967N 8.666E (gesla.refmar) | MSL+ΣA (MSL+196 cm) | 97..303 | — | 5.4 |
| ticon-1b2d0f | ticon3:29.857,-81.263 | TICON-3 29.857N 81.263W (gesla.meds) | MSL+ΣA (MSL+171 cm) | 63..293 | — | 1.7 |
| ticon-1bb5de | ticon3:55.200,-6.667 | TICON-3 55.200N 6.667W (gesla.usgs) | MSL+ΣA (MSL+175 cm) | 67..300 | — | 3.1 |
| ticon-1c9970 | ticon3:-17.605,177.438 | TICON-3 17.605S 177.438E (gesla.uhslc) | MSL+ΣA (MSL+147 cm) | 34..257 | — | 0.9 |
| ticon-1fb951 | ticon3:57.144,-2.080 | TICON-3 57.144N 2.080W (gesla.noaa) | MSL+ΣA (MSL+313 cm) | 71..532 | — | 2.4 |
| ticon-215748 | ticon3:20.900,-156.467 | TICON-3 20.900N 156.467W (gesla.noaa) | MSL+ΣA (MSL+88 cm) | 29..145 | — | 0.5 |
| ticon-22ec01 | ticon3:36.540,-6.283 | TICON-3 36.540N 6.283W (gesla.cmems) | MSL+ΣA (MSL+242 cm) | 62..434 | — | 2.5 |
| ticon-233ae7 | ticon3:-18.132,178.427 | TICON-3 18.132S 178.427E (gesla.cmems) | MSL+ΣA (MSL+124 cm) | 29..218 | — | 0.7 |
| ticon-2559e1 | ticon3:-22.933,-43.133 | TICON-3 22.933S 43.133W (gesla.noaa) | MSL+ΣA (MSL+113 cm) | 31..182 | — | 1.3 |
| ticon-27bb40 | ticon3:-9.478,147.140 | TICON-3 9.478S 147.140E (gesla.uhslc) | MSL+ΣA (MSL+198 cm) | 60..341 | — | 2.0 |
| ticon-283bad | ticon3:43.463,-8.326 | TICON-3 43.463N 8.326W (gesla.meds) | MSL+ΣA (MSL+264 cm) | 58..472 | — | 2.1 |
| ticon-293edc | ticon3:9.425,-84.172 | TICON-3 9.425N 84.172W (gesla.uhslc) | MSL+ΣA (MSL+209 cm) | 50..373 | — | 1.4 |
| ticon-2aab05 | ticon3:4.190,73.527 | TICON-3 4.190N 73.527E (gesla.uhslc) | MSL+ΣA (MSL+90 cm) | 26..145 | — | 0.9 |
| ticon-2b1454 | ticon3:-8.350,-34.950 | TICON-3 8.350S 34.950W (gesla.noaa) | MSL+ΣA (MSL+178 cm) | 50..321 | — | 2.1 |
| ticon-2cdea6 | ticon3:42.094,11.790 | TICON-3 42.094N 11.790E (gesla.bom) | MSL+ΣA (MSL+36 cm) | 14..59 | — | 0.5 |
| ticon-2e5983 | ticon3:-32.601,115.630 | TICON-3 32.601S 115.630E (gesla.noaa) | MSL+ΣA (MSL+73 cm) | 26..124 | — | 0.6 |
| ticon-2ebaf5 | ticon3:-20.935,55.285 | TICON-3 20.935S 55.285E (gesla.noaa) | MSL+ΣA (MSL+62 cm) | 16..102 | — | 0.8 |
| ticon-2fe7b0 | ticon3:-29.429,153.362 | TICON-3 29.429S 153.362E (gesla.cmems) | MSL+ΣA (MSL+138 cm) | 57..243 | — | 1.2 |
| ticon-34de1f | ticon3:16.838,-99.903 | TICON-3 16.838N 99.903W (gesla.meds) | MSL+ΣA (MSL+88 cm) | 30..142 | — | 0.7 |
| ticon-388f65 | ticon3:50.608,-2.448 | TICON-3 50.608N 2.448W (gesla.noaa) | MSL+ΣA (MSL+225 cm) | 101..379 | — | 3.3 |
| ticon-3927f3 | ticon3:-38.351,141.620 | TICON-3 38.351S 141.620E (gesla.mi_c) | MSL+ΣA (MSL+100 cm) | 41..165 | — | 0.9 |
| ticon-393286 | ticon3:-33.551,151.275 | TICON-3 33.551S 151.275E (gesla.cmems) | MSL+ΣA (MSL+140 cm) | 52..248 | — | 1.0 |
| ticon-39e748 | ticon3:-18.467,-70.333 | TICON-3 18.467S 70.333W (gesla.uhslc) | MSL+ΣA (MSL+107 cm) | 48..188 | — | 0.9 |
| ticon-3b2a68 | ticon3:-17.002,-72.108 | TICON-3 17.002S 72.108W (gesla.cmems) | MSL+ΣA (MSL+104 cm) | 47..183 | — | 0.8 |
| ticon-3eec34 | ticon3:-14.283,-170.683 | TICON-3 14.283S 170.683W (gesla.uhslc) | MSL+ΣA (MSL+81 cm) | 22..147 | — | 0.7 |
| ticon-406688 | ticon3:38.533,-28.622 | TICON-3 38.533N 28.622W (gesla.noaa) | MSL+ΣA (MSL+105 cm) | 33..186 | — | 1.2 |
| ticon-41bc98 | ticon3:-12.068,-77.167 | TICON-3 12.068S 77.167W (gesla.cmems) | MSL+ΣA (MSL+91 cm) | 36..155 | — | 0.7 |
| ticon-440073 | ticon3:28.936,-95.294 | TICON-3 28.936N 95.294W (gesla.noaa) | MSL+ΣA (MSL+93 cm) | 25..145 | — | 1.1 |
| ticon-448fcc | ticon3:68.213,14.482 | TICON-3 68.213N 14.482E (gesla.uhslc) | MSL+ΣA (MSL+236 cm) | 66..413 | — | 1.7 |
| ticon-44917a | ticon3:61.934,5.113 | TICON-3 61.934N 5.113E (gesla.uhslc) | MSL+ΣA (MSL+144 cm) | 37..244 | — | 1.1 |
| ticon-45502d | ticon3:15.667,-96.492 | TICON-3 15.667N 96.492W (gesla.noaa) | MSL+ΣA (MSL+108 cm) | 41..188 | — | 1.0 |
| ticon-458133 | ticon3:10.340,107.072 | TICON-3 10.340N 107.072E (gesla.meds) | MSL+ΣA (MSL+346 cm) | 68..499 | — | 2.7 |
| ticon-48327e | ticon3:28.480,-16.240 | TICON-3 28.480N 16.240W (gesla.cmems) | MSL+ΣA (MSL+155 cm) | 35..288 | — | 1.4 |
| ticon-488f81 | ticon3:50.510,-128.030 | TICON-3 50.510N 128.030W (gesla.uhslc) | MSL+ΣA (MSL+312 cm) | 76..522 | — | 1.6 |
| ticon-48cda1 | ticon3:-42.877,147.341 | TICON-3 42.877S 147.341E (gesla.noaa) | MSL+ΣA (MSL+110 cm) | 29..190 | — | 0.7 |
| ticon-4a3da2 | ticon3:37.098,-8.668 | TICON-3 37.098N 8.668W (gesla.meds) | MSL+ΣA (MSL+234 cm) | 55..418 | — | 2.0 |
| ticon-4a4b08 | ticon3:39.148,8.309 | TICON-3 39.148N 8.309E (gesla.uhslc) | MSL+ΣA (MSL+35 cm) | 12..57 | — | 0.4 |
| ticon-4bcc10 | ticon3:57.117,8.600 | TICON-3 57.117N 8.600E (gesla.refmar) | MSL+ΣA (MSL+72 cm) | 34..111 | — | 2.5 |
| ticon-4c1497 | ticon3:-3.828,-32.403 | TICON-3 3.828S 32.403W (gesla.usgs) | MSL+ΣA (MSL+176 cm) | 47..320 | — | 1.6 |
| ticon-4c1a6a | ticon3:14.678,-60.941 | TICON-3 14.678N 60.941W (gesla.fmi) | MSL+ΣA (MSL+67 cm) | 21..109 | — | 0.9 |
| ticon-4f62f3 | ticon3:50.102,-5.542 | TICON-3 50.102N 5.542W (gesla.uhslc) | MSL+ΣA (MSL+386 cm) | 102..663 | — | 3.8 |
| ticon-513a8d | ticon3:43.357,-3.050 | TICON-3 43.357N 3.050W (gesla.meds) | MSL+ΣA (MSL+292 cm) | 63..523 | — | 2.4 |
| ticon-5336d6 | ticon3:28.950,-13.567 | TICON-3 28.950N 13.567W (gesla.uhslc) | MSL+ΣA (MSL+197 cm) | 49..362 | — | 1.6 |
| ticon-55de77 | ticon3:-4.582,-81.282 | TICON-3 4.582S 81.282W (gesla.cmems) | MSL+ΣA (MSL+144 cm) | 38..252 | — | 1.2 |
| ticon-5699c9 | ticon3:-21.140,-175.180 | TICON-3 21.140S 175.180W (gesla.jodc_jcg) | MSL+ΣA (MSL+107 cm) | 23..190 | — | 0.6 |
| ticon-56fc43 | ticon3:35.745,140.858 | TICON-3 35.745N 140.858E (gesla.bom) | MSL+ΣA (MSL+140 cm) | 33..209 | — | 0.9 |
| ticon-5969a5 | ticon3:25.155,121.752 | TICON-3 25.155N 121.752E (gesla.noaa) | MSL+ΣA (MSL+123 cm) | 28..188 | — | 1.3 |
| ticon-5b4329 | ticon3:39.586,-9.074 | TICON-3 39.586N 9.074W (gesla.uhslc) | MSL+ΣA (MSL+231 cm) | 60..416 | — | 4.3 |
| ticon-5da85d | ticon3:38.692,-9.417 | TICON-3 38.692N 9.417W (gesla.cmems) | MSL+ΣA (MSL+225 cm) | 53..409 | — | 1.8 |
| ticon-5dd235 | ticon3:-30.303,153.146 | TICON-3 30.303S 153.146E (gesla.uhslc) | MSL+ΣA (MSL+153 cm) | 60..273 | — | 1.1 |
| ticon-62701e | ticon3:-0.687,73.152 | TICON-3 0.687S 73.152E (gesla.noaa) | MSL+ΣA (MSL+100 cm) | 30..164 | — | 1.0 |
| ticon-66c157 | ticon3:44.211,-1.295 | TICON-3 44.211N 1.295W (gesla.noaa) | MSL+ΣA (MSL+286 cm) | 138..505 | — | 7.7 |
| ticon-66dd4f | ticon3:43.546,10.299 | TICON-3 43.546N 10.299E (gesla.rws) | MSL+ΣA (MSL+33 cm) | 11..52 | — | 0.3 |
| ticon-67a479 | ticon3:3.890,-77.062 | TICON-3 3.890N 77.062W (gesla.noaa) | MSL+ΣA (MSL+332 cm) | 95..585 | — | 2.9 |
| ticon-67b5b2 | ticon3:38.650,-27.240 | TICON-3 38.650N 27.240W (gesla.cmems) | MSL+ΣA (MSL+109 cm) | 32..195 | — | 1.2 |
| ticon-67d63b | ticon3:43.367,-8.400 | TICON-3 43.367N 8.400W (gesla.usgs) | MSL+ΣA (MSL+262 cm) | 59..470 | — | 2.1 |
| ticon-6b84e3 | ticon3:19.063,-104.298 | TICON-3 19.063N 104.298W (gesla.usgs) | MSL+ΣA (MSL+114 cm) | 37..181 | — | 1.3 |
| ticon-701a8e | ticon3:57.895,-5.158 | TICON-3 57.895N 5.158W (gesla.meds) | MSL+ΣA (MSL+368 cm) | 80..632 | — | 3.3 |
| ticon-71d7df | ticon3:21.320,-158.120 | TICON-3 21.320N 158.120W (gesla.meds) | MSL+ΣA (MSL+78 cm) | 38..137 | — | 0.7 |
| ticon-73a14b | ticon3:10.650,-61.517 | TICON-3 10.650N 61.517W (gesla.meds) | MSL+ΣA (MSL+105 cm) | 37..170 | — | 1.5 |
| ticon-73effe | ticon3:15.753,-96.130 | TICON-3 15.753N 96.130W (gesla.noaa) | MSL+ΣA (MSL+116 cm) | 43..203 | — | 0.9 |
| ticon-752b4c | ticon3:-23.500,-45.117 | TICON-3 23.500S 45.117W (gesla.cmems) | MSL+ΣA (MSL+124 cm) | 36..186 | — | 2.9 |
| ticon-757122 | ticon3:-25.017,-47.925 | TICON-3 25.017S 47.925W (gesla.meds) | MSL+ΣA (MSL+154 cm) | 60..243 | — | 5.2 |
| ticon-789208 | ticon3:52.462,4.555 | TICON-3 52.462N 4.555E (gesla.uhslc) | MSL+ΣA (MSL+238 cm) | 120..364 | — | 3.7 |
| ticon-7b004f | ticon3:51.717,-5.050 | TICON-3 51.717N 5.050W (gesla.meds) | MSL+ΣA (MSL+488 cm) | 122..865 | — | 4.9 |
| ticon-7b330d | ticon3:17.940,-102.178 | TICON-3 17.940N 102.178W (gesla.jodc_jma) | MSL+ΣA (MSL+91 cm) | 29..138 | — | 1.1 |
| ticon-7cfb7a | ticon3:49.150,-125.910 | TICON-3 49.150N 125.910W (gesla.noaa) | MSL+ΣA (MSL+301 cm) | 80..498 | — | 1.8 |
| ticon-809086 | ticon3:-33.968,151.220 | TICON-3 33.968S 151.220E (gesla.meds) | MSL+ΣA (MSL+140 cm) | 53..250 | — | 1.0 |
| ticon-86ec39 | ticon3:-33.960,25.630 | TICON-3 33.960S 25.630E (gesla.usgs) | MSL+ΣA (MSL+133 cm) | 35..241 | — | 1.4 |
| ticon-8d43eb | ticon3:54.490,-0.615 | TICON-3 54.490N 0.615W (gesla.uhslc) | MSL+ΣA (MSL+385 cm) | 84..666 | — | 3.3 |
| ticon-8e0567 | ticon3:22.880,-109.908 | TICON-3 22.880N 109.908W (gesla.sfwmd) | MSL+ΣA (MSL+160 cm) | 49..261 | — | 1.3 |
| ticon-8ea705 | ticon3:-31.427,152.911 | TICON-3 31.427S 152.911E (gesla.usgs) | MSL+ΣA (MSL+127 cm) | 57..228 | — | 1.1 |
| ticon-8ecb10 | ticon3:36.009,-5.603 | TICON-3 36.009N 5.603W (gesla.noaa) | MSL+ΣA (MSL+106 cm) | 34..188 | — | 1.1 |
| ticon-8f3726 | ticon3:56.525,8.115 | TICON-3 56.525N 8.115E (gesla.cmems) | MSL+ΣA (MSL+102 cm) | 47..162 | — | 2.2 |
| ticon-902798 | ticon3:-38.292,144.614 | TICON-3 38.292S 144.614E (gesla.uhslc) | MSL+ΣA (MSL+140 cm) | 49..228 | — | 1.3 |
| ticon-90ea2b | ticon3:67.292,14.400 | TICON-3 67.292N 14.400E (gesla.usgs) | MSL+ΣA (MSL+213 cm) | 59..370 | — | 1.7 |
| ticon-91c7f2 | ticon3:42.238,-8.730 | TICON-3 42.238N 8.730W (gesla.noaa) | MSL+ΣA (MSL+247 cm) | 57..443 | — | 2.0 |
| ticon-920ef6 | ticon3:43.527,-1.515 | TICON-3 43.527N 1.515W (gesla.meds) | MSL+ΣA (MSL+272 cm) | 58..489 | — | 2.3 |
| ticon-92ede9 | ticon3:-28.776,114.602 | TICON-3 28.776S 114.602E (gesla.uhslc) | MSL+ΣA (MSL+86 cm) | 32..146 | — | 0.6 |
| ticon-930b55 | ticon3:4.883,-1.750 | TICON-3 4.883N 1.750W (gesla.wsv) | MSL+ΣA (MSL+138 cm) | 44..232 | — | 1.2 |
| ticon-936e57 | ticon3:37.132,-6.834 | TICON-3 37.132N 6.834W (gesla.uhslc) | MSL+ΣA (MSL+241 cm) | 58..434 | — | 1.9 |
| ticon-9450da | ticon3:-33.027,-71.627 | TICON-3 33.027S 71.627W (gesla.noaa) | MSL+ΣA (MSL+130 cm) | 50..232 | — | 0.7 |
| ticon-9ab05d | ticon3:55.628,-6.190 | TICON-3 55.628N 6.190W (gesla.usgs) | MSL+ΣA (MSL+109 cm) | 47..160 | — | 3.0 |
| ticon-9bc4f0 | ticon3:23.198,-106.422 | TICON-3 23.198N 106.422W (gesla.rws) | MSL+ΣA (MSL+162 cm) | 50..268 | — | 1.4 |
| ticon-9c5cfc | ticon3:51.592,3.555 | TICON-3 51.592N 3.555E (gesla.noaa) | MSL+ΣA (MSL+360 cm) | 170..570 | — | 5.3 |
| ticon-9caabc | ticon3:-41.283,174.783 | TICON-3 41.283S 174.783E (gesla.noaa) | MSL+ΣA (MSL+96 cm) | 31..172 | — | 1.1 |
| ticon-9cf100 | ticon3:28.500,-13.850 | TICON-3 28.500N 13.850W (gesla.noaa) | MSL+ΣA (MSL+190 cm) | 49..347 | — | 1.5 |
| ticon-9e0a4e | ticon3:-33.323,115.660 | TICON-3 33.323S 115.660E (gesla.noaa) | MSL+ΣA (MSL+84 cm) | 28..143 | — | 0.6 |
| ticon-a03088 | ticon3:52.017,-4.983 | TICON-3 52.017N 4.983W (gesla.usgs) | MSL+ΣA (MSL+336 cm) | 103..598 | — | 3.0 |
| ticon-a1343b | ticon3:-27.967,153.417 | TICON-3 27.967S 153.417E (gesla.noaa) | MSL+ΣA (MSL+151 cm) | 65..264 | — | 1.1 |
| ticon-a3cf33 | ticon3:45.568,-1.062 | TICON-3 45.568N 1.062W (gesla.bom) | MSL+ΣA (MSL+348 cm) | 92..601 | — | 3.8 |
| ticon-a43379 | ticon3:48.368,-124.617 | TICON-3 48.368N 124.617W (gesla.cmems) | MSL+ΣA (MSL+286 cm) | 63..474 | — | 1.5 |
| ticon-a4a070 | ticon3:52.205,4.362 | TICON-3 52.205N 4.362E (gesla.cmems) | MSL+ΣA (MSL+258 cm) | 138..401 | — | 4.4 |
| ticon-a6ef88 | ticon3:41.187,-8.704 | TICON-3 41.187N 8.704W (gesla.fmi) | MSL+ΣA (MSL+239 cm) | 56..429 | — | 4.0 |
| ticon-a75e0c | ticon3:47.025,-2.298 | TICON-3 47.025N 2.298W (gesla.usgs) | MSL+ΣA (MSL+404 cm) | 86..674 | — | 3.9 |
| ticon-a8dc55 | ticon3:-38.374,145.223 | TICON-3 38.374S 145.223E (gesla.noaa) | MSL+ΣA (MSL+249 cm) | 89..406 | — | 2.7 |
| ticon-acd761 | ticon3:50.368,-4.185 | TICON-3 50.368N 4.185W (gesla.noaa) | MSL+ΣA (MSL+414 cm) | 105..671 | — | 5.0 |
| ticon-ad634c | ticon3:45.853,-1.178 | TICON-3 45.853N 1.178W (gesla.meds) | MSL+ΣA (MSL+435 cm) | 113..701 | — | 4.4 |
| ticon-ae0728 | ticon3:43.398,-1.673 | TICON-3 43.398N 1.673W (gesla.nwfwmd) | MSL+ΣA (MSL+294 cm) | 63..527 | — | 2.5 |
| ticon-ae29cb | ticon3:28.100,-15.400 | TICON-3 28.100N 15.400W (gesla.jodc_jcg) | MSL+ΣA (MSL+177 cm) | 48..319 | — | 2.2 |
| ticon-afa9fb | ticon3:-34.780,138.481 | TICON-3 34.780S 138.481E (gesla.unam) | MSL+ΣA (MSL+230 cm) | 104..373 | — | 3.5 |
| ticon-b027ca | ticon3:58.441,-3.086 | TICON-3 58.441N 3.086W (gesla.meds) | MSL+ΣA (MSL+258 cm) | 72..440 | — | 2.1 |
| ticon-b3b22e | ticon3:24.452,122.942 | TICON-3 24.452N 122.942E (gesla.meds) | MSL+ΣA (MSL+164 cm) | 36..270 | — | 1.2 |
| ticon-b604d6 | ticon3:16.303,-61.072 | TICON-3 16.303N 61.072W (gesla.usgs) | MSL+ΣA (MSL+58 cm) | 19..86 | — | 0.8 |
| ticon-b63d75 | ticon3:19.798,-70.702 | TICON-3 19.798N 70.702W (gesla.noaa) | MSL+ΣA (MSL+72 cm) | 26..120 | — | 0.5 |
| ticon-b76b33 | ticon3:13.917,-90.833 | TICON-3 13.917N 90.833W (gesla.uhslc) | MSL+ΣA (MSL+159 cm) | 46..280 | — | 1.1 |
| ticon-b7fd2a | ticon3:-39.050,174.033 | TICON-3 39.050S 174.033E (gesla.noaa) | MSL+ΣA (MSL+243 cm) | 52..431 | — | 2.3 |
| ticon-b849f8 | ticon3:50.594,-4.834 | TICON-3 50.594N 4.834W (gesla.meds) | MSL+ΣA (MSL+531 cm) | 132..946 | — | 5.4 |
| ticon-bdc867 | ticon3:43.558,-5.698 | TICON-3 43.558N 5.698W (gesla.uhslc) | MSL+ΣA (MSL+287 cm) | 63..512 | — | 2.4 |
| ticon-bfaae8 | ticon3:-32.056,115.740 | TICON-3 32.056S 115.740E (gesla.noaa) | MSL+ΣA (MSL+73 cm) | 26..127 | — | 0.5 |
| ticon-c0a455 | ticon3:-33.825,151.258 | TICON-3 33.825S 151.258E (gesla.wsv) | MSL+ΣA (MSL+139 cm) | 51..248 | — | 1.0 |
| ticon-c17f38 | ticon3:4.183,73.517 | TICON-3 4.183N 73.517E (gesla.uhslc) | MSL+ΣA (MSL+100 cm) | 34..159 | — | 1.9 |
| ticon-c1874d | ticon3:-3.717,-38.483 | TICON-3 3.717S 38.483W (gesla.cmems) | MSL+ΣA (MSL+208 cm) | 55..371 | — | 2.0 |
| ticon-c238b7 | ticon3:28.147,-15.408 | TICON-3 28.147N 15.408W (gesla.cmems) | MSL+ΣA (MSL+182 cm) | 47..326 | — | 1.8 |
| ticon-c39d93 | ticon3:44.667,-63.583 | TICON-3 44.667N 63.583W (gesla.cmems) | MSL+ΣA (MSL+153 cm) | 43..256 | — | 1.2 |
| ticon-c4827f | ticon3:64.151,-21.940 | TICON-3 64.151N 21.940W (gesla.noaa) | MSL+ΣA (MSL+307 cm) | 79..536 | — | 2.4 |
| ticon-c5c611 | ticon3:-16.722,-151.032 | TICON-3 16.722S 151.032W (gesla.meds) | MSL+ΣA (MSL+32 cm) | 15..54 | — | 0.8 |
| ticon-c8afda | ticon3:11.235,-74.222 | TICON-3 11.235N 74.222W (gesla.noaa) | MSL+ΣA (MSL+55 cm) | 26..89 | — | 0.6 |
| ticon-c94350 | ticon3:35.223,-75.635 | TICON-3 35.223N 75.635W (gesla.noaa) | MSL+ΣA (MSL+117 cm) | 42..201 | — | 0.9 |
| ticon-c9798b | ticon3:28.047,-16.718 | TICON-3 28.047N 16.718W (gesla.ispra) | MSL+ΣA (MSL+158 cm) | 41..288 | — | 1.3 |
| ticon-cb76c0 | ticon3:-27.361,153.172 | TICON-3 27.361S 153.172E (gesla.noaa) | MSL+ΣA (MSL+198 cm) | 84..339 | — | 1.9 |
| ticon-cc4437 | ticon3:13.583,-89.833 | TICON-3 13.583N 89.833W (gesla.jodc_jma) | MSL+ΣA (MSL+165 cm) | 47..291 | — | 1.1 |
| ticon-ce6910 | ticon3:44.410,8.925 | TICON-3 44.410N 8.925E (gesla.cmems) | MSL+ΣA (MSL+37 cm) | 11..58 | — | 0.3 |
| ticon-cead8e | ticon3:51.217,-4.117 | TICON-3 51.217N 4.117W (gesla.meds) | MSL | -482..517 | — | 7.9 |
| ticon-cf2b1c | ticon3:-4.817,-37.050 | TICON-3 4.817S 37.050W (gesla.cmems) | MSL+ΣA (MSL+214 cm) | 54..383 | — | 1.9 |
| ticon-d1d551 | ticon3:8.273,-82.860 | TICON-3 8.273N 82.860W (gesla.meds) | MSL+ΣA (MSL+236 cm) | 58..421 | — | 1.8 |
| ticon-d44c01 | ticon3:-5.083,-81.167 | TICON-3 5.083S 81.167W (gesla.meds) | MSL+ΣA (MSL+138 cm) | 38..239 | — | 1.1 |
| ticon-d6e282 | ticon3:13.100,-59.617 | TICON-3 13.100N 59.617W (gesla.noaa) | MSL+ΣA (MSL+77 cm) | 19..123 | — | 1.6 |
| ticon-dad966 | ticon3:-13.417,-76.133 | TICON-3 13.417S 76.133W (gesla.meds) | MSL+ΣA (MSL+89 cm) | 39..152 | — | 0.7 |
| ticon-db052f | ticon3:58.974,5.730 | TICON-3 58.974N 5.730E (gesla.cmems) | MSL+ΣA (MSL+58 cm) | 18..95 | — | 0.7 |
| ticon-dcec93 | ticon3:-28.537,153.552 | TICON-3 28.537S 153.552E (gesla.noaa) | MSL+ΣA (MSL+147 cm) | 64..258 | — | 1.2 |
| ticon-de0584 | ticon3:20.868,-86.867 | TICON-3 20.868N 86.867W (gesla.smhi) | MSL+ΣA (MSL+4 cm) | 2..7 | — | 0.1 |
| ticon-e0b462 | ticon3:-34.716,135.870 | TICON-3 34.716S 135.870E (gesla.cco) | MSL+ΣA (MSL+152 cm) | 77..255 | — | 1.6 |
| ticon-e27616 | ticon3:-31.826,115.739 | TICON-3 31.826S 115.739E (gesla.meds) | MSL+ΣA (MSL+81 cm) | 28..138 | — | 0.6 |
| ticon-e3c7ab | ticon3:-34.907,150.759 | TICON-3 34.907S 150.759E (gesla.meds) | MSL+ΣA (MSL+130 cm) | 51..229 | — | 1.1 |
| ticon-e3d81c | ticon3:37.735,-25.672 | TICON-3 37.735N 25.672W (gesla.noaa) | MSL+ΣA (MSL+115 cm) | 29..209 | — | 0.9 |
| ticon-e4bed3 | ticon3:48.022,-4.538 | TICON-3 48.022N 4.538W (gesla.noaa) | MSL+ΣA (MSL+350 cm) | 86..610 | — | 3.1 |
| ticon-e56019 | ticon3:53.392,-6.068 | TICON-3 53.392N 6.068W (gesla.cmems) | MSL+ΣA (MSL+334 cm) | 99..557 | — | 3.3 |
| ticon-e56f80 | ticon3:46.007,-1.174 | TICON-3 46.007N 1.174W (gesla.noaa) | MSL+ΣA (MSL+446 cm) | 93..725 | — | 4.4 |
| ticon-e5fdba | ticon3:31.850,-116.633 | TICON-3 31.850N 116.633W (gesla.noaa) | MSL+ΣA (MSL+193 cm) | 60..324 | — | 1.1 |
| ticon-e6afd5 | ticon3:-7.752,109.017 | TICON-3 7.752S 109.017E (gesla.noaa) | MSL+ΣA (MSL+179 cm) | 67..298 | — | 1.3 |
| ticon-ea07a4 | ticon3:43.345,-124.322 | TICON-3 43.345N 124.322W (gesla.uhslc) | MSL+ΣA (MSL+260 cm) | 59..424 | — | 1.3 |
| ticon-ec093c | ticon3:-35.109,138.467 | TICON-3 35.109S 138.467E (gesla.jodc_jma) | MSL+ΣA (MSL+210 cm) | 98..341 | — | 3.3 |
| ticon-eede5f | ticon3:33.450,-118.483 | TICON-3 33.450N 118.483W (gesla.bom) | MSL+ΣA (MSL+197 cm) | 62..326 | — | 2.3 |
| ticon-f1b139 | ticon3:14.300,-91.917 | TICON-3 14.300N 91.917W (gesla.usgs) | MSL+ΣA (MSL+148 cm) | 45..260 | — | 1.6 |
| ticon-f43039 | ticon3:46.281,-124.046 | TICON-3 46.281N 124.046W (gesla.nhs) | MSL+ΣA (MSL+287 cm) | 75..465 | — | 1.5 |
| ticon-f58020 | ticon3:49.918,-6.316 | TICON-3 49.918N 6.316W (gesla.cdwr) | MSL+ΣA (MSL+387 cm) | 99..678 | — | 3.7 |
| ticon-f5b09a | ticon3:-12.973,-38.517 | TICON-3 12.973S 38.517W (gesla.cmems) | MSL+ΣA (MSL+189 cm) | 47..333 | — | 1.8 |
| ticon-f5d38f | ticon3:-34.475,150.910 | TICON-3 34.475S 150.910E (gesla.meds) | MSL+ΣA (MSL+140 cm) | 51..250 | — | 1.0 |
| ticon-f5f23b | ticon3:34.469,-120.682 | TICON-3 34.469N 120.682W (gesla.jodc_pahb) | MSL+ΣA (MSL+190 cm) | 53..316 | — | 0.9 |
| ticon-f6d60a | ticon3:9.400,-84.167 | TICON-3 9.400N 84.167W (gesla.noaa) | MSL+ΣA (MSL+210 cm) | 51..375 | — | 1.6 |
| ticon-f72d96 | ticon3:47.644,-3.446 | TICON-3 47.644N 3.446W (gesla.jodc_jma) | MSL+ΣA (MSL+341 cm) | 70..592 | — | 3.0 |
| ticon-f923c0 | ticon3:20.790,-156.995 | TICON-3 20.790N 156.995W (gesla.meds) | MSL+ΣA (MSL+84 cm) | 43..146 | — | 0.8 |
| ticon-f96d3c | ticon3:32.867,-117.257 | TICON-3 32.867N 117.257W (gesla.usgs) | MSL+ΣA (MSL+195 cm) | 58..327 | — | 1.1 |
| ticon-fb0d01 | ticon3:-33.900,18.433 | TICON-3 33.900S 18.433E (gesla.meds) | MSL+ΣA (MSL+124 cm) | 33..223 | — | 1.2 |
| ticon-fc3571 | ticon3:-17.762,168.293 | TICON-3 17.762S 168.293E (gesla.cmems) | MSL+ΣA (MSL+114 cm) | 23..183 | — | 0.8 |
| ticon-fd3ce7 | ticon3:-33.630,115.394 | TICON-3 33.630S 115.394E (gesla.sfwmd) | MSL+ΣA (MSL+86 cm) | 28..144 | — | 0.6 |

## Regiones

### AR-MDP — Mar del Plata–Necochea (22 picos)

- `got-6cb02d` GOT5.6 37.995S 57.544W (AR-MDP) — modelo global GOT5.6: 14 picos a 0.0–30 km, radio 40 km
- `got-7d5db3` GOT5.6 38.270S 57.840W (AR-MDP) — modelo global GOT5.6: 4 picos a 0.0–19 km, radio 30 km
- `got-798f17` GOT5.6 38.589S 58.740W (AR-MDP) — modelo global GOT5.6: 3 picos a 0.0–10 km, radio 20 km
- Sin puerto (Open-Meteo): CLAROMECÓ

### AR-BAN — Pinamar y Villa Gesell (16 picos)

- `got-2613c9` GOT5.6 37.230S 56.948W (AR-BAN) — modelo global GOT5.6: 10 picos a 0.0–15 km, radio 26 km
- `got-d42e6d` GOT5.6 36.580S 56.690W (AR-BAN) — modelo global GOT5.6: 6 picos a 0.0–25 km, radio 35 km

### AR-SUR — Patagonia (6 picos)

- `got-b2745e` GOT5.6 38.999S 61.295W (AR-SUR) — modelo global GOT5.6: 2 picos a 0.0–22 km, radio 33 km
- `got-2c8cf0` GOT5.6 41.053S 62.823W (AR-SUR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-1940fc` GOT5.6 40.812S 65.085W (AR-SUR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Sin puerto (Open-Meteo): PLAYA UNIÓN (ticon-1d4610 a 62 km: cruza 59 km de tierra), RADA TILLY
- Descartadas: `ticon-1d4610` 62 km, cruza 59 km de tierra

### BR-RS — Rio Grande do Sul (18 picos)

- `got-11c637` GOT5.6 29.544S 49.875W (BR-RS) — modelo global GOT5.6: 7 picos a 0.0–28 km, radio 39 km
- `got-642556` GOT5.6 29.976S 50.121W (BR-RS) — modelo global GOT5.6: 7 picos a 0.0–25 km, radio 36 km
- `got-a0b2f5` GOT5.6 30.240S 50.230W (BR-RS) — modelo global GOT5.6: 2 picos a 0.0–12 km, radio 22 km
- Sin puerto (Open-Meteo): CASSINO, MOLHES DA BARRA
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): CIDREIRA → got-a0b2f5

### BR-RS-SUL — Rio Grande do Sul sur (2 picos)

- `got-47f025` GOT5.6 33.743S 53.370W (BR-RS-SUL) — modelo global GOT5.6: 2 picos a 0.0–13 km, radio 24 km

### BR-SC-NOR — Santa Catarina norte y Paraná (20 picos)

- `got-c94e22` GOT5.6 26.630S 48.678W (BR-SC-NOR) — modelo global GOT5.6: 6 picos a 0.0–30 km, radio 40 km
- `got-d8f761` GOT5.6 25.697S 48.467W (BR-SC-NOR) — modelo global GOT5.6: 5 picos a 0.0–23 km, radio 34 km
- `got-dfbfb8` GOT5.6 27.115S 48.605W (BR-SC-NOR) — modelo global GOT5.6: 5 picos a 0.0–19 km, radio 30 km
- Sin puerto (Open-Meteo): BREJATUBA, ITAPOÁ, ENSEADA, UBATUBA
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): NAVEGANTES → got-dfbfb8
- Descartadas: `ticon-757122` 70 km, cruza 59 km de tierra

### BR-SP — São Paulo (29 picos)

- `ticon-752b4c` TICON-3 23.500S 45.117W (gesla.cmems) — TICON-3, misma costa: 16 picos a 1.3–55 km, radio 66 km (niveles 2,4)
- `ticon-757122` TICON-3 25.017S 47.925W (gesla.meds) — TICON-3, cruzando tierra: 1 picos a 49–49 km, radio 60 km
- `got-9803e3` GOT5.6 23.760S 45.870W (BR-SP) — modelo global GOT5.6: 6 picos a 0.0–26 km, radio 36 km
- Sin puerto (Open-Meteo): TOMBO, ASTÚRIAS, PITANGUEIRAS, ENSEADA, PRAIA GRANDE SP, ITANHAÉM
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): TOQUE-TOQUE → got-9803e3, PAÚBA → got-9803e3, MARESIAS → got-9803e3
- Descartadas: `ticon-752b4c` 61 km, cruza 22 km de tierra

### BR-RJ — Río de Janeiro (17 picos)

- `ticon-2559e1` TICON-3 22.933S 43.133W (gesla.noaa) — TICON-3, misma costa: 17 picos a 4.7–42 km, radio 53 km (niveles 2,4)
- Descartadas: `ticon-cd2c42` 7.2 km, fuera por el tope de 3 puertos (nivel 4)

### BR-RJL — Saquarema y Región de los Lagos (20 picos)

- `ticon-2559e1` TICON-3 22.933S 43.133W (gesla.noaa) — TICON-3, cruzando tierra: 6 picos a 17–59 km, radio 69 km
- `got-5c5f01` GOT5.6 22.752S 41.912W (BR-RJL) — modelo global GOT5.6: 10 picos a 0.0–26 km, radio 37 km
- `got-243beb` GOT5.6 22.942S 42.359W (BR-RJL) — modelo global GOT5.6: 4 picos a 0.0–16 km, radio 26 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): VILATUR → got-243beb, BARRA NOVA → got-243beb
- Descartadas: `ticon-cd2c42` 21 km, fuera por el tope de 3 puertos (nivel 4); `ticon-2559e1` 63 km, cruza 46 km de tierra

### BR-ES — Espírito Santo (19 picos)

- `got-d43a78` GOT5.6 20.330S 40.285W (BR-ES) — modelo global GOT5.6: 9 picos a 0.0–23 km, radio 34 km
- `got-1a5319` GOT5.6 20.659S 40.488W (BR-ES) — modelo global GOT5.6: 5 picos a 0.0–31 km, radio 42 km
- `got-1426bf` GOT5.6 18.426S 39.704W (BR-ES) — modelo global GOT5.6: 2 picos a 0.0–32 km, radio 43 km
- Sin puerto (Open-Meteo): REGÊNCIA, BARRA DO RIACHO, MARATAÍZES
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): PONTA DA FRUTA → got-1a5319

### BR-BA — Bahía (21 picos)

- `ticon-f5b09a` TICON-3 12.973S 38.517W (gesla.cmems) — TICON-3, cruzando tierra: 6 picos a 17–55 km, radio 66 km
- `got-260f66` GOT5.6 14.347S 38.980W (BR-BA) — modelo global GOT5.6: 7 picos a 0.0–6.7 km, radio 17 km
- `got-b18ed4` GOT5.6 12.577S 38.003W (BR-BA) — modelo global GOT5.6: 4 picos a 0.0–11 km, radio 21 km
- Sin puerto (Open-Meteo): CURURUPE (ticon-890b60 a 91 km: cruza 25 km de tierra), OLIVENÇA (ticon-890b60 a 80 km: cruza 25 km de tierra), MUCUGÊ (ticon-890b60 a 87 km: cruza 85 km de tierra), TRANCOSO (ticon-890b60 a 104 km: cruza 84 km de tierra)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BUSCA VIDA → got-b18ed4
- Descartadas: `ticon-f5b09a` 61 km, cruza 51 km de tierra; `ticon-890b60` 80 km, cruza 25 km de tierra

### BR-NE-CE — Ceará (12 picos)

- `ticon-c1874d` TICON-3 3.717S 38.483W (gesla.cmems) — TICON-3, misma costa: 6 picos a 2.0–102 km, radio 113 km (niveles 2,4)
- `ticon-cf2b1c` TICON-3 4.817S 37.050W (gesla.cmems) — TICON-3, misma costa: 1 picos a 81–81 km, radio 92 km
- `got-0a9164` GOT5.6 2.497S 44.248W (BR-NE-CE) — modelo global GOT5.6: 2 picos a 0.0–7.9 km, radio 18 km
- Sin puerto (Open-Meteo): JERICOACOARA, PREÁ, MUNDAÚ (ticon-c1874d a 115 km: cruza 22 km de tierra)
- Descartadas: `ticon-ee2dcc` 0.3 km, cruza 22 km de tierra; `ticon-c1874d` 115 km, cruza 22 km de tierra

### BR-NE-RN — Rio Grande do Norte y Paraíba (13 picos)

- `got-a8e5b2` GOT5.6 5.877S 35.173W (BR-NE-RN) — modelo global GOT5.6: 5 picos a 0.0–20 km, radio 31 km
- `got-770eaa` GOT5.6 7.148S 34.796W (BR-NE-RN) — modelo global GOT5.6: 5 picos a 0.0–20 km, radio 31 km
- `got-f89309` GOT5.6 6.237S 35.046W (BR-NE-RN) — modelo global GOT5.6: 3 picos a 0.0–16 km, radio 26 km
- Descartadas: `ticon-ead2f2` 85 km, cruza 22 km de tierra; `ticon-2b1454` 119 km, cruza 72 km de tierra

### BR-NE-PE — Pernambuco Alagoas y Sergipe (14 picos)

- `ticon-2b1454` TICON-3 8.350S 34.950W (gesla.noaa) — TICON-3, misma costa: 9 picos a 1.6–26 km, radio 37 km (niveles 2,4)
- `got-aa96f4` GOT5.6 9.667S 35.710W (BR-NE-PE) — modelo global GOT5.6: 3 picos a 0.0–18 km, radio 28 km
- `got-1afd1e` GOT5.6 11.000S 37.040W (BR-NE-PE) — modelo global GOT5.6: 2 picos a 0.0–5.8 km, radio 16 km
- Descartadas: `ticon-ead2f2` 8.4 km, fuera por el tope de 3 puertos (nivel 4)

### BR-NOR — Fernando de Noronha (5 picos)

- `ticon-4c1497` TICON-3 3.828S 32.403W (gesla.usgs) — TICON-3, misma costa: 5 picos a 1.4–4.3 km, radio 15 km

### CL-NOR — Arica a Antofagasta (11 picos)

- `ticon-39e748` TICON-3 18.467S 70.333W (gesla.uhslc) — TICON-3, misma costa: 6 picos a 1.5–7.3 km, radio 18 km (niveles 2,4)
- `got-332a05` GOT5.6 20.237S 70.140W (CL-NOR) — modelo global GOT5.6: 5 picos a 0.0–6.9 km, radio 17 km

### CL-CEN — Valparaíso y Coquimbo (20 picos)

- `ticon-9450da` TICON-3 33.027S 71.627W (gesla.noaa) — TICON-3, misma costa: 19 picos a 8.3–99 km, radio 110 km (niveles 2,4)
- `got-22dcfd` GOT5.6 30.092S 71.360W (CL-CEN) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### CL-PIC — Pichilemu (12 picos)

- `got-668790` GOT5.6 34.129S 71.998W (CL-PIC) — modelo global GOT5.6: 6 picos a 0.0–29 km, radio 40 km
- `got-dfa80c` GOT5.6 34.516S 72.041W (CL-PIC) — modelo global GOT5.6: 6 picos a 0.0–13 km, radio 24 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LA PUNTILLA → got-dfa80c, PLAYA PRINCIPAL → got-dfa80c, LAS TERRAZAS → got-dfa80c
- Descartadas: `ticon-9450da` 107 km, cruza 26 km de tierra

### CL-MAU — Maule y Biobío (14 picos)

- `got-5888b8` GOT5.6 36.070S 72.800W (CL-MAU) — modelo global GOT5.6: 4 picos a 0.0–35 km, radio 45 km
- `got-def45c` GOT5.6 34.923S 72.174W (CL-MAU) — modelo global GOT5.6: 3 picos a 0.0–20 km, radio 31 km
- `got-04ac46` GOT5.6 35.344S 72.430W (CL-MAU) — modelo global GOT5.6: 2 picos a 0.0–46 km, radio 57 km
- Sin puerto (Open-Meteo): DICHATO, COCHOLGÜE, PUNTA LAVAPIÉ, LEBU, TIRÚA
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): CHANCO → got-5888b8

### CL-SUR — Araucanía a Los Lagos (11 picos)

- `got-0d6795` GOT5.6 39.390S 73.215W (CL-SUR) — modelo global GOT5.6: 3 picos a 0.0–20 km, radio 31 km
- `got-b81c05` GOT5.6 40.575S 73.736W (CL-SUR) — modelo global GOT5.6: 3 picos a 0.0–4.3 km, radio 15 km
- `got-9decc4` GOT5.6 39.774S 73.400W (CL-SUR) — modelo global GOT5.6: 2 picos a 0.0–11 km, radio 21 km
- Sin puerto (Open-Meteo): PUERTO SAAVEDRA, MAR BRAVA (ticon-7b3808 a 100 km: cruza 66 km de tierra), CUCAO
- Descartadas: `ticon-7b3808` 100 km, cruza 66 km de tierra

### PE-NOR — Tumbes y Piura (10 picos)

- `ticon-55de77` TICON-3 4.582S 81.282W (gesla.cmems) — TICON-3, cruzando tierra: 7 picos a 15–59 km, radio 70 km
- `ticon-d44c01` TICON-3 5.083S 81.167W (gesla.meds) — TICON-3, misma costa: 1 picos a 14–14 km, radio 25 km
- `got-04911c` GOT5.6 3.677S 80.670W (PE-NOR) — modelo global GOT5.6: 2 picos a 0.0–48 km, radio 59 km
- Descartadas: `ticon-d44c01` 71 km, cruza 42 km de tierra; `ticon-55de77` 75 km, cruza 62 km de tierra

### PE-LLB — La Libertad y Lambayeque (7 picos)

- `got-30731c` GOT5.6 6.880S 79.950W (PE-LLB) — modelo global GOT5.6: 3 picos a 0.0–11 km, radio 22 km
- `got-ddd9f6` GOT5.6 7.410S 79.580W (PE-LLB) — modelo global GOT5.6: 2 picos a 0.0–36 km, radio 47 km
- `got-8a708f` GOT5.6 8.062S 79.123W (PE-LLB) — modelo global GOT5.6: 2 picos a 0.0–2.0 km, radio 13 km

### PE-LIM — Lima (15 picos)

- `ticon-41bc98` TICON-3 12.068S 77.167W (gesla.cmems) — TICON-3, misma costa: 14 picos a 14–58 km, radio 68 km (niveles 2,4)
- `ticon-dad966` TICON-3 13.417S 76.133W (gesla.meds) — TICON-3, cruzando tierra: 1 picos a 57–57 km, radio 68 km
- Descartadas: `ticon-50523e` 14 km, fuera por el tope de 3 puertos (nivel 4)

### PE-SUR — Ica y Arequipa (5 picos)

- `ticon-3b2a68` TICON-3 17.002S 72.108W (gesla.cmems) — TICON-3, misma costa: 5 picos a 8.5–106 km, radio 116 km (niveles 2,4)

### EC-COS — Costa de Ecuador (13 picos)

- `noaa-9991474` La Libertad, Bahia de Santa Elena — oficial, misma costa: 6 picos a 3.7–59 km, radio 70 km
- `got-26250e` GOT5.6 0.870N 79.850W (EC-COS) — modelo global GOT5.6: 2 picos a 0.0–45 km, radio 55 km
- `got-cff16a` GOT5.6 0.939S 80.733W (EC-COS) — modelo global GOT5.6: 2 picos a 0.0–21 km, radio 32 km
- Sin puerto (Open-Meteo): CANOA, ENGABAO (ticon-9f8ea6 a 63 km: cruza 34 km de tierra), PLAYAS (ticon-9f8ea6 a 76 km: cruza 73 km de tierra)
- Descartadas: `ticon-9f8ea6` 4.3 km, fuera por el tope de 3 puertos (nivel 2)

### EC-GAL — Galápagos (4 picos)

- `noaa-9992401` San Cristobal, Galapagos islands — oficial, misma costa: 4 picos a 0.7–2.3 km, radio 13 km
- Descartadas: `ticon-238d7e` 89 km, fuera por el tope de 3 puertos (nivel 2)

### CO-PAC — Pacífico colombiano (6 picos)

- `ticon-67a479` TICON-3 3.890N 77.062W (gesla.noaa) — TICON-3, cruzando tierra: 2 picos a 35–35 km, radio 45 km
- `got-cb31f0` GOT5.6 6.100N 77.420W (CO-PAC) — modelo global GOT5.6: 3 picos a 0.0–19 km, radio 29 km
- `got-b461dd` GOT5.6 5.713N 77.264W (CO-PAC) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### CO-CAR — Caribe colombiano (3 picos)

- `ticon-c8afda` TICON-3 11.235N 74.222W (gesla.noaa) — TICON-3, cruzando tierra: 1 picos a 42–42 km, radio 52 km
- `got-f4a045` GOT5.6 11.040N 74.910W (CO-CAR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-d2f680` GOT5.6 11.243N 73.568W (CO-CAR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-c8afda` 71 km, cruza 69 km de tierra; `ticon-6f989c` 100 km, cruza 97 km de tierra

### VE-ALL — Venezuela (2 picos)

- `got-c73835` GOT5.6 10.500N 67.690W (VE-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-c96e4a` GOT5.6 11.130N 63.850W (VE-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### PA-PAC — Pacífico de Panamá (7 picos)

- `got-5e72ab` GOT5.6 7.619N 81.243W (PA-PAC) — modelo global GOT5.6: 3 picos a 0.0–0.8 km, radio 11 km
- `got-f0c08b` GOT5.6 7.300N 80.380W (PA-PAC) — modelo global GOT5.6: 3 picos a 0.0–26 km, radio 36 km
- `got-b6d772` GOT5.6 8.456N 79.966W (PA-PAC) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-8ab032` 70 km, cruza 20 km de tierra; `ticon-eebce1` 71 km, cruza 35 km de tierra; `ticon-9edf76` 100 km, cruza 95 km de tierra

### PA-BDT — Bocas del Toro (4 picos)

- `got-707910` GOT5.6 9.382N 82.235W (PA-BDT) — modelo global GOT5.6: 4 picos a 0.0–5.2 km, radio 16 km

### CR-GUA — Guanacaste norte (12 picos)

- `got-3d80b7` GOT5.6 10.240N 85.842W (CR-GUA) — modelo global GOT5.6: 10 picos a 0.0–10 km, radio 21 km
- `got-91f084` GOT5.6 10.850N 85.801W (CR-GUA) — modelo global GOT5.6: 2 picos a 0.0–13 km, radio 23 km
- Descartadas: `ticon-c1d17a` 109 km, cruza 70 km de tierra

### CR-NIC — Nicoya sur (11 picos)

- `ticon-293edc` TICON-3 9.425N 84.172W (gesla.uhslc) — TICON-3, misma costa: 4 picos a 110–115 km, radio 125 km
- `got-06d168` GOT5.6 9.876N 85.628W (CR-NIC) — modelo global GOT5.6: 7 picos a 0.0–20 km, radio 31 km
- Descartadas: `ticon-c1d17a` 51 km, cruza 50 km de tierra; `noaa-9684403` 51 km, fuera por el tope de 3 puertos (nivel 3); `ticon-f6d60a` 111 km, fuera por el tope de 3 puertos (nivel 2)

### CR-PAC — Pacífico central (10 picos)

- `ticon-f6d60a` TICON-3 9.400N 84.167W (gesla.noaa) — TICON-3, misma costa: 7 picos a 2.7–54 km, radio 65 km (niveles 2,4)
- `noaa-9684403` Puntarenas — oficial, cruzando tierra: 3 picos a 11–53 km, radio 64 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): PLAYA HERMOSA → ticon-f6d60a
- Descartadas: `ticon-293edc` 4.9 km, cruza 81 km de tierra; `ticon-c1d17a` 11 km, fuera por el tope de 3 puertos (nivel 4); `ticon-f6d60a` 88 km, cruza 78 km de tierra

### CR-OSA — Osa y Golfo Dulce (4 picos)

- `ticon-d1d551` TICON-3 8.273N 82.860W (gesla.meds) — TICON-3, cruzando tierra: 4 picos a 33–50 km, radio 60 km

### CR-CAR — Caribe de Costa Rica (5 picos)

- `got-95d729` GOT5.6 9.634N 82.712W (CR-CAR) — modelo global GOT5.6: 3 picos a 0.0–2.6 km, radio 13 km
- `got-2175da` GOT5.6 10.003N 83.027W (CR-CAR) — modelo global GOT5.6: 2 picos a 0.0–49 km, radio 60 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): SALSA BRAVA → got-95d729

### NI-RIV — Rivas y Popoyo (8 picos)

- `got-8bd957` GOT5.6 11.300N 85.910W (NI-RIV) — modelo global GOT5.6: 8 picos a 0.0–32 km, radio 42 km

### NI-NW — Chinandega y León (4 picos)

- `got-e7ff80` GOT5.6 12.378N 87.042W (NI-NW) — modelo global GOT5.6: 3 picos a 0.0–38 km, radio 49 km
- `got-6f9c71` GOT5.6 12.760N 87.450W (NI-NW) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-955da1` 75 km, cruza 33 km de tierra

### SV-LIB — La Libertad (8 picos)

- `ticon-cc4437` TICON-3 13.583N 89.833W (gesla.jodc_jma) — TICON-3, cruzando tierra: 8 picos a 28–56 km, radio 67 km
- Descartadas: `ticon-cade3e` 28 km, fuera por el tope de 3 puertos (nivel 4)

### SV-ORI — Oriente de El Salvador (4 picos)

- `noaa-9640507` La Union (Cutuco) — oficial, cruzando tierra: 4 picos a 33–44 km, radio 54 km
- Descartadas: `ticon-955da1` 33 km, fuera por el tope de 3 puertos (nivel 4)

### GT-PAC — Pacífico de Guatemala (4 picos)

- `ticon-b76b33` TICON-3 13.917N 90.833W (gesla.uhslc) — TICON-3, misma costa: 3 picos a 26–39 km, radio 50 km (niveles 2,4)
- `ticon-f1b139` TICON-3 14.300N 91.917W (gesla.usgs) — TICON-3, misma costa: 1 picos a 1.7–1.7 km, radio 12 km
- Descartadas: `ticon-ac8ed6` 31 km, fuera por el tope de 3 puertos (nivel 4); `ticon-d6b62a` 71 km, cruza 52 km de tierra; `ticon-22d3ad` 74 km, cruza 18 km de tierra; `ticon-cc4437` 76 km, fuera por el tope de 3 puertos (nivel 2)

### MX-OAX — Oaxaca (13 picos)

- `ticon-45502d` TICON-3 15.667N 96.492W (gesla.noaa) — TICON-3, misma costa: 5 picos a 3.0–59 km, radio 69 km (niveles 2,4)
- `ticon-73effe` TICON-3 15.753N 96.130W (gesla.noaa) — TICON-3, cruzando tierra: 1 picos a 21–21 km, radio 31 km
- `got-56fcd4` GOT5.6 15.861N 97.063W (MX-OAX) — modelo global GOT5.6: 6 picos a 0.0–3.5 km, radio 14 km
- Sin puerto (Open-Meteo): CHACAHUA
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BARRA DE COLOTEPEC → got-56fcd4
- Descartadas: `ticon-3a8b4f` 2.8 km, cruza 60 km de tierra; `ticon-45502d` 60 km, cruza 58 km de tierra; `ticon-73effe` 66 km, cruza 64 km de tierra; `ticon-da7060` 88 km, cruza 82 km de tierra

### MX-PAC — Colima Michoacán y Guerrero (12 picos)

- `ticon-6b84e3` TICON-3 19.063N 104.298W (gesla.usgs) — TICON-3, misma costa: 4 picos a 8.2–103 km, radio 114 km (niveles 2,4)
- `ticon-7b330d` TICON-3 17.940N 102.178W (gesla.jodc_jma) — TICON-3, misma costa: 3 picos a 45–88 km, radio 98 km
- `ticon-34de1f` TICON-3 16.838N 99.903W (gesla.meds) — TICON-3, misma costa: 2 picos a 8.4–13 km, radio 24 km
- Sin puerto (Open-Meteo): NEXPA (ticon-7b330d a 67 km: cruza 19 km de tierra), MARUATA, FARO DE BUCERIAS
- Descartadas: `ticon-41f6ff` 5.2 km, fuera por el tope de 3 puertos (nivel 4); `ticon-aa9293` 6.5 km, fuera por el tope de 3 puertos (nivel 2); `ticon-32cb80` 7.0 km, fuera por el tope de 3 puertos (nivel 2); `ticon-b15d4e` 16 km, fuera por el tope de 3 puertos (nivel 2)

### MX-NAY — Nayarit Jalisco y Sinaloa (9 picos)

- `ticon-9bc4f0` TICON-3 23.198N 106.422W (gesla.rws) — TICON-3, misma costa: 2 picos a 1.3–12 km, radio 23 km (niveles 2,4)
- `got-addc69` GOT5.6 20.955N 105.356W (MX-NAY) — modelo global GOT5.6: 4 picos a 0.0–27 km, radio 37 km
- `got-c504a0` GOT5.6 20.769N 105.526W (MX-NAY) — modelo global GOT5.6: 3 picos a 0.0–0.9 km, radio 11 km

### MX-BCS — Baja California Sur (6 picos)

- `ticon-8e0567` TICON-3 22.880N 109.908W (gesla.sfwmd) — TICON-3, cruzando tierra: 5 picos a 24–57 km, radio 67 km
- `got-6d1313` GOT5.6 23.400N 110.211W (MX-BCS) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LOS CERRITOS → got-6d1313
- Descartadas: `ticon-8e0567` 66 km, cruza 55 km de tierra; `ticon-1e3abf` 86 km, cruza 83 km de tierra; `ticon-19b631` 97 km, cruza 84 km de tierra

### MX-BCS-N — Baja Sur Pacífico norte (2 picos)

- `got-8d76ed` GOT5.6 26.704N 113.578W (MX-BCS-N) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-a806af` GOT5.6 26.250N 112.480W (MX-BCS-N) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### MX-BCN — Baja California (4 picos)

- `noaa-9410135` South San Diego Bay, CA — oficial, cruzando tierra: 2 picos a 11–31 km, radio 42 km
- `ticon-e5fdba` TICON-3 31.850N 116.633W (gesla.noaa) — TICON-3, misma costa: 2 picos a 11–17 km, radio 28 km
- Descartadas: `ticon-d15dee` 21 km, fuera por el tope de 3 puertos (nivel 4); `noaa-9410170` 21 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9410196` 31 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9410230` 40 km, fuera por el tope de 3 puertos (nivel 3)

### MX-CAR — Caribe mexicano (3 picos)

- `ticon-de0584` TICON-3 20.868N 86.867W (gesla.smhi) — TICON-3, cruzando tierra: 2 picos a 23–34 km, radio 44 km
- `got-713511` GOT5.6 20.214N 87.429W (MX-CAR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-de0584` 93 km, cruza 43 km de tierra

### PR-NW — Rincón e Isabela (15 picos)

- `noaa-9759412` Aguadilla, PR — oficial, misma costa: 11 picos a 0.4–16 km, radio 27 km (niveles 1,3)
- `noaa-9757809` Arecibo, PR — oficial, misma costa: 3 picos a 38–42 km, radio 53 km
- `noaa-9759394` Mayaguez, PR — oficial, misma costa: 1 picos a 16–16 km, radio 26 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): TUNELES → noaa-9759412, GAS CHAMBERS → noaa-9759412, JOBOS → noaa-9759412
- Descartadas: `ticon-b30a21` 0.3 km, fuera por el tope de 3 puertos (nivel 4); `noaa-9759421` 20 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9759183` 25 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9759189` 29 km, fuera por el tope de 3 puertos (nivel 3)

### PR-N — San Juan y costa norte (8 picos)

- `noaa-9756567` Boca del Cibuco, PR — oficial, misma costa: 4 picos a 1.3–15 km, radio 25 km
- `noaa-9754986` Boca de Cangrejos, PR — oficial, misma costa: 3 picos a 1.5–6.8 km, radio 17 km
- `noaa-9753766` Luquillo, PR — oficial, misma costa: 1 picos a 1.3–1.3 km, radio 12 km
- Descartadas: `noaa-9755371` 6.4 km, fuera por el tope de 3 puertos (nivel 3); `ticon-538987` 6.4 km, fuera por el tope de 3 puertos (nivel 4); `noaa-9753216` 11 km, fuera por el tope de 3 puertos (nivel 3); `ticon-70ba43` 11 km, cruza 49 km de tierra

### BB-ALL — Barbados (8 picos)

- `ticon-d6e282` TICON-3 13.100N 59.617W (gesla.noaa) — TICON-3, misma costa: 8 picos a 1.9–16 km, radio 27 km (niveles 2,4)

### DO-ALL — República Dominicana (2 picos)

- `ticon-b63d75` TICON-3 19.798N 70.702W (gesla.noaa) — TICON-3, misma costa: 2 picos a 26–30 km, radio 40 km (niveles 2,4)

### GP-ALL — Guadalupe (3 picos)

- `ticon-b604d6` TICON-3 16.303N 61.072W (gesla.usgs) — TICON-3, misma costa: 3 picos a 12–52 km, radio 62 km (niveles 2,4)
- Descartadas: `ticon-8856b1` 22 km, fuera por el tope de 3 puertos (nivel 4); `ticon-3aa8da` 30 km, fuera por el tope de 3 puertos (nivel 4); `ticon-7c3620` 108 km, cruza 30 km de tierra

### MQ-ALL — Martinica (3 picos)

- `ticon-4c1a6a` TICON-3 14.678N 60.941W (gesla.fmi) — TICON-3, misma costa: 3 picos a 11–29 km, radio 40 km (niveles 2,4)
- Descartadas: `ticon-4f5636` 14 km, fuera por el tope de 3 puertos (nivel 4); `ticon-af7a2e` 25 km, fuera por el tope de 3 puertos (nivel 4); `ticon-7c3620` 57 km, fuera por el tope de 3 puertos (nivel 4)

### BS-ALL — Bahamas (1 picos)

- `got-87528f` GOT5.6 25.420N 76.623W (BS-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### TT-ALL — Trinidad y Tobago (4 picos)

- `ticon-73a14b` TICON-3 10.650N 61.517W (gesla.meds) — TICON-3, cruzando tierra: 2 picos a 15–18 km, radio 29 km
- `got-7c798b` GOT5.6 11.196N 60.800W (TT-ALL) — modelo global GOT5.6: 2 picos a 0.0–9.3 km, radio 20 km
- Descartadas: `ticon-73a14b` 99 km, cruza 26 km de tierra

### US-CA-SD — San Diego (38 picos)

- `noaa-9410230` La Jolla (Scripps Institution Wharf), CA — oficial, misma costa: 26 picos a 0.0–40 km, radio 51 km
- `noaa-9410196` Mission Bay, Campland, CA — oficial, misma costa: 7 picos a 3.1–8.7 km, radio 19 km (niveles 1,3)
- `noaa-9410135` South San Diego Bay, CA — oficial, misma costa: 5 picos a 6.0–17 km, radio 28 km (niveles 1,3)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LUSCOMBS → noaa-9410230, LUSCOMBS → noaa-9410196, LADERA ST → noaa-9410230, LADERA ST → noaa-9410196
- Descartadas: `ticon-f96d3c` 0.1 km, fuera por el tope de 3 puertos (nivel 2); `ticon-d15dee` 3.8 km, fuera por el tope de 3 puertos (nivel 4); `noaa-9410170` 3.9 km, fuera por el tope de 3 puertos (nivel 3); `ticon-e5fdba` 91 km, cruza 88 km de tierra

### US-CA-OC — Orange County (32 picos)

- `noaa-9410678` Long Beach Fire Boat Pier, CA — oficial, misma costa: 13 picos a 10–58 km, radio 69 km
- `noaa-9410580` Newport Bay Entrance, Corona del Mar, CA — oficial, misma costa: 10 picos a 1.1–23 km, radio 34 km
- `ticon-f96d3c` TICON-3 32.867N 117.257W (gesla.usgs) — TICON-3, misma costa: 9 picos a 63–75 km, radio 86 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): GOLDENWEST → noaa-9410580, HUNTINGTON PIER → noaa-9410580, HUNTINGTON CLIFFS → noaa-9410580, MAIN BEACH → noaa-9410580, BROOKS STREET → noaa-9410580, THALIA STREET → noaa-9410580, VICTORIA BEACH → noaa-9410580, ALISO BEACH → noaa-9410580, TABLE ROCK → noaa-9410580, DOHENY → noaa-9410580, CAPO BEACH → noaa-9410678, CAPO BEACH → noaa-9410580, POCHE → noaa-9410678, POCHE → noaa-9410580, CALAFIA → noaa-9410678, CALAFIA → noaa-9410580, SAN CLEMENTE PIER → noaa-9410678, SAN CLEMENTE PIER → noaa-9410580, T-STREET → noaa-9410678, T-STREET → noaa-9410580
- Descartadas: `noaa-9410680` 11 km, fuera por el tope de 3 puertos (nivel 1); `noaa-9410660` 15 km, fuera por el tope de 3 puertos (nivel 1); `noaa-9410079` 44 km, fuera por el tope de 3 puertos (nivel 1); `noaa-9410840` 47 km, fuera por el tope de 3 puertos (nivel 3)

### US-CA-LA — Los Ángeles (23 picos)

- `noaa-9410840` Santa Monica, Municipal Pier, CA — oficial, misma costa: 17 picos a 0.1–30 km, radio 41 km
- `ticon-eede5f` TICON-3 33.450N 118.483W (gesla.bom) — TICON-3, misma costa: 4 picos a 71–78 km, radio 89 km
- `noaa-9410660` LOS ANGELES (Outer Harbor), CA — oficial, misma costa: 2 picos a 1.6–4.3 km, radio 15 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LUNADA BAY → noaa-9410660, LEO CARRILLO → noaa-9410840, NICHOLAS CANYON → noaa-9410840, LECHUZA → noaa-9410840, TRANCAS → noaa-9410840
- Descartadas: `noaa-9410680` 6.9 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9410678` 7.4 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9410580` 39 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9410079` 41 km, fuera por el tope de 3 puertos (nivel 1)

### US-CA-SB — Santa Bárbara y Ventura (27 picos)

- `noaa-9411270` Rincon Island, Mussel Shoals, CA — oficial, misma costa: 17 picos a 3.7–55 km, radio 66 km (niveles 1,3)
- `noaa-9411340` Santa Barbara, CA — oficial, misma costa: 9 picos a 0.4–40 km, radio 50 km (niveles 1,3)
- `noaa-9411406` Oil Platform Harvest, CA — oficial, misma costa: 1 picos a 17–17 km, radio 28 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LOOKOUT → noaa-9411340, CAMPUS POINT → noaa-9411340, COAL OIL POINT → noaa-9411340, HASKELL'S → noaa-9411340, ELLWOOD → noaa-9411340, VENTURA PIER → noaa-9411270, C STREET → noaa-9411270
- Descartadas: `noaa-9411399` 15 km, fuera por el tope de 3 puertos (nivel 3); `ticon-f5f23b` 17 km, cruza 16 km de tierra; `noaa-9410840` 43 km, fuera por el tope de 3 puertos (nivel 3); `ticon-27b349` 77 km, cruza 34 km de tierra

### US-CA-CEN — Big Sur y San Luis Obispo (16 picos)

- `noaa-9412110` PORT SAN LUIS, CA — oficial, misma costa: 8 picos a 0.3–56 km, radio 67 km (niveles 1,3)
- `ticon-f5f23b` TICON-3 34.469N 120.682W (gesla.jodc_pahb) — TICON-3, misma costa: 6 picos a 89–111 km, radio 121 km
- `noaa-9413450` MONTEREY, MONTEREY BAY, CA — oficial, cruzando tierra: 2 picos a 20–35 km, radio 46 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): HAZARD CANYON → noaa-9412110, SPOONER'S COVE → noaa-9412110, SANDSPIT → noaa-9412110, MORRO ROCK → noaa-9412110, MORRO STRAND → noaa-9412110, CAYUCOS PIER → noaa-9412110
- Descartadas: `ticon-27b349` 0.3 km, fuera por el tope de 3 puertos (nivel 2); `ticon-431aeb` 0.9 km, fuera por el tope de 3 puertos (nivel 2); `noaa-9413631` 45 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9413643` 47 km, fuera por el tope de 3 puertos (nivel 3)

### US-CA-SC — Santa Cruz y Monterey (30 picos)

- `noaa-9413450` MONTEREY, MONTEREY BAY, CA — oficial, misma costa: 26 picos a 1.1–57 km, radio 67 km (niveles 1,3)
- `noaa-9413631` Elkhorn, Elkhorn Slough, CA — oficial, misma costa: 4 picos a 4.4–56 km, radio 67 km (niveles 1,3)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): SCOTT CREEK → noaa-9413631, DAVENPORT LANDING → noaa-9413631, NATURAL BRIDGES → noaa-9413631, MITCHELL'S COVE → noaa-9413631, STEAMER LANE → noaa-9413631, COWELL'S → noaa-9413631, 26TH AVE → noaa-9413631, 38TH AVE → noaa-9413631, SEWER PEAK → noaa-9413631, THE HOOK → noaa-9413631, PLEASURE POINT → noaa-9413631, MORAN LAKE → noaa-9413631, CAPITOLA → noaa-9413631, SEACLIFF → noaa-9413631, RIO DEL MAR → noaa-9413631, MANRESA → noaa-9413631, SUNSET BEACH → noaa-9413631
- Descartadas: `noaa-9413643` 5.4 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9413651` 5.9 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9413663` 6.7 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9414523` 46 km, fuera por el tope de 3 puertos (nivel 3)

### US-CA-SF — San Francisco y San Mateo (29 picos)

- `noaa-9414958` Bolinas Lagoon, CA — oficial, misma costa: 16 picos a 0.5–38 km, radio 48 km
- `noaa-9414131` Pillar Point Harbor, Half Moon Bay, CA — oficial, misma costa: 11 picos a 0.3–25 km, radio 35 km
- `noaa-9415020` Point Reyes, CA — oficial, misma costa: 2 picos a 9.3–48 km, radio 59 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): FORT FUNSTON → noaa-9414131, MUSSEL ROCK → noaa-9414131, PACIFICA PIER → noaa-9414131, SHARP PARK → noaa-9414131, ROCKAWAY → noaa-9414131, LINDA MAR → noaa-9414131, PEDRO POINT → noaa-9414131, FORT POINT → noaa-9414958, FORT POINT → noaa-9414131
- Descartadas: `ticon-091b06` 0.4 km, fuera por el tope de 3 puertos (nivel 4); `noaa-9414290` 1.1 km, fuera por el tope de 3 puertos (nivel 1); `ticon-b6ac13` 1.1 km, fuera por el tope de 3 puertos (nivel 2); `noaa-9414317` 8.2 km, fuera por el tope de 3 puertos (nivel 3)

### US-CA-NOR — Humboldt y Mendocino (25 picos)

- `noaa-9416841` ARENA COVE, CA — oficial, misma costa: 9 picos a 0.0–58 km, radio 68 km (niveles 1,3)
- `noaa-9418817` Samoa, CA — oficial, misma costa: 7 picos a 7.6–36 km, radio 46 km (niveles 1,3)
- `noaa-9415020` Point Reyes, CA — oficial, misma costa: 4 picos a 36–52 km, radio 62 km (niveles 1,3)
- Sin puerto (Open-Meteo): GLASS BEACH (noaa-9417426 a 3.0 km: fuera por el tope de 3 puertos), VIRGIN CREEK (noaa-9417426 a 4.6 km: fuera por el tope de 3 puertos), WESTPORT (noaa-9417426 a 23 km: fuera por el tope de 3 puertos), SHELTER COVE (noaa-9418024 a 1.2 km: fuera por el tope de 3 puertos), CRESCENT BEACH (noaa-9419750 a 5.2 km: fuera por el tope de 3 puertos)
- Descartadas: `ticon-0aba89` 0.0 km, cruza 37 km de tierra; `noaa-9417426` 0.7 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9418024` 1.2 km, fuera por el tope de 3 puertos (nivel 1); `ticon-00bd43` 2.1 km, fuera por el tope de 3 puertos (nivel 4)

### US-PNW — Oregón y Washington (33 picos)

- `ticon-f43039` TICON-3 46.281N 124.046W (gesla.nhs) — TICON-3, misma costa: 12 picos a 3.1–119 km, radio 130 km (niveles 2,4)
- `noaa-9435380` Southbeach, OR — oficial, misma costa: 10 picos a 2.2–53 km, radio 64 km (niveles 1,3)
- `ticon-ea07a4` TICON-3 43.345N 124.322W (gesla.uhslc) — TICON-3, misma costa: 5 picos a 4.4–71 km, radio 81 km (niveles 2,4)
- Sin puerto (Open-Meteo): HOBUCK (ticon-a43379 a 8.7 km: fuera por el tope de 3 puertos), RIALTO (noaa-9442396 a 1.0 km: fuera por el tope de 3 puertos), SECOND BEACH (noaa-9442396 a 4.0 km: fuera por el tope de 3 puertos), MANZANITA (noaa-9437954 a 5.2 km: fuera por el tope de 3 puertos), PORT ORFORD (noaa-9431647 a 0.1 km: fuera por el tope de 3 puertos), HARRIS BEACH (noaa-9419945 a 15 km: fuera por el tope de 3 puertos)
- Descartadas: `noaa-9431647` 0.1 km, fuera por el tope de 3 puertos (nivel 3); `ticon-c2a383` 0.2 km, cruza 45 km de tierra; `noaa-9435827` 0.6 km, fuera por el tope de 3 puertos (nivel 3); `noaa-9433445` 0.9 km, fuera por el tope de 3 puertos (nivel 3)

### US-GULF — Texas (13 picos)

- `ticon-440073` TICON-3 28.936N 95.294W (gesla.noaa) — TICON-3, misma costa: 6 picos a 1.0–66 km, radio 76 km (niveles 2,4)
- `noaa-8775270` Port Aransas (H. Caldwell Pier), TX — oficial, misma costa: 4 picos a 0.9–51 km, radio 62 km
- `noaa-8779770` Port Isabel, TX — oficial, misma costa: 3 picos a 5.9–10 km, radio 20 km
- Descartadas: `noaa-8779750` 0.2 km, fuera por el tope de 3 puertos (nivel 3); `noaa-8772479` 0.4 km, fuera por el tope de 3 puertos (nivel 1); `noaa-8779749` 0.4 km, fuera por el tope de 3 puertos (nivel 3); `ticon-cf3fe8` 0.4 km, fuera por el tope de 3 puertos (nivel 4)

### US-FL — Florida (46 picos)

- `ticon-1b2d0f` TICON-3 29.857N 81.263W (gesla.meds) — TICON-3, misma costa: 17 picos a 0.3–113 km, radio 124 km (niveles 2,4)
- `noaa-8721649` Cocoa Beach, FL — oficial, misma costa: 12 picos a 0.1–59 km, radio 69 km (niveles 1,3)
- `noaa-8723080` Haulover Pier, N. Miami Beach, FL — oficial, misma costa: 6 picos a 0.4–49 km, radio 59 km (niveles 1,3)
- Sin puerto (Open-Meteo): FLAGLER AVE (noaa-8721164 a 0.6 km: fuera por el tope de 3 puertos), WABASSO (ticon-fe5fc9 a 4.9 km: fuera por el tope de 3 puertos), VERO BEACH (noaa-8722125 a 2.6 km: fuera por el tope de 3 puertos), FORT PIERCE INLET (noaa-8722213 a 0.6 km: fuera por el tope de 3 puertos), JENSEN BEACH (noaa-8722329 a 2.3 km: fuera por el tope de 3 puertos), STUART BEACH (noaa-8722371 a 3.3 km: fuera por el tope de 3 puertos), JUPITER INLET (ticon-d6a529 a 1.7 km: fuera por el tope de 3 puertos), JUNO PIER (noaa-8722548 a 4.2 km: fuera por el tope de 3 puertos), LAKE WORTH PIER (ticon-4477db a 0.1 km: fuera por el tope de 3 puertos), BOYNTON INLET (ticon-bbc21e a 0.9 km: fuera por el tope de 3 puertos), DELRAY BEACH (noaa-8722761 a 1.6 km: fuera por el tope de 3 puertos)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): APOLLO BEACH → noaa-8721649
- Descartadas: `ticon-266c41` 0.1 km, cruza 50 km de tierra; `ticon-4477db` 0.1 km, cruza 59 km de tierra; `noaa-8722670` 0.1 km, fuera por el tope de 3 puertos (nivel 3); `noaa-8723178` 0.2 km, fuera por el tope de 3 puertos (nivel 3)

### US-FL-PAN — Golfo este (Luisiana a Florida) (6 picos)

- `noaa-8731269` Gulf State Park Pier, AL — oficial, misma costa: 4 picos a 0.6–52 km, radio 62 km (niveles 1,3)
- `noaa-8729210` Panama City Beach, FL — oficial, misma costa: 1 picos a 6.2–6.2 km, radio 17 km
- `noaa-8761724` EAST POINT, GRAND ISLE, LA — oficial, misma costa: 1 picos a 3.3–3.3 km, radio 14 km
- Descartadas: `noaa-8730667` 0.3 km, fuera por el tope de 3 puertos (nivel 3); `noaa-8729806` 0.6 km, fuera por el tope de 3 puertos (nivel 1); `noaa-8729807` 0.6 km, fuera por el tope de 3 puertos (nivel 1); `noaa-8735181` 3.0 km, fuera por el tope de 3 puertos (nivel 1)

### US-SE — Carolina del Norte (22 picos)

- `ticon-c94350` TICON-3 35.223N 75.635W (gesla.noaa) — TICON-3, misma costa: 12 picos a 10–117 km, radio 127 km (niveles 2,4)
- `noaa-8658163` Wrightsville Beach, NC — oficial, misma costa: 6 picos a 0.8–32 km, radio 43 km
- `noaa-8659897` Sunset Beach Pier, NC — oficial, misma costa: 3 picos a 12–57 km, radio 67 km
- Sin puerto (Open-Meteo): COROLLA (noaa-8651370 a 22 km: fuera por el tope de 3 puertos)
- Descartadas: `ticon-083b2e` 0.2 km, fuera por el tope de 3 puertos (nivel 2); `noaa-8653215` 0.8 km, fuera por el tope de 3 puertos (nivel 3); `noaa-8661419` 0.8 km, fuera por el tope de 3 puertos (nivel 1); `ticon-9ddfca` 0.8 km, cruza 19 km de tierra

### US-SC-GA — Carolina del Sur y Georgia (10 picos)

- `noaa-8668498` Fripps Inlet, Hunting Island Bridge, SC — oficial, misma costa: 5 picos a 5.1–60 km, radio 70 km (niveles 1,3)
- `noaa-8665530` CHARLESTON (Customhouse Wharf), SC — oficial, misma costa: 3 picos a 8.0–14 km, radio 25 km (niveles 1,3)
- `noaa-8677344` St. Simons Light, GA — oficial, misma costa: 2 picos a 0.6–3.9 km, radio 14 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): THE WASHOUT → noaa-8665530
- Descartadas: `ticon-c9840c` 0.6 km, cruza 20 km de tierra; `ticon-3bbb9d` 5.1 km, cruza 24 km de tierra; `noaa-8670870` 6.7 km, fuera por el tope de 3 puertos (nivel 3); `ticon-ee3312` 6.7 km, cruza 19 km de tierra

### US-MID — Virginia Maryland y Delaware (11 picos)

- `noaa-8536110` Cape May, ferry terminal, NJ — oficial, misma costa: 6 picos a 24–57 km, radio 68 km
- `noaa-8639207` Rudee Inlet, interior channel, VA — oficial, misma costa: 3 picos a 0.4–13 km, radio 23 km
- `noaa-8570280` OCEAN CITY (FISHING PIER), MD — oficial, misma costa: 2 picos a 0.2–12 km, radio 22 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): FENWICK ISLAND → noaa-8570280
- Descartadas: `ticon-13e72d` 0.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-9f975c` 0.2 km, fuera por el tope de 3 puertos (nivel 2); `noaa-8558690` 0.3 km, fuera por el tope de 3 puertos (nivel 3); `ticon-b5103e` 0.3 km, fuera por el tope de 3 puertos (nivel 4)

### US-NE — Nueva Inglaterra Nueva York y Nueva Jersey (60 picos)

- `noaa-8517137` Beach Channel (bridge), NY — oficial, misma costa: 14 picos a 0.6–59 km, radio 69 km (niveles 1,3)
- `noaa-8459338` Block Island (Old Harbor), RI — oficial, misma costa: 10 picos a 22–58 km, radio 68 km (niveles 1,3)
- `noaa-8534720` Atlantic City (Ocean), NJ — oficial, misma costa: 10 picos a 0.5–56 km, radio 66 km (niveles 1,3)
- Sin puerto (Open-Meteo): HIGGINS BEACH (noaa-8418445 a 10 km: fuera por el tope de 3 puertos), OLD ORCHARD PIER (noaa-8418445 a 4.6 km: fuera por el tope de 3 puertos), CAMP ELLIS (noaa-8418606 a 0.4 km: fuera por el tope de 3 puertos), LONG SANDS (noaa-8423898 a 15 km: fuera por el tope de 3 puertos), POPHAM BEACH (noaa-8417177 a 2.7 km: fuera por el tope de 3 puertos), HAMPTON BEACH (noaa-8440452 a 10 km: fuera por el tope de 3 puertos), JENNESS BEACH (ticon-a3d2bf a 8.3 km: fuera por el tope de 3 puertos), WALLIS SANDS (ticon-a3d2bf a 5.2 km: fuera por el tope de 3 puertos), SALISBURY BEACH (noaa-8440452 a 3.2 km: fuera por el tope de 3 puertos), PLUM ISLAND (noaa-8440452 a 1.9 km: fuera por el tope de 3 puertos), GOOD HARBOR (noaa-8441551 a 6.1 km: fuera por el tope de 3 puertos), NAHANT (noaa-8443187 a 3.5 km: fuera por el tope de 3 puertos), REVERE BEACH (noaa-8443725 a 4.4 km: fuera por el tope de 3 puertos), NANTASKET (noaa-8444162 a 6.9 km: fuera por el tope de 3 puertos), NAUSET LIGHT (noaa-8447435 a 19 km: fuera por el tope de 3 puertos), MARCONI BEACH (noaa-8447241 a 23 km: fuera por el tope de 3 puertos), CAHOON HOLLOW (noaa-8446121 a 21 km: fuera por el tope de 3 puertos), NOBADEER (noaa-8449130 a 3.7 km: fuera por el tope de 3 puertos), SURFSIDE (noaa-8449130 a 4.6 km: fuera por el tope de 3 puertos), CISCO (noaa-8449130 a 4.8 km: fuera por el tope de 3 puertos), SOUTH BEACH MV (noaa-8448558 a 3.7 km: fuera por el tope de 3 puertos), SQUIBNOCKET (noaa-8448725 a 3.1 km: fuera por el tope de 3 puertos), FLYING POINT (noaa-8512354 a 7.3 km: fuera por el tope de 3 puertos), SHINNECOCK INLET (noaa-8512354 a 0.2 km: fuera por el tope de 3 puertos), SEASIDE HEIGHTS (ticon-fe5724 a 1.3 km: fuera por el tope de 3 puertos), CAPE MAY (ticon-8eeb07 a 3.1 km: fuera por el tope de 3 puertos)
- Descartadas: `noaa-8512354` 0.2 km, fuera por el tope de 3 puertos (nivel 3); `ticon-c19baa` 0.3 km, fuera por el tope de 3 puertos (nivel 2); `noaa-8515186` 0.3 km, fuera por el tope de 3 puertos (nivel 1); `ticon-096046` 0.4 km, cruza 18 km de tierra

### US-HI-OAN — North Shore de Oahu (21 picos)

- `noaa-1612401` Ford Island, Pearl Harbor, HI — oficial, cruzando tierra: 21 picos a 30–36 km, radio 47 km
- Descartadas: `ticon-71d7df` 30 km, fuera por el tope de 3 puertos (nivel 4); `noaa-1612404` 31 km, fuera por el tope de 3 puertos (nivel 3); `noaa-1612366` 34 km, fuera por el tope de 3 puertos (nivel 3); `noaa-1612480` 37 km, fuera por el tope de 3 puertos (nivel 3)

### US-HI-OAS — Oahu sur oeste y este (25 picos)

- `noaa-1612340` HONOLULU, HI — oficial, misma costa: 13 picos a 1.7–49 km, radio 59 km (niveles 1,3)
- `ticon-f923c0` TICON-3 20.790N 156.995W (gesla.meds) — TICON-3, misma costa: 8 picos a 89–102 km, radio 112 km
- `ticon-71d7df` TICON-3 21.320N 158.120W (gesla.meds) — TICON-3, misma costa: 4 picos a 4.4–21 km, radio 31 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): YOKOHAMA BAY → ticon-71d7df, KAHALA → noaa-1612340, PORTLOCK → noaa-1612340, CHINA WALLS → noaa-1612340, SANDY BEACH → noaa-1612340, MAKAPUU → noaa-1612340, WAIMANALO → noaa-1612340, BELLOWS → noaa-1612340, KAILUA → noaa-1612340
- Descartadas: `ticon-30cfc5` 0.8 km, fuera por el tope de 3 puertos (nivel 2); `ticon-8de1e3` 2.2 km, fuera por el tope de 3 puertos (nivel 2); `ticon-1dd3c0` 4.2 km, fuera por el tope de 3 puertos (nivel 2); `noaa-1612480` 7.6 km, fuera por el tope de 3 puertos (nivel 3)

### US-HI-MAU — Maui (21 picos)

- `noaa-1615680` KAHULUI, HI — oficial, misma costa: 12 picos a 6.4–54 km, radio 65 km (niveles 1,3)
- `noaa-1613198` Kaunakakai, HI — oficial, misma costa: 5 picos a 42–53 km, radio 63 km
- `ticon-215748` TICON-3 20.900N 156.467W (gesla.noaa) — TICON-3, misma costa: 4 picos a 8.2–12 km, radio 23 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): JAWS → ticon-215748, PAIA BAY → ticon-215748, STABLES → ticon-215748, SPRECKS → ticon-215748, HONOLUA → ticon-215748, MALA RAMP → noaa-1615680, MALA RAMP → ticon-215748, BREAKWALL → noaa-1615680, BREAKWALL → ticon-215748, PUAMANA → noaa-1615680, PUAMANA → ticon-215748, LAUNIUPOKO → noaa-1615680, LAUNIUPOKO → ticon-215748, OLOWALU → noaa-1615680, OLOWALU → ticon-215748
- Descartadas: `ticon-828e7d` 7.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-b36d04` 25 km, cruza 24 km de tierra; `ticon-f923c0` 34 km, cruza 21 km de tierra; `ticon-311cc3` 77 km, cruza 25 km de tierra

### US-HI-KAU — Kauai (21 picos)

- `noaa-1611400` NAWILIWILI, HI — oficial, misma costa: 11 picos a 0.8–35 km, radio 45 km (niveles 1,3)
- `noaa-1611347` Port Allen, Hanapepe Bay, HI — oficial, misma costa: 10 picos a 1.4–36 km, radio 47 km (niveles 1,3)
- Descartadas: `ticon-51d791` 1.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-8e273c` 1.4 km, fuera por el tope de 3 puertos (nivel 4)

### US-HI-BIG — Isla Grande de Hawái (15 picos)

- `noaa-1617433` Kawaihae, HI — oficial, misma costa: 10 picos a 4.9–55 km, radio 65 km (niveles 1,3)
- `noaa-1617760` HILO, HI — oficial, misma costa: 4 picos a 4.3–40 km, radio 51 km (niveles 1,3)
- `got-b07ca8` GOT5.6 19.415N 155.909W (US-HI-BIG) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-67ab43` 4.8 km, fuera por el tope de 3 puertos (nivel 2); `ticon-311cc3` 4.9 km, cruza 60 km de tierra; `ticon-215748` 109 km, cruza 42 km de tierra; `ticon-828e7d` 109 km, cruza 41 km de tierra

### CA-BC-VI — Isla de Vancouver (14 picos)

- `ticon-a43379` TICON-3 48.368N 124.617W (gesla.cmems) — TICON-3, misma costa: 8 picos a 27–115 km, radio 126 km
- `ticon-7cfb7a` TICON-3 49.150N 125.910W (gesla.noaa) — TICON-3, misma costa: 4 picos a 1.4–11 km, radio 21 km
- `ticon-488f81` TICON-3 50.510N 128.030W (gesla.uhslc) — TICON-3, cruzando tierra: 2 picos a 18–27 km, radio 37 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LONG BEACH → ticon-7cfb7a, COMBERS → ticon-7cfb7a
- Descartadas: `ticon-a68c68` 7.9 km, fuera por el tope de 3 puertos (nivel 4); `ticon-8bf5f3` 11 km, cruza 62 km de tierra; `noaa-9443361` 24 km, fuera por el tope de 3 puertos (nivel 1); `ticon-7b82ce` 24 km, fuera por el tope de 3 puertos (nivel 4)

### CA-NS — Nueva Escocia (11 picos)

- `ticon-c39d93` TICON-3 44.667N 63.583W (gesla.cmems) — TICON-3, cruzando tierra: 8 picos a 12–35 km, radio 46 km
- `ticon-10c275` TICON-3 44.520N 64.000W (gesla.uhslc) — TICON-3, misma costa: 2 picos a 40–43 km, radio 53 km
- `got-e49ea1` GOT5.6 43.951N 64.818W (CA-NS) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-d63c38` 15 km, fuera por el tope de 3 puertos (nivel 4); `ticon-827ed5` 34 km, fuera por el tope de 3 puertos (nivel 4); `ticon-2a5ef5` 37 km, fuera por el tope de 3 puertos (nivel 4); `ticon-307108` 41 km, fuera por el tope de 3 puertos (nivel 4)

### AU-QLD-SC — Sunshine Coast (27 picos)

- `ticon-cb76c0` TICON-3 27.361S 153.172E (gesla.noaa) — TICON-3, misma costa: 5 picos a 31–109 km, radio 120 km
- `got-7a487c` GOT5.6 26.596S 153.107E (AU-QLD-SC) — modelo global GOT5.6: 21 picos a 0.0–24 km, radio 34 km
- `got-3334f6` GOT5.6 25.932S 153.189E (AU-QLD-SC) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): TEA TREE BAY → got-7a487c, GRANITE BAY → got-7a487c, ALEXANDRIA BAY → got-7a487c, SUNRISE BEACH → got-7a487c
- Descartadas: `ticon-cb76c0` 62 km, cruza 16 km de tierra; `ticon-a04e3a` 76 km, cruza 22 km de tierra; `ticon-a1343b` 101 km, fuera por el tope de 3 puertos (nivel 2)

### AU-QLD-GC — Gold Coast (24 picos)

- `ticon-a1343b` TICON-3 27.967S 153.417E (gesla.noaa) — TICON-3, misma costa: 24 picos a 1.2–60 km, radio 71 km (niveles 2,4)
- Descartadas: `ticon-cb76c0` 38 km, cruza 25 km de tierra; `ticon-dcec93` 40 km, fuera por el tope de 3 puertos (nivel 4)

### AU-NSW-NR — Northern Rivers (26 picos)

- `ticon-dcec93` TICON-3 28.537S 153.552E (gesla.noaa) — TICON-3, misma costa: 14 picos a 0.4–30 km, radio 41 km (niveles 2,4)
- `ticon-2fe7b0` TICON-3 29.429S 153.362E (gesla.cmems) — TICON-3, misma costa: 11 picos a 1.1–74 km, radio 84 km (niveles 2,4)
- `ticon-a1343b` TICON-3 27.967S 153.417E (gesla.noaa) — TICON-3, misma costa: 1 picos a 31–31 km, radio 42 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LENNOX HEAD → ticon-dcec93, LIGHTHOUSE BEACH → ticon-dcec93, SHELLY BEACH → ticon-dcec93, NORTH WALL → ticon-dcec93
- Descartadas: `ticon-a1343b` 65 km, cruza 56 km de tierra; `ticon-dcec93` 65 km, cruza 54 km de tierra; `ticon-2fe7b0` 77 km, cruza 13 km de tierra; `ticon-5dd235` 80 km, cruza 25 km de tierra

### AU-NSW-MN — Mid North Coast (33 picos)

- `ticon-5dd235` TICON-3 30.303S 153.146E (gesla.uhslc) — TICON-3, misma costa: 16 picos a 0.8–85 km, radio 95 km (niveles 2,4)
- `ticon-8ea705` TICON-3 31.427S 152.911E (gesla.usgs) — TICON-3, misma costa: 11 picos a 1.2–117 km, radio 127 km (niveles 2,4)
- `got-03f20d` GOT5.6 32.181S 152.524E (AU-NSW-MN) — modelo global GOT5.6: 6 picos a 0.0–26 km, radio 37 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BACK BEACH → ticon-8ea705, HAT HEAD → ticon-8ea705, BLUEYS BEACH → got-03f20d, TREACHERY BEACH → got-03f20d
- Descartadas: `ticon-8ea705` 61 km, cruza 29 km de tierra; `ticon-2fe7b0` 64 km, cruza 17 km de tierra; `ticon-03a6be` 89 km, cruza 53 km de tierra; `ticon-5dd235` 99 km, cruza 31 km de tierra

### AU-NSW-NC — Newcastle y Central Coast (30 picos)

- `ticon-03a6be` TICON-3 32.924S 151.789E (gesla.cmems) — TICON-3, misma costa: 23 picos a 0.6–74 km, radio 84 km (niveles 2,4)
- `ticon-393286` TICON-3 33.551S 151.275E (gesla.cmems) — TICON-3, misma costa: 4 picos a 5.1–22 km, radio 32 km (niveles 2,4)
- `ticon-809086` TICON-3 33.968S 151.220E (gesla.meds) — TICON-3, misma costa: 3 picos a 74–108 km, radio 118 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BATEAU BAY → ticon-393286, FORRESTERS BEACH → ticon-393286, TERRIGAL → ticon-393286, TERRIGAL → ticon-809086, AVOCA BEACH → ticon-393286, AVOCA BEACH → ticon-809086, COPACABANA → ticon-393286, COPACABANA → ticon-809086, MACMASTERS BEACH → ticon-393286, MACMASTERS BEACH → ticon-809086, BLACKSMITHS → ticon-03a6be, CATHERINE HILL BAY → ticon-03a6be, THE ENTRANCE → ticon-03a6be, THE ENTRANCE → ticon-393286
- Descartadas: `ticon-c0a455` 32 km, cruza 16 km de tierra; `ticon-aa5af3` 36 km, cruza 10 km de tierra; `ticon-393286` 61 km, cruza 12 km de tierra; `ticon-809086` 62 km, cruza 11 km de tierra

### AU-NSW-SYD — Sídney (37 picos)

- `ticon-f5d38f` TICON-3 34.475S 150.910E (gesla.meds) — TICON-3, misma costa: 18 picos a 31–105 km, radio 115 km
- `ticon-809086` TICON-3 33.968S 151.220E (gesla.meds) — TICON-3, misma costa: 10 picos a 3.1–12 km, radio 22 km
- `ticon-c0a455` TICON-3 33.825S 151.258E (gesla.wsv) — TICON-3, misma costa: 9 picos a 5.0–9.1 km, radio 20 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): MONA VALE → ticon-c0a455, WARRIEWOOD → ticon-c0a455, TURIMETTA → ticon-c0a455, NORTH NARRABEEN → ticon-c0a455, NARRABEEN → ticon-c0a455, COLLAROY → ticon-c0a455, LONG REEF → ticon-c0a455, DEE WHY → ticon-c0a455, DEE WHY POINT → ticon-c0a455, BUNGAN → ticon-c0a455, BRONTE → ticon-809086
- Descartadas: `ticon-aa5af3` 6.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-393286` 7.3 km, fuera por el tope de 3 puertos (nivel 2); `ticon-e3c7ab` 81 km, cruza 17 km de tierra; `ticon-03a6be` 86 km, cruza 24 km de tierra

### AU-NSW-SC — Illawarra y South Coast (31 picos)

- `ticon-f5d38f` TICON-3 34.475S 150.910E (gesla.meds) — TICON-3, misma costa: 21 picos a 6.1–28 km, radio 39 km
- `ticon-e3c7ab` TICON-3 34.907S 150.759E (gesla.meds) — TICON-3, misma costa: 4 picos a 3.8–20 km, radio 30 km
- `ticon-079795` TICON-3 35.705S 150.178E (gesla.cmems) — TICON-3, misma costa: 4 picos a 6.8–57 km, radio 67 km (niveles 2,4)
- Sin puerto (Open-Meteo): TATHRA (ticon-f9f8cf a 34 km: fuera por el tope de 3 puertos), PAMBULA BEACH (ticon-f9f8cf a 59 km: fuera por el tope de 3 puertos)
- Descartadas: `ticon-8800cd` 2.1 km, cruza 36 km de tierra; `ticon-ce4bf0` 21 km, cruza 16 km de tierra; `ticon-f9f8cf` 24 km, cruza 14 km de tierra; `ticon-809086` 36 km, fuera por el tope de 3 puertos (nivel 4)

### AU-VIC-SC — Surf Coast (20 picos)

- `ticon-902798` TICON-3 38.292S 144.614E (gesla.uhslc) — TICON-3, misma costa: 20 picos a 1.1–62 km, radio 72 km
- Descartadas: `ticon-dd3cfd` 5.7 km, fuera por el tope de 3 puertos (nivel 2); `ticon-f1d70a` 17 km, fuera por el tope de 3 puertos (nivel 2); `ticon-a1d519` 19 km, fuera por el tope de 3 puertos (nivel 4); `ticon-3e42a1` 23 km, fuera por el tope de 3 puertos (nivel 4)

### AU-VIC-PI — Phillip Island y Mornington (18 picos)

- `ticon-a8dc55` TICON-3 38.374S 145.223E (gesla.noaa) — TICON-3, misma costa: 10 picos a 15–22 km, radio 33 km (niveles 2,4)
- `ticon-902798` TICON-3 38.292S 144.614E (gesla.uhslc) — TICON-3, misma costa: 8 picos a 10–32 km, radio 43 km
- Descartadas: `ticon-dd3cfd` 9.0 km, fuera por el tope de 3 puertos (nivel 4); `ticon-d6c2b1` 13 km, fuera por el tope de 3 puertos (nivel 4); `ticon-f1d70a` 17 km, fuera por el tope de 3 puertos (nivel 4); `ticon-3e42a1` 28 km, cruza 14 km de tierra

### AU-VIC-W — Oeste de Victoria (9 picos)

- `ticon-3927f3` TICON-3 38.351S 141.620E (gesla.mi_c) — TICON-3, misma costa: 4 picos a 20–112 km, radio 123 km (niveles 2,4)
- `ticon-902798` TICON-3 38.292S 144.614E (gesla.uhslc) — TICON-3, misma costa: 2 picos a 74–77 km, radio 87 km
- `got-78d608` GOT5.6 38.780S 143.400E (AU-VIC-W) — modelo global GOT5.6: 2 picos a 0.0–21 km, radio 32 km
- Sin puerto (Open-Meteo): KILLARNEY BEACH (ticon-3927f3 a 61 km: cruza 18 km de tierra)
- Descartadas: `ticon-4ab7b4` 19 km, cruza 18 km de tierra; `ticon-3927f3` 61 km, cruza 18 km de tierra; `ticon-a1d519` 69 km, cruza 45 km de tierra; `ticon-dd3cfd` 79 km, fuera por el tope de 3 puertos (nivel 2)

### AU-TAS — Tasmania (12 picos)

- `ticon-48cda1` TICON-3 42.877S 147.341E (gesla.noaa) — TICON-3, misma costa: 4 picos a 19–50 km, radio 61 km (niveles 2,4)
- `ticon-00efc3` TICON-3 42.549S 147.928E (gesla.cmems) — TICON-3, misma costa: 2 picos a 2.3–31 km, radio 42 km (niveles 2,4)
- `got-23237f` GOT5.6 41.880S 148.296E (AU-TAS) — modelo global GOT5.6: 2 picos a 0.0–13 km, radio 23 km
- Sin puerto (Open-Meteo): BINALONG BAY, MARRAWAH (ticon-c246f2 a 107 km: cruza 104 km de tierra), GREEN POINT (ticon-c246f2 a 108 km: cruza 106 km de tierra), OCEAN BEACH
- Descartadas: `ticon-48cda1` 60 km, cruza 41 km de tierra; `ticon-00efc3` 69 km, cruza 12 km de tierra; `ticon-c246f2` 107 km, cruza 104 km de tierra

### AU-SA — Australia del Sur (14 picos)

- `ticon-ec093c` TICON-3 35.109S 138.467E (gesla.jodc_jma) — TICON-3, misma costa: 8 picos a 4.6–105 km, radio 116 km (niveles 2,4)
- `ticon-e0b462` TICON-3 34.716S 135.870E (gesla.cco) — TICON-3, misma costa: 3 picos a 103–108 km, radio 118 km
- `ticon-afa9fb` TICON-3 34.780S 138.481E (gesla.unam) — TICON-3, misma costa: 2 picos a 54–62 km, radio 72 km
- Sin puerto (Open-Meteo): VIVONNE BAY (ticon-e560dd a 94 km: cruza 57 km de tierra)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): PORT WILLUNGA → ticon-ec093c, SELLICKS → ticon-ec093c
- Descartadas: `ticon-8a7678` 34 km, fuera por el tope de 3 puertos (nivel 4); `ticon-e560dd` 36 km, fuera por el tope de 3 puertos (nivel 2); `ticon-afa9fb` 84 km, cruza 81 km de tierra

### AU-SA-EYR — Península de Eyre (3 picos)

- `got-a905b1` GOT5.6 32.083S 132.989E (AU-SA-EYR) — modelo global GOT5.6: 3 picos a 0.0–0.6 km, radio 11 km
- Descartadas: `ticon-ad0e9d` 61 km, cruza 40 km de tierra

### AU-WA-MR — Margaret River (32 picos)

- `ticon-fd3ce7` TICON-3 33.630S 115.394E (gesla.sfwmd) — TICON-3, misma costa: 25 picos a 37–59 km, radio 70 km (niveles 2,4)
- `ticon-9e0a4e` TICON-3 33.323S 115.660E (gesla.noaa) — TICON-3, misma costa: 5 picos a 67–70 km, radio 80 km
- `got-210825` GOT5.6 34.169S 115.030E (AU-WA-MR) — modelo global GOT5.6: 2 picos a 0.0–10 km, radio 20 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): REDGATE → got-210825, BOODJIDUP → got-210825, GAS BAY → got-210825, SUPERTUBES → ticon-fd3ce7, SMITHS → ticon-fd3ce7, YALLINGUP → ticon-fd3ce7, RABBIT HILL → ticon-fd3ce7, THREE BEARS → ticon-fd3ce7
- Descartadas: `ticon-fd3ce7` 64 km, cruza 60 km de tierra; `ticon-9e0a4e` 74 km, cruza 13 km de tierra; `ticon-a99647` 114 km, fuera por el tope de 3 puertos (nivel 2); `ticon-95a181` 120 km, fuera por el tope de 3 puertos (nivel 2)

### AU-WA-PER — Perth y Rottnest (20 picos)

- `ticon-bfaae8` TICON-3 32.056S 115.740E (gesla.noaa) — TICON-3, misma costa: 11 picos a 1.4–57 km, radio 68 km
- `ticon-e27616` TICON-3 31.826S 115.739E (gesla.meds) — TICON-3, misma costa: 7 picos a 1.2–39 km, radio 50 km
- `ticon-2e5983` TICON-3 32.601S 115.630E (gesla.noaa) — TICON-3, misma costa: 2 picos a 75–80 km, radio 90 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): YANCHEP → ticon-e27616, BURNS BEACH → ticon-e27616, OCEAN REEF → ticon-e27616, FLOREAT → ticon-e27616, SCARBOROUGH → ticon-bfaae8, SCARBOROUGH → ticon-e27616, CITY BEACH → ticon-bfaae8, CITY BEACH → ticon-e27616
- Descartadas: `ticon-fe7c61` 10 km, fuera por el tope de 3 puertos (nivel 4); `ticon-663fbe` 61 km, cruza 13 km de tierra; `ticon-95a181` 64 km, fuera por el tope de 3 puertos (nivel 2); `ticon-a99647` 72 km, cruza 16 km de tierra

### AU-WA-NW — Kalbarri y Geraldton (5 picos)

- `ticon-92ede9` TICON-3 28.776S 114.602E (gesla.uhslc) — TICON-3, misma costa: 3 picos a 0.6–25 km, radio 36 km
- `got-68a040` GOT5.6 27.720S 114.151E (AU-WA-NW) — modelo global GOT5.6: 2 picos a 0.0–1.7 km, radio 12 km

### AU-WA-GAS — Gascoyne (3 picos)

- `got-d032d9` GOT5.6 23.881S 113.488E (AU-WA-GAS) — modelo global GOT5.6: 2 picos a 0.0–17 km, radio 28 km
- `got-91ed50` GOT5.6 24.366S 113.406E (AU-WA-GAS) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-d814a1` 64 km, cruza 35 km de tierra

### NZ-NTL — Northland (14 picos)

- `linz-ben-gunn-wharf` Ben Gunn Wharf — oficial, cruzando tierra: 7 picos a 24–60 km, radio 70 km
- `linz-marsden-point` Marsden Point — oficial, misma costa: 6 picos a 4.7–33 km, radio 44 km (niveles 1,3)
- `linz-dargaville` Dargaville — oficial, cruzando tierra: 1 picos a 11–11 km, radio 22 km
- Descartadas: `ticon-563267` 4.7 km, cruza 63 km de tierra; `linz-whangaroa` 12 km, fuera por el tope de 3 puertos (nivel 3); `linz-whangarei` 19 km, fuera por el tope de 3 puertos (nivel 3); `linz-town-basin` 23 km, fuera por el tope de 3 puertos (nivel 3)

### NZ-AKL — Auckland oeste (9 picos)

- `linz-anawhata` Anawhata — oficial, misma costa: 7 picos a 1.8–14 km, radio 25 km
- `linz-paratutae-island` Paratutae Island — oficial, misma costa: 2 picos a 1.7–42 km, radio 53 km (niveles 1,3)
- Descartadas: `linz-helensville` 16 km, fuera por el tope de 3 puertos (nivel 3); `linz-onehunga` 28 km, fuera por el tope de 3 puertos (nivel 3); `linz-auckland` 29 km, fuera por el tope de 3 puertos (nivel 3); `ticon-c2422a` 29 km, fuera por el tope de 3 puertos (nivel 4)

### NZ-RAG — Raglan (5 picos)

- `linz-manu-bay` Manu Bay — oficial, misma costa: 5 picos a 0.6–10 km, radio 21 km (niveles 1,3)
- Descartadas: `linz-raglan` 5.4 km, fuera por el tope de 3 puertos (nivel 1); `linz-kawhia` 19 km, fuera por el tope de 3 puertos (nivel 3); `ticon-c2422a` 107 km, cruza 97 km de tierra

### NZ-TAR — Taranaki (7 picos)

- `linz-port-taranaki` Port Taranaki — oficial, misma costa: 6 picos a 2.4–47 km, radio 58 km (niveles 1,3)
- `ticon-b7fd2a` TICON-3 39.050S 174.033E (gesla.noaa) — TICON-3, misma costa: 1 picos a 63–63 km, radio 74 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): STENT ROAD → ticon-b7fd2a, OAKURA → ticon-b7fd2a, OPUNAKE → ticon-b7fd2a
- Descartadas: `ticon-ae5a20` 112 km, cruza 42 km de tierra

### NZ-BOP — Coromandel y Bay of Plenty (11 picos)

- `linz-moturiki-island` Moturiki Island — oficial, misma costa: 9 picos a 0.5–57 km, radio 67 km
- `linz-huruhi-harbour` Huruhi Harbour — oficial, misma costa: 1 picos a 32–32 km, radio 43 km
- `linz-port-ohope-wharf` Port Ōhope Wharf — oficial, misma costa: 1 picos a 4.4–4.4 km, radio 15 km
- Descartadas: `ticon-232aea` 1.5 km, fuera por el tope de 3 puertos (nivel 2); `linz-tauranga` 1.5 km, fuera por el tope de 3 puertos (nivel 1); `linz-kaituna-river-entrance` 3.0 km, fuera por el tope de 3 puertos (nivel 1); `linz-whakatane` 5.4 km, fuera por el tope de 3 puertos (nivel 1)

### NZ-GIS — Gisborne (13 picos)

- `linz-gisborne` Gisborne — oficial, misma costa: 13 picos a 2.6–12 km, radio 22 km (niveles 1,3)
- Descartadas: `ticon-407855` 2.4 km, fuera por el tope de 3 puertos (nivel 4)

### NZ-WEL — Wellington (13 picos)

- `linz-rangatira-point` Rangatira Point — oficial, misma costa: 6 picos a 6.2–45 km, radio 56 km
- `linz-wellington` Wellington — oficial, misma costa: 5 picos a 5.4–56 km, radio 66 km (niveles 1,3)
- `linz-castlepoint` Castlepoint — oficial, misma costa: 2 picos a 0.9–22 km, radio 33 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): MAKARA BEACH → linz-wellington, TITAHI BAY → linz-wellington
- Descartadas: `linz-mana-marina` 3.5 km, fuera por el tope de 3 puertos (nivel 3); `ticon-9caabc` 5.4 km, fuera por el tope de 3 puertos (nivel 2); `linz-okukari-bay` 33 km, fuera por el tope de 3 puertos (nivel 3); `linz-long-island` 38 km, fuera por el tope de 3 puertos (nivel 3)

### NZ-KAI — Kaikoura y Canterbury (9 picos)

- `linz-new-brighton-pier` New Brighton Pier — oficial, misma costa: 5 picos a 1.1–58 km, radio 69 km
- `linz-kaikoura` Kaikōura — oficial, misma costa: 3 picos a 1.1–13 km, radio 24 km
- `ticon-9caabc` TICON-3 41.283S 174.783E (gesla.noaa) — TICON-3, misma costa: 1 picos a 102–102 km, radio 113 km
- Descartadas: `linz-sumner-head` 1.1 km, fuera por el tope de 3 puertos (nivel 1); `ticon-2f9d0a` 5.6 km, fuera por el tope de 3 puertos (nivel 2); `linz-lyttelton` 5.6 km, fuera por el tope de 3 puertos (nivel 3); `linz-akaroa` 28 km, fuera por el tope de 3 puertos (nivel 3)

### NZ-OTA — Otago y Southland (13 picos)

- `linz-green-island` Green Island — oficial, misma costa: 4 picos a 4.1–10 km, radio 21 km
- `linz-spit-wharf` Spit Wharf — oficial, misma costa: 4 picos a 1.0–17 km, radio 27 km
- `linz-dog-island` Dog Island — oficial, misma costa: 3 picos a 24–53 km, radio 63 km (niveles 1,3)
- Sin puerto (Open-Meteo): KAKA POINT, PAPATOWAI
- Descartadas: `linz-dunedin` 3.6 km, fuera por el tope de 3 puertos (nivel 3); `linz-port-chalmers` 6.4 km, fuera por el tope de 3 puertos (nivel 1); `linz-riverton-aparima` 7.4 km, fuera por el tope de 3 puertos (nivel 1); `linz-waihopai-river-entrance` 7.5 km, fuera por el tope de 3 puertos (nivel 3)

### NZ-WC — Costa Oeste (4 picos)

- `linz-westport` Westport — oficial, misma costa: 2 picos a 3.1–11 km, radio 21 km
- `got-bea209` GOT5.6 42.450S 171.198E (NZ-WC) — modelo global GOT5.6: 2 picos a 0.0–36 km, radio 46 km
- Descartadas: `ticon-5b5bc7` 2.5 km, fuera por el tope de 3 puertos (nivel 2); `linz-charleston` 18 km, fuera por el tope de 3 puertos (nivel 3)

### FJ-MAM — Mamanucas (6 picos)

- `ticon-1c9970` TICON-3 17.605S 177.438E (gesla.uhslc) — TICON-3, misma costa: 6 picos a 38–41 km, radio 52 km

### FJ-SOU — Coral Coast y Beqa (2 picos)

- `ticon-233ae7` TICON-3 18.132S 178.427E (gesla.cmems) — TICON-3, misma costa: 1 picos a 65–65 km, radio 76 km
- `got-295992` GOT5.6 18.162S 177.504E (FJ-SOU) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-1c9970` 62 km, cruza 59 km de tierra; `ticon-233ae7` 98 km, cruza 84 km de tierra

### PF-TAH — Tahití y Moorea (8 picos)

- `noaa-1732417` Papeete Harbor, Fare Ute Point — oficial, misma costa: 8 picos a 10–49 km, radio 60 km (niveles 1,3)
- Descartadas: `ticon-0d0b90` 10 km, fuera por el tope de 3 puertos (nivel 4); `ticon-f3d3c0` 11 km, fuera por el tope de 3 puertos (nivel 4)

### PF-ISL — Islas de Sotavento (2 picos)

- `ticon-c5c611` TICON-3 16.722S 151.032W (gesla.meds) — TICON-3, misma costa: 2 picos a 3.1–41 km, radio 51 km

### WS-ALL — Samoa (6 picos)

- `ticon-3eec34` TICON-3 14.283S 170.683W (gesla.uhslc) — TICON-3, misma costa: 4 picos a 92–119 km, radio 130 km
- `noaa-1778000` APIA (Observatory), Upolu Island, AS — oficial, cruzando tierra: 2 picos a 23–23 km, radio 34 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BOULDERS → noaa-1778000, DEVIL'S ISLAND → noaa-1778000, TAFATAFA → noaa-1778000
- Descartadas: `ticon-7abf3a` 22 km, fuera por el tope de 3 puertos (nivel 4); `ticon-cbe192` 23 km, fuera por el tope de 3 puertos (nivel 4)

### TO-ALL — Tonga (6 picos)

- `ticon-5699c9` TICON-3 21.140S 175.180W (gesla.jodc_jcg) — TICON-3, misma costa: 6 picos a 13–17 km, radio 28 km (niveles 2,4)

### VU-ALL — Vanuatu (5 picos)

- `ticon-fc3571` TICON-3 17.762S 168.293E (gesla.cmems) — TICON-3, misma costa: 3 picos a 2.8–12 km, radio 23 km
- `got-1e8580` GOT5.6 19.532S 169.268E (VU-ALL) — modelo global GOT5.6: 2 picos a 0.0–25 km, radio 35 km
- Descartadas: `ticon-1af54e` 6.9 km, fuera por el tope de 3 puertos (nivel 2)

### PG-ALL — Papúa Nueva Guinea (2 picos)

- `ticon-27bb40` TICON-3 9.478S 147.140E (gesla.uhslc) — TICON-3, cruzando tierra: 1 picos a 10–10 km, radio 20 km
- `got-c1e848` GOT5.6 2.674S 141.299E (PG-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ID-BAL-BUK — Bukit (Bali) (16 picos)

- `ticon-0ccd99` TICON-3 8.747S 115.212E (gesla.usgs) — TICON-3, misma costa: 16 picos a 6.5–16 km, radio 27 km (niveles 2,4)
- Descartadas: `ticon-8bef32` 110 km, cruza 39 km de tierra

### ID-BAL-W — Kuta y Canggu (Bali) (18 picos)

- `ticon-0ccd99` TICON-3 8.747S 115.212E (gesla.usgs) — TICON-3, misma costa: 18 picos a 5.1–58 km, radio 68 km (niveles 2,4)
- Descartadas: `ticon-8bef32` 57 km, cruza 69 km de tierra

### ID-BAL-E — Keramas y Nusas (Bali) (12 picos)

- `ticon-0ccd99` TICON-3 8.747S 115.212E (gesla.usgs) — TICON-3, misma costa: 12 picos a 3.8–26 km, radio 37 km (niveles 2,4)
- Descartadas: `ticon-8bef32` 114 km, cruza 106 km de tierra

### ID-JAV-E — Java oriental (7 picos)

- `got-125cb8` GOT5.6 8.724S 114.350E (ID-JAV-E) — modelo global GOT5.6: 6 picos a 0.0–39 km, radio 49 km
- `got-d5b42a` GOT5.6 8.218S 111.095E (ID-JAV-E) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-8bef32` 66 km, cruza 28 km de tierra; `ticon-6b6562` 70 km, cruza 68 km de tierra; `ticon-0ccd99` 92 km, cruza 24 km de tierra

### ID-JAV-W — Java occidental (7 picos)

- `ticon-e6afd5` TICON-3 7.752S 109.017E (gesla.noaa) — TICON-3, cruzando tierra: 3 picos a 42–58 km, radio 69 km
- `got-2f1c38` GOT5.6 7.063S 106.508E (ID-JAV-W) — modelo global GOT5.6: 4 picos a 0.0–34 km, radio 44 km

### ID-LOM — Lombok (14 picos)

- `ticon-0ccd99` TICON-3 8.747S 115.212E (gesla.usgs) — TICON-3, misma costa: 5 picos a 83–115 km, radio 125 km
- `got-b32477` GOT5.6 8.915S 116.355E (ID-LOM) — modelo global GOT5.6: 8 picos a 0.0–9.4 km, radio 20 km
- `got-2e40a2` GOT5.6 8.735S 115.836E (ID-LOM) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): MAWI → got-b32477, MAWUN → got-b32477
- Descartadas: `ticon-0ccd99` 69 km, cruza 20 km de tierra

### ID-SBW — Sumbawa (9 picos)

- `got-82a78a` GOT5.6 8.816S 118.376E (ID-SBW) — modelo global GOT5.6: 5 picos a 0.0–2.2 km, radio 13 km
- `got-684e80` GOT5.6 8.973S 116.729E (ID-SBW) — modelo global GOT5.6: 4 picos a 0.0–4.9 km, radio 15 km

### ID-SMB — Sumba (2 picos)

- `got-28a8b3` GOT5.6 9.738S 119.314E (ID-SMB) — modelo global GOT5.6: 2 picos a 0.0–34 km, radio 45 km

### ID-ROT — Rote (4 picos)

- `got-799775` GOT5.6 10.893S 122.812E (ID-ROT) — modelo global GOT5.6: 4 picos a 0.0–6.0 km, radio 17 km

### ID-MEN — Mentawai (10 picos)

- `got-56d0a4` GOT5.6 2.410S 99.855E (ID-MEN) — modelo global GOT5.6: 5 picos a 0.0–44 km, radio 55 km
- `got-c774f7` GOT5.6 1.900S 99.300E (ID-MEN) — modelo global GOT5.6: 5 picos a 0.0–1.6 km, radio 12 km

### ID-NIA — Nias y Banyak (3 picos)

- `got-d76764` GOT5.6 0.912N 97.263E (ID-NIA) — modelo global GOT5.6: 2 picos a 0.0–14 km, radio 25 km
- `got-39b84c` GOT5.6 0.569N 97.734E (ID-NIA) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ID-KRU — Krui y Lampung (4 picos)

- `got-d30559` GOT5.6 5.305S 103.992E (ID-KRU) — modelo global GOT5.6: 4 picos a 0.0–15 km, radio 25 km

### PH-SIA — Siargao (8 picos)

- `got-1682f6` GOT5.6 9.818N 126.170E (PH-SIA) — modelo global GOT5.6: 8 picos a 0.0–16 km, radio 27 km

### PH-LUZ — La Union y Baler (5 picos)

- `got-f8b86d` GOT5.6 16.669N 120.320E (PH-LUZ) — modelo global GOT5.6: 3 picos a 0.0–0.8 km, radio 11 km
- `got-529ee2` GOT5.6 15.765N 121.574E (PH-LUZ) — modelo global GOT5.6: 2 picos a 0.0–0.5 km, radio 11 km

### PH-EAS — Samar y Catanduanes (2 picos)

- `got-72b502` GOT5.6 13.659N 124.398E (PH-EAS) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-9b0ee7` GOT5.6 11.605N 125.440E (PH-EAS) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### LK-E — Arugam Bay (8 picos)

- `got-94cadf` GOT5.6 6.800N 81.820E (LK-E) — modelo global GOT5.6: 8 picos a 0.0–15 km, radio 25 km

### LK-S — Sur y oeste de Sri Lanka (11 picos)

- `got-964843` GOT5.6 5.998N 80.269E (LK-S) — modelo global GOT5.6: 10 picos a 0.0–24 km, radio 35 km
- `got-d6cb2e` GOT5.6 5.968N 80.685E (LK-S) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-ef0f0a` 93 km, cruza 39 km de tierra; `ticon-afdd8d` 94 km, cruza 49 km de tierra

### MV-NMA — Malé Norte (6 picos)

- `ticon-2aab05` TICON-3 4.190N 73.527E (gesla.uhslc) — TICON-3, misma costa: 6 picos a 14–26 km, radio 36 km
- Descartadas: `ticon-c17f38` 16 km, fuera por el tope de 3 puertos (nivel 2)

### MV-SMA — Malé Sur (3 picos)

- `ticon-c17f38` TICON-3 4.183N 73.517E (gesla.uhslc) — TICON-3, misma costa: 3 picos a 32–34 km, radio 45 km
- Descartadas: `ticon-2aab05` 33 km, fuera por el tope de 3 puertos (nivel 2)

### MV-SOU — Atolones del sur (2 picos)

- `ticon-62701e` TICON-3 0.687S 73.152E (gesla.noaa) — TICON-3, misma costa: 2 picos a 100–113 km, radio 123 km

### MV-CEN — Atolones centrales (1 picos)

- `got-4e1d64` GOT5.6 2.919N 73.570E (MV-CEN) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### JP-CHI — Chiba (8 picos)

- `ticon-56fc43` TICON-3 35.745N 140.858E (gesla.bom) — TICON-3, misma costa: 5 picos a 59–77 km, radio 88 km
- `jma-zf` 勝浦 (JMA ZF) — oficial, cruzando tierra: 3 picos a 13–51 km, radio 62 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): TSURIGASAKI → jma-zf, SHIDASHITA → jma-zf, ICHINOMIYA → jma-zf, OHARA → jma-zf, ONJUKU → jma-zf, HASUNUMA → ticon-56fc43, KATAKAI → ticon-56fc43
- Descartadas: `ticon-a9d86d` 12 km, fuera por el tope de 3 puertos (nivel 4); `jma-tt` 27 km, fuera por el tope de 3 puertos (nivel 3); `jma-cb` 32 km, fuera por el tope de 3 puertos (nivel 3); `jma-mr` 33 km, fuera por el tope de 3 puertos (nivel 3)

### JP-SHO — Shonan (9 picos)

- `jma-d8` 湘南港 (JMA D8) — oficial, misma costa: 9 picos a 1.6–15 km, radio 25 km
- Descartadas: `jma-qn` 5.9 km, fuera por el tope de 3 puertos (nivel 3); `ticon-fe558c` 6.0 km, fuera por el tope de 3 puertos (nivel 4); `jma-z1` 11 km, fuera por el tope de 3 puertos (nivel 1); `ticon-7ff645` 12 km, fuera por el tope de 3 puertos (nivel 2)

### JP-IZU — Izu (4 picos)

- `jma-d6` 下田 (JMA D6) — oficial, misma costa: 3 picos a 1.1–6.0 km, radio 17 km
- `jma-ok` 岡田 (JMA OK) — oficial, misma costa: 1 picos a 37–37 km, radio 48 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): KAWAZU → jma-d6
- Descartadas: `ticon-571a75` 1.0 km, fuera por el tope de 3 puertos (nivel 2); `jma-qk` 5.5 km, fuera por el tope de 3 puertos (nivel 3); `jma-g9` 8.7 km, fuera por el tope de 3 puertos (nivel 3); `ticon-1044bb` 8.9 km, fuera por el tope de 3 puertos (nivel 4)

### JP-IBA — Ibaraki y Fukushima (5 picos)

- `jma-on` 小名浜 (JMA ON) — oficial, misma costa: 2 picos a 10–15 km, radio 25 km
- `jma-d2` 鹿島 (JMA D2) — oficial, misma costa: 2 picos a 4.5–43 km, radio 54 km
- `jma-cs` 銚子漁港 (JMA CS) — oficial, misma costa: 1 picos a 2.9–2.9 km, radio 13 km
- Descartadas: `ticon-56fc43` 2.0 km, fuera por el tope de 3 puertos (nivel 2); `jma-d3` 2.5 km, fuera por el tope de 3 puertos (nivel 3); `ticon-f4c33d` 4.5 km, fuera por el tope de 3 puertos (nivel 4); `ticon-f2a2df` 9.3 km, fuera por el tope de 3 puertos (nivel 2)

### JP-SHK — Shikoku (3 picos)

- `jma-hw` 日和佐 (JMA HW) — oficial, misma costa: 3 picos a 2.2–27 km, radio 37 km
- Descartadas: `jma-l7` 3.2 km, fuera por el tope de 3 puertos (nivel 1); `ticon-5879db` 7.5 km, fuera por el tope de 3 puertos (nivel 4); `jma-aw` 7.8 km, fuera por el tope de 3 puertos (nivel 3); `jma-j6` 18 km, fuera por el tope de 3 puertos (nivel 3)

### JP-KYU — Miyazaki y Kyushu (2 picos)

- `jma-mg` 宮崎 (JMA MG) — oficial, misma costa: 2 picos a 9.1–11 km, radio 22 km
- Descartadas: `jma-ab` 25 km, fuera por el tope de 3 puertos (nivel 3); `ticon-6cd1ae` 25 km, fuera por el tope de 3 puertos (nivel 4); `ticon-33dab1` 26 km, fuera por el tope de 3 puertos (nivel 4); `jma-x6` 49 km, fuera por el tope de 3 puertos (nivel 3)

### TW-E — Taitung y Hualien (4 picos)

- `got-a1d318` GOT5.6 22.900N 121.233E (TW-E) — modelo global GOT5.6: 3 picos a 0.0–11 km, radio 21 km
- `got-a95390` GOT5.6 24.027N 121.627E (TW-E) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Descartadas: `ticon-f34273` 96 km, cruza 93 km de tierra

### TW-NE — Yilan y costa norte (6 picos)

- `ticon-5969a5` TICON-3 25.155N 121.752E (gesla.noaa) — TICON-3, misma costa: 4 picos a 7.1–35 km, radio 45 km (niveles 2,4)
- `ticon-b3b22e` TICON-3 24.452N 122.942E (gesla.meds) — TICON-3, misma costa: 2 picos a 116–119 km, radio 130 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): FULONG → ticon-5969a5, HONEYMOON BAY → ticon-5969a5

### IN-W — India oeste (3 picos)

- `got-af9925` GOT5.6 8.731N 76.703E (IN-W) — modelo global GOT5.6: 2 picos a 0.0–49 km, radio 59 km
- `got-528c98` GOT5.6 13.077N 74.787E (IN-W) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### IN-E — India este (3 picos)

- `got-b495c3` GOT5.6 12.787N 80.255E (IN-E) — modelo global GOT5.6: 2 picos a 0.0–20 km, radio 31 km
- `got-e5aa1d` GOT5.6 11.978N 79.833E (IN-E) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### VN-ALL — Vietnam (4 picos)

- `ticon-458133` TICON-3 10.340N 107.072E (gesla.meds) — TICON-3, misma costa: 2 picos a 3.6–20 km, radio 30 km
- `got-c38d4b` GOT5.6 16.062N 108.249E (VN-ALL) — modelo global GOT5.6: 2 picos a 0.0–7.1 km, radio 18 km

### KR-ALL — Corea del Sur (6 picos)

- `ticon-041ef0` TICON-3 34.655N 129.478E (gesla.noaa) — TICON-3, misma costa: 2 picos a 63–64 km, radio 74 km
- `got-a989b9` GOT5.6 37.969N 128.760E (KR-ALL) — modelo global GOT5.6: 2 picos a 0.0–7.1 km, radio 18 km
- `got-0e82ac` GOT5.6 33.245N 126.412E (KR-ALL) — modelo global GOT5.6: 2 picos a 0.0–41 km, radio 51 km
- Descartadas: `ticon-bc0ee6` 101 km, cruza 19 km de tierra; `ticon-bd10b8` 108 km, fuera por el tope de 3 puertos (nivel 2)

### CN-HAI — Hainan (2 picos)

- `got-0548a0` GOT5.6 18.630N 110.222E (CN-HAI) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-2ee07d` GOT5.6 18.271N 109.723E (CN-HAI) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ZA-WC-CPT — Península del Cabo (20 picos)

- `ticon-fb0d01` TICON-3 33.900S 18.433E (gesla.meds) — TICON-3, misma costa: 20 picos a 7.1–57 km, radio 67 km (niveles 2,4)

### ZA-WC-WCO — Costa Oeste del Cabo (6 picos)

- `ticon-fb0d01` TICON-3 33.900S 18.433E (gesla.meds) — TICON-3, misma costa: 3 picos a 19–116 km, radio 126 km
- `got-b68b0a` GOT5.6 32.312S 18.324E (ZA-WC-WCO) — modelo global GOT5.6: 2 picos a 0.0–25 km, radio 35 km
- `got-8af89e` GOT5.6 32.811S 17.885E (ZA-WC-WCO) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ZA-WC-GR — Garden Route (11 picos)

- `got-f03581` GOT5.6 34.046S 22.418E (ZA-WC-GR) — modelo global GOT5.6: 7 picos a 0.0–37 km, radio 48 km
- `got-38e06a` GOT5.6 34.078S 22.954E (ZA-WC-GR) — modelo global GOT5.6: 3 picos a 0.0–14 km, radio 25 km
- `got-ec35aa` GOT5.6 33.984S 23.562E (ZA-WC-GR) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ZA-EC-JB — Jeffreys Bay y St Francis (10 picos)

- `got-4b911c` GOT5.6 34.055S 24.925E (ZA-EC-JB) — modelo global GOT5.6: 10 picos a 0.0–19 km, radio 29 km
- Descartadas: `ticon-86ec39` 64 km, cruza 30 km de tierra

### ZA-EC-PE — Gqeberha y East London (17 picos)

- `ticon-86ec39` TICON-3 33.960S 25.630E (gesla.usgs) — TICON-3, misma costa: 6 picos a 0.9–87 km, radio 98 km (niveles 2,4)
- `got-63d295` GOT5.6 33.023S 27.919E (ZA-EC-PE) — modelo global GOT5.6: 7 picos a 0.0–24 km, radio 34 km
- `got-07bdb8` GOT5.6 33.605S 26.922E (ZA-EC-PE) — modelo global GOT5.6: 2 picos a 0.0–25 km, radio 36 km
- Sin puerto (Open-Meteo): CINTSA, HAGA HAGA
- Descartadas: `ticon-86ec39` 101 km, cruza 27 km de tierra

### ZA-EC-WLD — Wild Coast (5 picos)

- `got-e4029c` GOT5.6 31.980S 29.153E (ZA-EC-WLD) — modelo global GOT5.6: 2 picos a 0.0–15 km, radio 25 km
- `got-041b3c` GOT5.6 32.682S 28.383E (ZA-EC-WLD) — modelo global GOT5.6: 2 picos a 0.0–5.8 km, radio 16 km
- `got-913e13` GOT5.6 31.643S 29.550E (ZA-EC-WLD) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ZA-KZN-DBN — Durban (8 picos)

- `got-e07ca7` GOT5.6 29.855S 31.049E (ZA-KZN-DBN) — modelo global GOT5.6: 8 picos a 0.0–24 km, radio 34 km

### ZA-KZN-N — KwaZulu-Natal norte (6 picos)

- `got-57076f` GOT5.6 29.493S 31.275E (ZA-KZN-N) — modelo global GOT5.6: 4 picos a 0.0–16 km, radio 26 km
- `got-16f772` GOT5.6 28.957S 31.780E (ZA-KZN-N) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- `got-a0b028` GOT5.6 28.125S 32.558E (ZA-KZN-N) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### ZA-KZN-S — KwaZulu-Natal sur (9 picos)

- `got-c939f5` GOT5.6 30.891S 30.354E (ZA-KZN-S) — modelo global GOT5.6: 5 picos a 0.0–10 km, radio 20 km
- `got-b0dc74` GOT5.6 30.200S 30.807E (ZA-KZN-S) — modelo global GOT5.6: 4 picos a 0.0–18 km, radio 29 km

### NA-ERO — Walvis Bay y Swakopmund (3 picos)

- `got-f341c0` GOT5.6 22.938S 14.418E (NA-ERO) — modelo global GOT5.6: 2 picos a 0.0–30 km, radio 41 km
- `got-439ad8` GOT5.6 22.115S 14.268E (NA-ERO) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### MA-TAG — Taghazout y Agadir (19 picos)

- `got-1a2bc4` GOT5.6 30.640N 9.830W (MA-TAG) — modelo global GOT5.6: 17 picos a 0.0–31 km, radio 41 km
- `got-bbafe3` GOT5.6 31.359N 9.809W (MA-TAG) — modelo global GOT5.6: 2 picos a 0.0–17 km, radio 27 km

### MA-N — Rabat a Safi (6 picos)

- `got-3cd5c4` GOT5.6 34.257N 6.689W (MA-N) — modelo global GOT5.6: 2 picos a 0.0–28 km, radio 39 km
- `got-1c5103` GOT5.6 33.597N 7.679W (MA-N) — modelo global GOT5.6: 2 picos a 0.0–14 km, radio 24 km
- `got-ca232b` GOT5.6 33.790N 7.175W (MA-N) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Sin puerto (Open-Meteo): SAFI LE JARDIN

### MA-S — Mirleft y Sidi Ifni (6 picos)

- `got-cb786a` GOT5.6 29.430N 10.130W (MA-S) — modelo global GOT5.6: 4 picos a 0.0–18 km, radio 29 km
- `got-360725` GOT5.6 30.198N 9.639W (MA-S) — modelo global GOT5.6: 2 picos a 0.0–47 km, radio 58 km

### SN-ALL — Senegal (5 picos)

- `got-48d2ad` GOT5.6 14.752N 17.509W (SN-ALL) — modelo global GOT5.6: 5 picos a 0.0–2.6 km, radio 13 km

### LR-ALL — Liberia (3 picos)

- `got-3ba912` GOT5.6 6.753N 11.379W (LR-ALL) — modelo global GOT5.6: 3 picos a 0.0–1.7 km, radio 12 km

### GH-ALL — Ghana (3 picos)

- `ticon-930b55` TICON-3 4.883N 1.750W (gesla.wsv) — TICON-3, misma costa: 2 picos a 23–25 km, radio 35 km
- `got-ef40bc` GOT5.6 5.490N 0.405W (GH-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### MZ-S — Ponta do Ouro (3 picos)

- `got-0f94d8` GOT5.6 26.846S 32.895E (MZ-S) — modelo global GOT5.6: 3 picos a 0.0–15 km, radio 26 km

### MZ-INH — Inhambane y Tofo (3 picos)

- `got-e51b06` GOT5.6 23.858S 35.549E (MZ-INH) — modelo global GOT5.6: 3 picos a 0.0–7.9 km, radio 18 km

### MG-ALL — Madagascar (3 picos)

- `got-56aa18` GOT5.6 25.030S 46.999E (MG-ALL) — modelo global GOT5.6: 2 picos a 0.0–2.3 km, radio 13 km
- `got-ab6d4c` GOT5.6 23.650S 43.635E (MG-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

### RE-ALL — Reunión (8 picos)

- `ticon-2ebaf5` TICON-3 20.935S 55.285E (gesla.noaa) — TICON-3, misma costa: 8 picos a 13–60 km, radio 70 km (niveles 2,4)
- Descartadas: `ticon-e3ec7b` 9.3 km, fuera por el tope de 3 puertos (nivel 4); `ticon-e021f9` 15 km, fuera por el tope de 3 puertos (nivel 2)

### MU-ALL — Mauricio (3 picos)

- `ticon-0a453c` TICON-3 20.153S 57.490E (gesla.noaa) — TICON-3, cruzando tierra: 3 picos a 24–41 km, radio 52 km

### CV-ALL — Cabo Verde (3 picos)

- `ticon-18a200` TICON-3 16.755N 22.983W (gesla.refmar) — TICON-3, misma costa: 3 picos a 19–72 km, radio 82 km (niveles 2,4)

### FR-PBA — País Vasco francés (24 picos)

- `ticon-ae0728` TICON-3 43.398N 1.673W (gesla.nwfwmd) — TICON-3, misma costa: 13 picos a 0.9–12 km, radio 22 km
- `ticon-920ef6` TICON-3 43.527N 1.515W (gesla.meds) — TICON-3, misma costa: 11 picos a 1.4–7.1 km, radio 18 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): ILBARRITZ → ticon-920ef6, MILADY → ticon-920ef6
- Descartadas: `ticon-66c157` 79 km, fuera por el tope de 3 puertos (nivel 2); `ticon-513a8d` 103 km, cruza 42 km de tierra

### FR-HOS — Hossegor y Capbreton (16 picos)

- `ticon-ae0728` TICON-3 43.398N 1.673W (gesla.nwfwmd) — TICON-3, misma costa: 8 picos a 33–37 km, radio 48 km
- `ticon-920ef6` TICON-3 43.527N 1.515W (gesla.meds) — TICON-3, misma costa: 8 picos a 6.2–25 km, radio 35 km (niveles 2,4)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): L'ESTACADE → ticon-920ef6, SANTOCHA → ticon-920ef6, LE PREVENT → ticon-920ef6, LA PISTE → ticon-920ef6, LA SUD → ticon-920ef6, LA CENTRALE → ticon-920ef6, LA GRAVIERE → ticon-920ef6, LES ESTAGNOTS → ticon-920ef6
- Descartadas: `ticon-66c157` 53 km, cruza 13 km de tierra; `ticon-b486e0` 105 km, cruza 43 km de tierra

### FR-GIR — Gironda y Landas norte (18 picos)

- `ticon-66c157` TICON-3 44.211N 1.295W (gesla.noaa) — TICON-3, misma costa: 10 picos a 0.4–59 km, radio 69 km (niveles 2,4)
- `ticon-a3cf33` TICON-3 45.568N 1.062W (gesla.bom) — TICON-3, misma costa: 4 picos a 12–52 km, radio 62 km (niveles 2,4)
- `ticon-ad634c` TICON-3 45.853N 1.178W (gesla.meds) — TICON-3, misma costa: 4 picos a 94–107 km, radio 118 km
- Descartadas: `ticon-b486e0` 8.6 km, cruza 49 km de tierra; `ticon-bebc3a` 18 km, fuera por el tope de 3 puertos (nivel 2); `ticon-a3f536` 20 km, fuera por el tope de 3 puertos (nivel 4); `ticon-a21394` 29 km, fuera por el tope de 3 puertos (nivel 4)

### FR-VEN — Vendée y Charentes (12 picos)

- `ticon-e56f80` TICON-3 46.007N 1.174W (gesla.noaa) — TICON-3, misma costa: 5 picos a 18–69 km, radio 79 km (niveles 2,4)
- `ticon-a75e0c` TICON-3 47.025N 2.298W (gesla.usgs) — TICON-3, cruzando tierra: 5 picos a 24–57 km, radio 67 km
- `ticon-a3cf33` TICON-3 45.568N 1.062W (gesla.bom) — TICON-3, misma costa: 2 picos a 6.6–15 km, radio 26 km
- Descartadas: `ticon-bebc3a` 1.9 km, cruza 18 km de tierra; `ticon-ad634c` 6.0 km, cruza 17 km de tierra; `ticon-d941c1` 9.2 km, cruza 58 km de tierra; `ticon-a3f536` 22 km, cruza 19 km de tierra

### FR-BRE — Bretaña (15 picos)

- `ticon-e4bed3` TICON-3 48.022N 4.538W (gesla.noaa) — TICON-3, misma costa: 8 picos a 18–43 km, radio 54 km (niveles 2,4)
- `ticon-f72d96` TICON-3 47.644N 3.446W (gesla.jodc_jma) — TICON-3, misma costa: 5 picos a 8.5–25 km, radio 36 km
- `ticon-16f890` TICON-3 48.641N 2.028W (gesla.bodc) — TICON-3, misma costa: 1 picos a 1.5–1.5 km, radio 12 km
- Sin puerto (Open-Meteo): DOSSEN (ticon-150382 a 4.8 km: fuera por el tope de 3 puertos)
- Descartadas: `ticon-6ca24b` 1.8 km, cruza 62 km de tierra; `ticon-150382` 4.8 km, fuera por el tope de 3 puertos (nivel 2); `ticon-5c788a` 20 km, fuera por el tope de 3 puertos (nivel 4); `ticon-c355cf` 30 km, cruza 25 km de tierra

### ES-PV — País Vasco (26 picos)

- `ticon-ae0728` TICON-3 43.398N 1.673W (gesla.nwfwmd) — TICON-3, misma costa: 12 picos a 9.4–100 km, radio 110 km
- `ticon-513a8d` TICON-3 43.357N 3.050W (gesla.meds) — TICON-3, misma costa: 8 picos a 3.2–9.0 km, radio 19 km (niveles 2,4)
- `ticon-920ef6` TICON-3 43.527N 1.515W (gesla.meds) — TICON-3, misma costa: 6 picos a 44–116 km, radio 127 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): ARMINTZA → ticon-513a8d, ZURRIOLA → ticon-ae0728, ORIO → ticon-ae0728, ZARAUTZ → ticon-ae0728, GAZTETAPE → ticon-ae0728, GORLIZ → ticon-ae0728, GORLIZ → ticon-513a8d, PLENTZIA → ticon-ae0728, PLENTZIA → ticon-513a8d
- Descartadas: `ticon-513a8d` 64 km, cruza 51 km de tierra; `ticon-66c157` 101 km, fuera por el tope de 3 puertos (nivel 2); `ticon-ae0728` 102 km, cruza 18 km de tierra; `ticon-920ef6` 117 km, cruza 18 km de tierra

### ES-CAN — Cantabria (14 picos)

- `ticon-513a8d` TICON-3 43.357N 3.050W (gesla.meds) — TICON-3, misma costa: 7 picos a 35–56 km, radio 67 km (niveles 2,4)
- `got-441786` GOT5.6 43.443N 4.048W (ES-CAN) — modelo global GOT5.6: 7 picos a 0.0–27 km, radio 37 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): SOMO → got-441786, LOREDO → got-441786, GALIZANO → got-441786, LANGRE → got-441786
- Descartadas: `ticon-513a8d` 73 km, cruza 25 km de tierra; `ticon-bdc867` 109 km, cruza 34 km de tierra

### ES-AST — Asturias (14 picos)

- `ticon-bdc867` TICON-3 43.558N 5.698W (gesla.uhslc) — TICON-3, misma costa: 11 picos a 3.5–60 km, radio 70 km (niveles 2,4)
- `got-0bc1cc` GOT5.6 43.564N 6.703W (ES-AST) — modelo global GOT5.6: 2 picos a 0.0–21 km, radio 31 km
- `got-70a590` GOT5.6 43.427N 4.893W (ES-AST) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): OTUR → got-0bc1cc
- Descartadas: `ticon-bdc867` 67 km, cruza 35 km de tierra; `ticon-283bad` 111 km, cruza 93 km de tierra; `ticon-2a8e09` 118 km, cruza 97 km de tierra; `ticon-67d63b` 118 km, cruza 96 km de tierra

### ES-GAL — Galicia (18 picos)

- `ticon-67d63b` TICON-3 43.367N 8.400W (gesla.usgs) — TICON-3, misma costa: 6 picos a 0.5–51 km, radio 61 km (niveles 2,4)
- `ticon-91c7f2` TICON-3 42.238N 8.730W (gesla.noaa) — TICON-3, misma costa: 6 picos a 14–102 km, radio 112 km (niveles 2,4)
- `ticon-283bad` TICON-3 43.463N 8.326W (gesla.meds) — TICON-3, misma costa: 6 picos a 5.0–35 km, radio 46 km (niveles 2,4)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): BARRAÑAN → ticon-67d63b, BALDAIO → ticon-67d63b, RAZO → ticon-67d63b
- Descartadas: `ticon-2a8e09` 2.0 km, fuera por el tope de 3 puertos (nivel 4); `ticon-26e050` 18 km, cruza 39 km de tierra; `ticon-283bad` 61 km, cruza 15 km de tierra; `ticon-67d63b` 78 km, cruza 55 km de tierra

### ES-AND — Cádiz (15 picos)

- `ticon-936e57` TICON-3 37.132N 6.834W (gesla.uhslc) — TICON-3, misma costa: 7 picos a 57–120 km, radio 130 km
- `ticon-8ecb10` TICON-3 36.009N 5.603W (gesla.noaa) — TICON-3, misma costa: 5 picos a 2.0–43 km, radio 54 km (niveles 2,4)
- `ticon-22ec01` TICON-3 36.540N 6.283W (gesla.cmems) — TICON-3, misma costa: 3 picos a 3.1–34 km, radio 44 km (niveles 2,4)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): REGLA → ticon-22ec01, LA COSTILLA → ticon-22ec01, CAMPOSOTO → ticon-22ec01, LA BARROSA → ticon-22ec01, ROCHE → ticon-22ec01, LA FONTANILLA → ticon-8ecb10, LA FONTANILLA → ticon-22ec01, EL PALMAR → ticon-8ecb10, EL PALMAR → ticon-22ec01
- Descartadas: `ticon-df46ba` 6.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-7b6f41` 20 km, cruza 60 km de tierra; `ticon-83c0c8` 27 km, cruza 59 km de tierra; `ticon-90a49b` 30 km, cruza 17 km de tierra

### ES-CN-E — Lanzarote y Fuerteventura (11 picos)

- `ticon-5336d6` TICON-3 28.950N 13.567W (gesla.uhslc) — TICON-3, misma costa: 7 picos a 19–40 km, radio 51 km (niveles 2,4)
- `ticon-9cf100` TICON-3 28.500N 13.850W (gesla.noaa) — TICON-3, cruzando tierra: 3 picos a 24–27 km, radio 37 km
- `ticon-ae29cb` TICON-3 28.100N 15.400W (gesla.jodc_jcg) — TICON-3, misma costa: 1 picos a 117–117 km, radio 127 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): LOBOS → ticon-9cf100, FLAG BEACH → ticon-9cf100, MAJANICHO → ticon-9cf100
- Descartadas: `ticon-fc260c` 16 km, fuera por el tope de 3 puertos (nivel 4); `ticon-9cf100` 70 km, cruza 23 km de tierra; `ticon-5336d6` 103 km, cruza 61 km de tierra; `ticon-c238b7` 117 km, fuera por el tope de 3 puertos (nivel 2)

### ES-CN-W — Gran Canaria y Tenerife (17 picos)

- `ticon-c238b7` TICON-3 28.147N 15.408W (gesla.cmems) — TICON-3, misma costa: 11 picos a 3.4–101 km, radio 112 km
- `ticon-c9798b` TICON-3 28.047N 16.718W (gesla.ispra) — TICON-3, misma costa: 4 picos a 2.1–18 km, radio 28 km (niveles 2,4)
- `ticon-48327e` TICON-3 28.480N 16.240W (gesla.cmems) — TICON-3, misma costa: 2 picos a 63–64 km, radio 75 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): EL SOCORRO → ticon-48327e, ALMACIGA → ticon-48327e, BENIJO → ticon-48327e, BAJAMAR → ticon-48327e, PUNTA DEL HIDALGO → ticon-48327e, EL FRONTON → ticon-c238b7, SARDINA → ticon-c238b7
- Descartadas: `ticon-ae29cb` 5.1 km, fuera por el tope de 3 puertos (nivel 2); `ticon-2594ab` 26 km, fuera por el tope de 3 puertos (nivel 2); `ticon-48327e` 67 km, cruza 64 km de tierra; `ticon-c9798b` 68 km, cruza 65 km de tierra

### PT-NOR — Porto y norte (19 picos)

- `ticon-a6ef88` TICON-3 41.187N 8.704W (gesla.fmi) — TICON-3, misma costa: 17 picos a 0.6–66 km, radio 76 km (niveles 2,4)
- `ticon-91c7f2` TICON-3 42.238N 8.730W (gesla.noaa) — TICON-3, cruzando tierra: 2 picos a 46–49 km, radio 60 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): AFIFE → ticon-91c7f2
- Descartadas: `ticon-91c7f2` 60 km, cruza 58 km de tierra; `ticon-a6ef88` 70 km, cruza 17 km de tierra; `ticon-26e050` 85 km, cruza 28 km de tierra

### PT-CEN — Figueira da Foz y Nazaré (20 picos)

- `ticon-a6ef88` TICON-3 41.187N 8.704W (gesla.fmi) — TICON-3, misma costa: 10 picos a 25–109 km, radio 120 km
- `ticon-5b4329` TICON-3 39.586N 9.074W (gesla.uhslc) — TICON-3, misma costa: 9 picos a 1.7–59 km, radio 69 km (niveles 2,4)
- `got-a65a9d` GOT5.6 40.133N 8.874W (PT-CEN) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): QUIAIOS → got-a65a9d, COSTA DE LAVOS → got-a65a9d, LEIROSA → got-a65a9d
- Descartadas: `ticon-5b4329` 63 km, cruza 29 km de tierra; `ticon-5da85d` 97 km, cruza 92 km de tierra; `ticon-a6ef88` 118 km, cruza 19 km de tierra

### PT-PEN — Peniche (12 picos)

- `ticon-5b4329` TICON-3 39.586N 9.074W (gesla.uhslc) — TICON-3, misma costa: 12 picos a 21–58 km, radio 68 km (niveles 2,4)
- Descartadas: `ticon-5da85d` 48 km, cruza 57 km de tierra

### PT-ERI — Ericeira (11 picos)

- `ticon-5da85d` TICON-3 38.692N 9.417W (gesla.cmems) — TICON-3, cruzando tierra: 11 picos a 24–36 km, radio 46 km
- Descartadas: `ticon-5b4329` 70 km, cruza 67 km de tierra

### PT-LIS — Lisboa y Caparica (15 picos)

- `ticon-5da85d` TICON-3 38.692N 9.417W (gesla.cmems) — TICON-3, misma costa: 15 picos a 4.8–30 km, radio 40 km (niveles 2,4)
- Descartadas: `ticon-5b4329` 90 km, cruza 75 km de tierra

### PT-ALG — Alentejo y Algarve (18 picos)

- `ticon-4a3da2` TICON-3 37.098N 8.668W (gesla.meds) — TICON-3, misma costa: 14 picos a 19–56 km, radio 67 km (niveles 2,4)
- `ticon-5da85d` TICON-3 38.692N 9.417W (gesla.cmems) — TICON-3, misma costa: 3 picos a 102–113 km, radio 123 km
- `got-f0b002` GOT5.6 37.653N 8.801W (PT-ALG) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): CARVALHAL → got-f0b002
- Descartadas: `ticon-4a3da2` 63 km, cruza 60 km de tierra

### PT-AZO — Azores (7 picos)

- `ticon-e3d81c` TICON-3 37.735N 25.672W (gesla.noaa) — TICON-3, misma costa: 5 picos a 3.0–21 km, radio 32 km (niveles 2,4)
- `ticon-67b5b2` TICON-3 38.650N 27.240W (gesla.cmems) — TICON-3, cruzando tierra: 1 picos a 19–19 km, radio 30 km
- `ticon-406688` TICON-3 38.533N 28.622W (gesla.noaa) — TICON-3, misma costa: 1 picos a 2.9–2.9 km, radio 13 km

### PT-MAD — Madeira (8 picos)

- `got-043c05` GOT5.6 32.643N 16.955W (PT-MAD) — modelo global GOT5.6: 8 picos a 0.0–28 km, radio 39 km

### GB-CON — Cornualles (28 picos)

- `ticon-4f62f3` TICON-3 50.102N 5.542W (gesla.uhslc) — TICON-3, misma costa: 12 picos a 11–63 km, radio 73 km (niveles 2,4)
- `ticon-f58020` TICON-3 49.918N 6.316W (gesla.cdwr) — TICON-3, misma costa: 11 picos a 47–110 km, radio 120 km
- `ticon-b849f8` TICON-3 50.594N 4.834W (gesla.meds) — TICON-3, misma costa: 5 picos a 5.9–34 km, radio 45 km (niveles 2,4)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): HARLYN BAY → ticon-b849f8, CONSTANTINE BAY → ticon-b849f8, TREYARNON → ticon-b849f8, PORTHCOTHAN → ticon-b849f8, MAWGAN PORTH → ticon-4f62f3, MAWGAN PORTH → ticon-b849f8, WATERGATE BAY → ticon-4f62f3, WATERGATE BAY → ticon-b849f8, TOWAN → ticon-4f62f3, TOWAN → ticon-b849f8, FISTRAL → ticon-4f62f3, FISTRAL → ticon-b849f8, THE CRIBBAR → ticon-4f62f3, THE CRIBBAR → ticon-b849f8, CRANTOCK → ticon-4f62f3, CRANTOCK → ticon-b849f8, HOLYWELL BAY → ticon-4f62f3, HOLYWELL BAY → ticon-b849f8, PERRANPORTH → ticon-4f62f3, PERRANPORTH → ticon-b849f8, CHAPEL PORTH → ticon-4f62f3, CHAPEL PORTH → ticon-b849f8, GWENVER → ticon-4f62f3, SENNEN → ticon-4f62f3
- Descartadas: `ticon-cead8e` 52 km, cruza 25 km de tierra; `ticon-acd761` 53 km, fuera por el tope de 3 puertos (nivel 4); `ticon-b849f8` 62 km, cruza 10 km de tierra; `ticon-f58020` 68 km, cruza 17 km de tierra

### GB-DEV — Devon (9 picos)

- `ticon-7b004f` TICON-3 51.717N 5.050W (gesla.meds) — TICON-3, misma costa: 6 picos a 84–94 km, radio 104 km
- `ticon-acd761` TICON-3 50.368N 4.185W (gesla.noaa) — TICON-3, cruzando tierra: 2 picos a 23–24 km, radio 34 km
- `ticon-388f65` TICON-3 50.608N 2.448W (gesla.noaa) — TICON-3, misma costa: 1 picos a 108–108 km, radio 119 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): THURLESTONE → ticon-acd761
- Descartadas: `ticon-cead8e` 8.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-869669` 41 km, cruza 74 km de tierra; `ticon-3efbc1` 50 km, cruza 71 km de tierra; `ticon-b849f8` 65 km, cruza 34 km de tierra

### GB-SOU — Dorset e Isla de Wight (3 picos)

- `ticon-07792e` TICON-3 50.714N 1.875W (gesla.noaa) — TICON-3, misma costa: 2 picos a 2.4–32 km, radio 43 km
- `ticon-388f65` TICON-3 50.608N 2.448W (gesla.noaa) — TICON-3, misma costa: 1 picos a 23–23 km, radio 33 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): KIMMERIDGE → ticon-07792e
- Descartadas: `ticon-71c0f3` 10 km, fuera por el tope de 3 puertos (nivel 4); `ticon-e1fcad` 13 km, fuera por el tope de 3 puertos (nivel 4); `ticon-b7bb71` 19 km, cruza 17 km de tierra; `ticon-61ca4e` 25 km, cruza 34 km de tierra

### GB-WAL — Gales (21 picos)

- `ticon-cead8e` TICON-3 51.217N 4.117W (gesla.meds) — TICON-3, misma costa: 14 picos a 39–112 km, radio 122 km
- `ticon-a03088` TICON-3 52.017N 4.983W (gesla.usgs) — TICON-3, misma costa: 6 picos a 23–94 km, radio 104 km (niveles 2,4)
- `ticon-e56019` TICON-3 53.392N 6.068W (gesla.cmems) — TICON-3, misma costa: 1 picos a 105–105 km, radio 115 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): WHITESANDS → ticon-a03088, FRESHWATER WEST → ticon-a03088, BROAD HAVEN SOUTH → ticon-a03088, MANORBIER → ticon-a03088
- Descartadas: `ticon-7b004f` 7.5 km, cruza 72 km de tierra; `ticon-70fbc6` 12 km, fuera por el tope de 3 puertos (nivel 4); `ticon-672ff4` 30 km, cruza 16 km de tierra; `ticon-8fb0ea` 33 km, cruza 32 km de tierra

### GB-SCO — Escocia (21 picos)

- `ticon-b027ca` TICON-3 58.441N 3.086W (gesla.meds) — TICON-3, misma costa: 8 picos a 25–105 km, radio 115 km (niveles 2,4)
- `ticon-1fb951` TICON-3 57.144N 2.080W (gesla.noaa) — TICON-3, misma costa: 3 picos a 2.6–33 km, radio 44 km
- `ticon-701a8e` TICON-3 57.895N 5.158W (gesla.meds) — TICON-3, misma costa: 3 picos a 93–111 km, radio 121 km
- Sin puerto (Open-Meteo): BAY OF SKAILL (ticon-947cf4 a 118 km: fuera por el tope de 3 puertos), MACHIR BAY (ticon-9ab05d a 25 km: fuera por el tope de 3 puertos), GOTT BAY (ticon-f7d787 a 47 km: fuera por el tope de 3 puertos), WEST SANDS (ticon-1fb951 a 97 km: cruza 79 km de tierra), BELHAVEN BAY, PEASE BAY, COLDINGHAM
- Descartadas: `ticon-9ab05d` 25 km, fuera por el tope de 3 puertos (nivel 4); `ticon-3e251a` 34 km, fuera por el tope de 3 puertos (nivel 4); `ticon-f7d787` 47 km, cruza 16 km de tierra; `ticon-1fb951` 61 km, cruza 52 km de tierra

### GB-NE — Noreste de Inglaterra (25 picos)

- `ticon-8d43eb` TICON-3 54.490N 0.615W (gesla.uhslc) — TICON-3, misma costa: 25 picos a 0.5–118 km, radio 129 km (niveles 2,4)
- Descartadas: `ticon-f51d1a` 65 km, cruza 55 km de tierra

### GB-NIR — Irlanda del Norte (9 picos)

- `ticon-1bb5de` TICON-3 55.200N 6.667W (gesla.usgs) — TICON-3, misma costa: 6 picos a 0.8–16 km, radio 27 km
- `imi-port-oriel` Port Oriel — oficial, misma costa: 2 picos a 51–59 km, radio 70 km (niveles 1,3)
- `ticon-9ab05d` TICON-3 55.628N 6.190W (gesla.usgs) — TICON-3, misma costa: 1 picos a 47–47 km, radio 58 km
- Descartadas: `ticon-4cfaeb` 0.3 km, fuera por el tope de 3 puertos (nivel 4); `imi-malin-head` 34 km, fuera por el tope de 3 puertos (nivel 3); `ticon-2bf4e1` 34 km, cruza 17 km de tierra; `imi-buncranna` 35 km, fuera por el tope de 3 puertos (nivel 3)

### IE-NW — Donegal Sligo y Mayo (9 picos)

- `imi-killybegs` Killybegs — oficial, misma costa: 4 picos a 15–19 km, radio 30 km
- `imi-sligo` Sligo — oficial, misma costa: 4 picos a 4.4–36 km, radio 46 km (niveles 1,3)
- `imi-achill-island` Achill Island (modelado) — oficial, misma costa: 1 picos a 4.0–4.0 km, radio 15 km
- Descartadas: `ticon-c46c58` 4.4 km, fuera por el tope de 3 puertos (nivel 4); `ticon-a7e19b` 4.5 km, fuera por el tope de 3 puertos (nivel 4); `ticon-8f786f` 15 km, fuera por el tope de 3 puertos (nivel 2); `imi-clare-island` 22 km, fuera por el tope de 3 puertos (nivel 1)

### IE-SW — Clare y Kerry (12 picos)

- `imi-inishmore` Inishmore — oficial, misma costa: 5 picos a 20–34 km, radio 44 km (niveles 1,3)
- `imi-fenit` Fenit — oficial, misma costa: 4 picos a 7.2–30 km, radio 40 km (niveles 1,3)
- `imi-dingle` Dingle — oficial, misma costa: 3 picos a 5.4–24 km, radio 35 km (niveles 1,3)
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): ROSSBEIGH → imi-fenit
- Descartadas: `imi-lahinch` 3.7 km, fuera por el tope de 3 puertos (nivel 3); `ticon-2bef8b` 5.4 km, fuera por el tope de 3 puertos (nivel 4); `ticon-cff91b` 7.3 km, fuera por el tope de 3 puertos (nivel 4); `imi-carrigaholt` 9.3 km, fuera por el tope de 3 puertos (nivel 1)

### IE-SE — Waterford y Cork (10 picos)

- `imi-kinsale` Kinsale (modelado) — oficial, misma costa: 5 picos a 8.1–58 km, radio 69 km (niveles 1,3)
- `imi-dungarvan` Dungarvan (modelado) — oficial, misma costa: 4 picos a 14–30 km, radio 40 km (niveles 1,3)
- `imi-castletownbere` Castletownbere — oficial, misma costa: 1 picos a 21–21 km, radio 31 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): ARDMORE → imi-dungarvan
- Descartadas: `ticon-fbe95e` 10 km, cruza 16 km de tierra; `imi-dunmore` 11 km, fuera por el tope de 3 puertos (nivel 1); `imi-union-hall` 12 km, fuera por el tope de 3 puertos (nivel 3); `ticon-c1f60c` 16 km, fuera por el tope de 3 puertos (nivel 4)

### NO-S — Noruega sur (Jaeren y Stad) (3 picos)

- `ticon-44917a` TICON-3 61.934N 5.113E (gesla.uhslc) — TICON-3, cruzando tierra: 2 picos a 14–21 km, radio 32 km
- `ticon-db052f` TICON-3 58.974N 5.730E (gesla.cmems) — TICON-3, cruzando tierra: 1 picos a 34–34 km, radio 45 km
- Descartadas: `ticon-72a205` 64 km, cruza 12 km de tierra

### NO-N — Lofoten (3 picos)

- `ticon-448fcc` TICON-3 68.213N 14.482E (gesla.uhslc) — TICON-3, misma costa: 2 picos a 38–54 km, radio 65 km (niveles 2,4)
- `ticon-90ea2b` TICON-3 67.292N 14.400E (gesla.usgs) — TICON-3, misma costa: 1 picos a 108–108 km, radio 118 km
- Radios superpuestos (el reloj toma el puerto más cercano que lo cubre): HAUKLAND → ticon-448fcc
- Descartadas: `ticon-90ea2b` 114 km, cruza 18 km de tierra

### DK-ALL — Dinamarca (5 picos)

- `ticon-4bcc10` TICON-3 57.117N 8.600E (gesla.refmar) — TICON-3, misma costa: 3 picos a 1.4–22 km, radio 33 km
- `ticon-8f3726` TICON-3 56.525N 8.115E (gesla.cmems) — TICON-3, misma costa: 2 picos a 17–30 km, radio 41 km
- Descartadas: `ticon-c69ccb` 0.7 km, cruza 28 km de tierra; `ticon-b7d357` 9.1 km, fuera por el tope de 3 puertos (nivel 4); `ticon-3a1929` 42 km, cruza 70 km de tierra; `ticon-8f3726` 61 km, cruza 30 km de tierra

### NL-ALL — Países Bajos (11 picos)

- `ticon-789208` TICON-3 52.462N 4.555E (gesla.uhslc) — TICON-3, misma costa: 6 picos a 1.1–71 km, radio 81 km
- `ticon-a4a070` TICON-3 52.205N 4.362E (gesla.cmems) — TICON-3, misma costa: 4 picos a 5.8–30 km, radio 41 km
- `ticon-9c5cfc` TICON-3 51.592N 3.555E (gesla.noaa) — TICON-3, misma costa: 1 picos a 5.7–5.7 km, radio 16 km
- Descartadas: `ticon-91108e` 0.8 km, fuera por el tope de 3 puertos (nivel 2); `ticon-6ef75f` 1.2 km, fuera por el tope de 3 puertos (nivel 2); `ticon-030619` 2.3 km, fuera por el tope de 3 puertos (nivel 2); `ticon-9356dc` 3.7 km, fuera por el tope de 3 puertos (nivel 2)

### DE-ALL — Alemania (4 picos)

- `ticon-1af31e` TICON-3 54.967N 8.666E (gesla.refmar) — TICON-3, misma costa: 4 picos a 23–34 km, radio 44 km
- Descartadas: `ticon-a0c721` 1.5 km, fuera por el tope de 3 puertos (nivel 2); `ticon-bffea6` 16 km, fuera por el tope de 3 puertos (nivel 4); `ticon-ddd798` 23 km, fuera por el tope de 3 puertos (nivel 2); `ticon-dd036b` 32 km, fuera por el tope de 3 puertos (nivel 2)

### IT-ALL — Italia peninsular y Sicilia (7 picos)

- `ticon-66dd4f` TICON-3 43.546N 10.299E (gesla.rws) — TICON-3, misma costa: 2 picos a 15–48 km, radio 58 km
- `ticon-2cdea6` TICON-3 42.094N 11.790E (gesla.bom) — TICON-3, misma costa: 2 picos a 28–58 km, radio 68 km (niveles 2,4)
- `ticon-ce6910` TICON-3 44.410N 8.925E (gesla.cmems) — TICON-3, misma costa: 2 picos a 28–61 km, radio 71 km
- Sin puerto (Open-Meteo): MONDELLO (ticon-74189e a 10 km: fuera por el tope de 3 puertos)
- Descartadas: `ticon-74189e` 10 km, fuera por el tope de 3 puertos (nivel 4); `ticon-b094b0` 22 km, fuera por el tope de 3 puertos (nivel 4); `ticon-9a246d` 43 km, cruza 18 km de tierra; `ticon-0cee3a` 70 km, cruza 26 km de tierra

### IT-SAR — Cerdeña (4 picos)

- `ticon-4a4b08` TICON-3 39.148N 8.309E (gesla.uhslc) — TICON-3, misma costa: 4 picos a 29–101 km, radio 112 km (niveles 2,4)
- Descartadas: `ticon-502c40` 65 km, cruza 63 km de tierra; `ticon-d3f43a` 88 km, cruza 55 km de tierra

### IS-ALL — Islandia (3 picos)

- `ticon-c4827f` TICON-3 64.151N 21.940W (gesla.noaa) — TICON-3, cruzando tierra: 2 picos a 43–53 km, radio 63 km
- `got-8ae671` GOT5.6 63.405N 19.071W (IS-ALL) — modelo global GOT5.6: 1 picos a 0.0–0.0 km, radio 10 km

## Fuentes y licencias

- NOAA/NOS/CO-OPS (dominio público): predicciones horarias sobre MLLW, estaciones armónicas.
- 気象庁 JMA, 潮位表 (Public Data License 1.0): alturas horarias, JST → UTC, datum DL.
- Marine Institute, Ireland (CC BY 4.0): ERDDAP `IMI-TidePrediction`, de 5 min a la hora.
- LINZ (CC BY 4.0, Crown copyright): pleamares y bajamares → horarias con medios cosenos.
- TICON-3 (CC BY 4.0): Hart-Davis, M. G., Dettmering, D., Seitz, F. (2022). TICON-3: Tidal Constants based on GESLA-3 sea-level records from globally distributed tide gauges including gauge type information (data). PANGAEA, https://doi.org/10.1594/PANGAEA.951610

