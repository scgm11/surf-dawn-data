# surf-dawn-data

Datos públicos que consumen la esfera **Surf Dawn** y su app de pronóstico
(repo privado `scgm11/surf-dawn-watchface`) en el Garmin fēnix.

## Marea oficial — `tide/punta-del-este/AAAA-MM.json`

Alturas horarias de la **Tabla de Mareas del SOHMA** (Servicio de Oceanografía,
Hidrografía y Meteorología de la Armada Nacional, Uruguay, Publicación Nº 3)
para el **Puerto de Punta del Este**, en centímetros sobre el cero del puerto,
hora local (UTC−3, sin horario de verano).

```json
{"port":"punta-del-este","month":"2026-10","days":31,"utc_offset":-3,"unit":"cm",
 "h":[99,98,96, ...]}            // 24 valores por día, h[(día-1)*24 + hora]
```

`index.json` lista los meses disponibles. Se sirve por GitHub Pages:
`https://scgm11.github.io/surf-dawn-data/tide/punta-del-este/2026-10.json`

**Se actualiza solo:** la Action `update.yml` corre los días 1 y 15 de cada mes,
busca en el sitio del SOHMA el PDF del año en curso y del siguiente, lo convierte
(`tools/sohma_tide.py`, necesita `pdftotext`) y publica lo que cambió. Si el
SOHMA cambia el nombre del archivo y no se encuentra, la Action falla y GitHub
avisa por mail; el reloj mientras tanto usa armónicos ajustados a la tabla.

Fuente: https://sohma.armada.mil.uy (Información mareográfica). Los datos son
predicciones astronómicas; no incluyen el efecto del viento, que en el Río de la
Plata suele ser mayor que la marea.
