# Picos: controles por pico

Generado 2026-11-05 08:28 UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). 213 regiones, 2511 picos.

- **Orientación (§5.2):** olas de los últimos 14 días y los próximos 2 en el punto de olas de cada pico (el modelo de su zona). Se marca un pico al que las olas de al menos 0.3 m casi nunca le llegan a menos de 55° de hacia donde mira, o de su ventana de swell si la tiene (menos del 5 % de las horas) mientras a su zona sí (al menos 25 %).
- **Zona entera:** en una zona donde la mayoría tampoco las recibe de frente (menos del 25 %) los vecinos no dicen nada: ahí se marca el pico con mar (olas de al menos 0.3 m en el 25 % de las horas o más) que casi nunca las recibe de frente.
- **Temporada:** los marcados por la orientación se miran de nuevo con 92 días de olas; 47 dejaron de estarlo (en dos semanas no les tocaba su ventana de swell).
- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media de su zona.
- **Emblemáticos (§5.8):** la posición contra fuentes públicas (el ítem más cercano con su nombre en Wikidata o GeoNames, hasta 6 km; si no, OpenStreetMap; si no, el ítem de otro nombre del que se tomó a mano la posición, en el `src` de la semilla): 319 bien (a menos de 1.5 km; 12 de ellos por la fuente de su semilla), 0 lejos, 21 lejos pero revisados a mano (el ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), 52 sin fuente (revisar a mano; `validation/lookup.md` tiene lo que hay con su nombre alrededor), 0 sin respuesta.
- Open-Meteo: 35 pedidos, ~2390 llamadas de las 10.000 diarias gratuitas.

## Orientación probablemente del lado equivocado (1)

Mira a más de 135° de sus vecinos (a 30 km) y de las olas, y dada vuelta coincide con ellos: casi seguro se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla.

| Región | Pico | Mira a | Vecinos | Olas desde |
|---|---|---|---|---|
| CA-BC-VI | SCHOONER COVE | 44° | 204° | 241° |

## Zonas enteras que casi nunca reciben las olas de frente (2)

Zonas con 3 picos o más que, en 92 días, casi nunca recibieron las olas de frente aunque había mar, y a las que la comparación con los vecinos no ve porque están todos igual. O la orientación de toda la costa se calculó del lado equivocado, o son reefs y puntas a los que el swell entra dando la vuelta: ahí la orientación de la costa está bien para el viento y lo que falta es la ventana de swell del pico.

| Región | Marcados | Puntas y reefs | Miran a | Olas desde | Picos |
|---|---|---|---|---|---|
| CL-CEN | 10 de 20 | 0 | 344° | 234° | PICHICUY, PAPUDO, MAITENCILLO, HORCÓN, LA BOCA, AMARILLA, TUNQUÉN, ALGARROBO, EL QUISCO, CARTAGENA |
| ZA-WC-WCO | 4 de 6 | 0 | 325° | 235° | MELKBOS, LAMBERTS BAY, JACOBSBAAI, YZERFONTEIN |

## Picos marcados (138)

Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y el semáforo del swell es conservador ahí); se revisan a mano.

| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |
|---|---|---|---|---|---|---|
| AU-NSW-NC | OCEAN BEACH |  | 250° | 127° | 117° | las olas casi nunca le entran de frente (1 % de las horas; la zona 59 %) y en 92 días 0 % |
| AU-SA | CHINAMANS |  | 325° | 235° | 250° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| AU-TAS | CLIFTON BEACH | sí | 119° | 207° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 43 %) y en 92 días 3 % |
| AU-TAS | MARION BAY |  | 269° | 87° | 146° | las olas casi nunca le entran de frente (0 % de las horas; la zona 43 %) y en 92 días 2 % |
| AU-TAS | MARRAWAH |  | 314° | 230° | — | 2.7 m de media, más del doble de la zona (1.2 m); las olas casi nunca le entran de frente (1 % de las horas; la zona 43 %) y en 92 días 1 % |
| AU-TAS | GREEN POINT |  | 290° | 230° | — | 2.7 m de media, más del doble de la zona (1.2 m) |
| AU-VIC-PI | FOREST CAVES |  | 127° | 223° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-VIC-SC | JAN JUC |  | 118° | 221° | 154° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| AU-VIC-SC | POINT ADDIS |  | 91° | 221° | 151° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| AU-VIC-W | WYE RIVER |  | 110° | 229° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| AU-VIC-W | KENNETT RIVER |  | 117° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| AU-VIC-W | PORT FAIRY EAST |  | 140° | 219° | 229° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BB-ALL | DRILL HALL |  | 180° | 5° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 4 % |
| BR-NE-PE | GAIBU |  | 31° | 107° | 105° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 0 % |
| BR-SP | FAZENDA |  | 260° | 145° | 125° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 0 % |
| BR-SP | MARANDUBA |  | 234° | 137° | 141° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BR-SP | PAÚBA |  | 264° | 151° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| BR-SP | CAMBURI |  | 261° | 151° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| BR-SP | ILHA COMPRIDA |  | 269° | 140° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BS-ALL | SURFERS BEACH |  | 168° | 40° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| CA-BC-VI | SCHOONER COVE |  | 44° | 241° | 204° | las olas casi nunca le entran de frente (0 % de las horas; la zona 64 %) y en 92 días 0 % |
| CA-BC-VI | WYA POINT |  | 90° | 246° | 210° | las olas casi nunca le entran de frente (0 % de las horas; la zona 64 %) y en 92 días 0 % |
| CA-BC-VI | CHINA BEACH |  | 202° | 279° | 218° | las olas casi nunca le entran de frente (2 % de las horas; la zona 64 %) y en 92 días 1 % |
| CL-CEN | PICHICUY |  | 150° | 230° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 0 % |
| CL-CEN | PAPUDO |  | 19° | 237° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 0 % |
| CL-CEN | MAITENCILLO | sí | 323° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 2 % |
| CL-CEN | HORCÓN |  | 45° | 232° | 291° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 0 % |
| CL-CEN | LA BOCA |  | 314° | 232° | 277° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 2 % |
| CL-CEN | AMARILLA |  | 341° | 232° | 272° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 1 % |
| CL-CEN | TUNQUÉN |  | 335° | 236° | 281° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 1 % |
| CL-CEN | ALGARROBO |  | 339° | 236° | 293° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 1 % |
| CL-CEN | EL QUISCO |  | 335° | 235° | 294° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 1 % |
| CL-CEN | CARTAGENA |  | 325° | 235° | 281° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (4 %) y en 92 días 3 % |
| CL-MAU | LLICO |  | 344° | 238° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 3 % |
| CL-MAU | CURANIPE |  | 346° | 244° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 5 % |
| CL-NOR | LAS MACHAS |  | 324° | 223° | 280° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CL-PIC | MATANZAS |  | 338° | 244° | 325° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 2 % |
| CL-PIC | PLAYA PRINCIPAL |  | 344° | 234° | 307° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 2 % |
| CL-PIC | LAS TERRAZAS |  | 313° | 234° | 311° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 4 % |
| CO-PAC | HUINA |  | 312° | 228° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CO-PAC | NUQUÍ |  | 303° | 239° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 100 %) y en 92 días 3 % |
| CR-GUA | TAMARINDO | sí | 312° | 226° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-NIC | SAMARA |  | 146° | 210° | 225° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 4 % |
| CR-OSA | RIO CLARO |  | 308° | 214° | 246° | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 0 % |
| CV-ALL | SANTA MARIA |  | 193° | 354° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 89 %) y en 92 días 0 % |
| EC-COS | BALLENITA |  | 317° | 237° | 296° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ES-AND | REGLA |  | 7° | 269° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ES-AND | ZAHORA |  | 172° | 260° | 234° | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 3 % |
| ES-AND | BOLONIA |  | 191° | 286° | 226° | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 1 % |
| ES-AST | XAGO |  | 82° | 332° | 1° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| ES-CN-E | FLAG BEACH |  | 88° | 333° | 274° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ES-CN-W | PLAYA DEL HOMBRE |  | 89° | 356° | 325° | las olas casi nunca le entran de frente (0 % de las horas; la zona 70 %) y en 92 días 3 % |
| ES-CN-W | SARDINA |  | 215° | 344° | 330° | las olas casi nunca le entran de frente (0 % de las horas; la zona 70 %) y en 92 días 0 % |
| ES-CN-W | EL MEDANO |  | 119° | 108° | 285° | las olas casi nunca le entran de frente (1 % de las horas; la zona 70 %) y en 92 días 2 % |
| ES-GAL | DONIÑOS |  | 225° | 313° | 343° | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 2 % |
| ES-GAL | TRABA |  | 202° | 313° | 343° | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 1 % |
| ES-PV | LAGA |  | 73° | 329° | 352° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| ES-PV | MUNDAKA | sí | 64° | 329° | 351° | las olas casi nunca le entran de frente (1 % de las horas; la zona 91 %) y en 92 días 1 % |
| ES-PV | PLENTZIA |  | 96° | 328° | 349° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| FJ-MAM | CLOUDBREAK | sí | 220° | 206° | 254° | 1.0 m de media, más del doble de la zona (0.4 m) |
| FR-BRE | LE POULDU |  | 132° | 246° | 221° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| FR-VEN | LA TRANCHE |  | 151° | 263° | 211° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| GB-CON | PORTHCOTHAN |  | 194° | 277° | 317° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| GB-DEV | WESTWARD HO |  | 345° | 269° | 266° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 3 % |
| GB-DEV | THURLESTONE |  | 326° | 229° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 3 % |
| GB-SCO | STRATHY |  | 77° | 286° | 358° | las olas casi nunca le entran de frente (0 % de las horas; la zona 33 %) y en 92 días 3 % |
| GB-SCO | GOTT BAY |  | 138° | 243° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 33 %) y en 92 días 2 % |
| GB-WAL | BROAD HAVEN SOUTH |  | 149° | 243° | 229° | las olas casi nunca le entran de frente (1 % de las horas; la zona 81 %) y en 92 días 4 % |
| GB-WAL | RHOSSILI |  | 336° | 243° | 203° | las olas casi nunca le entran de frente (0 % de las horas; la zona 81 %) y en 92 días 1 % |
| GB-WAL | LANGLAND BAY |  | 120° | 244° | 249° | las olas casi nunca le entran de frente (3 % de las horas; la zona 81 %) y en 92 días 4 % |
| GB-WAL | LLANTWIT MAJOR |  | 199° | 272° | 244° | las olas casi nunca le entran de frente (2 % de las horas; la zona 81 %) y en 92 días 3 % |
| GP-ALL | TARARE |  | 180° | 85° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| GP-ALL | PORT LOUIS |  | 270° | 33° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | DREAMLAND |  | 286° | 206° | 321° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | PURNAMA |  | 133° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| ID-BAL-E | SABA |  | 130° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| ID-BAL-E | LEBIH |  | 132° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| ID-JAV-W | PANGANDARAN |  | 280° | 198° | 100° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| ID-JAV-W | MADASARI |  | 119° | 194° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| ID-LOM | SELONG BELANAK |  | 296° | 211° | 182° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | MAWUN |  | 133° | 211° | 190° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-LOM | KUTA LOMBOK |  | 140° | 211° | 189° | las olas casi nunca le entran de frente (1 % de las horas; la zona 99 %) y en 92 días 0 % |
| IE-NW | TULLAN STRAND |  | 358° | 285° | 307° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| IE-NW | KEEL |  | 186° | 273° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 3 % |
| IE-SW | INCH |  | 172° | 260° | 268° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 3 % |
| LR-ALL | COTTON TREE |  | 310° | 202° | 311° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-S | TIFNIT |  | 230° | 308° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | AGADIR |  | 186° | 311° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | MADRABA |  | 234° | 305° | 229° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-NAY | LO DE MARCOS |  | 311° | 230° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 3 % |
| MX-NAY | SAN PANCHO |  | 297° | 217° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 4 % |
| MX-OAX | MAZUNTE |  | 123° | 210° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-PAC | MIRAMAR |  | 314° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| NA-ERO | SKELETON BAY | sí | 321° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| NZ-BOP | ONEMANA |  | 164° | 29° | 55° | las olas casi nunca le entran de frente (0 % de las horas; la zona 74 %) y en 92 días 4 % |
| NZ-NTL | SHIPWRECK BAY | sí | 225° | 226° | 19° | 2.0 m de media, más del doble de la zona (1.0 m) |
| NZ-NTL | SUPER TUBES | sí | 225° | 226° | 27° | 2.0 m de media, más del doble de la zona (1.0 m) |
| NZ-NTL | MUKIES 2 | sí | 225° | 226° | 20° | 2.0 m de media, más del doble de la zona (1.0 m) |
| NZ-NTL | MUKIES 1 | sí | 225° | 226° | 23° | 2.0 m de media, más del doble de la zona (1.0 m) |
| NZ-NTL | PEAKS | sí | 225° | 226° | 25° | 2.0 m de media, más del doble de la zona (1.0 m) |
| NZ-NTL | MATAURI BAY |  | 224° | 31° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 91 %) y en 92 días 1 % |
| NZ-NTL | BAYLYS BEACH |  | 235° | 228° | — | 2.1 m de media, más del doble de la zona (1.0 m) |
| NZ-OTA | PORPOISE BAY |  | 103° | 214° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 4 % |
| NZ-OTA | COLAC BAY |  | 182° | 259° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| NZ-WC | TAURANGA BAY |  | 34° | 276° | — | las olas casi nunca le entran de frente (5 % de las horas; la zona 69 %) y en 92 días 1 % |
| PA-PAC | PLAYA VENAO | sí | 235° | 212° | — | 1.0 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | GUANICO |  | 153° | 202° | 209° | 0.8 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | CAMBUTAL |  | 183° | 214° | — | 1.1 m de media, más del doble de la zona (0.3 m) |
| PE-LIM | AGUA DULCE |  | 291° | 216° | 232° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| PR-NW | CRASH BOAT |  | 231° | 8° | 286° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PR-NW | SANDY BEACH |  | 235° | 5° | 286° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PR-NW | CÓRCEGA |  | 246° | 5° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PT-ALG | ZAVIAL |  | 173° | 289° | 278° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| PT-AZO | SANTA BÁRBARA | sí | 343° | 244° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (15 %) y en 92 días 1 % |
| PT-AZO | ALMOXARIFE |  | 91° | 291° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (15 %) y en 92 días 0 % |
| PT-MAD | MACHICO |  | 122° | 339° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 0 % |
| PT-NOR | MATOSINHOS | sí | 181° | 298° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| RE-ALL | BOUCAN CANOT |  | 312° | 214° | 265° | las olas casi nunca le entran de frente (0 % de las horas; la zona 78 %) y en 92 días 0 % |
| RE-ALL | BARACHOIS |  | 325° | 125° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 78 %) y en 92 días 0 % |
| US-CA-CEN | PIRATE'S COVE |  | 175° | 273° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 3 % |
| US-CA-CEN | ANDREW MOLERA |  | 186° | 287° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 4 % |
| US-CA-NOR | NORTH JETTY |  | 19° | 304° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-CA-SB | SANDSPIT |  | 112° | 205° | 193° | las olas casi nunca le entran de frente (1 % de las horas; la zona 99 %) y en 92 días 0 % |
| US-CA-SC | MORAN LAKE |  | 130° | 256° | 200° | las olas casi nunca le entran de frente (0 % de las horas; la zona 87 %) y en 92 días 0 % |
| US-CA-SC | CAPITOLA |  | 157° | 256° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 87 %) y en 92 días 3 % |
| US-CA-SD | LA JOLLA SHORES |  | 298° | 210° | 254° | las olas casi nunca le entran de frente (2 % de las horas; la zona 92 %) y en 92 días 1 % |
| US-CA-SD | MARINE STREET |  | 293° | 210° | 254° | las olas casi nunca le entran de frente (2 % de las horas; la zona 92 %) y en 92 días 1 % |
| US-PNW | PORT ORFORD |  | 162° | 290° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-SE | OCRACOKE |  | 262° | 109° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ZA-EC-PE | HOBIE BEACH |  | 31° | 189° | 132° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| ZA-WC-CPT | LLANDUDNO | sí | 311° | 232° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 84 %) y en 92 días 0 % |
| ZA-WC-CPT | LONG BEACH | sí | 344° | 231° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 84 %) y en 92 días 0 % |
| ZA-WC-CPT | KOGEL BAY |  | 332° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 84 %) y en 92 días 0 % |
| ZA-WC-GR | SANTOS |  | 50° | 202° | 147° | las olas casi nunca le entran de frente (0 % de las horas; la zona 94 %) y en 92 días 0 % |
| ZA-WC-WCO | MELKBOS |  | 310° | 236° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ZA-WC-WCO | LAMBERTS BAY |  | 320° | 238° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | JACOBSBAAI |  | 318° | 230° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | YZERFONTEIN |  | 351° | 234° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |

## Emblemáticos lejos de su ítem en Wikidata, GeoNames u OpenStreetMap

Ninguno.

## Emblemáticos sin fuente en Wikidata, GeoNames ni OpenStreetMap (revisar a mano)

AU-NSW-SYD/OURS, AU-VIC-SC/WINKIPOP, AU-WA-MR/MAIN BREAK, AU-WA-MR/NORTH POINT, CL-NOR/EL GRINGO, CR-GUA/WITCH'S ROCK, CR-OSA/PAVONES, ES-CN-E/EL QUEMAO, ES-CN-W/EL FRONTON, ES-CN-W/LA IZQUIERDA, FJ-MAM/CLOUDBREAK, FJ-MAM/RESTAURANTS, FJ-MAM/SWIMMING POOLS, ID-BAL-E/SHIPWRECKS, ID-JAV-E/MONEY TREES, ID-MEN/MACARONIS, ID-MEN/KANDUI LEFT, ID-MEN/RIFLES, ID-ROT/T-LAND, ID-SBW/SUPERSUCK, IE-NW/EASKEY, IE-SW/AILEEN'S, LK-E/WHISKEY POINT, MA-N/SAFI LE JARDIN, MV-NMA/PASTA POINT, MV-NMA/SULTANS, MV-NMA/HONKY'S, MV-NMA/COKES, MV-NMA/CHICKENS, MV-NMA/JAILBREAKS, MV-SOU/TIGER STRIPES, MV-SOU/BEACONS, MX-BCS/ZIPPERS, NA-ERO/SKELETON BAY, NZ-GIS/CENTRES, NZ-GIS/WHALES, NZ-GIS/THE ISLAND, NZ-KAI/MEATWORKS, NZ-NTL/SUPER TUBES, NZ-NTL/MUKIES 2, NZ-NTL/MUKIES 1, NZ-NTL/PEAKS, NZ-RAG/INDICATORS, PH-SIA/JACKING HORSE, SV-ORI/LAS FLORES, US-HI-BIG/BANYANS, US-HI-KAU/PK'S, US-HI-OAN/BACKDOOR, US-NE/RUGGLES, ZA-EC-JB/BRUCE'S BEAUTIES, ZA-WC-CPT/DUNGEONS, ZA-WC-CPT/SUNSET REEF

## Zonas

| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |
|---|---|---|---|
| AR-BAN | ncep_gfswave025 | 0.9 m | 92 % |
| AR-MDP | ncep_gfswave025 | 0.9 m | 68 % |
| AR-SUR | ncep_gfswave025 | 0.8 m | 61 % |
| AU-NSW-MN | ncep_gfswave025 | 1.4 m | 55 % |
| AU-NSW-NC | ncep_gfswave025 | 1.3 m | 59 % |
| AU-NSW-NR | ncep_gfswave025 | 1.4 m | 54 % |
| AU-NSW-SC | ncep_gfswave025 | 1.4 m | 58 % |
| AU-NSW-SYD | ncep_gfswave025 | 1.5 m | 54 % |
| AU-QLD-GC | ncep_gfswave025 | 0.9 m | 77 % |
| AU-QLD-SC | ncep_gfswave025 | 0.9 m | 86 % |
| AU-SA-EYR | ncep_gfswave025 | 1.3 m | 100 % |
| AU-SA | ecmwf_wam | 1.3 m | 90 % |
| AU-TAS | ncep_gfswave025 | 1.2 m | 43 % |
| AU-VIC-PI | ncep_gfswave025 | 1.3 m | 100 % |
| AU-VIC-SC | ncep_gfswave025 | 1.1 m | 91 % |
| AU-VIC-W | ncep_gfswave025 | 2.4 m | 90 % |
| AU-WA-GAS | ncep_gfswave025 | 1.4 m | 100 % |
| AU-WA-MR | ncep_gfswave025 | 2.6 m | 100 % |
| AU-WA-NW | ncep_gfswave025 | 1.9 m | 97 % |
| AU-WA-PER | ncep_gfswave025 | 1.7 m | 99 % |
| BB-ALL | ncep_gfswave016 | 1.1 m | 65 % |
| BR-BA | ncep_gfswave025 | 1.2 m | 90 % |
| BR-ES | ncep_gfswave025 | 1.1 m | 94 % |
| BR-NE-CE | ncep_gfswave016 | 1.0 m | 90 % |
| BR-NE-PE | ncep_gfswave016 | 1.0 m | 100 % |
| BR-NE-RN | ncep_gfswave016 | 0.9 m | 100 % |
| BR-NOR | ncep_gfswave016 | 1.2 m | 55 % |
| BR-RJ | ncep_gfswave025 | 0.9 m | 100 % |
| BR-RJL | ncep_gfswave025 | 1.1 m | 75 % |
| BR-RS-SUL | ncep_gfswave025 | 0.9 m | 99 % |
| BR-RS | ncep_gfswave025 | 1.3 m | 97 % |
| BR-SC-FLN | ncep_gfswave025 | 1.3 m | 85 % |
| BR-SC-NOR | ncep_gfswave025 | 0.9 m | 100 % |
| BR-SC-SUL | ncep_gfswave025 | 1.3 m | 88 % |
| BR-SP | ncep_gfswave025 | 0.8 m | 90 % |
| BS-ALL | ncep_gfswave016 | 1.8 m | 0 % |
| CA-BC-VI | ecmwf_wam | 1.7 m | 64 % |
| CA-NS | ncep_gfswave016 | 1.0 m | 51 % |
| CL-CEN | ncep_gfswave025 | 1.7 m | 4 % |
| CL-MAU | ncep_gfswave025 | 1.5 m | 98 % |
| CL-NOR | ncep_gfswave025 | 1.7 m | 100 % |
| CL-PIC | ncep_gfswave025 | 1.9 m | 90 % |
| CL-SUR | ncep_gfswave025 | 1.6 m | 100 % |
| CN-HAI | ncep_gfswave016 | 1.0 m | 18 % |
| CO-CAR | ncep_gfswave016 | 0.6 m | 95 % |
| CO-PAC | ncep_gfswave016 | 0.8 m | 100 % |
| CR-CAR | ncep_gfswave016 | 0.7 m | 100 % |
| CR-GUA | ncep_gfswave016 | 1.1 m | 100 % |
| CR-NIC | ncep_gfswave016 | 1.0 m | 100 % |
| CR-OSA | ncep_gfswave016 | 1.1 m | 98 % |
| CR-PAC | ncep_gfswave016 | 1.0 m | 100 % |
| CV-ALL | ncep_gfswave016 | 1.2 m | 89 % |
| DE-ALL | ncep_gfswave025 | 1.1 m | 90 % |
| DK-ALL | ncep_gfswave025 | 1.5 m | 86 % |
| DO-ALL | ncep_gfswave016 | 1.2 m | 100 % |
| EC-COS | ncep_gfswave016 | 0.8 m | 100 % |
| EC-GAL | ncep_gfswave016 | 1.1 m | 100 % |
| ES-AND | ncep_gfswave016 | 0.5 m | 99 % |
| ES-AST | ncep_gfswave016 | 1.7 m | 91 % |
| ES-CAN | ncep_gfswave016 | 1.6 m | 95 % |
| ES-CN-E | ncep_gfswave016 | 1.3 m | 100 % |
| ES-CN-W | ncep_gfswave016 | 1.0 m | 70 % |
| ES-GAL | ncep_gfswave016 | 2.1 m | 75 % |
| ES-PV | ncep_gfswave016 | 1.5 m | 91 % |
| FJ-MAM | ncep_gfswave025 | 0.4 m | 100 % |
| FJ-SOU | ncep_gfswave025 | 1.2 m | 89 % |
| FR-BRE | ncep_gfswave016 | 1.8 m | 97 % |
| FR-GIR | ncep_gfswave016 | 1.9 m | 96 % |
| FR-HOS | ncep_gfswave016 | 1.8 m | 97 % |
| FR-PBA | ncep_gfswave016 | 1.8 m | 100 % |
| FR-VEN | ncep_gfswave016 | 1.4 m | 91 % |
| GB-CON | ncep_gfswave016 | 2.1 m | 91 % |
| GB-DEV | ncep_gfswave016 | 1.7 m | 93 % |
| GB-NE | ncep_gfswave025 | 1.0 m | 47 % |
| GB-NIR | ecmwf_wam | 1.0 m | 59 % |
| GB-SCO | ncep_gfswave025 | 1.4 m | 33 % |
| GB-SOU | ncep_gfswave016 | 1.1 m | 70 % |
| GB-WAL | ncep_gfswave025 | 1.6 m | 81 % |
| GH-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| GP-ALL | ncep_gfswave016 | 1.1 m | 0 % |
| GT-PAC | ncep_gfswave016 | 1.1 m | 100 % |
| ID-BAL-BUK | ncep_gfswave016 | 1.6 m | 100 % |
| ID-BAL-E | ncep_gfswave016 | 1.1 m | 75 % |
| ID-BAL-W | ncep_gfswave016 | 1.1 m | 100 % |
| ID-JAV-E | ncep_gfswave016 | 1.4 m | 100 % |
| ID-JAV-W | ncep_gfswave016 | 1.5 m | 95 % |
| ID-KRU | ncep_gfswave016 | 1.6 m | 100 % |
| ID-LOM | ncep_gfswave016 | 1.5 m | 99 % |
| ID-MEN | ncep_gfswave016 | 1.2 m | 100 % |
| ID-NIA | ncep_gfswave016 | 1.2 m | 100 % |
| ID-ROT | ncep_gfswave016 | 0.9 m | 100 % |
| ID-SBW | ncep_gfswave016 | 1.2 m | 100 % |
| ID-SMB | ncep_gfswave016 | 1.4 m | 100 % |
| IE-NW | ncep_gfswave025 | 2.0 m | 100 % |
| IE-SE | ncep_gfswave016 | 1.8 m | 60 % |
| IE-SW | ecmwf_wam | 1.6 m | 95 % |
| IN-E | ncep_gfswave016 | 0.8 m | 94 % |
| IN-W | ncep_gfswave016 | 0.8 m | 95 % |
| IS-ALL | ncep_gfswave025 | 2.7 m | 95 % |
| IT-ALL | ncep_gfswave016 | 0.6 m | 58 % |
| IT-SAR | ncep_gfswave016 | 0.9 m | 97 % |
| JP-CHI | ncep_gfswave016 | 1.7 m | 75 % |
| JP-IBA | ncep_gfswave016 | 1.3 m | 82 % |
| JP-IZU | ncep_gfswave016 | 1.2 m | 34 % |
| JP-KYU | ncep_gfswave016 | 1.4 m | 67 % |
| JP-SHK | ncep_gfswave016 | 1.4 m | 90 % |
| JP-SHO | ncep_gfswave016 | 1.0 m | 74 % |
| KR-ALL | ncep_gfswave016 | 1.0 m | 34 % |
| LK-E | ncep_gfswave016 | 1.4 m | 57 % |
| LK-S | ncep_gfswave016 | 1.3 m | 100 % |
| LR-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| MA-N | ncep_gfswave016 | 1.3 m | 99 % |
| MA-S | ncep_gfswave016 | 1.2 m | 100 % |
| MA-TAG | ncep_gfswave016 | 0.8 m | 100 % |
| MG-ALL | ncep_gfswave025 | 1.8 m | 36 % |
| MQ-ALL | ncep_gfswave016 | 1.1 m | 71 % |
| MU-ALL | ncep_gfswave025 | 1.1 m | 95 % |
| MV-CEN | ncep_gfswave016 | 0.9 m | 100 % |
| MV-NMA | ncep_gfswave016 | 0.9 m | 100 % |
| MV-SMA | ncep_gfswave016 | 0.9 m | 88 % |
| MV-SOU | ncep_gfswave016 | 1.0 m | 61 % |
| MX-BCN | ecmwf_wam | 1.2 m | 92 % |
| MX-BCS-N | ncep_gfswave016 | 1.0 m | 99 % |
| MX-BCS | ncep_gfswave016 | 1.0 m | 98 % |
| MX-CAR | ncep_gfswave016 | 0.5 m | 31 % |
| MX-NAY | ncep_gfswave016 | 0.7 m | 97 % |
| MX-OAX | ncep_gfswave016 | 1.2 m | 100 % |
| MX-PAC | ncep_gfswave016 | 1.4 m | 97 % |
| MZ-INH | ncep_gfswave025 | 1.0 m | 92 % |
| MZ-S | ncep_gfswave025 | 1.5 m | 37 % |
| NA-ERO | ncep_gfswave025 | 1.6 m | 100 % |
| NI-NW | ncep_gfswave016 | 1.1 m | 100 % |
| NI-RIV | ncep_gfswave016 | 1.1 m | 100 % |
| NL-ALL | ncep_gfswave025 | 1.1 m | 63 % |
| NO-N | ncep_gfswave025 | 2.1 m | 59 % |
| NO-S | ncep_gfswave025 | 1.7 m | 80 % |
| NZ-AKL | ncep_gfswave025 | 2.0 m | 100 % |
| NZ-BOP | ncep_gfswave025 | 0.6 m | 74 % |
| NZ-GIS | ncep_gfswave025 | 1.1 m | 69 % |
| NZ-KAI | ncep_gfswave025 | 0.9 m | 59 % |
| NZ-NTL | ncep_gfswave025 | 1.0 m | 91 % |
| NZ-OTA | ncep_gfswave025 | 1.3 m | 28 % |
| NZ-RAG | ncep_gfswave025 | 1.6 m | 100 % |
| NZ-TAR | ncep_gfswave025 | 1.7 m | 28 % |
| NZ-WC | ncep_gfswave025 | 1.9 m | 69 % |
| NZ-WEL | ncep_gfswave025 | 1.6 m | 62 % |
| PA-BDT | ncep_gfswave016 | 0.7 m | 88 % |
| PA-PAC | ncep_gfswave016 | 0.3 m | 100 % |
| PE-LIM | ncep_gfswave025 | 1.8 m | 100 % |
| PE-LLB | ncep_gfswave016 | 1.3 m | 100 % |
| PE-NOR | ncep_gfswave016 | 0.9 m | 56 % |
| PE-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| PF-ISL | ncep_gfswave025 | 2.0 m | 54 % |
| PF-TAH | ncep_gfswave025 | 2.1 m | 95 % |
| PG-ALL | ncep_gfswave016 | 0.9 m | 70 % |
| PH-EAS | ncep_gfswave016 | 1.3 m | 89 % |
| PH-LUZ | ncep_gfswave016 | 0.9 m | 96 % |
| PH-SIA | ncep_gfswave016 | 1.2 m | 95 % |
| PR-N | ncep_gfswave016 | 1.1 m | 99 % |
| PR-NW | ncep_gfswave016 | 1.0 m | 100 % |
| PT-ALG | ncep_gfswave016 | 1.6 m | 100 % |
| PT-AZO | ncep_gfswave016 | 1.3 m | 15 % |
| PT-CEN | ncep_gfswave016 | 1.6 m | 100 % |
| PT-ERI | ncep_gfswave016 | 1.7 m | 99 % |
| PT-LIS | ncep_gfswave016 | 1.2 m | 79 % |
| PT-MAD | ncep_gfswave016 | 1.0 m | 73 % |
| PT-NOR | ncep_gfswave016 | 1.6 m | 100 % |
| PT-PEN | ncep_gfswave016 | 1.8 m | 99 % |
| RE-ALL | ncep_gfswave025 | 1.1 m | 78 % |
| SN-ALL | ncep_gfswave016 | 1.4 m | 99 % |
| SV-LIB | ncep_gfswave016 | 1.1 m | 100 % |
| SV-ORI | ncep_gfswave016 | 1.1 m | 100 % |
| TO-ALL | ncep_gfswave025 | 1.5 m | 51 % |
| TT-ALL | ncep_gfswave016 | 0.8 m | 99 % |
| TW-E | ncep_gfswave016 | 1.8 m | 59 % |
| TW-NE | ncep_gfswave016 | 1.8 m | 77 % |
| US-CA-CEN | ecmwf_wam | 1.5 m | 94 % |
| US-CA-LA | ecmwf_wam | 0.9 m | 100 % |
| US-CA-NOR | ecmwf_wam | 1.8 m | 100 % |
| US-CA-OC | ecmwf_wam | 1.0 m | 100 % |
| US-CA-SB | ecmwf_wam | 0.8 m | 99 % |
| US-CA-SC | ecmwf_wam | 1.2 m | 87 % |
| US-CA-SD | ncep_gfswave016 | 0.8 m | 92 % |
| US-CA-SF | ecmwf_wam | 1.4 m | 100 % |
| US-FL-PAN | ecmwf_wam | 0.6 m | 60 % |
| US-FL | ncep_gfswave016 | 1.7 m | 100 % |
| US-GULF | ecmwf_wam | 0.4 m | 95 % |
| US-HI-BIG | ecmwf_wam | 1.0 m | 76 % |
| US-HI-KAU | ecmwf_wam | 1.9 m | 77 % |
| US-HI-MAU | ecmwf_wam | 1.6 m | 56 % |
| US-HI-OAN | ncep_gfswave016 | 1.6 m | 85 % |
| US-HI-OAS | ecmwf_wam | 1.1 m | 69 % |
| US-MID | ncep_gfswave025 | 0.8 m | 97 % |
| US-NE | ecmwf_wam | 0.6 m | 69 % |
| US-PNW | ecmwf_wam | 1.8 m | 100 % |
| US-SC-GA | ncep_gfswave016 | 0.9 m | 91 % |
| US-SE | ncep_gfswave025 | 1.3 m | 100 % |
| UY-CAN | ncep_gfswave025 | 0.7 m | 45 % |
| UY-MAL | ncep_gfswave025 | 1.0 m | 76 % |
| UY-ROC | ncep_gfswave025 | 1.1 m | 61 % |
| VE-ALL | ncep_gfswave016 | 0.5 m | 91 % |
| VN-ALL | ncep_gfswave016 | 0.7 m | 100 % |
| VU-ALL | ncep_gfswave025 | 1.2 m | 27 % |
| WS-ALL | ncep_gfswave025 | 1.9 m | 75 % |
| ZA-EC-JB | ncep_gfswave025 | 2.0 m | 98 % |
| ZA-EC-PE | ncep_gfswave025 | 2.1 m | 19 % |
| ZA-EC-WLD | ncep_gfswave025 | 1.8 m | 42 % |
| ZA-KZN-DBN | ncep_gfswave025 | 1.7 m | 61 % |
| ZA-KZN-N | ncep_gfswave025 | 1.6 m | 65 % |
| ZA-KZN-S | ncep_gfswave025 | 1.8 m | 51 % |
| ZA-WC-CPT | ncep_gfswave025 | 1.7 m | 84 % |
| ZA-WC-GR | ncep_gfswave025 | 1.6 m | 94 % |
| ZA-WC-WCO | ncep_gfswave025 | 1.6 m | 0 % |
