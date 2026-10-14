# Formatos que bajan las apps

Todo se sirve por GitHub Pages desde `https://scgm11.github.io/surf-dawn-data/`. Los archivos que
lee el reloj son chicos a propósito: el proceso de segundo plano de la esfera tiene 64 KB, y un
JSON de 3,5 KB llega a ocupar 12 KB al leerse. Tope: **6 KB por archivo** (la Action falla si pasa).

## Picos: `spots/`

### `spots/g/<LAT>_<LON>.json` — qué regiones hay cerca (esfera y apps, modo automático)

Una celda de 10° × 10°; `<LAT>` y `<LON>` son el piso de la posición en múltiplos de 10
(`-40_-60` cubre de −40 a −30 de latitud y de −60 a −50 de longitud). Lista las regiones cuyo
círculo (centro y radio) toca la celda:

```json
[["AR-MDP",-38.21,-57.71,95,"3f2a9c"],["UY-MAL",-34.91,-54.86,45,"a1b2c3"]]
```

Fila: `[región, lat del centro, lon del centro, radio km, versión]`. Una celda sin regiones no
existe (404): el reloj lo toma como "sin picos acá".

### `spots/idx.json` — continentes (apps)

```json
{"v":1,"c":[["AM","América","Americas",76],["OC","Oceanía","Oceania",33]]}
```

Fila: `[código, nombre es, nombre en, regiones]`.

### `spots/idx/<CONTINENTE>.json` — países y regiones de un continente (apps)

```json
{"c":[["AR","Argentina","Argentina"],["BR","Brasil","Brazil"]],
 "r":[["AR-MDP","AR","Mar del Plata–Necochea","Mar del Plata–Necochea",-38.21,-57.71,95,24,2950,"3f2a9c"]]}
```

Fila de región: `[código, país, nombre es, nombre en, lat, lon, radio km, picos, bytes, versión]`.

### `spots/r/<REGIÓN>.json` — una región (esfera y apps)

```json
{"id":"AR-MDP","v":"3f2a9c","c":"AR","n":["Mar del Plata–Necochea","Mar del Plata–Necochea"],
 "m":["ncep_gfswave025","gfs_seamless"],
 "p":[["mdp",-38.04,-57.53,80,0]],
 "s":[["BIOLOGÍA",-38.03,-57.53,105,1],
      ["PLAYA GRANDE",-38.02,-57.53,110,1,-38.0,-57.25]]}
```

- `v`: versión (hash corto del contenido). Cambia si cambia cualquier cosa de la región.
- `m`: `[modelo de olas, modelo de viento]` de Open-Meteo para esa región.
- `p`: puertos de marea que la cubren: `[clave, lat, lon, radio km, desfase UTC en segundos]`. La
  clave arma la URL de los meses (`tide/<clave>/AAAA-MM.json`) y de los armónicos. Un pico fuera
  de todos los radios usa `sea_level_height_msl` de Open-Meteo.
- `s`: picos `[NOMBRE, lat, lon, orientación, tipo, (lat ola, lon ola)]`. Tipo: 0 sin dato,
  1 beach, 2 point, 3 reef. Orientación: grados hacia donde mira la playa (al mar). El punto de
  olas va solo si la celda del modelo de la región es tierra en la posición del pico.
- El id de un pico en el reloj es `<REGIÓN>/<NOMBRE>`.

## Mareas: `tide/`

### `tide/<clave>/AAAA-MM.json` — un mes (formato de siempre)

```json
{"port":"mdp","month":"2026-10","days":31,"utc_offset":0,"unit":"cm","src":"ticon:...",
 "datum":"LAT","h":[99,98,96]}
```

24 alturas horarias por día en cm, `h[(día-1)*24 + hora]`, con día y hora en el reloj de
`utc_offset` (horas). Los puertos de Uruguay y Brasil siguen en −3; los nuevos van en UTC (0).
Alturas sobre el datum del puerto (`datum`): `LAT`/`MLLW`/cero de carta en las tablas oficiales;
en las calculadas desde armónicos, el nivel medio más la suma de amplitudes (siempre ≥ 0).

### `tide/<clave>/harmonics.json` — respaldo sin red

```json
{"port":"mdp","t0":1767225600,"mean":120.3,"cos":[...30],"sin":[...30],"rms":3.1}
```

Ajuste de un año de alturas horarias con los 30 períodos de `TideTable.PERIODS` (mismo orden),
en cm, con `t0` en segundos Unix. El reloj calcula
`h(t) = mean + Σ cos[k]·cos(2π·τ/P[k]) + sin[k]·sin(2π·τ/P[k])`, con `τ = (t − t0)/3600`.

### `tide/ports.json` — todos los puertos

```json
[{"key":"mdp","name":"Mar del Plata","lat":-38.04,"lon":-57.53,"utc_offset":0,
  "src":"ticon:MAR_DEL_PLATA","datum":"LAT","license":"CC BY 4.0","credit":"TICON-3"}]
```

### `tide/regions.json` — puertos de cada región (lo lee `build_zones.py`)

```json
{"AR-MDP":[["mdp",-38.04,-57.53,80,0]]}
```

## Validación: `validation/`

### `validation/<REGIÓN>.json`

```json
{"region":"US-CA-SD","from":"2026-09-01","to":"2026-09-30","buoys":["cdip:100","ndbc:46225"],
 "wave":{"ecmwf_wam":{"n":712,"hs_bias":0.05,"hs_rmse":0.19,"hs_si":0.18,"tp_bias":-0.4,"tp_mae":1.6,"dir_mae":14,"eligible":true},
         "meteofrance_wave":{"n":712,"hs_bias":-0.02,"hs_rmse":0.18,"hs_si":0.16,"tp_bias":-2.1,"tp_mae":2.4,"dir_mae":12,"eligible":false}},
 "wind":{"stations":["ndbc:46086"],"current":"gfs_seamless",
         "models":{"ecmwf_ifs":{"n":700,"spd_bias":0.04,"spd_bias_ms":0.2,"spd_rmse":1.5,"dir_mae":21,"dir_bias":-3,"dir_n":520,"obs_spd":5.6},
                   "gfs_seamless":{"n":700,"spd_bias":0.12,"spd_bias_ms":0.7,"spd_rmse":1.8,"dir_mae":24,"dir_bias":-5,"dir_n":520,"obs_spd":5.6}},
         "best":"ecmwf_ifs","confidence":"media","vs":"gfs_seamless","margin":0.2,
         "per_station":{"ndbc:46086":{"n":700,"best":"ecmwf_ifs","km":76.4,"kind":"buoy","z":4.1}}},
 "best":{"wave":"ecmwf_wam","wind":"ecmwf_ifs"},"confidence":"media"}
```

`hs_bias` relativo (fracción), `hs_rmse` en m, `tp_bias` y `tp_mae` en s, `dir_mae` en grados.

Lo escribe `validate/run.py` (ver `validate/README.md`), que agrega estos campos:

- `wave.<modelo>`: además `dir_bias` (media circular de modelo − boya, °), `tm_bias` (período medio
  del modelo − período medio de la boya, s), `obs_hs` (Hs media de las boyas, m), `tp_mae` (error
  medio absoluto de período contra el período pico de la boya, s) y `tp_type`: `"peak"` si `tp_bias`
  usa el período pico del modelo (ECMWF WAM, siempre su `wave_peak_period`); si el modelo no lo da en
  Open-Meteo se usa su `wave_period`: `"primary"` en GFS-Wave (período del sistema principal, se
  comporta como un pico) y `"mean"` en MFWAM y EWAM (período medio: `tp_bias` negativo por
  construcción). `eligible`: si el modelo se puede elegir (`ecmwf_wam`, `ncep_gfswave016`,
  `ncep_gfswave025`, los que dan período pico); MFWAM y EWAM se miden para informar. Van primero los
  elegibles, cada grupo del mejor al peor.
- `best.wave` y `confidence` (`alta`/`media`/`baja`): el elegible de menor `hs_rmse` con
  |`hs_bias`| ≤ 0,15 (empates de 0,01 m: menor `tp_mae`, después menor `dir_mae`); sin `best.wave` si
  ningún elegible califica o hay menos de 72 horas. `vs`: el modelo contra el que se mide la confianza
  (el de hoy, o el segundo elegible si el mejor ya es el de hoy); `margin`: cuánto peor es su
  `hs_rmse` (fracción).
- `per_buoy`: por boya, `n`, el mejor modelo elegible con esa boya sola y la distancia `km` al pico
  más cercano.
- `excluded`: boyas a menos de 150 km que no se usaron, con el motivo (`why`): miran a otro mar o
  están abrigadas (ven menos de la mitad de las direcciones abiertas de los picos), todos los modelos
  con |sesgo| > 0,5, o Open-Meteo no tiene ahí (o tiene pocas horas de) el modelo de hoy. Un modelo
  con menos del 80 % de las horas del mejor cubierto en una boya no se compara en esa región.
- `current`: el modelo de olas que usa hoy la región; `fixed`: `true` en las regiones fijas del issue #7.
- `spread`: dispersión de Hs entre modelos en un pico (`point`: el más cercano al centro donde el
  modelo de hoy tiene mar, probando hasta 4): `hs` (desvío / media,
  promedio de `hours` horas) y `mean_hs` por modelo. En una región sin boyas (`"buoys": []`) es lo
  único que hay, y `confidence` es `baja` si `hs` > 0,30.
- `wind`: el viento a 10 m de los modelos de Open-Meteo contra hasta 3 estaciones (boyas y estaciones
  costeras) a menos de 150 km, con la misma lógica (la más cercana primero, mismo mar, mismas horas
  para todos los modelos). `stations` (vacío si no hay), `current` (el modelo de viento de hoy) y,
  con estaciones, `models.<modelo>`: `n`, `spd_bias` (relativo, fracción), `spd_bias_ms` (m/s),
  `spd_rmse` (m/s), `dir_mae` y `dir_bias` (°, sólo horas con viento observado ≥ 3 m/s, `dir_n`
  horas) y `obs_spd` (velocidad media observada a 10 m, m/s), del mejor al peor. `best`: el de menor
  `spd_rmse` con |`spd_bias`| ≤ 0,20 (con ≥ 72 horas); `confidence`, `vs` y `margin` como en olas
  (con `spd_rmse`); `per_station`: `n`, `best`, `km`, `kind` (`buoy` o `fixed`, en tierra) y `z`
  (altura del anemómetro sobre el mar, m; `null` si la estación no la publica: entonces la velocidad
  va sin ajustar); `excluded` como en olas (una estación donde todos los modelos erran la velocidad
  por más de 35 % no se usa). Se comparan `gfs_seamless` y `ecmwf_ifs` en todas partes, y
  `meteofrance_seamless` (Europa), `ukmo_seamless` (Islas Británicas), `cmc_gem_seamless`
  (Norteamérica), `jma_seamless` (Japón, Corea, Taiwán), `bom_access_global` (Australia, Nueva Zelanda,
  Pacífico sudoeste) e `icon_seamless` (Europa) en su dominio (`validate/models.py`, `WIND_DOMAINS`).
- `best`: `{"wave": ..., "wind": ...}`, cada uno sólo si hay un mejor; `confidence` (arriba) es la de olas.

`validation/models-suggested.csv` tiene las columnas de `models.csv` y sólo las regiones no fijas en
las que el mejor modelo de olas o de viento, con confianza alta o media, no es el de hoy (la regla por
defecto o la fila de `models.csv`); la otra columna queda con el modelo de hoy y `why` explica cada
cambio. `validation/buoys.csv` tiene las boyas de olas usadas (`id,name,lat,lon,hours,regions`);
`validation/wind-stations.csv`, las estaciones de viento usadas o descartadas
(`id,name,lat,lon,kind,z,factor,hours,regions`: `factor` es lo que se multiplicó la velocidad para
llevarla a 10 m); `validation/stations.csv`, todas las estaciones leídas con sus horas
(`id,name,lat,lon,kind,records,hours,wind_hours,first,last`, para diagnóstico).

### `models.csv` — modelos elegidos (lo lee `build_zones.py`)

`region,wave,wind,why`. Una región sin fila usa la regla por defecto: olas `ncep_gfswave016`
entre 15°S y 52,5°N y `ncep_gfswave025` fuera; viento `gfs_seamless`. Uruguay, Santa Catarina,
Rio Grande do Sul y Argentina quedan fijos en `ncep_gfswave025` + `gfs_seamless` (como Windguru,
decidido en el issue #7). La regla y la lectura de este archivo están una sola vez, en
`tools/lib/models.py` (las usan `build_zones.py` y `validate/`). Una fila nueva entra por PR con su
`validation/<REGIÓN>.json`; las de la validación del 2026-10-13 (confianza alta o media) ya están. En `wave` sólo van modelos
que dan período pico (el reloj lo muestra y puntúa las horas con él): `ecmwf_wam`, `ncep_gfswave016`
(en su dominio) o `ncep_gfswave025`; MFWAM y DWD EWAM no, sólo dan período medio.
