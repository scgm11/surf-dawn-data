# Semillas de los picos

De acá sale todo lo que el reloj sabe de cada pico. `tools/build_zones.py` lee estas tablas,
ajusta cada pico a la costa de OpenStreetMap, calcula hacia dónde mira la playa y el punto de
mar donde pedir las olas, y escribe `spots/` (lo que bajan las apps).

## Tablas

- `continents.csv`: `code,name_es,name_en,name_pt,order`.
- `countries.csv`: `code,continent,name_es,name_en,name_pt`. Código ISO 3166-1 alfa-2 (ojo: Namibia es `NA`;
  se lee con el módulo `csv`, nunca con pandas, que lo toma como vacío).
- `regions.csv`: `code,country,name_es,name_en,name_pt`. El código de región es `<PAÍS>-<ZONA>`, solo
  mayúsculas, dígitos y guiones (`AR-MDP`, `US-HI-OAN`, `BB-ALL`). Una región es de un solo país.
- `spots/<REGIÓN>.csv`: los picos de cada región, de 20 a 60 (un país chico puede tener menos).

## Una fila de `spots/<REGIÓN>.csv`

```
name,lat,lon,type,conf,src,flags,note
PIPELINE,21.6650,-158.0520,R,V,web:hawaii-gis,top,WSL CT
```

| Columna | Qué |
|---|---|
| `name` | Como lo dice la gente del lugar, en MAYÚSCULAS, hasta 18 caracteres. Letras: A–Z, `ÁÉÍÓÚÑÜÃÕÂÊÔÇÀ`, dígitos, espacio, `'`, `.` y `-`. Otras letras se transliteran (È→E, Ō→O, ʻ→'). Único dentro de la región |
| `lat`, `lon` | Grados decimales, 4 decimales, sobre la rompiente o la playa (no tierra adentro). Puede ser aproximado: el script lo lleva a la costa más cercana, hasta 2,5 km |
| `type` | `B` beach break, `P` point break, `R` reef; vacío si no se sabe |
| `conf` | Confianza en la posición: `V` verificada contra una fuente pública, `K` conocimiento general (±0,02°), `L` dudosa |
| `src` | Procedencia: `local`, `osm:<tipo>/<id>`, `wd:Q<id>`, `geonames:<id>`, `gov:<fuente>`, `web:<sitio>` (solo para chequear un dato suelto: nunca se copian listas de Surfline, surf-forecast, wannasurf ni breakfinder) |
| `flags` | Separadas por espacio: `top` pico emblemático (revisión a mano obligatoria); `nosnap` no ajustar a la costa (arrecifes mar adentro, o picos ya validados); `checked` posición revisada a mano aunque el ítem de Wikidata u OSM con su nombre esté lejos (es el pueblo, un hotel u otra ola: `validation/spots.md`); `facing=NNN` orientación puesta a mano (grados hacia donde mira la playa, al mar); `wave=LAT;LON` punto de mar para pedir las olas |
| `note` | Corta: `WSL CT`, `ola grande`, `isla`, por qué la posición es dudosa… |

## Reglas

- Una fila por pico real que la gente surfea; nada de piscinas de olas.
- Arrecifes a más de 2,5 km de la costa (Cloudbreak, Belharra, Mavericks…): `nosnap` y
  `facing=` a mano, con la posición sobre el arrecife.
- La orientación es hacia dónde **mira** la playa (al mar), no de dónde viene el swell.
- Los picos de Uruguay y Santa Catarina (`UY-CAN`, `UY-MAL`, `UY-ROC`, `BR-SC-FLN`, `BR-SC-SUL`)
  están congelados con `nosnap`, `facing=` y `wave=` de la lista validada de 2026-10 (`UY-CAN`: los
  que calculó `build_zones.py` el 2026-10-22): no se recalculan. Una región nueva que se congela va
  también en `FROZEN` de `tools/build_zones.py`, `tools/resolve_seeds.py` y `tools/tide/build_tides.py`.
