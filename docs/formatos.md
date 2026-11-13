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
{"v":1,"c":[["AM","América","Americas",76],["OC","Oceanía","Oceania",33]],
 "pt":{"AM":"Américas","OC":"Oceania"}}
```

Fila: `[código, nombre es, nombre en, regiones]`. `pt`: el nombre en portugués de los que no se
escriben igual que en español (el reloj en portugués usa el español para los demás). Va aparte de
las filas porque los relojes de antes de él revisan cuántos datos tiene cada una.

### `spots/idx/<CONTINENTE>.json` — países y regiones de un continente (apps)

```json
{"c":[["AR","Argentina","Argentina"],["BR","Brasil","Brazil"]],
 "r":[["AR-MDP","AR","Mar del Plata–Necochea","Mar del Plata–Necochea",-38.21,-57.71,95,24,2950,"3f2a9c"]],
 "pt":{"BR-RJ":"Rio de Janeiro"}}
```

Fila de región: `[código, país, nombre es, nombre en, lat, lon, radio km, picos, bytes, versión]`.
`pt`: países y regiones en portugués, como en `idx.json`.

### `spots/c/<I>_<J>.json` — los picos de una celda de 0,2° (campos de datos)

```json
{"z":[["UY-ROC","ncep_gfswave025","gfs_seamless"]],
 "p":[["la-paloma",-34.6533,-54.1417,135,-10800]],
 "s":[["EL FARO",-34.667,-54.1608,206,0,0],["PLAYA X",-34.7,-54.2,180,0,-1,-34.75,-54.2]],
 "w":[[1.8,13.0]]}
```

`I = piso(lat × 5)`, `J = piso(lon × 5)`. Lo que necesitan los campos de datos Marea y Olas y viento
para elegir el pico más cercano y bajar sus datos, sin la región entera: el servicio de fondo de un
campo tiene 32 KB en los relojes anteriores a Connect IQ 4 (fēnix 6 Pro) y ahí una respuesta de más
de 1 KB no entra (una región llega a 3 KB). Los picos a menos de 10 km de la celda (como mucho 24:
primero los de adentro, después los más cercanos al centro; menos si el archivo pasa de 1100 bytes,
porque la celda de Bali, de 1351, no entraba en el fēnix 6 Pro), cada uno
`[NOMBRE, lat, lon, orientación, índice en z, índice en p o -1, (lat ola, lon ola)]`; `z` son sus
regiones (`[región, modelo de olas, modelo de viento]`) y `p` sus puertos de marea, elegidos acá
como en el reloj (`TideTable.portFor`: el más cercano cuyo radio lo cubre); `w`, uno por fila de `z`, la escala
de las olas de cada región (su `w`, o `null`), aparte de `z` porque los campos anteriores solo aceptan filas
de 3 ahí; `sw`, uno por fila de `s`, la ventana de swell de cada pico (el `sw` de su región, o `null`),
aparte de `s` por lo mismo y solo en las celdas que tienen alguna. Una celda sin picos cerca
no tiene archivo (404). Los arma `tools/build_cells.py` desde las regiones después de cada corrida
de las zonas.

### `spots/r/<REGIÓN>.json` — una región (esfera y apps)

```json
{"id":"AR-MDP","v":"3f2a9c","c":"AR","n":["Mar del Plata–Necochea","Mar del Plata–Necochea"],
 "m":["ncep_gfswave025","gfs_seamless"],
 "p":[["mdp",-38.04,-57.53,80,0]],
 "s":[["BIOLOGÍA",-38.03,-57.53,105,1],
      ["PLAYA GRANDE",-38.02,-57.53,110,1,-38.0,-57.25]],
 "x":[129140163,129127395],
 "w":[1.48,13.0]}
```

- `v`: versión (hash corto del contenido). Cambia si cambia cualquier cosa de la región.
- `np` (opcional): el nombre en portugués, si no es el mismo que en español (`n` es `[es, en]`: los
  relojes de antes de él toman dos nombres).
- `m`: `[modelo de olas, modelo de viento]` de Open-Meteo para esa región.
- `p`: puertos de marea que la cubren: `[clave, lat, lon, radio km, desfase UTC en segundos]`. La
  clave arma la URL de los meses (`tide/<clave>/AAAA-MM.json`) y de los armónicos. Un pico fuera
  de todos los radios usa `sea_level_height_msl` de Open-Meteo.
- `s`: picos `[NOMBRE, lat, lon, orientación, tipo, (lat ola, lon ola)]`. Tipo: 0 sin dato,
  1 beach, 2 point, 3 reef. Orientación: grados hacia donde mira la playa (al mar). El punto de
  olas va solo si la celda del modelo de la región es tierra en la posición del pico.
- `x` (opcional): qué tan abierto al mar está cada pico, un número por pico en el orden de `s`
  (`tools/lib/shelter.py`). Guarda un nivel por cada uno de 18 sectores de 20° (el sector `i`
  centrado en `i × 20°`, la dirección **desde** la que viene el viento o el swell) en base 3:
  `nivel(i) = (x ÷ 3^i) mod 3`, con 0 = tierra a menos de 2 km, 1 = tierra a menos de 25 km,
  2 = mar abierto (la mediana de 5 rayos por sector, sobre la costa de OpenStreetMap). Un pico
  sin ningún sector abierto suele haber quedado pegado a un río, una ría o un puerto, con la
  orientación cruzando el agua: el build lo mueve al punto de costa más abierto a menos de 2 km
  de su semilla (salvo `nosnap`; con `facing=` conserva esa orientación y solo se mueve por costa
  que mire a menos de 60° de ella) y lo avisa en el reporte. `null` si aun así no hay mar abierto: el reloj puntúa ese pico como antes. El reloj
  lo usa en el puntaje: viento que cruza tierra cerca levanta poco picado, y swell con tierra en
  el camino llega cortado. Va aparte de `s` porque los relojes anteriores rechazan filas que no
  tengan 5 o 7 valores.
- `w` (opcional): la escala de las olas de la región, `[altura m, período s]` donde el puntaje de
  las olas de las apps llega a todo (`Score.wave` en surf-dawn: con la del mundo, 1,8 m y 13 s).
  El 88 % de la altura que se pasa el 10 % de las horas con luz (07–18 h) de un año y 1,7 s más que
  el período que se pasa el 10 % de las horas, en el punto de olas del pico del medio de la región
  y en su modelo de olas (GFS Wave 0,25° donde es ECMWF WAM, que no tiene historia de ese año en
  Open-Meteo; si GFS tiene tierra en ese pico, en la celda de mar delante de él):
  así la de Rocha (UY-ROC) es la del mundo. Lo calcula `tools/build_scale.py` en
  `seeds/scale.csv` (un año pesa 26 llamadas de la API gratis: se corre a mano, no en cada build) y
  `tools/build_zones.py` lo copia acá. Los niveles de la energía del mar van con ella. Las apps
  anteriores no la leen; sin `w`, la del mundo.
- `sw` (opcional): la ventana de swell de los reefs y las puntas donde el swell entra dando la vuelta
  (el Bukit, G-Land, Raglan, Rincón…), un valor por pico en el orden de `s`: grados **desde** donde
  viene el swell que lo hace andar, o `null` donde no hay (la semilla `swell=`). Con ventana, el
  reloj mide el swell contra ella y no contra la orientación, sin el corte de `x` (la ventana ya
  cuenta con la punta que el swell rodea); el viento sigue con la orientación y `x`. Solo en las
  regiones que tienen alguna, y aparte de `s` como `x`.
- El id de un pico en el reloj es `<REGIÓN>/<NOMBRE>`.

### Cuando cambia una región

Las apps guardan por código la zona, el pico elegido a mano, los tipos de ola y las sesiones, y solo
vuelven a bajar una zona que `spots/g/` lista y que cubre la posición (`Zones.wanted` en surf-dawn).

- **Un código nuevo** no pide nada en las apps: aparece en `spots/g/` e `idx/` y se baja como cualquier otro.
  Las zonas de un solo pico ya existen (`MV-CEN`, `BS-ALL`).
- **Un código que deja de existir** queda como estaba en el reloj que lo tenía: nada lo actualiza ni lo
  borra, y su `r/` da 404 si hay que bajarlo. En un empate de distancia `Zones.locate` elige la zona de
  centro más lejano, que suele ser la vieja. Por eso un código no se borra (`seeds/README.md`).
- **Un pico que sale de su zona**: al bajar la versión nueva, el id viejo deja de encontrarse
  (`Zones.find`) y las apps vuelven al pico más cercano, al último mostrado o al de fábrica. La copia vieja
  de la zona sigue valiendo hasta que el reloj pasa cerca de ella.

## Mareas: `tide/`

### `tide/<clave>/AAAA-MM.json` — un mes (formato de siempre)

```json
{"port":"mdp","month":"2026-10","days":31,"utc_offset":0,"unit":"cm","src":"ticon:...",
 "datum":"LAT","h":[99,98,96]}
```

24 alturas horarias por día en cm, `h[(día-1)*24 + hora]`, con día y hora en el reloj de
`utc_offset` (horas). Los puertos de Uruguay y Brasil siguen en −3; los nuevos van en UTC (0).
Alturas sobre el datum del puerto (`datum`): `LAT`/`MLLW`/cero de carta en las tablas oficiales;
en las calculadas desde armónicos, el nivel medio más la suma de amplitudes (siempre ≥ 0); en las del
modelo global GOT5.6 (`got-…`, donde no hay mareógrafo cerca), el nivel medio más lo justo para que
ninguna altura sea negativa (`"datum":"MSL+N cm (modelo)"`).

### `tide/<clave>/harmonics.json` — respaldo sin red

```json
{"port":"mdp","t0":1767225600,"mean":120.3,"cos":[...30],"sin":[...30],"rms":3.1}
```

Ajuste de un año de alturas horarias con los 30 períodos de `TideTable.PERIODS` (mismo orden),
en cm, con `t0` en segundos Unix. El reloj calcula
`h(t) = mean + Σ cos[k]·cos(2π·τ/P[k]) + sin[k]·sin(2π·τ/P[k])`, con `τ = (t − t0)/3600`.

### `tide/<clave>/d/AAAA-MM-DD.json` — un tramo, para el campo Marea

```json
{"t0":1793199600,"h":[40,47,50,48,43]}
```

156 alturas horarias en cm (las mismas de los meses) desde `t0` (segundos Unix): las 12:00 del día
anterior al día del nombre, en el reloj del puerto, hasta 6 días después. Hay un tramo cada 4 días
(1, 5, 9… 29) del mes en curso y el siguiente; los arma `tools/tide/chunks.py` en cada corrida de
las mareas (días 1 y 15) y borra los demás. El campo pide el tramo del día de ahora (unos 500
bytes): un mes entero ocupa unos 11 KB en la memoria del reloj y el servicio de fondo de un campo
tiene 32 KB en el fēnix 6 Pro. Al final de los datos del año el tramo sale más corto (nunca con
menos de 60 horas).

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
- `spread`: dispersión de Hs entre modelos donde las apps piden las olas de un pico (`point`: su punto
  de olas si tiene, si no el pico; el del pico más cercano al centro donde el modelo de hoy tiene mar,
  probando hasta 4 puntos; `cell`: la celda de la que contestó la API): `hs` (desvío / media,
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

### `validation/spots.md` y `validation/spots.json` — controles por pico

`tools/check_spots.py` (Action `checks.yml`, el día 5 de cada mes) revisa cada pico de `spots/`:
la orientación contra las olas de las últimas dos semanas en su punto de olas (se marca el que casi
nunca las recibe de frente mientras su zona sí: suele ser una orientación del lado equivocado de una
punta o una laguna), la altura contra la mediana de su zona (sin olas, o más del doble) y, para los
emblemáticos (`top`), la posición contra el ítem más cercano con su nombre en Wikidata o GeoNames
(si no hay, OpenStreetMap). También pregunta a la API desde qué celda contesta a cada pico, como las
apps (sin `cell_selection`, que puede correr el punto): marca el punto de olas corrido o detrás de la
playa (a más de 75° de hacia donde mira, o de su ventana de swell) y el pico que la API corre a una
celda detrás de la playa o a más de 35 km. El JSON tiene `flags` (`region`, `spot`, `why`, `top`),
`cells` (`region`, `spot`, `wave`, `cell`, `km`, `why`), `flagship`
(`status`: `ok`, `lejos`, `revisado`, `sin fuente` o `error`; `km`, `qid`, `wd_lat`, `wd_lon`) y, por
región, la mediana de la altura y de las horas con olas de frente.

Buscar los emblemáticos lleva casi una hora, así que lo demás se escribe antes. Si la corrida se corta
en esa búsqueda, o corre con `--no-wikidata`, quedan los emblemáticos de la corrida anterior y
`flagship_old` es `true`.

### `validation/lookup.md` — búsqueda por nombre

`tools/lookup.py` (Action `lookup.yml`, a mano) lista, para los emblemáticos sin fuente o lejos de la
suya (o los picos que se le pidan), todo lo que Wikidata (con qué es cada ítem), Wikipedia, GeoNames
(de cualquier tipo) y OpenStreetMap tienen con su nombre o una de sus palabras a 15 km. Es para la
revisión a mano: no cambia semillas.

### `models.csv` — modelos elegidos (lo lee `build_zones.py`)

`region,wave,wind,why`. Una región sin fila usa la regla por defecto: olas `ncep_gfswave016`
entre 15°S y 52,5°N y `ncep_gfswave025` fuera; viento `gfs_seamless`. Uruguay, Santa Catarina,
Rio Grande do Sul y Argentina quedan fijos en `ncep_gfswave025` + `gfs_seamless` (como Windguru,
decidido en el issue #7). La regla y la lectura de este archivo están una sola vez, en
`tools/lib/models.py` (las usan `build_zones.py` y `validate/`). Una fila nueva entra por PR con su
`validation/<REGIÓN>.json`; las de la validación del 2026-10-13 (confianza alta o media) ya están. En `wave` sólo van modelos
que dan período pico (el reloj lo muestra y puntúa las horas con él): `ecmwf_wam`, `ncep_gfswave016`
(en su dominio) o `ncep_gfswave025`; MFWAM y DWD EWAM no, sólo dan período medio.

## Lo normal: `normals/`

### `normals/normals.json` — lo normal de cada región (app de iPhone, Cómo viene)

```json
{
"UY-MAL": {"k":0.87,"m":[[7.7,8.7,11.6],[8.6,12.9,15], ...],"y":"2016-2024"},
...
}
```

Por región: `m`, los 12 meses de enero a diciembre, cada uno con los días que dan olas en 30 (algún
pico con 3 estrellas o más en el ranking de Pronóstico): el cuartil de abajo, la mediana y el de arriba
de los años `y`; `k`, el factor por el que van las alturas de ERA5-Ocean (el modelo de olas de la región
sobre ERA5-Ocean en los últimos 92 días, entre 0,7 y 1,6). El agua y el aire en el pico de referencia, cada uno
con 12 meses de [cuartil de abajo, mediana, cuartil de arriba] de la media de cada año, en °C: `tx` la máxima
del aire y `tn` la mínima (ERA5 de los años `y`, llevado al modelo de viento de la región por lo que dio de más
o de menos en los últimos 92 días), `tw` el agua (la temperatura del mar del pronóstico de Open-Meteo, que
tiene historia recién desde 2023: sus años en `yw`). Pueden faltar. Una línea por región, en orden. Lo escribe la
app (repo de las apps: `swift run normals --answers`, con `watchos/tools/normals.sh`) y el iPhone lo baja
una vez por semana (unos 50 KB); una región que no está, o que no es válida (12 meses de tres números
crecientes entre 0 y 31), queda sin "lo normal". Los relojes no lo leen.

### Release `era5` — las respuestas de las que sale

`<REGIÓN>.json.gz`: las siete respuestas de Open-Meteo de una región tal como llegan (`wind`, ERA5
en el pico de referencia: viento en km/h, salida y puesta del sol y la máxima y la mínima del aire, del
1/1/2016 al 17/11/2024 en su hora; `marine`, ERA5-Ocean en su punto de olas, los mismos días en la hora
del viento; `factor_model` y `factor_era5`, la altura del modelo de la región y la de ERA5-Ocean en los
últimos 92 días, en GMT; `water`, la temperatura del mar en el pico de 2023 a 2025; `air_model` y
`air_era5`, la máxima y la mínima del modelo de viento de la región y las de ERA5 en los últimos 92 días),
con `v` (2 desde que tienen el agua y el aire: una región de la versión 1 se vuelve a pedir) y `asked` (la consulta de cada pedido, que la app compara con la suya), `spot`, `at`,
`wave`, `model` y `fetched`. `index.json`: por región, dónde se pidió, cuándo y cuántas horas con
período pico trajo (`hours` de `of`), o `error` si no se pudo (sin olas en el punto: no se vuelve a pedir
hasta que se mueva el pico de referencia). Lo arma `tools/era5_normals.py` (Action `era5.yml`).

