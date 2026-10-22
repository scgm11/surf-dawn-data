# surf-dawn-data

Datos públicos que bajan la esfera **Surf Dawn**, **Pronóstico** y **Sesión** (repo
[`scgm11/surf-dawn`](https://github.com/scgm11/surf-dawn)) en los Garmin. Todo se sirve como JSON
por GitHub Pages desde `https://scgm11.github.io/surf-dawn-data/`, lo arman las Actions de este
repo y los formatos están en [`docs/formatos.md`](docs/formatos.md).

| Carpeta | Qué es | Lo arma |
|---|---|---|
| `spots/` | Los picos del mundo en zonas de hasta 60: una por región (`r/`), los índices por continente (`idx.json`, `idx/`) y las celdas de 10° que el reloj mira por posición (`g/`) | `tools/build_zones.py` (Action `zones.yml`) |
| `tide/` | Mareas de los puertos de cada zona, mes a mes, con armónicos de respaldo | `tools/tide/` (Action `tides.yml`), `tools/sohma_tide.py` y `tools/ciram_tide.py` (Action `update.yml`) |
| `validation/` | Los modelos de olas y viento de Open-Meteo contra boyas y estaciones, por región; y los controles de cada pico (`spots.md`) | `validate/` (Action `validation.yml`), `tools/check_spots.py` (Action `checks.yml`), `tools/lookup.py` (Action `lookup.yml`) |
| `models.csv` | Los modelos elegidos por región (el resto usa la regla por defecto) | a mano, desde `validation/models-suggested.csv` |
| `seeds/` | Las tablas de las que sale todo: continentes, países, regiones y picos | a mano ([`seeds/README.md`](seeds/README.md)) |
| `manual/` | El manual de las apps en PDF, el link público de la tienda Connect IQ ([`manual/Surf-Dawn-manual.pdf`](https://scgm11.github.io/surf-dawn-data/manual/Surf-Dawn-manual.pdf)) | copiado de `docs/Surf-Dawn-manual.pdf` del repo de las apps en cada versión de la tienda |

## Picos — `spots/`

Unas 210 regiones y más de 2.400 picos: las Américas completas, Hawái, Nueva Zelanda, Australia,
Maldivas, Sudáfrica y los picos más conocidos del resto del mundo (`seeds/emblematicos.md`). Cada
pico sale de una fila de `seeds/spots/<REGIÓN>.csv`; `build_zones.py` lo ajusta a la costa de
OpenStreetMap, calcula hacia dónde mira la playa y el punto de mar donde pedir las olas (Open-Meteo),
y le pone a la región sus modelos (`models.csv` o la regla) y sus puertos de marea
(`tide/regions.json`). Las regiones de Uruguay y Santa Catarina están congeladas: sus semillas traen
las posiciones, orientaciones y puntos de olas validados en 2026-10 (Canelones y Montevideo, `UY-CAN`:
calculados por `build_zones.py` el 2026-10-22 y congelados igual).

**Agregar o corregir un pico:** una fila en la tabla de su región y un PR
([`seeds/README.md`](seeds/README.md) tiene las columnas y las reglas). `tools/check_seeds.py`
valida las tablas (nombres que el reloj puede dibujar, a lo sumo 60 por región, posiciones en su
región); la Action `zones.yml` arma `spots/` y deja el detalle en `spots/build.log`. La costa sale
del archivo de líneas de costa de OSM de osmdata.openstreetmap.de (se baja una vez, ~1 GB) cortado en
mosaicos fijos de 0,5° que quedan en caché: mover un pico no obliga a bajar nada salvo que caiga en un
mosaico nuevo; Overpass queda de respaldo si osmdata no está. Una semilla a
más de 2,5 km de la costa no entra: `tools/resolve_seeds.py` (Action `resolve.yml`) la busca por
nombre en OpenStreetMap y la mueve al lugar con ese nombre sobre la costa; un pico mar adentro
(un reef) lleva `nosnap` y su `facing=`.

**Las apps:** traen de fábrica las zonas de Uruguay y Santa Catarina (las copia `tools/sync_zones.py`
del repo del reloj) y bajan las demás solas donde estás, o a mano desde el selector de picos:
continente → país → región. Guardan hasta 10 además de las de fábrica y borran la menos usada.

## Mareas — `tide/`

Alturas horarias, mes a mes (`tide/<puerto>/AAAA-MM.json`), en cm sobre el cero de cada puerto y en
su hora local (`utc_offset`), y `harmonics.json` con 30 períodos ajustados para cuando no hay red.
`tide/ports.json` lista todos los puertos; `tide/regions.json`, los de cada región (el reloj usa el
más cercano que cubra el pico; si no hay ninguno, el nivel del mar de Open-Meteo). El último build
está en [`tide/report.md`](tide/report.md): unos 266 puertos para unas 155 regiones.

- **Uruguay:** las Tablas de Mareas del **SOHMA** (Armada Nacional) para Montevideo, Punta del Este y
  La Paloma (`tools/sohma_tide.py`; la Action `update.yml` las busca los días 1 y 15).
- **Santa Catarina:** la tábua de la **DHN** (Marinha do Brasil) para Imbituba, del PDF que publica la
  Epagri/CIRAM (`tools/ciram_tide.py`).
- **El resto** (`tools/tide/build_tides.py`): predicciones oficiales de **NOAA** (EE. UU. y sus
  territorios), **JMA** (Japón), **Marine Institute** (Irlanda) y **LINZ** (Nueva Zelanda); donde no
  hay, las constantes armónicas de **TICON-3** (mareógrafos GESLA-3) con correcciones nodales de pyTMD.
  Las predicciones de TICON-3 se comparan con las de NOAA en las mismas estaciones (el reporte trae la
  tabla: entre 1,6 y 3,7 cm de error RMS).
- **Donde no hay mareógrafo cerca** (Argentina, buena parte de Indonesia, Centroamérica, Maldivas…): el
  modelo global **GOT5.6** de la NASA (R. Ray, GSFC; dominio público), con sus grillas extendidas a la
  costa, predicho con pyTMD en un pico de cada grupo de picos a menos de 50 km (`tools/tide/got.py`).
  Es menos preciso que un mareógrafo cerca, pero mejor que el nivel del mar genérico.

Son predicciones astronómicas: no incluyen el viento ni la presión, que en el Río de la Plata suelen
mover el agua más que la marea.

## Modelos — `validation/` y `models.csv`

Cada región usa un modelo de olas y uno de viento de Open-Meteo. Por defecto: GFS-Wave 0,16° entre
15°S y 52,5°N (0,25° fuera) y GFS. Uruguay, Argentina, Santa Catarina y Rio Grande do Sul quedan fijos
en GFS-Wave 0,25° + GFS, los de Windguru, la referencia de quien surfea ahí (issue #7 del repo del
reloj). En el resto, `validate/` compara cada mes los modelos contra boyas (NDBC, CDIP, IMOS/AODN y el
Marine Institute) y estaciones de viento, y sugiere un cambio cuando otro modelo erra claramente
menos (`validation/models-suggested.csv`, con el porqué); la sugerencia entra a `models.csv` por PR.
La regla y la lectura de `models.csv` están en `tools/lib/models.py`. Detalle en
[`validate/README.md`](validate/README.md) y el último resultado en
[`validation/report.md`](validation/report.md).

## Fuentes y créditos

- Costas y nombres: © colaboradores de **OpenStreetMap** (ODbL), vía osmdata.openstreetmap.de, Overpass y Nominatim; nombres y
  posiciones de **Wikidata** (CC0) y **GeoNames** (CC BY 4.0) para revisar los picos.
- Olas, viento, nivel del mar y puntos de olas: **Open-Meteo** (CC BY 4.0; uso no comercial
  gratis), con los modelos de NOAA, ECMWF, Météo-France, DWD, ECCC, JMA, UK Met Office y BoM.
- Mareas: SOHMA (Uruguay), DHN vía Epagri/CIRAM (Brasil), NOAA CO-OPS (dominio público), JMA
  (Public Data License 1.0), Marine Institute (CC BY 4.0), LINZ (CC BY 4.0, Crown copyright) y
  TICON-3 (CC BY 4.0, Hart-Davis et al. 2022) y el modelo GOT5.6 (NASA GSFC, dominio público), con pyTMD.
- Boyas y estaciones: NOAA NDBC, CDIP (SIO/UCSD), IMOS/AODN y Marine Institute (detalle y licencias
  en `validate/README.md`).
- Tierra y mar para los puntos de olas: `global-land-mask`.

Las apps son gratuitas y no comerciales.
