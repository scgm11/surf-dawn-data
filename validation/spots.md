# Picos: controles por pico

Generado 2026-11-19 22:41 UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). 214 regiones, 2518 picos.

- **Orientación (§5.2):** olas de los últimos 14 días y los próximos 2 en el punto de olas de cada pico (el modelo de su zona). Se marca un pico al que las olas de al menos 0.3 m casi nunca le llegan a menos de 55° de hacia donde mira, o de su ventana de swell si la tiene (menos del 5 % de las horas) mientras a su zona sí (al menos 25 %).
- **Zona entera:** en una zona donde la mayoría tampoco las recibe de frente (menos del 25 %) los vecinos no dicen nada: ahí se marca el pico con mar (olas de al menos 0.3 m en el 25 % de las horas o más) que casi nunca las recibe de frente.
- **Temporada:** los marcados por la orientación se miran de nuevo con 92 días de olas; 89 dejaron de estarlo (en dos semanas no les tocaba su ventana de swell).
- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media de su zona.
- **Celdas:** la celda de la que contesta la API a cada pico, abajo las que no son buenas.
- **Emblemáticos (§5.8, de la corrida anterior):** la posición contra fuentes públicas (el ítem más cercano con su nombre en Wikidata o GeoNames, hasta 6 km; si no, OpenStreetMap; si no, el ítem de otro nombre del que se tomó a mano la posición, en el `src` de la semilla): 319 bien (a menos de 1.5 km; 12 de ellos por la fuente de su semilla), 0 lejos, 21 lejos pero revisados a mano (el ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), 52 sin fuente (revisar a mano; `validation/lookup.md` tiene lo que hay con su nombre alrededor), 0 sin respuesta.
- Open-Meteo: 46 pedidos, ~5045 llamadas de las 10.000 diarias gratuitas.

## Orientación probablemente del lado equivocado (1)

Mira a más de 135° de sus vecinos (a 30 km) y de las olas, y dada vuelta coincide con ellos: casi seguro se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla.

| Región | Pico | Mira a | Vecinos | Olas desde |
|---|---|---|---|---|
| CA-BC-VI | SCHOONER COVE | 44° | 204° | 233° |

## Zonas enteras que casi nunca reciben las olas de frente (1)

Zonas con 3 picos o más que, en 92 días, casi nunca recibieron las olas de frente aunque había mar, y a las que la comparación con los vecinos no ve porque están todos igual. O la orientación de toda la costa se calculó del lado equivocado, o son reefs y puntas a los que el swell entra dando la vuelta: ahí la orientación de la costa está bien para el viento y lo que falta es la ventana de swell del pico.

| Región | Marcados | Puntas y reefs | Miran a | Olas desde | Picos |
|---|---|---|---|---|---|
| ZA-WC-WCO | 4 de 6 | 0 | 325° | 231° | MELKBOS, LAMBERTS BAY, JACOBSBAAI, YZERFONTEIN |

## Celdas de olas para mirar (51)

La celda desde la que contesta la API cuando se le pregunta como las apps (sin `cell_selection`). Se marca el punto de olas que la API corre o que queda detrás de la playa (a más de 75° de hacia donde mira, o de su ventana de swell), el pico que la API corre a una celda detrás de la playa o a más de 35 km, y el que contesta desde su propia celda cuando esa queda detrás de la playa y tiene menos del 70 % de las olas de la de enfrente (una laguna, una bahía detrás de una isla de barrera o de una punta). A veces es con razón: su celda es tierra y la siguiente queda de costado. Se corrige con `wave=` en la semilla, después de mirar la celda; «Enfrente» es la celda que se propone (a menos de 75° y de 25 km, con olas, y desde la que contesta la API), con la altura media de las dos.

| Región | Pico | Punto de olas | Celda | Por qué | Enfrente |
|---|---|---|---|---|---|
| AU-NSW-MN | WOOLGOOLGA | — | -30.00, 153.25 (1.1 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 85° de hacia donde mira, 13 km): 1.1 m de media contra 1.6 m en la de enfrente, a 31 km (ninguna a menos de 25 km) | — |
| AU-NSW-SC | PAMBULA BEACH | — | -37.00, 150.00 (0.9 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 88° de hacia donde mira, 9 km): 0.9 m de media contra 1.5 m en la de enfrente, a 29 km (ninguna a menos de 25 km) | — |
| AU-NSW-SC | SURF BEACH | — | -36.00, 150.25 (1.3 m) | la API lo contesta desde una celda detrás de la playa (a 89° de hacia donde mira, 27 km) | — |
| AU-QLD-GC | CYLINDER BEACH | — | -27.50, 153.50 (1.0 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 132° de hacia donde mira, 9 km): 1.0 m de media contra 1.6 m en la de enfrente, a 29 km (ninguna a menos de 25 km) | — |
| AU-QLD-GC | HOME BEACH | — | -27.50, 153.50 (1.0 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 170° de hacia donde mira, 9 km): 1.0 m de media contra 1.6 m en la de enfrente, a 30 km (ninguna a menos de 25 km) | — |
| AU-TAS | CLIFTON BEACH | — | -43.00, 147.50 (0.3 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 129° de hacia donde mira, 2 km): 0.3 m de media contra 0.9 m en la de enfrente, a 29 km (ninguna a menos de 25 km) | — |
| AU-VIC-SC | POINT LONSDALE | — | -38.25, 144.75 (0.7 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 135° de hacia donde mira, 13 km): 0.7 m de media contra 1.4 m en la de enfrente, a 25 km (ninguna a menos de 25 km) | — |
| AU-WA-MR | THREE BEARS | — | -33.50, 115.00 (1.5 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 104° de hacia donde mira, 9 km): 1.5 m de media contra 2.1 m en la de enfrente, a 26 km (ninguna a menos de 25 km) | — |
| AU-WA-MR | WINDMILLS | — | -33.50, 115.00 (1.5 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 91° de hacia donde mira, 5 km): 1.5 m de media contra 2.1 m en la de enfrente | -33.5000;114.7500 (2.1 m) |
| BR-NE-CE | LAGOINHA | -3.33, -39.00 | -3.33, -39.00 (1.0 m) | punto de olas detrás de la playa (a 88° de hacia donde mira, 15 km) | -3.1667;-39.1667 (1.1 m) |
| BR-NE-PE | PORTO DE GALINHAS | — | -8.67, -35.00 (1.1 m) | la API lo contesta desde una celda detrás de la playa (a 92° de hacia donde mira, 18 km) | -8.5000;-34.8333 (1.1 m) |
| BR-NE-RN | PRAIA DO MEIO | — | -5.83, -35.17 (0.8 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 82° de hacia donde mira, 7 km): 0.8 m de media contra 1.1 m en la de enfrente | -5.8333;-35.0000 (1.1 m) |
| BR-SP | ILHA COMPRIDA | — | -24.75, -47.50 (0.7 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 144° de hacia donde mira, 7 km): 0.7 m de media contra 1.1 m en la de enfrente, a 63 km (ninguna a menos de 25 km) | — |
| CA-BC-VI | SCHOONER COVE | — | 49.03, -125.72 (3.2 m) | la API lo contesta desde una celda detrás de la playa (a 105° de hacia donde mira, 8 km) | — |
| CL-CEN | PAPUDO | — | -32.50, -71.50 (1.4 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 101° de hacia donde mira, 5 km): 1.4 m de media contra 2.0 m en la de enfrente, a 40 km (ninguna a menos de 25 km) | — |
| CR-OSA | MATAPALO | 8.33, -83.33 | 8.33, -83.33 (1.1 m) | punto de olas detrás de la playa (a 94° de hacia donde mira, 7 km) | 8.1667;-83.3333 (1.2 m) |
| ES-GAL | ORZAN | — | 43.50, -8.33 (1.9 m) | la API lo contesta desde una celda detrás de la playa (a 79° de hacia donde mira, 15 km) | 43.5000;-8.5000 (2.0 m) |
| FR-PBA | LA BARRE | — | 43.67, -1.50 (1.5 m) | la API lo contesta desde una celda detrás de la playa (a 79° de hacia donde mira, 16 km) | 43.5000;-1.6667 (1.4 m) |
| FR-VEN | PONTAILLAC | — | 45.67, -1.17 (0.3 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 79° de hacia donde mira, 10 km): 0.4 m de media contra 1.7 m en la de enfrente | 45.6667;-1.3333 (1.7 m) |
| GB-CON | TREVAUNANCE COVE | — | 50.33, -5.33 (1.5 m) | la API lo contesta desde una celda detrás de la playa (a 76° de hacia donde mira, 9 km) | 50.5000;-5.1667 (1.6 m) |
| GB-NIR | WEST STRAND | — | 55.22, -6.67 (0.8 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 102° de hacia donde mira, 2 km): 0.8 m de media contra 1.4 m en la de enfrente, a 45 km (ninguna a menos de 25 km) | — |
| GB-WAL | RHOSNEIGR | — | 53.25, -4.75 (0.9 m) | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 16 km) | — |
| ID-JAV-W | CIMAJA | — | -7.00, 106.33 (1.0 m) | la API lo contesta desde una celda detrás de la playa (a 83° de hacia donde mira, 23 km) | -7.1667;106.3333 (1.2 m) |
| ID-JAV-W | KARANG HAWU | — | -7.00, 106.33 (1.0 m) | la API lo contesta desde una celda detrás de la playa (a 86° de hacia donde mira, 23 km) | -7.1667;106.3333 (1.2 m) |
| ID-MEN | PITSTOPS | — | -1.83, 99.33 (0.8 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 161° de hacia donde mira, 9 km): 0.8 m de media contra 1.3 m en la de enfrente, a 34 km (ninguna a menos de 25 km) | — |
| ID-ROT | SQUEALERS | — | -11.00, 122.83 (0.8 m) | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 16 km) | -11.0000;122.6667 (0.8 m) |
| ID-ROT | SUCKY MAMAS | — | -11.00, 122.83 (0.8 m) | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 18 km) | -11.0000;122.6667 (0.8 m) |
| IE-NW | TULLAN STRAND | — | 54.50, -8.50 (0.5 m) | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 13 km) | — |
| LK-E | ARUGAM BAY | — | 6.83, 82.00 (1.2 m) | la API lo contesta desde una celda detrás de la playa (a 92° de hacia donde mira, 18 km) | — |
| LK-E | BABY POINT | — | 6.83, 82.00 (1.2 m) | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 18 km) | — |
| LK-E | CROCODILE ROCK | — | 6.67, 81.83 (1.2 m) | la API lo contesta desde una celda detrás de la playa (a 100° de hacia donde mira, 16 km) | 6.8333;82.0000 (1.2 m) |
| MX-CAR | PLAYA DEL CARMEN | — | 20.67, -87.00 (0.6 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 84° de hacia donde mira, 8 km): 0.6 m de media contra 0.9 m en la de enfrente | 20.6667;-86.8333 (0.9 m) |
| MX-OAX | SAN AGUSTINILLO | — | 15.67, -96.67 (1.1 m) | la API lo contesta desde una celda detrás de la playa (a 82° de hacia donde mira, 13 km) | 15.5000;-96.5000 (1.2 m) |
| MX-OAX | ZIPOLITE | — | 15.67, -96.67 (1.1 m) | la API lo contesta desde una celda detrás de la playa (a 86° de hacia donde mira, 16 km) | 15.5000;-96.5000 (1.2 m) |
| NZ-WEL | MAKARA BEACH | — | -41.25, 174.50 (1.3 m) | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 18 km) | -41.0000;174.7500 (1.1 m) |
| PT-ALG | AMOREIRA | — | 37.50, -8.83 (2.1 m) | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 17 km) | 37.3333;-9.0000 (2.4 m) |
| US-CA-LA | POINT DUME | — | 33.99, -118.76 (1.0 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 76° de hacia donde mira, 4 km): 1.0 m de media contra 1.4 m en la de enfrente | 33.9192;-118.8404 (1.4 m) |
| US-CA-NOR | MANCHESTER | — | 38.91, -123.73 (3.5 m) | la API lo contesta desde una celda detrás de la playa (a 108° de hacia donde mira, 7 km) | 38.9807;-123.7808 (3.6 m) |
| US-CA-NOR | AGATE BEACH | — | 41.09, -124.20 (3.6 m) | la API lo contesta desde una celda detrás de la playa (a 147° de hacia donde mira, 7 km) | 41.1599;-124.2489 (3.8 m) |
| US-CA-SF | FORT POINT | — | 37.86, -122.45 (0.3 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 113° de hacia donde mira, 5 km): 0.3 m de media contra 2.9 m en la de enfrente | 37.7856;-122.6506 (2.9 m) |
| US-CA-SF | PACIFICA PIER | — | 37.57, -122.52 (3.0 m) | la API lo contesta desde una celda detrás de la playa (a 75° de hacia donde mira, 7 km) | 37.6450;-122.5634 (3.0 m) |
| US-CA-SF | MIRADA SURF | — | 37.57, -122.52 (2.9 m) | la API lo contesta desde una celda detrás de la playa (a 127° de hacia donde mira, 8 km) | 37.5044;-122.5965 (3.4 m) |
| US-CA-SF | MUIR BEACH | — | 37.79, -122.53 (2.4 m) | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 9 km) | 37.8559;-122.6944 (2.7 m) |
| US-NE | WALLIS SANDS | — | 43.06, -70.71 (0.4 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 102° de hacia donde mira, 4 km): 0.4 m de media contra 0.6 m en la de enfrente | 43.0580;-70.5804 (0.6 m) |
| US-NE | NARRAGANSETT | — | 41.37, -71.51 (0.6 m) | la API lo contesta desde una celda detrás de la playa (a 121° de hacia donde mira, 8 km) | 41.4411;-71.3525 (0.7 m) |
| US-NE | ROCKAWAY | — | 40.60, -73.83 (0.4 m) | la API lo contesta desde su celda, que queda detrás de la playa (a 148° de hacia donde mira, 2 km): 0.4 m de media contra 0.6 m en la de enfrente | 40.5272;-73.8559 (0.7 m) |
| US-PNW | GRAYLAND | — | 46.85, -124.08 (1.7 m) | la API lo contesta desde una celda detrás de la playa (a 106° de hacia donde mira, 7 km) | 46.7838;-124.1680 (1.7 m) |
| US-PNW | OTTER ROCK | — | 44.82, -124.08 (3.5 m) | la API lo contesta desde una celda detrás de la playa (a 114° de hacia donde mira, 8 km) | 44.7452;-124.1667 (3.7 m) |
| US-PNW | BEVERLY BEACH | — | 44.82, -124.08 (3.5 m) | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 9 km) | 44.7452;-124.1667 (3.7 m) |
| ZA-EC-PE | CANNON ROCKS | — | -33.75, 26.75 (2.0 m) | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 20 km) | — |
| ZA-KZN-S | SCOTTBURGH | — | -30.50, 30.75 (2.0 m) | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 24 km) | -30.2500;31.0000 (2.0 m) |

## Picos marcados (111)

Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y el semáforo del swell es conservador ahí); se revisan a mano.

| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |
|---|---|---|---|---|---|---|
| AU-QLD-SC | DOUBLE ISLAND PT | sí | 17° | 121° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 90 %) y en 92 días 4 % |
| AU-SA | CHINAMANS |  | 325° | 232° | 250° | las olas casi nunca le entran de frente (2 % de las horas; la zona 71 %) y en 92 días 1 % |
| AU-TAS | MARION BAY |  | 269° | 126° | 146° | las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 2 % |
| AU-TAS | MARRAWAH |  | 314° | 227° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 1 % |
| AU-VIC-PI | FOREST CAVES |  | 127° | 221° | 207° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-VIC-SC | TORQUAY BACK BEACH |  | 133° | 218° | 152° | las olas casi nunca le entran de frente (2 % de las horas; la zona 96 %) y en 92 días 2 % |
| AU-VIC-SC | JAN JUC |  | 118° | 218° | 153° | las olas casi nunca le entran de frente (2 % de las horas; la zona 96 %) y en 92 días 2 % |
| AU-VIC-SC | POINT ADDIS |  | 71° | 218° | 148° | las olas casi nunca le entran de frente (2 % de las horas; la zona 96 %) y en 92 días 1 % |
| AU-VIC-W | WYE RIVER |  | 110° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 1 % |
| AU-VIC-W | KENNETT RIVER |  | 82° | 222° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 96 %) y en 92 días 1 % |
| AU-VIC-W | PORT FAIRY EAST |  | 140° | 216° | 229° | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 0 % |
| AU-WA-MR | HUZZAWOUIE |  | 7° | 236° | 270° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| AU-WA-MR | SOUTH POINT |  | 331° | 236° | 271° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 2 % |
| AU-WA-MR | PEA BREAK |  | 313° | 247° | 281° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 4 % |
| AU-WA-MR | INJIDUP POINT |  | 350° | 247° | 280° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| AU-WA-MR | SMITHS |  | 318° | 247° | 281° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 3 % |
| BB-ALL | BRANDONS |  | 277° | 31° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| BR-NE-PE | CALHETAS |  | 19° | 103° | 96° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| BR-NE-PE | GAIBU |  | 37° | 103° | 95° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 3 % |
| BR-RJL | PRAIA GRANDE |  | 272° | 154° | 148° | las olas casi nunca le entran de frente (1 % de las horas; la zona 71 %) y en 92 días 1 % |
| BR-SP | FAZENDA |  | 260° | 137° | 141° | las olas casi nunca le entran de frente (1 % de las horas; la zona 95 %) y en 92 días 0 % |
| BR-SP | MARANDUBA |  | 234° | 131° | 156° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| BR-SP | CAMBURI |  | 261° | 140° | 188° | las olas casi nunca le entran de frente (1 % de las horas; la zona 95 %) y en 92 días 1 % |
| BR-SP | ILHA COMPRIDA |  | 269° | 132° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| CA-BC-VI | SCHOONER COVE |  | 44° | 233° | 204° | las olas casi nunca le entran de frente (0 % de las horas; la zona 77 %) y en 92 días 0 % |
| CA-BC-VI | WYA POINT |  | 90° | 236° | 210° | las olas casi nunca le entran de frente (0 % de las horas; la zona 77 %) y en 92 días 0 % |
| CA-BC-VI | CHINA BEACH |  | 202° | 272° | 213° | las olas casi nunca le entran de frente (2 % de las horas; la zona 77 %) y en 92 días 1 % |
| CL-CEN | PAPUDO |  | 19° | 243° | 283° | las olas casi nunca le entran de frente (0 % de las horas; la zona 52 %) y en 92 días 0 % |
| CL-CEN | ALGARROBO |  | 339° | 242° | 293° | las olas casi nunca le entran de frente (4 % de las horas; la zona 52 %) y en 92 días 1 % |
| CL-MAU | CURANIPE |  | 346° | 254° | 309° | las olas casi nunca le entran de frente (4 % de las horas; la zona 80 %) y en 92 días 5 % |
| CL-MAU | BUCHUPUREO | sí | 350° | 246° | 310° | las olas casi nunca le entran de frente (4 % de las horas; la zona 80 %) y en 92 días 4 % |
| CL-NOR | LA ISLA |  | 309° | 218° | 273° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CO-PAC | HUINA |  | 312° | 231° | 236° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-CAR | SALSA BRAVA | sí | 344° | 58° | 16° | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 4 % |
| CR-GUA | TAMARINDO | sí | 312° | 229° | 251° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-OSA | RIO CLARO |  | 308° | 216° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 39 %) y en 92 días 0 % |
| CR-OSA | MATAPALO |  | 131° | 214° | 284° | las olas casi nunca le entran de frente (0 % de las horas; la zona 39 %) y en 92 días 0 % |
| CV-ALL | SANTA MARIA |  | 193° | 359° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| ES-AND | REGLA |  | 7° | 247° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| ES-AND | BOLONIA |  | 191° | 265° | 226° | las olas casi nunca le entran de frente (3 % de las horas; la zona 91 %) y en 92 días 2 % |
| ES-AST | XAGO |  | 82° | 326° | 353° | las olas casi nunca le entran de frente (1 % de las horas; la zona 91 %) y en 92 días 1 % |
| ES-CN-E | FLAG BEACH |  | 72° | 313° | 272° | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 0 % |
| ES-CN-W | PLAYA DEL HOMBRE |  | 89° | 343° | 330° | las olas casi nunca le entran de frente (0 % de las horas; la zona 72 %) y en 92 días 0 % |
| ES-PV | LAGA |  | 73° | 317° | 351° | las olas casi nunca le entran de frente (1 % de las horas; la zona 76 %) y en 92 días 1 % |
| FJ-MAM | RESTAURANTS | sí | 354° | 236° | 252° | las olas casi nunca le entran de frente (0 % de las horas; la zona 71 %) y en 92 días 0 % |
| FR-BRE | LE POULDU |  | 132° | 239° | 221° | las olas casi nunca le entran de frente (3 % de las horas; la zona 94 %) y en 92 días 1 % |
| FR-VEN | LA TRANCHE |  | 151° | 255° | 230° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 0 % |
| GB-DEV | THURLESTONE |  | 326° | 226° | 217° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 2 % |
| GB-SCO | STRATHY |  | 77° | 335° | 351° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 3 % |
| GH-ALL | DIXCOVE |  | 107° | 184° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| GP-ALL | TARARE |  | 180° | 86° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (1 %) y en 92 días 0 % |
| GP-ALL | PORT LOUIS |  | 270° | 44° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (1 %) y en 92 días 0 % |
| ID-BAL-BUK | DREAMLAND |  | 286° | 206° | 315° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | PURNAMA |  | 133° | 200° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 42 %) y en 92 días 0 % |
| ID-BAL-E | SABA |  | 130° | 200° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 42 %) y en 92 días 0 % |
| ID-BAL-E | LEBIH |  | 132° | 200° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 42 %) y en 92 días 0 % |
| ID-BAL-E | SERANGAN |  | 145° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 42 %) y en 92 días 0 % |
| ID-JAV-W | PANGANDARAN |  | 280° | 203° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 0 % |
| ID-JAV-W | MADASARI |  | 119° | 198° | 260° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 0 % |
| ID-LOM | SELONG BELANAK |  | 296° | 210° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | MAWUN |  | 133° | 210° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | KUTA LOMBOK |  | 140° | 210° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-MEN | PITSTOPS |  | 290° | 194° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-ROT | T-LAND | sí | 290° | 225° | 246° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| KR-ALL | SONGJEONG |  | 142° | 36° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 41 %) y en 92 días 4 % |
| LR-ALL | COTTON TREE |  | 307° | 200° | 290° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | IMSOUANE | sí | 193° | 293° | 209° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-NAY | EL ANCLOTE | sí | 149° | 236° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-OAX | LA PUNTA | sí | 301° | 209° | 210° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 4 % |
| MX-OAX | MAZUNTE |  | 123° | 210° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-OAX | BARRA DE LA CRUZ | sí | 122° | 201° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| MX-PAC | MIRAMAR |  | 314° | 210° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| MZ-INH | TOFO |  | 15° | 143° | 79° | las olas casi nunca le entran de frente (0 % de las horas; la zona 71 %) y en 92 días 1 % |
| NA-ERO | SKELETON BAY | sí | 321° | 210° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| NZ-BOP | ONEMANA |  | 164° | 49° | 80° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| NZ-NTL | MATAURI BAY |  | 224° | 46° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 1 % |
| NZ-OTA | COLAC BAY |  | 159° | 253° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| NZ-WC | TAURANGA BAY |  | 34° | 277° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 64 %) y en 92 días 0 % |
| PR-NW | GAS CHAMBERS |  | 234° | 17° | 286° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| PR-NW | CRASH BOAT |  | 239° | 17° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| PR-NW | CÓRCEGA |  | 246° | 18° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| PT-AZO | ALMOXARIFE |  | 68° | 284° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| PT-MAD | MACHICO |  | 122° | 306° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 80 %) y en 92 días 0 % |
| RE-ALL | BOUCAN CANOT |  | 312° | 209° | 265° | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| RE-ALL | BARACHOIS |  | 325° | 107° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| US-CA-CEN | PIRATE'S COVE |  | 175° | 282° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| US-CA-NOR | NORTH JETTY |  | 19° | 282° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 3 % |
| US-CA-SB | SANDSPIT |  | 112° | 226° | 193° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (5 %) y en 92 días 0 % |
| US-CA-SC | MITCHELL'S COVE |  | 161° | 269° | 198° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 3 % |
| US-CA-SC | 38TH AVE |  | 144° | 269° | 196° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 0 % |
| US-CA-SC | SEWER PEAK |  | 158° | 269° | 195° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 3 % |
| US-CA-SC | CAPITOLA |  | 157° | 269° | 195° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 3 % |
| US-HI-BIG | HONOLI'I | sí | 88° | 60° | — | 2.4 m de media, más del doble de la zona (0.9 m) |
| US-HI-BIG | RICHARDSONS |  | 35° | 60° | — | 2.4 m de media, más del doble de la zona (0.9 m) |
| US-HI-BIG | POHOIKI |  | 126° | 85° | — | 2.4 m de media, más del doble de la zona (0.9 m) |
| US-HI-BIG | LAUPAHOEHOE |  | 58° | 46° | — | 2.3 m de media, más del doble de la zona (0.9 m) |
| US-HI-BIG | WAIPIO |  | 351° | 45° | — | 2.3 m de media, más del doble de la zona (0.9 m) |
| US-HI-BIG | POLOLU |  | 57° | 56° | 307° | 2.4 m de media, más del doble de la zona (0.9 m) |
| US-HI-MAU | MALA RAMP |  | 262° | 37° | 253° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (20 %) y en 92 días 1 % |
| US-NE | ATLANTIC CITY |  | 149° | 274° | 134° | las olas casi nunca le entran de frente (0 % de las horas; la zona 46 %) y en 92 días 3 % |
| US-PNW | PORT ORFORD |  | 162° | 268° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-SE | OCRACOKE |  | 262° | 126° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 0 % |
| ZA-EC-PE | HOBIE BEACH |  | 31° | 180° | 132° | las olas casi nunca le entran de frente (0 % de las horas; la zona 32 %) y en 92 días 0 % |
| ZA-WC-CPT | LLANDUDNO | sí | 311° | 228° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 85 %) y en 92 días 0 % |
| ZA-WC-CPT | LONG BEACH | sí | 344° | 226° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 85 %) y en 92 días 0 % |
| ZA-WC-CPT | KOGEL BAY |  | 332° | 207° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 85 %) y en 92 días 0 % |
| ZA-WC-GR | SANTOS |  | 50° | 195° | 147° | las olas casi nunca le entran de frente (0 % de las horas; la zona 92 %) y en 92 días 0 % |
| ZA-WC-WCO | MELKBOS |  | 310° | 231° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ZA-WC-WCO | LAMBERTS BAY |  | 320° | 235° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | JACOBSBAAI |  | 318° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | YZERFONTEIN |  | 351° | 231° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |

## Emblemáticos lejos de su ítem en Wikidata, GeoNames u OpenStreetMap

Ninguno.

## Emblemáticos sin fuente en Wikidata, GeoNames ni OpenStreetMap (revisar a mano)

AU-NSW-SYD/OURS, AU-VIC-SC/WINKIPOP, AU-WA-MR/MAIN BREAK, AU-WA-MR/NORTH POINT, CL-NOR/EL GRINGO, CR-GUA/WITCH'S ROCK, CR-OSA/PAVONES, ES-CN-E/EL QUEMAO, ES-CN-W/EL FRONTON, ES-CN-W/LA IZQUIERDA, FJ-MAM/CLOUDBREAK, FJ-MAM/RESTAURANTS, FJ-MAM/SWIMMING POOLS, ID-BAL-E/SHIPWRECKS, ID-JAV-E/MONEY TREES, ID-MEN/MACARONIS, ID-MEN/KANDUI LEFT, ID-MEN/RIFLES, ID-ROT/T-LAND, ID-SBW/SUPERSUCK, IE-NW/EASKEY, IE-SW/AILEEN'S, LK-E/WHISKEY POINT, MA-N/SAFI LE JARDIN, MV-NMA/PASTA POINT, MV-NMA/SULTANS, MV-NMA/HONKY'S, MV-NMA/COKES, MV-NMA/CHICKENS, MV-NMA/JAILBREAKS, MV-SOU/TIGER STRIPES, MV-SOU/BEACONS, MX-BCS/ZIPPERS, NA-ERO/SKELETON BAY, NZ-GIS/CENTRES, NZ-GIS/WHALES, NZ-GIS/THE ISLAND, NZ-KAI/MEATWORKS, NZ-NTL/SUPER TUBES, NZ-NTL/MUKIES 2, NZ-NTL/MUKIES 1, NZ-NTL/PEAKS, NZ-RAG/INDICATORS, PH-SIA/JACKING HORSE, SV-ORI/LAS FLORES, US-HI-BIG/BANYANS, US-HI-KAU/PK'S, US-HI-OAN/BACKDOOR, US-NE/RUGGLES, ZA-EC-JB/BRUCE'S BEAUTIES, ZA-WC-CPT/DUNGEONS, ZA-WC-CPT/SUNSET REEF

## Zonas

| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |
|---|---|---|---|
| AR-BAN | ncep_gfswave025 | 0.9 m | 91 % |
| AR-MDP | ncep_gfswave025 | 1.1 m | 76 % |
| AR-SUR | ncep_gfswave025 | 0.9 m | 66 % |
| AU-NSW-MN | ncep_gfswave025 | 1.5 m | 40 % |
| AU-NSW-NC | ncep_gfswave025 | 1.5 m | 80 % |
| AU-NSW-NR | ncep_gfswave025 | 1.6 m | 37 % |
| AU-NSW-SC | ncep_gfswave025 | 1.6 m | 49 % |
| AU-NSW-SYD | ncep_gfswave025 | 1.7 m | 54 % |
| AU-QLD-GC | ncep_gfswave025 | 0.9 m | 81 % |
| AU-QLD-SC | ncep_gfswave025 | 1.0 m | 90 % |
| AU-SA-EYR | ncep_gfswave025 | 1.2 m | 100 % |
| AU-SA | ecmwf_wam | 1.3 m | 71 % |
| AU-TAS | ncep_gfswave025 | 1.3 m | 36 % |
| AU-VIC-PI | ncep_gfswave025 | 1.3 m | 100 % |
| AU-VIC-SC | ncep_gfswave025 | 1.2 m | 96 % |
| AU-VIC-W | ncep_gfswave025 | 2.2 m | 96 % |
| AU-WA-GAS | ncep_gfswave025 | 1.2 m | 100 % |
| AU-WA-MR | ncep_gfswave025 | 2.1 m | 97 % |
| AU-WA-NW | ncep_gfswave025 | 1.7 m | 100 % |
| AU-WA-PER | ncep_gfswave025 | 1.5 m | 100 % |
| BB-ALL | ncep_gfswave016 | 1.2 m | 35 % |
| BR-BA | ncep_gfswave025 | 1.2 m | 93 % |
| BR-ES | ncep_gfswave025 | 1.1 m | 96 % |
| BR-NE-CE | ncep_gfswave016 | 1.0 m | 86 % |
| BR-NE-PE | ncep_gfswave016 | 1.0 m | 99 % |
| BR-NE-RN | ncep_gfswave016 | 1.0 m | 95 % |
| BR-NOR | ncep_gfswave016 | 1.2 m | 72 % |
| BR-RJ | ncep_gfswave025 | 0.9 m | 100 % |
| BR-RJL | ncep_gfswave025 | 1.1 m | 71 % |
| BR-RS-SUL | ncep_gfswave025 | 1.0 m | 88 % |
| BR-RS | ncep_gfswave025 | 1.4 m | 100 % |
| BR-SC-FLN | ncep_gfswave025 | 1.5 m | 79 % |
| BR-SC-NOR | ncep_gfswave025 | 1.0 m | 100 % |
| BR-SC-SUL | ncep_gfswave025 | 1.4 m | 88 % |
| BR-SP | ncep_gfswave025 | 0.8 m | 95 % |
| BS-ALL | ncep_gfswave016 | 1.6 m | 95 % |
| CA-BC-VI | ecmwf_wam | 3.2 m | 77 % |
| CA-NS | ncep_gfswave016 | 0.9 m | 80 % |
| CL-CEN | ncep_gfswave025 | 1.8 m | 52 % |
| CL-MAU | ncep_gfswave025 | 1.6 m | 80 % |
| CL-NOR | ncep_gfswave025 | 1.6 m | 100 % |
| CL-PIC | ncep_gfswave025 | 2.0 m | 83 % |
| CL-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| CN-HAI | ncep_gfswave016 | 1.2 m | 16 % |
| CO-CAR | ncep_gfswave016 | 0.9 m | 98 % |
| CO-PAC | ncep_gfswave016 | 0.7 m | 100 % |
| CR-CAR | ncep_gfswave016 | 0.7 m | 96 % |
| CR-GUA | ncep_gfswave016 | 0.9 m | 100 % |
| CR-NIC | ncep_gfswave016 | 0.9 m | 100 % |
| CR-OSA | ncep_gfswave016 | 1.1 m | 39 % |
| CR-PAC | ncep_gfswave016 | 0.9 m | 100 % |
| CV-ALL | ncep_gfswave016 | 1.3 m | 83 % |
| DE-ALL | ncep_gfswave025 | 1.2 m | 66 % |
| DK-ALL | ncep_gfswave025 | 1.2 m | 60 % |
| DO-ALL | ncep_gfswave016 | 1.1 m | 92 % |
| EC-COS | ncep_gfswave016 | 0.8 m | 100 % |
| EC-GAL | ncep_gfswave016 | 1.0 m | 94 % |
| ES-AND | ncep_gfswave016 | 1.3 m | 91 % |
| ES-AST | ncep_gfswave016 | 1.4 m | 91 % |
| ES-CAN | ncep_gfswave016 | 1.4 m | 79 % |
| ES-CN-E | ncep_gfswave016 | 1.5 m | 96 % |
| ES-CN-W | ncep_gfswave016 | 1.0 m | 72 % |
| ES-GAL | ncep_gfswave016 | 2.2 m | 84 % |
| ES-PV | ncep_gfswave016 | 1.2 m | 76 % |
| FJ-MAM | ncep_gfswave025 | 1.0 m | 71 % |
| FJ-SOU | ncep_gfswave025 | 1.2 m | 91 % |
| FR-BRE | ncep_gfswave016 | 1.7 m | 94 % |
| FR-GIR | ncep_gfswave016 | 1.8 m | 95 % |
| FR-HOS | ncep_gfswave016 | 1.5 m | 90 % |
| FR-PBA | ncep_gfswave016 | 1.5 m | 93 % |
| FR-VEN | ncep_gfswave016 | 1.6 m | 93 % |
| GB-CON | ncep_gfswave016 | 1.6 m | 79 % |
| GB-DEV | ncep_gfswave016 | 1.2 m | 93 % |
| GB-NE | ncep_gfswave025 | 1.2 m | 68 % |
| GB-NIR | ecmwf_wam | 0.8 m | 65 % |
| GB-SCO | ncep_gfswave025 | 1.5 m | 58 % |
| GB-SOU | ncep_gfswave016 | 1.3 m | 78 % |
| GB-WAL | ncep_gfswave025 | 1.2 m | 86 % |
| GH-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| GP-ALL | ncep_gfswave016 | 1.0 m | 1 % |
| GT-PAC | ncep_gfswave016 | 1.0 m | 100 % |
| ID-BAL-BUK | ncep_gfswave016 | 1.2 m | 100 % |
| ID-BAL-E | ncep_gfswave016 | 0.9 m | 42 % |
| ID-BAL-W | ncep_gfswave016 | 1.2 m | 100 % |
| ID-JAV-E | ncep_gfswave016 | 1.1 m | 100 % |
| ID-JAV-W | ncep_gfswave016 | 1.2 m | 97 % |
| ID-KRU | ncep_gfswave016 | 1.4 m | 100 % |
| ID-LOM | ncep_gfswave016 | 1.3 m | 99 % |
| ID-MEN | ncep_gfswave016 | 1.0 m | 100 % |
| ID-NIA | ncep_gfswave016 | 1.3 m | 93 % |
| ID-ROT | ncep_gfswave016 | 0.8 m | 100 % |
| ID-SBW | ncep_gfswave016 | 1.0 m | 100 % |
| ID-SMB | ncep_gfswave016 | 1.3 m | 100 % |
| IE-NW | ncep_gfswave025 | 0.9 m | 87 % |
| IE-SE | ncep_gfswave016 | 1.7 m | 82 % |
| IE-SW | ecmwf_wam | 1.4 m | 58 % |
| IN-E | ncep_gfswave016 | 1.0 m | 100 % |
| IN-W | ncep_gfswave016 | 0.5 m | 91 % |
| IS-ALL | ncep_gfswave025 | 2.1 m | 62 % |
| IT-ALL | ncep_gfswave016 | 1.1 m | 93 % |
| IT-SAR | ncep_gfswave016 | 1.3 m | 93 % |
| JP-CHI | ncep_gfswave016 | 1.5 m | 72 % |
| JP-IBA | ncep_gfswave016 | 1.2 m | 79 % |
| JP-IZU | ncep_gfswave016 | 1.1 m | 50 % |
| JP-KYU | ncep_gfswave016 | 1.0 m | 97 % |
| JP-SHK | ncep_gfswave016 | 1.0 m | 76 % |
| JP-SHO | ncep_gfswave016 | 0.9 m | 74 % |
| KR-ALL | ncep_gfswave016 | 1.0 m | 41 % |
| LK-E | ncep_gfswave016 | 1.2 m | 34 % |
| LK-S | ncep_gfswave016 | 1.0 m | 100 % |
| LR-ALL | ncep_gfswave016 | 0.7 m | 100 % |
| MA-N | ncep_gfswave016 | 1.6 m | 98 % |
| MA-S | ncep_gfswave016 | 1.4 m | 100 % |
| MA-TAG | ncep_gfswave016 | 1.2 m | 100 % |
| MG-ALL | ncep_gfswave025 | 1.9 m | 65 % |
| MQ-ALL | ncep_gfswave016 | 1.1 m | 44 % |
| MU-ALL | ncep_gfswave025 | 1.3 m | 100 % |
| MV-CEN | ncep_gfswave016 | 0.7 m | 98 % |
| MV-NMA | ncep_gfswave016 | 0.7 m | 93 % |
| MV-SMA | ncep_gfswave016 | 0.7 m | 97 % |
| MV-SOU | ncep_gfswave016 | 0.9 m | 54 % |
| MX-BCN | ecmwf_wam | 1.8 m | 100 % |
| MX-BCS-N | ncep_gfswave016 | 0.9 m | 73 % |
| MX-BCS | ncep_gfswave016 | 0.6 m | 69 % |
| MX-CAR | ncep_gfswave016 | 0.6 m | 91 % |
| MX-NAY | ncep_gfswave016 | 0.6 m | 100 % |
| MX-OAX | ncep_gfswave016 | 1.1 m | 100 % |
| MX-PAC | ncep_gfswave016 | 1.1 m | 100 % |
| MZ-INH | ncep_gfswave025 | 1.9 m | 71 % |
| MZ-S | ncep_gfswave025 | 1.8 m | 35 % |
| NA-ERO | ncep_gfswave025 | 1.6 m | 100 % |
| NI-NW | ncep_gfswave016 | 0.9 m | 100 % |
| NI-RIV | ncep_gfswave016 | 1.0 m | 100 % |
| NL-ALL | ncep_gfswave025 | 0.9 m | 56 % |
| NO-N | ncep_gfswave025 | 2.1 m | 57 % |
| NO-S | ncep_gfswave025 | 1.6 m | 95 % |
| NZ-AKL | ncep_gfswave025 | 1.8 m | 100 % |
| NZ-BOP | ncep_gfswave025 | 0.9 m | 100 % |
| NZ-GIS | ncep_gfswave025 | 1.2 m | 35 % |
| NZ-KAI | ncep_gfswave025 | 1.0 m | 55 % |
| NZ-NTL | ncep_gfswave025 | 1.3 m | 98 % |
| NZ-OTA | ncep_gfswave025 | 1.4 m | 35 % |
| NZ-RAG | ncep_gfswave025 | 1.4 m | 100 % |
| NZ-TAR | ncep_gfswave025 | 1.5 m | 29 % |
| NZ-WC | ncep_gfswave025 | 1.6 m | 64 % |
| NZ-WEL | ncep_gfswave025 | 1.1 m | 51 % |
| PA-BDT | ncep_gfswave016 | 0.8 m | 100 % |
| PA-PAC | ncep_gfswave016 | 0.7 m | 100 % |
| PE-LIM | ncep_gfswave025 | 1.6 m | 100 % |
| PE-LLB | ncep_gfswave016 | 1.1 m | 100 % |
| PE-NOR | ncep_gfswave016 | 0.9 m | 80 % |
| PE-SUR | ncep_gfswave025 | 1.5 m | 100 % |
| PF-ISL | ncep_gfswave025 | 2.2 m | 43 % |
| PF-TAH | ncep_gfswave025 | 2.1 m | 41 % |
| PG-ALL | ncep_gfswave016 | 0.8 m | 21 % |
| PH-EAS | ncep_gfswave016 | 1.4 m | 100 % |
| PH-LUZ | ncep_gfswave016 | 0.9 m | 97 % |
| PH-SIA | ncep_gfswave016 | 1.4 m | 95 % |
| PR-N | ncep_gfswave016 | 1.0 m | 100 % |
| PR-NW | ncep_gfswave016 | 0.9 m | 83 % |
| PT-ALG | ncep_gfswave016 | 2.2 m | 98 % |
| PT-AZO | ncep_gfswave016 | 2.4 m | 29 % |
| PT-CEN | ncep_gfswave016 | 2.2 m | 98 % |
| PT-ERI | ncep_gfswave016 | 2.6 m | 98 % |
| PT-LIS | ncep_gfswave016 | 2.2 m | 88 % |
| PT-MAD | ncep_gfswave016 | 1.9 m | 80 % |
| PT-NOR | ncep_gfswave016 | 2.5 m | 100 % |
| PT-PEN | ncep_gfswave016 | 2.5 m | 88 % |
| RE-ALL | ncep_gfswave025 | 1.1 m | 75 % |
| SN-ALL | ncep_gfswave016 | 1.6 m | 99 % |
| SV-LIB | ncep_gfswave016 | 0.9 m | 100 % |
| SV-ORI | ncep_gfswave016 | 1.0 m | 100 % |
| TO-ALL | ncep_gfswave025 | 1.8 m | 12 % |
| TT-ALL | ncep_gfswave016 | 0.9 m | 98 % |
| TW-E | ncep_gfswave016 | 1.3 m | 29 % |
| TW-NE | ncep_gfswave016 | 1.6 m | 70 % |
| US-CA-CEN | ecmwf_wam | 2.7 m | 100 % |
| US-CA-LA | ecmwf_wam | 1.2 m | 100 % |
| US-CA-NOR | ecmwf_wam | 3.5 m | 97 % |
| US-CA-OC | ecmwf_wam | 1.3 m | 100 % |
| US-CA-SB | ecmwf_wam | 1.4 m | 5 % |
| US-CA-SC | ecmwf_wam | 2.5 m | 82 % |
| US-CA-SD | ncep_gfswave016 | 0.8 m | 100 % |
| US-CA-SF | ecmwf_wam | 2.9 m | 100 % |
| US-FL-PAN | ecmwf_wam | 0.7 m | 18 % |
| US-FL | ncep_gfswave016 | 1.1 m | 88 % |
| US-GULF | ecmwf_wam | 1.0 m | 94 % |
| US-HI-BIG | ecmwf_wam | 0.9 m | 72 % |
| US-HI-KAU | ecmwf_wam | 2.1 m | 78 % |
| US-HI-MAU | ecmwf_wam | 2.6 m | 20 % |
| US-HI-OAN | ncep_gfswave016 | 1.9 m | 89 % |
| US-HI-OAS | ecmwf_wam | 1.3 m | 0 % |
| US-MID | ncep_gfswave025 | 0.7 m | 74 % |
| US-NE | ecmwf_wam | 0.7 m | 46 % |
| US-PNW | ecmwf_wam | 3.5 m | 100 % |
| US-SC-GA | ncep_gfswave016 | 0.8 m | 69 % |
| US-SE | ncep_gfswave025 | 0.9 m | 76 % |
| UY-CAN | ncep_gfswave025 | 0.7 m | 48 % |
| UY-MAL | ncep_gfswave025 | 1.0 m | 52 % |
| UY-ROC | ncep_gfswave025 | 1.2 m | 74 % |
| VE-ALL | ncep_gfswave016 | 1.0 m | 100 % |
| VE-MAR | ncep_gfswave016 | 1.0 m | 100 % |
| VN-ALL | ncep_gfswave016 | 0.9 m | 100 % |
| VU-ALL | ncep_gfswave025 | 1.1 m | 17 % |
| WS-ALL | ncep_gfswave025 | 2.1 m | 76 % |
| ZA-EC-JB | ncep_gfswave025 | 2.2 m | 95 % |
| ZA-EC-PE | ncep_gfswave025 | 2.4 m | 32 % |
| ZA-EC-WLD | ncep_gfswave025 | 2.0 m | 53 % |
| ZA-KZN-DBN | ncep_gfswave025 | 1.9 m | 65 % |
| ZA-KZN-N | ncep_gfswave025 | 1.9 m | 73 % |
| ZA-KZN-S | ncep_gfswave025 | 2.0 m | 55 % |
| ZA-WC-CPT | ncep_gfswave025 | 2.0 m | 85 % |
| ZA-WC-GR | ncep_gfswave025 | 2.0 m | 92 % |
| ZA-WC-WCO | ncep_gfswave025 | 1.8 m | 0 % |
