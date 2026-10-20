# Validación de los modelos de olas y viento

`validate/run.py` compara los modelos de olas de Open-Meteo con boyas reales, y los de viento con
boyas y estaciones costeras, de los últimos 30 días y deja el resultado en `validation/` (formato en
`docs/formatos.md`, sección *Validación*). Sirve para elegir, región por región, los modelos de olas
y de viento de `models.csv` con datos y no a ojo.

**No toca `models.csv`.** Las sugerencias quedan en `validation/models-suggested.csv` y entran a mano,
por PR, después de mirar más de un mes.

## Cómo corre

Lo corre la Action `.github/workflows/validation.yml`: el día 3 de cada mes, a mano
(*workflow_dispatch*) y con cada push a `validacion-mundo` que toque `validate/`. Publica siempre
`validation/` (también si falla una fuente), con el log en `validation/build.log`.

A mano, con red:

```sh
pip install -r validate/requirements.txt              # pyarrow (boyas de Australia) y global-land-mask
python3 validate/run.py                                # todas las regiones
python3 validate/run.py --regions US-CA-SD AU-NSW-SYD  # algunas
python3 validate/run.py --sources cdip ndbc            # sólo algunas fuentes
python3 -m unittest discover validate                  # pruebas, sin red
```

Las descargas del día quedan en `validate/.cache/<fecha>/` (no se versiona; la Action la guarda con
`actions/cache`), así que repetir la corrida el mismo día no vuelve a bajar nada.

## Qué hace

1. **Regiones**: los picos de `seeds/spots/<REGIÓN>.csv`; el centro y el modelo de hoy salen de la
   misma regla que `tools/build_zones.py` (olas `ncep_gfswave016` entre 15°S y 52,5°N, si no
   `ncep_gfswave025`; viento `gfs_seamless`; o la fila de `models.csv`).
2. **Boyas**: las de cada fuente con al menos 72 horas de altura de ola en la ventana, pasadas a
   registros horarios (el dato más cercano a la hora en punto, ±30 min) con Hs (m), Tp pico (s),
   dirección pico *de donde vienen* (°) y período medio (s). Una boya publicada por dos fuentes (las
   de CDIP tienen también número de NDBC) se usa una sola vez. Para el viento, las estaciones con al
   menos 72 horas de viento (ver *Viento* abajo).
3. **Emparejado**: hasta 3 boyas a menos de 150 km de algún pico de la región, la más cercana
   primero, que miren **al mismo mar** que los picos: desde cada pico y cada boya se tiran 32 rayos
   de 60 km sobre la máscara de tierra de 1 km (`global-land-mask`, la misma de `tools/`) y una
   dirección está abierta si el rayo no toca tierra. La boya tiene que ver abiertas al menos la mitad
   de las direcciones abiertas de los picos (y no mucho menos que la mejor boya de la región). Así
   quedan afuera la boya del otro lado de una isla o de un cabo (Waimea no se valida con Barbers
   Point) y las de bahías cerradas (Port Phillip para la costa de surf de Victoria). Además, una boya
   donde todos los modelos erran la altura por más de 50 % se descarta como no representativa
   (puerto, arrecife protegido). Todo lo descartado queda en `excluded` con el motivo.
4. **Modelos**: series horarias de Open-Meteo Marine en la posición de cada boya
   (`past_days=30`, `forecast_days=1`, `cell_selection=sea`) de `ncep_gfswave016` (sólo 15°S–52,5°N),
   `ncep_gfswave025`, `meteofrance_wave`, `ecmwf_wam` y `dwd_ewam` (sólo Europa, 30–66°N,
   10,5°W–42°E). Diez ubicaciones por pedido, a ritmo, con el costo ponderado como lo cuenta la API
   (por ubicación, máx(1, variables × modelos / 10 × días / 14)) a la vista en el log y en el reporte,
   separado Marine / Forecast (una corrida completa, olas y viento, usa unos pocos miles de las 10.000
   llamadas diarias; repetirla el mismo día sale de la caché).
5. **Métricas** por región y modelo, sobre las mismas horas para todos los modelos: `n`, `hs_bias`
   (relativo), `hs_rmse` (m), `hs_si` (índice de dispersión), `tp_bias` y `tp_mae` (s), `dir_mae` (°), más
   `dir_bias`, `tm_bias` y `tp_type` (ver `docs/formatos.md`).
6. **Mejor modelo**: sólo entre los que dan **período pico** (el reloj muestra el período y puntúa
   las horas con él; los surfistas leen el pico): `ecmwf_wam` (su `wave_peak_period`),
   `ncep_gfswave016` (sólo 15°S–52,5°N) y `ncep_gfswave025`. MFWAM y DWD EWAM sólo dan período medio
   en Open-Meteo: se siguen midiendo para informar (`eligible: false`, columna *No elegible* del
   reporte) y nunca se eligen. El mejor es el de menor `hs_rmse` con |`hs_bias`| ≤ 15 %; si dos están
   a menos de 1 cm, el de menor `tp_mae` (error de período contra el pico de la boya) y después el de
   menor `dir_mae`. **Confianza** `alta` / `media` / `baja` según las horas (≥ 480 / ≥ 240), cuánto
   peor es el modelo de hoy (≥ 10 % / ≥ 5 % de `hs_rmse`), que la mayoría de las boyas coincida y,
   para `alta`, una boya a ≤ 100 km. Sólo se cambia el de hoy con confianza alta o media; las regiones
   sin boyas siguen con la regla por defecto (`ncep_gfswave016` en su dominio, si no `ncep_gfswave025`).
7. **Sin boyas**: la dispersión de Hs entre modelos en el pico más cercano al centro de la región
   donde el modelo de hoy tiene mar (desvío / media, promedio de las horas); más de 0,30 es
   confianza `baja`.
8. **Viento** (ver abajo): bloque `wind` y `best.wind` de cada región.
9. **Salidas**: `validation/<REGIÓN>.json`, `report.md`, `models-suggested.csv` (sólo regiones cuyo
   mejor modelo de olas o de viento, con confianza alta o media, no es el de hoy; la otra columna
   queda como hoy), `buoys.csv` (las boyas de olas usadas), `wind-stations.csv` (las estaciones de
   viento, con la altura del anemómetro) y `stations.csv` (todas las estaciones leídas, con sus horas
   de olas y de viento: para ver por qué falta una).

**Regiones fijas (issue #7)**: Uruguay, Argentina, Santa Catarina y Rio Grande do Sul (`UY-*`,
`AR-*`, `BR-SC-*`, `BR-RS*`) quedan en `ncep_gfswave025` + `gfs_seamless`, como Windguru. Se
validan para informar y nunca se sugiere cambiarlas.

### Viento

- **Observaciones**: NDBC `realtime2` (`WSPD` en m/s a la altura del anemómetro, promedio de 8 min en
  boyas y 2 min en C-MAN; `WDIR` de donde viene): las boyas y además todas las estaciones con datos
  meteorológicos (`met="y"` en `activestations.xml`: C-MAN y estaciones costeras de NOS) cerca de las
  regiones. Marine Institute: las boyas meteorológicas M2–M6 (`IWBNetwork`, `WindSpeed` en la unidad
  del dataset, nudos, pasada a m/s; `WindDirection`); las boyas de olas no miden viento. AODN: si el
  parquet de olas trae columnas de viento (`WSPD`/`WDIR`) se usan; el log lista sus columnas. CDIP no
  mide viento.
- **A 10 m**: la altura del anemómetro sale de la página de cada estación de NDBC
  (`station_page.php`: *Anemometer height … above site elevation* + *Site elevation*); con altura, la
  velocidad se lleva a 10 m con la ley de potencia U₁₀ = U(z)·(10/z)^0,11 (sobre el mar, casi neutral;
  Hsu et al. 1994): ×1,10 a 4,1 m (boya de 3 m de NDBC), ×0,93 a 20 m. Sin altura (Marine Institute, o
  una página sin el dato) se usa como viene y queda `z: null`.
- **Emparejado**: la misma lógica que las olas (hasta 3 estaciones a ≤ 150 km de un pico, la más
  cercana primero, mismo mar), mirando hasta 8 candidatas porque muchas estaciones costeras están
  en puertos. Una estación donde todos los modelos erran la velocidad por más de 35 % se descarta (abrigada).
- **Modelos** (API Forecast, `wind_speed_10m` y `wind_direction_10m`, `wind_speed_unit=ms`):
  `gfs_seamless` (el de hoy) y `ecmwf_ifs` en todas partes; `meteofrance_seamless` (Europa, dominio de
  ARPEGE Europa), `ukmo_seamless` (Islas Británicas, UKV), `cmc_gem_seamless` (Norteamérica, RDPS/HRDPS),
  `jma_seamless` (Japón, Corea y Taiwán, MSM), `bom_access_global` (Australia, Nueva Zelanda y Pacífico
  sudoeste) e `icon_seamless` (Europa, ICON-EU) sólo en su dominio (`WIND_DOMAINS` en `models.py`).
  Cada estación pide los modelos de las regiones que valida. Boyas: `cell_selection=sea`; estaciones
  en tierra: `nearest`. Antes se prueba cada modelo con un pedido de una llamada: si la API no lo
  conoce queda afuera (y lo dice el reporte) en vez de fallar punto por punto.
- **Métricas** (mismas horas para todos los modelos): `spd_bias` (relativo) y `spd_bias_ms` (m/s),
  `spd_rmse` (m/s), `dir_mae`/`dir_bias` (°) con viento observado ≥ 3 m/s.
- **Mejor**: el de menor `spd_rmse` con |`spd_bias`| ≤ 20 %; confianza con las mismas reglas que las
  olas (sobre `spd_rmse`). Se cambia `gfs_seamless` sólo con confianza alta o media; las regiones fijas
  siguen en `gfs_seamless` y las que no tienen estaciones también.
- **Controles**: el reporte trae, por fuente y modelo, la velocidad media observada, el sesgo y el rmse
  en m/s y el sesgo circular de dirección: un sesgo de velocidad de ×1,9 o ×0,5 delataría nudos por
  m/s, uno de dirección cerca de ±180° una convención "hacia".

### Ojo con los períodos

En Open-Meteo sólo `ecmwf_wam` da período pico (`wave_peak_period`, y su `tp_bias`/`tp_mae` usan
siempre ése contra el período pico de la boya); GFS-Wave, MFWAM y EWAM lo devuelven vacío y para ellos
`tp_bias` usa su `wave_period`, que no es lo mismo en todos (por eso MFWAM y EWAM no se eligen):

- **GFS-Wave** (`tp_type: "primary"`): es el período del sistema de olas principal (salta de golpe
  cuando entra un swell nuevo). Contra las boyas queda a ~0,5 s de su período pico y 4–5 s por encima
  de su período medio: se comporta como un pico.
- **MFWAM y EWAM** (`tp_type: "mean"`): es un período medio, así que su `tp_bias` sale negativo por
  construcción (−1 a −2 s) y no habla de la calidad del modelo.

`tm_bias` compara el `wave_period` del modelo con el período medio de la boya, pero cada fuente
publica un momento distinto (NDBC `APD` y CDIP `Ta` ≈ Tm01/Tm02, AODN `WPFM`, Marine Institute
`EnergyPeriod` = Tm−1,0). El reporte trae una tabla por fuente con estos promedios para controlar las
convenciones (también la de dirección: un sesgo cerca de ±180° delataría una boya en "hacia").

## Fuentes, licencias y créditos

| Fuente | Qué se usa | Licencia / crédito |
|---|---|---|
| **NOAA NDBC** | `activestations.xml`, `data/realtime2/<ID>.txt` (WVHT, DPD, APD, MWD; WSPD, WDIR; 45 días) y `station_page.php` (altura del anemómetro). Boyas, C-MAN y estaciones costeras de NOS; incluye socios internacionales (PNBOIA de Brasil, Canadá, etc.) | Dominio público (NOAA) |
| **CDIP**, Scripps Institution of Oceanography (UCSD) | ERDDAP `wave_agg` (waveHs, waveTp, waveTa, waveDp; flag primario 1). Boyas someras de California, Hawái/PacIOOS, costa este | Uso libre; crédito: *Coastal Data Information Program (CDIP), SIO/UCSD*, financiado por USACE y el estado de California |
| **AODN / IMOS** | Parquet `s3://aodn-cloud-optimised/wave_buoy_realtime_nonqc.parquet` (WSSH, WPPE, WPDI, WPFM), acceso anónimo | CC BY 4.0; crédito: *IMOS / Australian Ocean Data Network* y los operadores de cada boya (NSW DCCEEW, Qld DESI, WA DoT, Deakin Univ., etc.) |
| **Marine Institute** (Irlanda) | ERDDAP `IWaveBNetwork30Min` (SignificantWaveHeight en **cm**, PeakPeriod, PeakDirection *hacia donde van*, EnergyPeriod) e `IWBNetwork` (boyas meteorológicas M2–M6, también WindSpeed y WindDirection). Las columnas y unidades se eligen por nombre estándar CF | CC BY 4.0; crédito: *Marine Institute, Irish Wave Buoy Network / Irish Marine Data Buoy Observation Network* |
| **Open-Meteo** Marine y Forecast | Series horarias de los modelos de olas y de viento | CC BY 4.0, uso no comercial gratis (10.000 llamadas/día); crédito a Open-Meteo y a NOAA, Météo-France, ECMWF, DWD, UK Met Office, ECCC, JMA y BoM |

| **Copernicus Marine In Situ** (con cuenta) | `INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030`, archivos diarios `latest` de los últimos 30 días (`validate/cmems.py`): el índice `index_latest.txt` elige las boyas fondeadas con altura de ola (VHM0, VAVH o VGHS) cerca de las regiones que no da otra fuente, se bajan con el Copernicus Marine Toolbox y se leen con h5netcdf (flags QC 1 y 2; los archivos con dos mensajes intercalados se juntan). Cubre lo que falta: Francia (las boyas CANDHIS del Cerema), España (Puertos del Estado), Portugal, Reino Unido (Cefas), Marruecos, Canarias y las boyas del GTS | Licencia de Copernicus Marine (libre, con crédito: *E.U. Copernicus Marine Service Information*) |

**Copernicus Marine necesita una cuenta gratuita** (marine.copernicus.eu): con los secretos del
repositorio `COPERNICUSMARINE_SERVICE_USERNAME` y `COPERNICUSMARINE_SERVICE_PASSWORD` la Action instala
el Toolbox y la fuente entra sola; sin ellos el reporte la lista como "sin credenciales" y sigue con
las demás. Con Copernicus, CANDHIS y Puertos del Estado ya no hacen falta por separado (sus boyas
llegan por ahí). Quedan sin usar el Channel Coastal Observatory (Inglaterra, pide registro y sus
boyas están en Copernicus sólo en parte) y el IH (Portugal).
