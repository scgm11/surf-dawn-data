# Picos: controles por pico

Generado 2026-11-07 05:58 UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). 213 regiones, 2511 picos.

- **Orientación (§5.2):** olas de los últimos 14 días y los próximos 2 en el punto de olas de cada pico (el modelo de su zona). Se marca un pico al que las olas de al menos 0.3 m casi nunca le llegan a menos de 55° de hacia donde mira, o de su ventana de swell si la tiene (menos del 5 % de las horas) mientras a su zona sí (al menos 25 %).
- **Zona entera:** en una zona donde la mayoría tampoco las recibe de frente (menos del 25 %) los vecinos no dicen nada: ahí se marca el pico con mar (olas de al menos 0.3 m en el 25 % de las horas o más) que casi nunca las recibe de frente.
- **Temporada:** los marcados por la orientación se miran de nuevo con 92 días de olas; 39 dejaron de estarlo (en dos semanas no les tocaba su ventana de swell).
- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media de su zona.
- **Celdas:** la celda de la que contesta la API a cada pico, abajo las que no son buenas.
- **Emblemáticos (§5.8):** la posición contra fuentes públicas (el ítem más cercano con su nombre en Wikidata o GeoNames, hasta 6 km; si no, OpenStreetMap; si no, el ítem de otro nombre del que se tomó a mano la posición, en el `src` de la semilla): 319 bien (a menos de 1.5 km; 12 de ellos por la fuente de su semilla), 0 lejos, 21 lejos pero revisados a mano (el ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), 52 sin fuente (revisar a mano; `validation/lookup.md` tiene lo que hay con su nombre alrededor), 0 sin respuesta.
- Open-Meteo: 35 pedidos, ~4680 llamadas de las 10.000 diarias gratuitas.

## Orientación probablemente del lado equivocado (1)

Mira a más de 135° de sus vecinos (a 30 km) y de las olas, y dada vuelta coincide con ellos: casi seguro se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla.

| Región | Pico | Mira a | Vecinos | Olas desde |
|---|---|---|---|---|
| CA-BC-VI | SCHOONER COVE | 44° | 204° | 236° |

## Zonas enteras que casi nunca reciben las olas de frente (1)

Zonas con 3 picos o más que, en 92 días, casi nunca recibieron las olas de frente aunque había mar, y a las que la comparación con los vecinos no ve porque están todos igual. O la orientación de toda la costa se calculó del lado equivocado, o son reefs y puntas a los que el swell entra dando la vuelta: ahí la orientación de la costa está bien para el viento y lo que falta es la ventana de swell del pico.

| Región | Marcados | Puntas y reefs | Miran a | Olas desde | Picos |
|---|---|---|---|---|---|
| ZA-WC-WCO | 4 de 6 | 0 | 325° | 233° | MELKBOS, LAMBERTS BAY, JACOBSBAAI, YZERFONTEIN |

## Celdas de olas para mirar (52)

La celda desde la que contesta la API cuando se le pregunta como las apps (sin `cell_selection`). Se marca el punto de olas que la API corre o que queda detrás de la playa (a más de 75° de hacia donde mira, o de su ventana de swell), y el pico que la API corre a una celda detrás de la playa o a más de 35 km. A veces es con razón: su celda es tierra y la siguiente queda de costado. Se corrige con `wave=` en la semilla, después de mirar la celda.

| Región | Pico | Punto de olas | Celda | Por qué |
|---|---|---|---|---|
| AU-NSW-MN | HAT HEAD | — | -31.25, 153.00 | la API lo contesta desde una celda detrás de la playa (a 155° de hacia donde mira, 22 km) |
| AU-NSW-MN | FORSTER MAIN | — | -32.25, 152.75 | la API lo contesta desde una celda detrás de la playa (a 100° de hacia donde mira, 23 km) |
| AU-NSW-SYD | MANLY | — | -34.00, 151.25 | la API lo contesta desde una celda detrás de la playa (a 95° de hacia donde mira, 24 km) |
| BR-NE-CE | LAGOINHA | — | -3.33, -39.00 | la API lo contesta desde una celda detrás de la playa (a 88° de hacia donde mira, 15 km) |
| BR-NE-PE | MARACAÍPE | — | -8.67, -35.00 | la API lo contesta desde una celda detrás de la playa (a 90° de hacia donde mira, 15 km) |
| BR-SP | PAÚBA | — | -24.00, -45.50 | la API lo contesta desde una celda detrás de la playa (a 98° de hacia donde mira, 23 km) |
| BR-SP | BARRA DO SAHY | — | -24.00, -45.75 | la API lo contesta desde una celda detrás de la playa (a 135° de hacia donde mira, 23 km) |
| CA-NS | COLE HARBOUR | — | 44.50, -63.33 | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 16 km) |
| CR-GUA | EL ESTERO | — | 10.17, -85.83 | la API lo contesta desde una celda detrás de la playa (a 93° de hacia donde mira, 16 km) |
| CR-GUA | TAMARINDO | — | 10.17, -85.83 | la API lo contesta desde una celda detrás de la playa (a 136° de hacia donde mira, 15 km) |
| ES-CN-E | EL COTILLO | — | 28.83, -14.00 | la API lo contesta desde una celda detrás de la playa (a 95° de hacia donde mira, 16 km) |
| ES-GAL | ORZAN | — | 43.50, -8.33 | la API lo contesta desde una celda detrás de la playa (a 79° de hacia donde mira, 15 km) |
| GB-CON | TREVAUNANCE COVE | — | 50.33, -5.33 | la API lo contesta desde una celda detrás de la playa (a 76° de hacia donde mira, 9 km) |
| GB-NIR | BALLYCASTLE | — | 55.22, -6.31 | la API lo contesta desde una celda detrás de la playa (a 104° de hacia donde mira, 5 km) |
| GB-WAL | RHOSNEIGR | — | 53.25, -4.75 | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 16 km) |
| ID-JAV-W | CIMAJA | — | -7.00, 106.33 | la API lo contesta desde una celda detrás de la playa (a 83° de hacia donde mira, 23 km) |
| ID-JAV-W | KARANG HAWU | — | -7.00, 106.33 | la API lo contesta desde una celda detrás de la playa (a 86° de hacia donde mira, 23 km) |
| ID-ROT | SQUEALERS | — | -11.00, 122.83 | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 16 km) |
| ID-ROT | SUCKY MAMAS | — | -11.00, 122.83 | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 18 km) |
| IE-NW | TULLAN STRAND | — | 54.50, -8.50 | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 13 km) |
| IE-NW | ENNISCRONE | 54.50, -9.00 | 54.50, -9.00 | punto de olas detrás de la playa (a 109° de hacia donde mira, 32 km) |
| IE-SE | GARRETTSTOWN | — | 51.50, -8.50 | la API lo contesta desde una celda detrás de la playa (a 122° de hacia donde mira, 15 km) |
| IE-SW | BALLYHEIGUE | — | 52.48, -9.87 | la API lo contesta desde una celda detrás de la playa (a 96° de hacia donde mira, 11 km) |
| IN-E | SERENITY BEACH | — | 11.83, 79.83 | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 16 km) |
| JP-CHI | ONJUKU | — | 35.17, 140.50 | la API lo contesta desde una celda detrás de la playa (a 109° de hacia donde mira, 12 km) |
| JP-SHO | OISO | — | 35.17, 139.33 | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 15 km) |
| LK-E | ARUGAM BAY | — | 6.83, 82.00 | la API lo contesta desde una celda detrás de la playa (a 92° de hacia donde mira, 18 km) |
| MG-ALL | LIBANONA | — | -25.25, 47.00 | la API lo contesta desde una celda detrás de la playa (a 79° de hacia donde mira, 24 km) |
| MX-OAX | SAN AGUSTINILLO | — | 15.67, -96.67 | la API lo contesta desde una celda detrás de la playa (a 82° de hacia donde mira, 13 km) |
| MX-OAX | ZIPOLITE | — | 15.67, -96.67 | la API lo contesta desde una celda detrás de la playa (a 86° de hacia donde mira, 16 km) |
| MX-PAC | REVOLCADERO | — | 16.67, -99.83 | la API lo contesta desde una celda detrás de la playa (a 110° de hacia donde mira, 15 km) |
| NZ-KAI | MANGAMAUNU | — | -42.50, 173.75 | la API lo contesta desde una celda detrás de la playa (a 122° de hacia donde mira, 22 km) |
| NZ-NTL | OCEAN BEACH | — | -35.75, 174.75 | la API lo contesta desde una celda detrás de la playa (a 138° de hacia donde mira, 22 km) |
| NZ-WEL | MAKARA BEACH | — | -41.25, 174.50 | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 18 km) |
| PG-ALL | TAURAMA POINT | — | -9.67, 147.17 | la API lo contesta desde una celda detrás de la playa (a 91° de hacia donde mira, 22 km) |
| PT-AZO | MONTE VERDE | — | 37.67, -25.50 | la API lo contesta desde una celda detrás de la playa (a 131° de hacia donde mira, 18 km) |
| PT-AZO | SANTA BÁRBARA | — | 37.67, -25.50 | la API lo contesta desde una celda detrás de la playa (a 174° de hacia donde mira, 18 km) |
| PT-MAD | SEIXAL | — | 32.67, -17.17 | la API lo contesta desde una celda detrás de la playa (a 109° de hacia donde mira, 19 km) |
| PT-NOR | MATOSINHOS | — | 41.17, -8.83 | la API lo contesta desde una celda detrás de la playa (a 82° de hacia donde mira, 11 km) |
| PT-NOR | CARNEIRO | — | 41.00, -8.67 | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 16 km) |
| PT-PEN | BALEAL | — | 39.50, -9.33 | la API lo contesta desde una celda detrás de la playa (a 77° de hacia donde mira, 14 km) |
| PT-PEN | CANTINHO | — | 39.50, -9.33 | la API lo contesta desde una celda detrás de la playa (a 105° de hacia donde mira, 14 km) |
| US-CA-CEN | ANDREW MOLERA | — | 36.38, -121.92 | la API lo contesta desde una celda detrás de la playa (a 164° de hacia donde mira, 9 km) |
| US-CA-SF | SURFER'S BEACH | — | 37.57, -122.52 | la API lo contesta desde una celda detrás de la playa (a 118° de hacia donde mira, 9 km) |
| US-HI-KAU | KEALIA | — | 22.18, -159.29 | la API lo contesta desde una celda detrás de la playa (a 131° de hacia donde mira, 9 km) |
| US-PNW | BEVERLY BEACH | — | 44.82, -124.08 | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 9 km) |
| US-SE | MYRTLE BEACH | — | 33.50, -79.00 | la API lo contesta desde una celda detrás de la playa (a 78° de hacia donde mira, 24 km) |
| VE-ALL | CUYAGUA | — | 10.50, -67.83 | la API lo contesta desde una celda detrás de la playa (a 113° de hacia donde mira, 16 km) |
| VU-ALL | PORT RESOLUTION | — | -19.75, 169.50 | la API lo contesta desde una celda detrás de la playa (a 83° de hacia donde mira, 24 km) |
| ZA-EC-PE | CANNON ROCKS | — | -33.75, 26.75 | la API lo contesta desde una celda detrás de la playa (a 85° de hacia donde mira, 20 km) |
| ZA-EC-PE | NAHOON REEF | — | -33.25, 28.00 | la API lo contesta desde una celda detrás de la playa (a 108° de hacia donde mira, 29 km) |
| ZA-KZN-S | SCOTTBURGH | — | -30.50, 30.75 | la API lo contesta desde una celda detrás de la playa (a 80° de hacia donde mira, 24 km) |

## Picos marcados (126)

Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y el semáforo del swell es conservador ahí); se revisan a mano.

| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |
|---|---|---|---|---|---|---|
| AU-NSW-NC | OCEAN BEACH |  | 250° | 148° | 117° | las olas casi nunca le entran de frente (1 % de las horas; la zona 69 %) y en 92 días 0 % |
| AU-SA | CHINAMANS |  | 325° | 233° | 250° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 1 % |
| AU-TAS | CLIFTON BEACH | sí | 119° | 211° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 39 %) y en 92 días 3 % |
| AU-TAS | MARION BAY |  | 269° | 105° | 146° | las olas casi nunca le entran de frente (0 % de las horas; la zona 39 %) y en 92 días 2 % |
| AU-TAS | MARRAWAH |  | 314° | 230° | — | 2.7 m de media, más del doble de la zona (1.2 m); las olas casi nunca le entran de frente (1 % de las horas; la zona 39 %) y en 92 días 1 % |
| AU-TAS | GREEN POINT |  | 290° | 230° | — | 2.7 m de media, más del doble de la zona (1.2 m) |
| AU-VIC-PI | FOREST CAVES |  | 127° | 223° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-VIC-SC | JAN JUC |  | 118° | 221° | 154° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| AU-VIC-SC | POINT ADDIS |  | 91° | 221° | 151° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| AU-VIC-W | WYE RIVER |  | 110° | 229° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| AU-VIC-W | KENNETT RIVER |  | 117° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| AU-VIC-W | PORT FAIRY EAST |  | 140° | 219° | 229° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| BR-NE-PE | GAIBU |  | 31° | 108° | 105° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 0 % |
| BR-SP | FAZENDA |  | 260° | 146° | 125° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| BR-SP | MARANDUBA |  | 234° | 137° | 141° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| BR-SP | PAÚBA |  | 264° | 154° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 86 %) y en 92 días 1 % |
| BR-SP | CAMBURI |  | 261° | 154° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 86 %) y en 92 días 1 % |
| BR-SP | ILHA COMPRIDA |  | 269° | 142° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| BS-ALL | SURFERS BEACH |  | 168° | 44° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| CA-BC-VI | SCHOONER COVE |  | 44° | 236° | 204° | las olas casi nunca le entran de frente (0 % de las horas; la zona 68 %) y en 92 días 0 % |
| CA-BC-VI | WYA POINT |  | 90° | 240° | 210° | las olas casi nunca le entran de frente (0 % de las horas; la zona 68 %) y en 92 días 0 % |
| CA-BC-VI | CHINA BEACH |  | 202° | 276° | 218° | las olas casi nunca le entran de frente (5 % de las horas; la zona 68 %) y en 92 días 1 % |
| CL-CEN | PAPUDO |  | 19° | 236° | 283° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 0 % |
| CL-CEN | MAITENCILLO | sí | 323° | 231° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 2 % |
| CL-CEN | HORCÓN |  | 330° | 231° | 291° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-CEN | LA BOCA |  | 314° | 231° | 277° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 2 % |
| CL-CEN | AMARILLA |  | 341° | 231° | 274° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-CEN | TUNQUÉN |  | 335° | 235° | 281° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-CEN | ALGARROBO |  | 339° | 235° | 293° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-CEN | EL QUISCO |  | 335° | 235° | 294° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-CEN | CARTAGENA |  | 325° | 235° | 281° | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 3 % |
| CL-MAU | LLICO |  | 344° | 238° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 3 % |
| CL-MAU | CURANIPE |  | 346° | 243° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 5 % |
| CL-NOR | LAS MACHAS |  | 324° | 221° | 280° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CL-PIC | MATANZAS |  | 338° | 243° | 325° | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 2 % |
| CL-PIC | LAS TERRAZAS |  | 313° | 233° | 311° | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 4 % |
| CO-PAC | HUINA |  | 312° | 228° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-GUA | TAMARINDO | sí | 312° | 227° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-NIC | SAMARA |  | 146° | 211° | 225° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-OSA | RIO CLARO |  | 308° | 214° | 246° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| CV-ALL | SANTA MARIA |  | 193° | 354° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 89 %) y en 92 días 0 % |
| EC-COS | BALLENITA |  | 317° | 238° | 296° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ES-AND | REGLA |  | 7° | 252° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| ES-AND | ZAHORA |  | 172° | 255° | 234° | las olas casi nunca le entran de frente (2 % de las horas; la zona 91 %) y en 92 días 3 % |
| ES-AND | BOLONIA |  | 191° | 290° | 226° | las olas casi nunca le entran de frente (2 % de las horas; la zona 91 %) y en 92 días 1 % |
| ES-AST | XAGO |  | 82° | 333° | 1° | las olas casi nunca le entran de frente (1 % de las horas; la zona 85 %) y en 92 días 2 % |
| ES-CN-E | FLAG BEACH |  | 88° | 329° | 274° | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 0 % |
| ES-CN-W | PLAYA DEL HOMBRE |  | 89° | 355° | 325° | las olas casi nunca le entran de frente (0 % de las horas; la zona 62 %) y en 92 días 1 % |
| ES-CN-W | SARDINA |  | 215° | 340° | 330° | las olas casi nunca le entran de frente (5 % de las horas; la zona 62 %) y en 92 días 1 % |
| ES-CN-W | EL MEDANO |  | 119° | 152° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 62 %) y en 92 días 1 % |
| ES-GAL | DONIÑOS |  | 225° | 311° | 343° | las olas casi nunca le entran de frente (1 % de las horas; la zona 70 %) y en 92 días 2 % |
| ES-GAL | TRABA |  | 202° | 311° | 343° | las olas casi nunca le entran de frente (2 % de las horas; la zona 70 %) y en 92 días 2 % |
| ES-PV | LAGA |  | 73° | 329° | 352° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| ES-PV | MUNDAKA | sí | 64° | 329° | 351° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| ES-PV | PLENTZIA |  | 96° | 328° | 349° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| FJ-MAM | CLOUDBREAK | sí | 220° | 208° | 254° | 1.0 m de media, más del doble de la zona (0.4 m) |
| FR-BRE | LE POULDU |  | 132° | 248° | 221° | las olas casi nunca le entran de frente (2 % de las horas; la zona 95 %) y en 92 días 1 % |
| FR-VEN | LA TRANCHE |  | 151° | 264° | 211° | las olas casi nunca le entran de frente (0 % de las horas; la zona 89 %) y en 92 días 0 % |
| GB-CON | PORTHCOTHAN |  | 194° | 278° | 317° | las olas casi nunca le entran de frente (0 % de las horas; la zona 92 %) y en 92 días 1 % |
| GB-DEV | WESTWARD HO |  | 345° | 269° | 266° | las olas casi nunca le entran de frente (0 % de las horas; la zona 92 %) y en 92 días 3 % |
| GB-DEV | THURLESTONE |  | 326° | 223° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 92 %) y en 92 días 3 % |
| GB-SCO | STRATHY |  | 77° | 287° | 358° | las olas casi nunca le entran de frente (0 % de las horas; la zona 34 %) y en 92 días 3 % |
| GB-SCO | GOTT BAY |  | 138° | 242° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 34 %) y en 92 días 2 % |
| GB-WAL | BROAD HAVEN SOUTH |  | 149° | 244° | 229° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 4 % |
| GB-WAL | RHOSSILI |  | 336° | 243° | 203° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 1 % |
| GB-WAL | LANGLAND BAY |  | 120° | 244° | 249° | las olas casi nunca le entran de frente (4 % de las horas; la zona 86 %) y en 92 días 4 % |
| GB-WAL | LLANTWIT MAJOR |  | 199° | 272° | 244° | las olas casi nunca le entran de frente (2 % de las horas; la zona 86 %) y en 92 días 3 % |
| GP-ALL | TARARE |  | 180° | 82° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| GP-ALL | PORT LOUIS |  | 270° | 35° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | DREAMLAND |  | 286° | 207° | 321° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | PURNAMA |  | 133° | 198° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 74 %) y en 92 días 0 % |
| ID-BAL-E | SABA |  | 130° | 198° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 74 %) y en 92 días 0 % |
| ID-BAL-E | LEBIH |  | 132° | 198° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 74 %) y en 92 días 0 % |
| ID-JAV-W | PANGANDARAN |  | 280° | 199° | 100° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| ID-JAV-W | MADASARI |  | 119° | 195° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| ID-LOM | SELONG BELANAK |  | 296° | 211° | 182° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | MAWUN |  | 133° | 211° | 190° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | KUTA LOMBOK |  | 140° | 212° | 189° | las olas casi nunca le entran de frente (1 % de las horas; la zona 99 %) y en 92 días 0 % |
| IE-NW | TULLAN STRAND |  | 358° | 284° | 307° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| IE-NW | KEEL |  | 186° | 271° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 3 % |
| IE-SW | INCH |  | 172° | 258° | 268° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 3 % |
| LR-ALL | COTTON TREE |  | 310° | 202° | 311° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-S | TIFNIT |  | 230° | 307° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | AGADIR |  | 186° | 309° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | MADRABA |  | 234° | 303° | 229° | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-NAY | LO DE MARCOS |  | 311° | 231° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 3 % |
| MX-NAY | SAN PANCHO |  | 297° | 219° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 4 % |
| MX-OAX | MAZUNTE |  | 123° | 211° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-PAC | MIRAMAR |  | 314° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 1 % |
| NA-ERO | SKELETON BAY | sí | 321° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| NZ-BOP | ONEMANA |  | 164° | 31° | 55° | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 3 % |
| NZ-NTL | MATAURI BAY |  | 224° | 30° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 91 %) y en 92 días 1 % |
| NZ-NTL | BAYLYS BEACH |  | 235° | 230° | — | 2.1 m de media, más del doble de la zona (1.1 m) |
| NZ-OTA | PORPOISE BAY |  | 103° | 214° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 31 %) y en 92 días 4 % |
| NZ-OTA | COLAC BAY |  | 182° | 259° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 31 %) y en 92 días 0 % |
| NZ-WC | TAURANGA BAY |  | 34° | 276° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 69 %) y en 92 días 1 % |
| PA-PAC | PLAYA VENAO | sí | 235° | 212° | — | 0.9 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | GUANICO |  | 153° | 201° | 209° | 0.8 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | CAMBUTAL |  | 183° | 214° | — | 1.1 m de media, más del doble de la zona (0.3 m) |
| PE-LIM | AGUA DULCE |  | 291° | 214° | 232° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| PR-NW | CRASH BOAT |  | 231° | 12° | 286° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PR-NW | SANDY BEACH |  | 235° | 9° | 286° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PR-NW | CÓRCEGA |  | 246° | 9° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PT-ALG | ZAVIAL |  | 173° | 285° | 278° | las olas casi nunca le entran de frente (5 % de las horas; la zona 99 %) y en 92 días 1 % |
| PT-AZO | SANTA BÁRBARA | sí | 343° | 246° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (15 %) y en 92 días 1 % |
| PT-AZO | ALMOXARIFE |  | 91° | 291° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (15 %) y en 92 días 0 % |
| PT-MAD | MACHICO |  | 122° | 328° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| RE-ALL | BOUCAN CANOT |  | 312° | 213° | 265° | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| RE-ALL | BARACHOIS |  | 325° | 108° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 75 %) y en 92 días 0 % |
| US-CA-CEN | PIRATE'S COVE |  | 175° | 278° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 3 % |
| US-CA-CEN | ANDREW MOLERA |  | 186° | 289° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 4 % |
| US-CA-NOR | NORTH JETTY |  | 19° | 300° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-CA-SB | SANDSPIT |  | 112° | 207° | 193° | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 0 % |
| US-CA-SC | MORAN LAKE |  | 130° | 261° | 200° | las olas casi nunca le entran de frente (0 % de las horas; la zona 87 %) y en 92 días 0 % |
| US-CA-SC | CAPITOLA |  | 157° | 261° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 87 %) y en 92 días 3 % |
| US-PNW | PORT ORFORD |  | 162° | 285° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-SE | OCRACOKE |  | 262° | 112° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 0 % |
| ZA-EC-PE | HOBIE BEACH |  | 31° | 188° | 132° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| ZA-WC-CPT | LLANDUDNO | sí | 311° | 231° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 0 % |
| ZA-WC-CPT | LONG BEACH | sí | 344° | 229° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 0 % |
| ZA-WC-CPT | KOGEL BAY |  | 332° | 209° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 0 % |
| ZA-WC-GR | SANTOS |  | 50° | 200° | 147° | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 0 % |
| ZA-WC-WCO | MELKBOS |  | 310° | 234° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ZA-WC-WCO | LAMBERTS BAY |  | 320° | 237° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | JACOBSBAAI |  | 318° | 228° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | YZERFONTEIN |  | 351° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |

## Emblemáticos lejos de su ítem en Wikidata, GeoNames u OpenStreetMap

Ninguno.

## Emblemáticos sin fuente en Wikidata, GeoNames ni OpenStreetMap (revisar a mano)

AU-NSW-SYD/OURS, AU-VIC-SC/WINKIPOP, AU-WA-MR/MAIN BREAK, AU-WA-MR/NORTH POINT, CL-NOR/EL GRINGO, CR-GUA/WITCH'S ROCK, CR-OSA/PAVONES, ES-CN-E/EL QUEMAO, ES-CN-W/EL FRONTON, ES-CN-W/LA IZQUIERDA, FJ-MAM/CLOUDBREAK, FJ-MAM/RESTAURANTS, FJ-MAM/SWIMMING POOLS, ID-BAL-E/SHIPWRECKS, ID-JAV-E/MONEY TREES, ID-MEN/MACARONIS, ID-MEN/KANDUI LEFT, ID-MEN/RIFLES, ID-ROT/T-LAND, ID-SBW/SUPERSUCK, IE-NW/EASKEY, IE-SW/AILEEN'S, LK-E/WHISKEY POINT, MA-N/SAFI LE JARDIN, MV-NMA/PASTA POINT, MV-NMA/SULTANS, MV-NMA/HONKY'S, MV-NMA/COKES, MV-NMA/CHICKENS, MV-NMA/JAILBREAKS, MV-SOU/TIGER STRIPES, MV-SOU/BEACONS, MX-BCS/ZIPPERS, NA-ERO/SKELETON BAY, NZ-GIS/CENTRES, NZ-GIS/WHALES, NZ-GIS/THE ISLAND, NZ-KAI/MEATWORKS, NZ-NTL/SUPER TUBES, NZ-NTL/MUKIES 2, NZ-NTL/MUKIES 1, NZ-NTL/PEAKS, NZ-RAG/INDICATORS, PH-SIA/JACKING HORSE, SV-ORI/LAS FLORES, US-HI-BIG/BANYANS, US-HI-KAU/PK'S, US-HI-OAN/BACKDOOR, US-NE/RUGGLES, ZA-EC-JB/BRUCE'S BEAUTIES, ZA-WC-CPT/DUNGEONS, ZA-WC-CPT/SUNSET REEF

## Zonas

| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |
|---|---|---|---|
| AR-BAN | ncep_gfswave025 | 0.9 m | 89 % |
| AR-MDP | ncep_gfswave025 | 0.9 m | 62 % |
| AR-SUR | ncep_gfswave025 | 0.7 m | 60 % |
| AU-NSW-MN | ncep_gfswave025 | 1.4 m | 48 % |
| AU-NSW-NC | ncep_gfswave025 | 1.4 m | 69 % |
| AU-NSW-NR | ncep_gfswave025 | 1.4 m | 45 % |
| AU-NSW-SC | ncep_gfswave025 | 1.5 m | 51 % |
| AU-NSW-SYD | ncep_gfswave025 | 1.6 m | 46 % |
| AU-QLD-GC | ncep_gfswave025 | 0.9 m | 77 % |
| AU-QLD-SC | ncep_gfswave025 | 0.9 m | 86 % |
| AU-SA-EYR | ncep_gfswave025 | 1.3 m | 100 % |
| AU-SA | ecmwf_wam | 1.3 m | 83 % |
| AU-TAS | ncep_gfswave025 | 1.2 m | 39 % |
| AU-VIC-PI | ncep_gfswave025 | 1.3 m | 100 % |
| AU-VIC-SC | ncep_gfswave025 | 1.2 m | 91 % |
| AU-VIC-W | ncep_gfswave025 | 2.4 m | 91 % |
| AU-WA-GAS | ncep_gfswave025 | 1.3 m | 100 % |
| AU-WA-MR | ncep_gfswave025 | 2.3 m | 100 % |
| AU-WA-NW | ncep_gfswave025 | 1.8 m | 97 % |
| AU-WA-PER | ncep_gfswave025 | 1.6 m | 99 % |
| BB-ALL | ncep_gfswave016 | 1.1 m | 59 % |
| BR-BA | ncep_gfswave025 | 1.2 m | 90 % |
| BR-ES | ncep_gfswave025 | 1.1 m | 92 % |
| BR-NE-CE | ncep_gfswave016 | 1.0 m | 94 % |
| BR-NE-PE | ncep_gfswave016 | 1.0 m | 100 % |
| BR-NE-RN | ncep_gfswave016 | 0.9 m | 100 % |
| BR-NOR | ncep_gfswave016 | 1.2 m | 50 % |
| BR-RJ | ncep_gfswave025 | 0.8 m | 100 % |
| BR-RJL | ncep_gfswave025 | 1.1 m | 75 % |
| BR-RS-SUL | ncep_gfswave025 | 0.9 m | 99 % |
| BR-RS | ncep_gfswave025 | 1.2 m | 97 % |
| BR-SC-FLN | ncep_gfswave025 | 1.4 m | 75 % |
| BR-SC-NOR | ncep_gfswave025 | 0.9 m | 99 % |
| BR-SC-SUL | ncep_gfswave025 | 1.3 m | 85 % |
| BR-SP | ncep_gfswave025 | 0.8 m | 86 % |
| BS-ALL | ncep_gfswave016 | 1.7 m | 0 % |
| CA-BC-VI | ecmwf_wam | 2.0 m | 68 % |
| CA-NS | ncep_gfswave016 | 0.8 m | 51 % |
| CL-CEN | ncep_gfswave025 | 1.8 m | 54 % |
| CL-MAU | ncep_gfswave025 | 1.5 m | 99 % |
| CL-NOR | ncep_gfswave025 | 1.7 m | 100 % |
| CL-PIC | ncep_gfswave025 | 2.0 m | 98 % |
| CL-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| CN-HAI | ncep_gfswave016 | 1.0 m | 13 % |
| CO-CAR | ncep_gfswave016 | 0.6 m | 95 % |
| CO-PAC | ncep_gfswave016 | 0.8 m | 100 % |
| CR-CAR | ncep_gfswave016 | 0.6 m | 100 % |
| CR-GUA | ncep_gfswave016 | 1.1 m | 100 % |
| CR-NIC | ncep_gfswave016 | 1.0 m | 100 % |
| CR-OSA | ncep_gfswave016 | 1.1 m | 95 % |
| CR-PAC | ncep_gfswave016 | 1.0 m | 100 % |
| CV-ALL | ncep_gfswave016 | 1.2 m | 89 % |
| DE-ALL | ncep_gfswave025 | 1.0 m | 79 % |
| DK-ALL | ncep_gfswave025 | 1.4 m | 82 % |
| DO-ALL | ncep_gfswave016 | 1.2 m | 100 % |
| EC-COS | ncep_gfswave016 | 0.8 m | 100 % |
| EC-GAL | ncep_gfswave016 | 1.1 m | 100 % |
| ES-AND | ncep_gfswave016 | 0.5 m | 91 % |
| ES-AST | ncep_gfswave016 | 1.4 m | 85 % |
| ES-CAN | ncep_gfswave016 | 1.3 m | 95 % |
| ES-CN-E | ncep_gfswave016 | 1.2 m | 96 % |
| ES-CN-W | ncep_gfswave016 | 1.0 m | 62 % |
| ES-GAL | ncep_gfswave016 | 1.7 m | 70 % |
| ES-PV | ncep_gfswave016 | 1.2 m | 90 % |
| FJ-MAM | ncep_gfswave025 | 0.4 m | 100 % |
| FJ-SOU | ncep_gfswave025 | 1.2 m | 89 % |
| FR-BRE | ncep_gfswave016 | 1.3 m | 95 % |
| FR-GIR | ncep_gfswave016 | 1.5 m | 96 % |
| FR-HOS | ncep_gfswave016 | 1.4 m | 97 % |
| FR-PBA | ncep_gfswave016 | 1.4 m | 100 % |
| FR-VEN | ncep_gfswave016 | 1.1 m | 89 % |
| GB-CON | ncep_gfswave016 | 1.7 m | 92 % |
| GB-DEV | ncep_gfswave016 | 1.4 m | 92 % |
| GB-NE | ncep_gfswave025 | 0.9 m | 47 % |
| GB-NIR | ecmwf_wam | 1.0 m | 60 % |
| GB-SCO | ncep_gfswave025 | 1.3 m | 34 % |
| GB-SOU | ncep_gfswave016 | 0.9 m | 67 % |
| GB-WAL | ncep_gfswave025 | 1.4 m | 86 % |
| GH-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| GP-ALL | ncep_gfswave016 | 1.1 m | 0 % |
| GT-PAC | ncep_gfswave016 | 1.1 m | 100 % |
| ID-BAL-BUK | ncep_gfswave016 | 1.5 m | 100 % |
| ID-BAL-E | ncep_gfswave016 | 1.0 m | 74 % |
| ID-BAL-W | ncep_gfswave016 | 1.0 m | 100 % |
| ID-JAV-E | ncep_gfswave016 | 1.4 m | 100 % |
| ID-JAV-W | ncep_gfswave016 | 1.4 m | 95 % |
| ID-KRU | ncep_gfswave016 | 1.5 m | 100 % |
| ID-LOM | ncep_gfswave016 | 1.4 m | 99 % |
| ID-MEN | ncep_gfswave016 | 1.1 m | 100 % |
| ID-NIA | ncep_gfswave016 | 1.1 m | 100 % |
| ID-ROT | ncep_gfswave016 | 0.9 m | 100 % |
| ID-SBW | ncep_gfswave016 | 1.1 m | 100 % |
| ID-SMB | ncep_gfswave016 | 1.3 m | 100 % |
| IE-NW | ncep_gfswave025 | 1.8 m | 100 % |
| IE-SE | ncep_gfswave016 | 1.6 m | 58 % |
| IE-SW | ecmwf_wam | 1.4 m | 90 % |
| IN-E | ncep_gfswave016 | 0.8 m | 94 % |
| IN-W | ncep_gfswave016 | 0.8 m | 91 % |
| IS-ALL | ncep_gfswave025 | 2.7 m | 90 % |
| IT-ALL | ncep_gfswave016 | 0.4 m | 53 % |
| IT-SAR | ncep_gfswave016 | 0.8 m | 97 % |
| JP-CHI | ncep_gfswave016 | 1.6 m | 75 % |
| JP-IBA | ncep_gfswave016 | 1.3 m | 82 % |
| JP-IZU | ncep_gfswave016 | 1.1 m | 40 % |
| JP-KYU | ncep_gfswave016 | 1.2 m | 74 % |
| JP-SHK | ncep_gfswave016 | 1.3 m | 97 % |
| JP-SHO | ncep_gfswave016 | 0.9 m | 71 % |
| KR-ALL | ncep_gfswave016 | 1.0 m | 24 % |
| LK-E | ncep_gfswave016 | 1.4 m | 58 % |
| LK-S | ncep_gfswave016 | 1.2 m | 100 % |
| LR-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| MA-N | ncep_gfswave016 | 1.2 m | 98 % |
| MA-S | ncep_gfswave016 | 1.1 m | 100 % |
| MA-TAG | ncep_gfswave016 | 0.8 m | 100 % |
| MG-ALL | ncep_gfswave025 | 1.8 m | 46 % |
| MQ-ALL | ncep_gfswave016 | 1.1 m | 70 % |
| MU-ALL | ncep_gfswave025 | 1.2 m | 95 % |
| MV-CEN | ncep_gfswave016 | 0.9 m | 100 % |
| MV-NMA | ncep_gfswave016 | 0.9 m | 97 % |
| MV-SMA | ncep_gfswave016 | 0.9 m | 97 % |
| MV-SOU | ncep_gfswave016 | 1.0 m | 55 % |
| MX-BCN | ecmwf_wam | 1.2 m | 93 % |
| MX-BCS-N | ncep_gfswave016 | 0.9 m | 95 % |
| MX-BCS | ncep_gfswave016 | 0.9 m | 98 % |
| MX-CAR | ncep_gfswave016 | 0.5 m | 39 % |
| MX-NAY | ncep_gfswave016 | 0.7 m | 99 % |
| MX-OAX | ncep_gfswave016 | 1.2 m | 100 % |
| MX-PAC | ncep_gfswave016 | 1.4 m | 94 % |
| MZ-INH | ncep_gfswave025 | 1.0 m | 95 % |
| MZ-S | ncep_gfswave025 | 1.5 m | 40 % |
| NA-ERO | ncep_gfswave025 | 1.6 m | 100 % |
| NI-NW | ncep_gfswave016 | 1.1 m | 100 % |
| NI-RIV | ncep_gfswave016 | 1.1 m | 100 % |
| NL-ALL | ncep_gfswave025 | 1.0 m | 63 % |
| NO-N | ncep_gfswave025 | 2.4 m | 60 % |
| NO-S | ncep_gfswave025 | 1.5 m | 85 % |
| NZ-AKL | ncep_gfswave025 | 2.0 m | 100 % |
| NZ-BOP | ncep_gfswave025 | 0.7 m | 76 % |
| NZ-GIS | ncep_gfswave025 | 1.1 m | 57 % |
| NZ-KAI | ncep_gfswave025 | 0.9 m | 60 % |
| NZ-NTL | ncep_gfswave025 | 1.1 m | 91 % |
| NZ-OTA | ncep_gfswave025 | 1.3 m | 31 % |
| NZ-RAG | ncep_gfswave025 | 1.7 m | 100 % |
| NZ-TAR | ncep_gfswave025 | 1.7 m | 32 % |
| NZ-WC | ncep_gfswave025 | 1.9 m | 69 % |
| NZ-WEL | ncep_gfswave025 | 1.6 m | 66 % |
| PA-BDT | ncep_gfswave016 | 0.7 m | 87 % |
| PA-PAC | ncep_gfswave016 | 0.3 m | 100 % |
| PE-LIM | ncep_gfswave025 | 1.8 m | 100 % |
| PE-LLB | ncep_gfswave016 | 1.2 m | 100 % |
| PE-NOR | ncep_gfswave016 | 0.9 m | 69 % |
| PE-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| PF-ISL | ncep_gfswave025 | 1.9 m | 56 % |
| PF-TAH | ncep_gfswave025 | 2.0 m | 94 % |
| PG-ALL | ncep_gfswave016 | 0.8 m | 63 % |
| PH-EAS | ncep_gfswave016 | 1.2 m | 93 % |
| PH-LUZ | ncep_gfswave016 | 0.7 m | 100 % |
| PH-SIA | ncep_gfswave016 | 1.1 m | 95 % |
| PR-N | ncep_gfswave016 | 1.1 m | 99 % |
| PR-NW | ncep_gfswave016 | 1.0 m | 100 % |
| PT-ALG | ncep_gfswave016 | 1.5 m | 99 % |
| PT-AZO | ncep_gfswave016 | 1.5 m | 15 % |
| PT-CEN | ncep_gfswave016 | 1.5 m | 98 % |
| PT-ERI | ncep_gfswave016 | 1.6 m | 89 % |
| PT-LIS | ncep_gfswave016 | 1.2 m | 85 % |
| PT-MAD | ncep_gfswave016 | 1.2 m | 75 % |
| PT-NOR | ncep_gfswave016 | 1.5 m | 91 % |
| PT-PEN | ncep_gfswave016 | 1.6 m | 89 % |
| RE-ALL | ncep_gfswave025 | 1.2 m | 75 % |
| SN-ALL | ncep_gfswave016 | 1.4 m | 99 % |
| SV-LIB | ncep_gfswave016 | 1.1 m | 100 % |
| SV-ORI | ncep_gfswave016 | 1.1 m | 100 % |
| TO-ALL | ncep_gfswave025 | 1.5 m | 58 % |
| TT-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| TW-E | ncep_gfswave016 | 1.3 m | 53 % |
| TW-NE | ncep_gfswave016 | 1.3 m | 82 % |
| US-CA-CEN | ecmwf_wam | 1.6 m | 94 % |
| US-CA-LA | ecmwf_wam | 0.9 m | 100 % |
| US-CA-NOR | ecmwf_wam | 2.0 m | 100 % |
| US-CA-OC | ecmwf_wam | 1.0 m | 100 % |
| US-CA-SB | ecmwf_wam | 0.8 m | 96 % |
| US-CA-SC | ecmwf_wam | 1.3 m | 87 % |
| US-CA-SD | ncep_gfswave016 | 0.8 m | 94 % |
| US-CA-SF | ecmwf_wam | 1.5 m | 100 % |
| US-FL-PAN | ecmwf_wam | 0.6 m | 54 % |
| US-FL | ncep_gfswave016 | 1.7 m | 100 % |
| US-GULF | ecmwf_wam | 0.5 m | 92 % |
| US-HI-BIG | ecmwf_wam | 1.0 m | 73 % |
| US-HI-KAU | ecmwf_wam | 2.0 m | 86 % |
| US-HI-MAU | ecmwf_wam | 1.7 m | 58 % |
| US-HI-OAN | ncep_gfswave016 | 1.7 m | 91 % |
| US-HI-OAS | ecmwf_wam | 1.1 m | 60 % |
| US-MID | ncep_gfswave025 | 0.7 m | 98 % |
| US-NE | ecmwf_wam | 0.6 m | 73 % |
| US-PNW | ecmwf_wam | 2.1 m | 100 % |
| US-SC-GA | ncep_gfswave016 | 0.9 m | 93 % |
| US-SE | ncep_gfswave025 | 1.3 m | 98 % |
| UY-CAN | ncep_gfswave025 | 0.7 m | 57 % |
| UY-MAL | ncep_gfswave025 | 1.0 m | 76 % |
| UY-ROC | ncep_gfswave025 | 1.1 m | 52 % |
| VE-ALL | ncep_gfswave016 | 0.5 m | 92 % |
| VN-ALL | ncep_gfswave016 | 0.6 m | 100 % |
| VU-ALL | ncep_gfswave025 | 1.1 m | 21 % |
| WS-ALL | ncep_gfswave025 | 1.8 m | 78 % |
| ZA-EC-JB | ncep_gfswave025 | 1.9 m | 98 % |
| ZA-EC-PE | ncep_gfswave025 | 2.0 m | 19 % |
| ZA-EC-WLD | ncep_gfswave025 | 1.7 m | 42 % |
| ZA-KZN-DBN | ncep_gfswave025 | 1.7 m | 62 % |
| ZA-KZN-N | ncep_gfswave025 | 1.7 m | 69 % |
| ZA-KZN-S | ncep_gfswave025 | 1.8 m | 51 % |
| ZA-WC-CPT | ncep_gfswave025 | 1.8 m | 82 % |
| ZA-WC-GR | ncep_gfswave025 | 1.7 m | 94 % |
| ZA-WC-WCO | ncep_gfswave025 | 1.6 m | 0 % |
