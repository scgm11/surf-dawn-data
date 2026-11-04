# Picos: controles por pico

Generado 2026-11-04 13:31 UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). 213 regiones, 2511 picos.

- **Orientación (§5.2):** olas de los últimos 14 días y los próximos 2 en el punto de olas de cada pico (el modelo de su zona). Se marca un pico al que las olas de al menos 0.3 m casi nunca le llegan a menos de 55° de hacia donde mira (menos del 5 % de las horas) mientras a su zona sí (al menos 25 %).
- **Zona entera:** en una zona donde la mayoría tampoco las recibe de frente (menos del 25 %) los vecinos no dicen nada: ahí se marca el pico con mar (olas de al menos 0.3 m en el 25 % de las horas o más) que casi nunca las recibe de frente.
- **Temporada:** los marcados por la orientación se miran de nuevo con 92 días de olas; 59 dejaron de estarlo (en dos semanas no les tocaba su ventana de swell).
- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media de su zona.
- **Emblemáticos (§5.8):** la posición contra fuentes públicas (el ítem más cercano con su nombre en Wikidata o GeoNames, hasta 6 km; si no, OpenStreetMap; si no, el ítem de otro nombre del que se tomó a mano la posición, en el `src` de la semilla): 319 bien (a menos de 1.5 km; 12 de ellos por la fuente de su semilla), 0 lejos, 21 lejos pero revisados a mano (el ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), 52 sin fuente (revisar a mano; `validation/lookup.md` tiene lo que hay con su nombre alrededor), 0 sin respuesta.
- Open-Meteo: 38 pedidos, ~3041 llamadas de las 10.000 diarias gratuitas.

## Orientación probablemente del lado equivocado (4)

Mira a más de 135° de sus vecinos (a 30 km) y de las olas, y dada vuelta coincide con ellos: casi seguro se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla.

| Región | Pico | Mira a | Vecinos | Olas desde |
|---|---|---|---|---|
| AU-NSW-NR | THE PASS | 304° | 80° | 98° |
| ES-CN-E | PUNTA MUJERES | 128° | 338° | 331° |
| ES-GAL | LAXE | 92° | 295° | 313° |
| MV-NMA | COKES | 0° | 164° | 156° |

## Zonas enteras que casi nunca reciben las olas de frente (21)

Zonas con 3 picos o más que, en 92 días, casi nunca recibieron las olas de frente aunque había mar, y a las que la comparación con los vecinos no ve porque están todos igual. O la orientación de toda la costa se calculó del lado equivocado, o son reefs y puntas a los que el swell entra dando la vuelta: ahí la orientación de la costa está bien para el viento y lo que falta es la ventana de swell del pico.

| Región | Marcados | Puntas y reefs | Miran a | Olas desde | Picos |
|---|---|---|---|---|---|
| AU-VIC-SC | 6 de 20 | 4 | 102° | 220° | BARWON BLUFF, JAN JUC, WINKIPOP, BELLS BEACH, POINT ADDIS, LORNE POINT |
| CA-BC-VI | 7 de 14 | 1 | 68° | 252° | SAN JOSEF, CHESTERMAN, COX BAY, SCHOONER COVE, WYA POINT, CHINA BEACH, JORDAN RIVER |
| CL-CEN | 12 de 20 | 2 | 1° | 236° | PICHIDANGUI, LOS MOLLES, PICHICUY, PAPUDO, MAITENCILLO, HORCÓN, LA BOCA, AMARILLA, TUNQUÉN, ALGARROBO, EL QUISCO, CARTAGENA |
| CL-PIC | 6 de 12 | 3 | 346° | 239° | MATANZAS, TOPOCALMA, LA PUNTILLA, PLAYA PRINCIPAL, LAS TERRAZAS, PUNTA DE LOBOS |
| EC-GAL | 3 de 4 | 3 | 303° | 207° | CAROLA, MANGLECITO, TONGO REEF |
| ID-BAL-BUK | 14 de 16 | 13 | 326° | 207° | ULUWATU, RACETRACKS, TEMPLES, OUTSIDE CORNER, THE BOMBIE, SULUBAN, PADANG PADANG, THUNDERS, IMPOSSIBLES, BINGIN, DREAMLAND, BALANGAN, NUSA DUA, SRI LANKA |
| ID-BAL-E | 8 de 12 | 5 | 83° | 198° | PURNAMA, SABA, LEBIH, SANUR REEF, MERTASARI, SHIPWRECKS, LACERATIONS, PLAYGROUNDS |
| ID-JAV-E | 5 de 7 | 5 | 320° | 204° | MONEY TREES, LAUNCHING PADS, KONGS, SPEEDIES, TIGER TRACKS |
| ID-JAV-W | 5 de 7 | 3 | 329° | 199° | BATU KARAS, PANGANDARAN, CIMAJA, KARANG HAWU, MADASARI |
| ID-KRU | 3 de 4 | 3 | 313° | 206° | MANDIRI, WAY JAMBU, UJUNG BOCUR |
| ID-LOM | 7 de 14 | 4 | 24° | 210° | DESERT POINT, SELONG BELANAK, MAWI, MAWUN, KUTA LOMBOK, GERUPUK, DON DON |
| ID-MEN | 7 de 10 | 7 | 68° | 193° | HT'S, LANCE'S LEFT, KANDUI LEFT, KANDUI RIGHT, RIFLES, BURGERWORLD, TELESCOPES |
| LR-ALL | 3 de 3 | 2 | 311° | 201° | CASSAVA POINT, FISHERMANS POINT, COTTON TREE |
| MA-TAG | 12 de 19 | 10 | 210° | 310° | BOILERS, KILLER POINT, ANCHOR POINT, LA SOURCE, HASH POINT, MYSTERIES, PANORAMAS, BANANA POINT, DEVIL'S ROCK, AGADIR, CATHEDRAL, MADRABA |
| MX-NAY | 5 de 9 | 3 | 318° | 219° | LO DE MARCOS, SAN PANCHO, SAYULITA, STINKY'S, LA LANCHA |
| NZ-OTA | 3 de 13 | 1 | 162° | 211° | WHAREAKEAKE, PORPOISE BAY, COLAC BAY |
| NZ-RAG | 3 de 5 | 3 | 0° | 252° | MANU BAY, WHALE BAY, INDICATORS |
| PE-NOR | 3 de 10 | 3 | 328° | 239° | ZORRITOS, CABO BLANCO, LOBITOS |
| PR-NW | 9 de 15 | 6 | 243° | 4° | CRASH BOAT, INDICATORS, DOMES, SANDY BEACH, DOGMAN'S, STEPS, TRES PALMAS, MARIA'S, CÓRCEGA |
| PT-MAD | 3 de 8 | 1 | 77° | 324° | MACHICO, SEIXAL, RIBEIRA DA JANELA |
| ZA-WC-WCO | 5 de 6 | 1 | 328° | 235° | ELANDS BAY, MELKBOS, LAMBERTS BAY, JACOBSBAAI, YZERFONTEIN |

## Picos marcados (328)

Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y el semáforo del swell es conservador ahí); se revisan a mano.

| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |
|---|---|---|---|---|---|---|
| AU-NSW-MN | WOOLGOOLGA |  | 9° | 100° | 120° | las olas casi nunca le entran de frente (1 % de las horas; la zona 55 %) y en 92 días 0 % |
| AU-NSW-NC | OCEAN BEACH |  | 250° | 119° | 117° | las olas casi nunca le entran de frente (1 % de las horas; la zona 57 %) y en 92 días 0 % |
| AU-NSW-NR | THE PASS | sí | 304° | 98° | 80° | las olas casi nunca le entran de frente (0 % de las horas; la zona 59 %) y en 92 días 0 % |
| AU-QLD-GC | RAINBOW BAY | sí | 337° | 100° | 58° | las olas casi nunca le entran de frente (4 % de las horas; la zona 77 %) y en 92 días 0 % |
| AU-QLD-SC | FIRST POINT | sí | 321° | 87° | 86° | las olas casi nunca le entran de frente (2 % de las horas; la zona 86 %) y en 92 días 1 % |
| AU-QLD-SC | LITTLE COVE |  | 312° | 87° | 85° | las olas casi nunca le entran de frente (1 % de las horas; la zona 86 %) y en 92 días 0 % |
| AU-SA-EYR | CAVES |  | 142° | 226° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-SA | CHINAMANS |  | 325° | 235° | 250° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| AU-TAS | CLIFTON BEACH | sí | 119° | 208° | — | las olas casi nunca le entran de frente (4 % de las horas; la zona 38 %) y en 92 días 3 % |
| AU-TAS | MARION BAY |  | 269° | 85° | 146° | las olas casi nunca le entran de frente (0 % de las horas; la zona 38 %) y en 92 días 2 % |
| AU-TAS | MARRAWAH |  | 314° | 230° | — | 2.6 m de media, más del doble de la zona (1.3 m); las olas casi nunca le entran de frente (1 % de las horas; la zona 38 %) y en 92 días 1 % |
| AU-TAS | GREEN POINT |  | 61° | 230° | — | 2.6 m de media, más del doble de la zona (1.3 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 38 %) y en 92 días 0 % |
| AU-VIC-PI | FOREST CAVES |  | 127° | 223° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-VIC-SC | BARWON BLUFF |  | 93° | 203° | 149° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 1 % |
| AU-VIC-SC | JAN JUC |  | 118° | 221° | 154° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 2 % |
| AU-VIC-SC | WINKIPOP | sí | 126° | 221° | 153° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 2 % |
| AU-VIC-SC | BELLS BEACH | sí | 135° | 221° | 152° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 2 % |
| AU-VIC-SC | POINT ADDIS |  | 91° | 221° | 151° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 2 % |
| AU-VIC-SC | LORNE POINT | sí | 43° | 230° | 160° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| AU-VIC-W | WYE RIVER |  | 110° | 230° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| AU-VIC-W | KENNETT RIVER |  | 117° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 1 % |
| AU-VIC-W | PORT FAIRY EAST |  | 140° | 219° | 229° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 0 % |
| AU-WA-GAS | TOMBSTONES | sí | 330° | 251° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| AU-WA-GAS | RED BLUFF | sí | 11° | 251° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| AU-WA-MR | COW BOMBIE |  | 318° | 235° | 265° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| AU-WA-MR | CAPE CLAIRAULT |  | 319° | 247° | 268° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| AU-WA-NW | JAKES POINT | sí | 320° | 238° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| AU-WA-PER | NORTH MOLE |  | 348° | 255° | 261° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| AU-WA-PER | STRICKLAND BAY | sí | 192° | 255° | 277° | las olas casi nunca le entran de frente (1 % de las horas; la zona 99 %) y en 92 días 0 % |
| AU-WA-PER | STARK BAY |  | 163° | 255° | 276° | las olas casi nunca le entran de frente (1 % de las horas; la zona 99 %) y en 92 días 0 % |
| BB-ALL | SANDY LANE |  | 262° | 4° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 30 %) y en 92 días 0 % |
| BB-ALL | DRILL HALL |  | 259° | 4° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 30 %) y en 92 días 0 % |
| BB-ALL | FREIGHTS BAY | sí | 255° | 85° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 30 %) y en 92 días 0 % |
| BB-ALL | SURFERS POINT |  | 235° | 85° | 319° | las olas casi nunca le entran de frente (0 % de las horas; la zona 30 %) y en 92 días 0 % |
| BR-ES | ITAPARICA |  | 0° | 115° | 115° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 0 % |
| BR-NE-PE | GAIBU |  | 31° | 107° | 105° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 0 % |
| BR-SP | FAZENDA |  | 260° | 145° | 125° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BR-SP | SUNUNGA |  | 224° | 138° | 142° | las olas casi nunca le entran de frente (4 % de las horas; la zona 90 %) y en 92 días 4 % |
| BR-SP | MARANDUBA |  | 234° | 138° | 142° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BR-SP | PAÚBA |  | 264° | 151° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| BR-SP | CAMBURI |  | 261° | 151° | 171° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| BR-SP | ILHA COMPRIDA |  | 269° | 140° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| BS-ALL | SURFERS BEACH |  | 168° | 39° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| CA-BC-VI | SAN JOSEF |  | 5° | 236° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 1 % |
| CA-BC-VI | CHESTERMAN | sí | 90° | 243° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| CA-BC-VI | COX BAY | sí | 2° | 243° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| CA-BC-VI | SCHOONER COVE |  | 44° | 241° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| CA-BC-VI | WYA POINT |  | 90° | 246° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (19 %) y en 92 días 0 % |
| CA-BC-VI | CHINA BEACH |  | 202° | 280° | 218° | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (19 %) y en 92 días 1 % |
| CA-BC-VI | JORDAN RIVER | sí | 201° | 280° | 218° | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (19 %) y en 92 días 1 % |
| CL-CEN | PICHIDANGUI |  | 32° | 232° | 136° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (2 %) y en 92 días 0 % |
| CL-CEN | LOS MOLLES |  | 122° | 232° | 91° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (2 %) y en 92 días 0 % |
| CL-CEN | PICHICUY |  | 150° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (2 %) y en 92 días 0 % |
| CL-CEN | PAPUDO |  | 19° | 239° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (2 %) y en 92 días 0 % |
| CL-CEN | MAITENCILLO | sí | 323° | 235° | — | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (2 %) y en 92 días 2 % |
| CL-CEN | HORCÓN |  | 45° | 235° | 291° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (2 %) y en 92 días 0 % |
| CL-CEN | LA BOCA |  | 314° | 235° | 277° | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (2 %) y en 92 días 2 % |
| CL-CEN | AMARILLA |  | 341° | 235° | 272° | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (2 %) y en 92 días 1 % |
| CL-CEN | TUNQUÉN |  | 335° | 238° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (2 %) y en 92 días 1 % |
| CL-CEN | ALGARROBO |  | 339° | 238° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (2 %) y en 92 días 1 % |
| CL-CEN | EL QUISCO |  | 16° | 239° | 294° | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (2 %) y en 92 días 1 % |
| CL-CEN | CARTAGENA |  | 325° | 239° | — | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (2 %) y en 92 días 3 % |
| CL-MAU | LLICO |  | 344° | 244° | — | las olas casi nunca le entran de frente (5 % de las horas; la zona 91 %) y en 92 días 3 % |
| CL-MAU | PUNTA LAVAPIÉ |  | 0° | 255° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 91 %) y en 92 días 4 % |
| CL-NOR | EL GRINGO | sí | 305° | 223° | 283° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 0 % |
| CL-NOR | EL BUEY |  | 290° | 223° | 287° | las olas casi nunca le entran de frente (5 % de las horas; la zona 97 %) y en 92 días 5 % |
| CL-NOR | LAS MACHAS |  | 324° | 223° | 280° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 0 % |
| CL-NOR | CORAZONES |  | 295° | 223° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 2 % |
| CL-PIC | MATANZAS |  | 338° | 249° | 325° | las olas casi nunca le entran de frente (5 % de las horas) y a su zona tampoco (18 %) y en 92 días 2 % |
| CL-PIC | TOPOCALMA |  | 355° | 235° | 331° | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (18 %) y en 92 días 1 % |
| CL-PIC | LA PUNTILLA | sí | 6° | 238° | 305° | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (18 %) y en 92 días 1 % |
| CL-PIC | PLAYA PRINCIPAL |  | 344° | 238° | 307° | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (18 %) y en 92 días 2 % |
| CL-PIC | LAS TERRAZAS |  | 313° | 238° | 311° | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (18 %) y en 92 días 4 % |
| CL-PIC | PUNTA DE LOBOS | sí | 358° | 238° | 299° | las olas casi nunca le entran de frente (3 % de las horas) y a su zona tampoco (18 %) y en 92 días 1 % |
| CO-PAC | HUINA |  | 312° | 228° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CO-PAC | NUQUÍ |  | 303° | 240° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 100 %) y en 92 días 3 % |
| CR-GUA | OLLIE'S POINT |  | 144° | 234° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-GUA | TAMARINDO | sí | 312° | 226° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-GUA | PICO PEQUEÑO |  | 331° | 226° | 253° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-NIC | SAMARA |  | 146° | 210° | 232° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 5 % |
| CR-NIC | CARRILLO |  | 291° | 210° | 209° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| CR-OSA | RIO CLARO |  | 308° | 214° | 246° | las olas casi nunca le entran de frente (0 % de las horas; la zona 48 %) y en 92 días 0 % |
| CR-OSA | PAVONES | sí | 294° | 214° | 250° | las olas casi nunca le entran de frente (0 % de las horas; la zona 48 %) y en 92 días 0 % |
| CV-ALL | PONTA PRETA |  | 257° | 351° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| CV-ALL | SANTA MARIA |  | 193° | 354° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| EC-COS | MOMPICHE | sí | 317° | 244° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 2 % |
| EC-COS | BALLENITA |  | 317° | 237° | 296° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| EC-COS | PUNTA CARNERO |  | 355° | 237° | 278° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| EC-GAL | CAROLA | sí | 289° | 207° | 282° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| EC-GAL | MANGLECITO |  | 322° | 207° | 270° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| EC-GAL | TONGO REEF | sí | 298° | 207° | 278° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ES-AND | REGLA |  | 7° | 270° | 285° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 0 % |
| ES-AND | ZAHORA |  | 172° | 260° | 234° | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 3 % |
| ES-AND | BOLONIA |  | 191° | 287° | 226° | las olas casi nunca le entran de frente (0 % de las horas; la zona 99 %) y en 92 días 1 % |
| ES-AST | SAN LORENZO |  | 78° | 335° | 16° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 4 % |
| ES-AST | XAGO |  | 82° | 332° | 9° | las olas casi nunca le entran de frente (0 % de las horas; la zona 91 %) y en 92 días 2 % |
| ES-CAN | LOS LOCOS | sí | 76° | 330° | 332° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 0 % |
| ES-CN-E | PUNTA MUJERES |  | 128° | 331° | 338° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| ES-CN-E | LOBOS | sí | 241° | 333° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| ES-CN-E | FLAG BEACH |  | 88° | 333° | 274° | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| ES-CN-E | ROCKY POINT |  | 218° | 331° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 86 %) y en 92 días 0 % |
| ES-CN-W | LAS CANTERAS |  | 215° | 344° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 70 %) y en 92 días 0 % |
| ES-CN-W | PLAYA DEL HOMBRE |  | 89° | 357° | 305° | las olas casi nunca le entran de frente (0 % de las horas; la zona 70 %) y en 92 días 3 % |
| ES-CN-W | SARDINA |  | 215° | 343° | 318° | las olas casi nunca le entran de frente (0 % de las horas; la zona 70 %) y en 92 días 0 % |
| ES-CN-W | EL MEDANO |  | 119° | 94° | 285° | las olas casi nunca le entran de frente (4 % de las horas; la zona 70 %) y en 92 días 2 % |
| ES-GAL | DONIÑOS |  | 225° | 313° | 343° | las olas casi nunca le entran de frente (0 % de las horas; la zona 77 %) y en 92 días 2 % |
| ES-GAL | TRABA |  | 202° | 313° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 77 %) y en 92 días 1 % |
| ES-GAL | LAXE |  | 92° | 313° | 295° | las olas casi nunca le entran de frente (3 % de las horas; la zona 77 %) y en 92 días 1 % |
| ES-PV | LAGA |  | 73° | 328° | 352° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| ES-PV | MUNDAKA | sí | 64° | 328° | 351° | las olas casi nunca le entran de frente (1 % de las horas; la zona 90 %) y en 92 días 1 % |
| ES-PV | PLENTZIA |  | 96° | 328° | 349° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 0 % |
| FJ-MAM | CLOUDBREAK | sí | 220° | 205° | 254° | 1.0 m de media, más del doble de la zona (0.4 m) |
| FR-BRE | LE POULDU |  | 132° | 247° | 221° | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| FR-VEN | LA TRANCHE |  | 151° | 263° | 211° | las olas casi nunca le entran de frente (0 % de las horas; la zona 92 %) y en 92 días 0 % |
| GB-CON | PORTHCOTHAN |  | 194° | 277° | 317° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 1 % |
| GB-CON | GWENVER |  | 29° | 264° | 282° | las olas casi nunca le entran de frente (0 % de las horas; la zona 90 %) y en 92 días 3 % |
| GB-DEV | WESTWARD HO |  | 345° | 269° | 266° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 3 % |
| GB-DEV | THURLESTONE |  | 326° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 3 % |
| GB-SCO | STRATHY |  | 77° | 287° | 358° | las olas casi nunca le entran de frente (0 % de las horas; la zona 34 %) y en 92 días 4 % |
| GB-SCO | GOTT BAY |  | 138° | 244° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 34 %) y en 92 días 3 % |
| GB-WAL | BROAD HAVEN SOUTH |  | 149° | 243° | 229° | las olas casi nunca le entran de frente (1 % de las horas; la zona 81 %) y en 92 días 4 % |
| GB-WAL | RHOSSILI |  | 336° | 243° | 203° | las olas casi nunca le entran de frente (0 % de las horas; la zona 81 %) y en 92 días 1 % |
| GB-WAL | LANGLAND BAY |  | 120° | 244° | 249° | las olas casi nunca le entran de frente (3 % de las horas; la zona 81 %) y en 92 días 4 % |
| GB-WAL | LLANTWIT MAJOR |  | 199° | 272° | 244° | las olas casi nunca le entran de frente (2 % de las horas; la zona 81 %) y en 92 días 3 % |
| GH-ALL | BUSUA |  | 92° | 186° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (11 %) y en 92 días 0 % |
| GP-ALL | TARARE |  | 180° | 86° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| GP-ALL | PORT LOUIS |  | 270° | 30° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | ULUWATU | sí | 310° | 207° | 318° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | RACETRACKS |  | 331° | 207° | 316° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | TEMPLES |  | 298° | 207° | 320° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | OUTSIDE CORNER |  | 295° | 207° | 320° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | THE BOMBIE |  | 289° | 207° | 321° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | SULUBAN |  | 315° | 207° | 318° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | PADANG PADANG | sí | 343° | 207° | 314° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | THUNDERS |  | 353° | 207° | 313° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | IMPOSSIBLES | sí | 338° | 207° | 315° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | BINGIN | sí | 332° | 207° | 316° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | DREAMLAND |  | 286° | 207° | 321° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | BALANGAN | sí | 328° | 207° | 316° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | NUSA DUA |  | 52° | 207° | 311° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-BUK | SRI LANKA |  | 111° | 207° | 315° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | PURNAMA |  | 133° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | SABA |  | 130° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | LEBIH |  | 132° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | SANUR REEF | sí | 81° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | MERTASARI |  | 64° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | SHIPWRECKS | sí | 289° | 200° | 122° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | LACERATIONS |  | 349° | 200° | 131° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-E | PLAYGROUNDS |  | 289° | 200° | 122° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-BAL-W | KUTA REEF |  | 293° | 197° | 237° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-W | HALFWAY KUTA |  | 312° | 197° | 236° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-JAV-E | MONEY TREES | sí | 326° | 204° | 318° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-E | LAUNCHING PADS |  | 292° | 204° | 327° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-E | KONGS |  | 314° | 204° | 322° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-E | SPEEDIES |  | 330° | 204° | 317° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-E | TIGER TRACKS |  | 337° | 204° | 316° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-W | BATU KARAS | sí | 81° | 194° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-W | PANGANDARAN |  | 280° | 198° | 100° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-W | CIMAJA |  | 314° | 204° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-W | KARANG HAWU |  | 305° | 204° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-JAV-W | MADASARI |  | 119° | 194° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-KRU | MANDIRI |  | 311° | 205° | 288° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-KRU | WAY JAMBU |  | 312° | 207° | 288° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-KRU | UJUNG BOCUR |  | 317° | 207° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-LOM | DESERT POINT | sí | 274° | 203° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | SELONG BELANAK |  | 296° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | MAWI |  | 0° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | MAWUN |  | 133° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | KUTA LOMBOK |  | 99° | 212° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | GERUPUK | sí | 80° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-LOM | DON DON |  | 0° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (13 %) y en 92 días 0 % |
| ID-MEN | HT'S | sí | 111° | 195° | 146° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | LANCE'S LEFT | sí | 91° | 195° | 152° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | KANDUI LEFT | sí | 305° | 189° | 61° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | KANDUI RIGHT |  | 291° | 189° | 57° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | RIFLES | sí | 95° | 203° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | BURGERWORLD |  | 85° | 189° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-MEN | TELESCOPES |  | 49° | 189° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-NIA | LAGUNDRI | sí | 111° | 203° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ID-NIA | ASU | sí | 288° | 203° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ID-SBW | SCAR REEF | sí | 320° | 205° | 234° | las olas casi nunca le entran de frente (0 % de las horas; la zona 31 %) y en 92 días 0 % |
| ID-SBW | SUPERSUCK | sí | 330° | 213° | 234° | las olas casi nunca le entran de frente (0 % de las horas; la zona 31 %) y en 92 días 0 % |
| IE-NW | TULLAN STRAND |  | 358° | 285° | 307° | las olas casi nunca le entran de frente (0 % de las horas; la zona 89 %) y en 92 días 0 % |
| IE-NW | MULLAGHMORE | sí | 20° | 285° | 306° | las olas casi nunca le entran de frente (0 % de las horas; la zona 89 %) y en 92 días 0 % |
| IE-NW | KEEL |  | 186° | 273° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 89 %) y en 92 días 3 % |
| IE-SW | INCH |  | 172° | 260° | 268° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 3 % |
| JP-KYU | AOSHIMA |  | 236° | 119° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (16 %) y en 92 días 0 % |
| JP-SHO | ZUSHI |  | 306° | 168° | 179° | las olas casi nunca le entran de frente (0 % de las horas; la zona 69 %) y en 92 días 0 % |
| LK-E | ARUGAM BAY | sí | 22° | 175° | 118° | las olas casi nunca le entran de frente (4 % de las horas; la zona 44 %) y en 92 días 1 % |
| LR-ALL | CASSAVA POINT |  | 312° | 201° | 310° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| LR-ALL | FISHERMANS POINT |  | 310° | 201° | 311° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| LR-ALL | COTTON TREE |  | 310° | 201° | 311° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-N | SAFI LE JARDIN | sí | 196° | 316° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 0 % |
| MA-S | TIFNIT |  | 230° | 308° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MA-TAG | BOILERS | sí | 190° | 317° | 229° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | KILLER POINT | sí | 223° | 310° | 219° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | ANCHOR POINT | sí | 203° | 310° | 221° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | LA SOURCE |  | 197° | 310° | 221° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | HASH POINT | sí | 202° | 310° | 221° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | MYSTERIES |  | 214° | 310° | 220° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | PANORAMAS | sí | 202° | 310° | 221° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | BANANA POINT |  | 211° | 310° | 220° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | DEVIL'S ROCK |  | 220° | 310° | 219° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | AGADIR |  | 186° | 310° | 225° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | CATHEDRAL |  | 235° | 304° | 229° | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MA-TAG | MADRABA |  | 234° | 304° | 229° | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MG-ALL | ANAKAO |  | 299° | 210° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 31 %) y en 92 días 0 % |
| MU-ALL | TAMARIN BAY |  | 317° | 212° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 85 %) y en 92 días 0 % |
| MV-CEN | MULI |  | 274° | 154° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (1 %) y en 92 días 1 % |
| MV-NMA | COKES | sí | 0° | 156° | 164° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MV-SMA | COCOA CORNER |  | 73° | 162° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (18 %) y en 92 días 0 % |
| MX-BCS-N | SCORPION BAY | sí | 90° | 216° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 49 %) y en 92 días 0 % |
| MX-NAY | LO DE MARCOS |  | 311° | 229° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 3 % |
| MX-NAY | SAN PANCHO |  | 297° | 217° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 4 % |
| MX-NAY | SAYULITA | sí | 353° | 217° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MX-NAY | STINKY'S |  | 140° | 217° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MX-NAY | LA LANCHA |  | 141° | 217° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| MX-OAX | CHACAHUA | sí | 116° | 209° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| MX-OAX | MAZUNTE |  | 123° | 210° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| MX-PAC | MIRAMAR |  | 314° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 97 %) y en 92 días 1 % |
| NA-ERO | SKELETON BAY | sí | 321° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| NO-N | HAUKLAND |  | 173° | 271° | 255° | las olas casi nunca le entran de frente (0 % de las horas; la zona 43 %) y en 92 días 0 % |
| NZ-BOP | ONEMANA |  | 164° | 27° | 55° | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 4 % |
| NZ-NTL | SHIPWRECK BAY | sí | 37° | 226° | 19° | 2.0 m de media, más del doble de la zona (0.9 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 0 % |
| NZ-NTL | SUPER TUBES | sí | 7° | 226° | 27° | 2.0 m de media, más del doble de la zona (0.9 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 0 % |
| NZ-NTL | MUKIES 2 | sí | 33° | 226° | 20° | 2.0 m de media, más del doble de la zona (0.9 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 0 % |
| NZ-NTL | MUKIES 1 | sí | 24° | 226° | 23° | 2.0 m de media, más del doble de la zona (0.9 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 0 % |
| NZ-NTL | PEAKS | sí | 14° | 226° | 25° | 2.0 m de media, más del doble de la zona (0.9 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 36 %) y en 92 días 0 % |
| NZ-NTL | MATAURI BAY |  | 224° | 30° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 36 %) y en 92 días 1 % |
| NZ-NTL | BAYLYS BEACH |  | 235° | 227° | — | 2.1 m de media, más del doble de la zona (0.9 m) |
| NZ-OTA | WHAREAKEAKE | sí | 311° | 157° | 112° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (22 %) y en 92 días 0 % |
| NZ-OTA | PORPOISE BAY |  | 103° | 214° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (22 %) y en 92 días 4 % |
| NZ-OTA | COLAC BAY |  | 182° | 259° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (22 %) y en 92 días 0 % |
| NZ-RAG | MANU BAY | sí | 14° | 252° | 315° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| NZ-RAG | WHALE BAY | sí | 354° | 252° | 320° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| NZ-RAG | INDICATORS | sí | 351° | 252° | 321° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| NZ-TAR | EAST END |  | 354° | 257° | 335° | las olas casi nunca le entran de frente (4 % de las horas) y a su zona tampoco (21 %) y en 92 días 2 % |
| NZ-TAR | FITZROY BEACH |  | 354° | 257° | 335° | las olas casi nunca le entran de frente (4 % de las horas) y a su zona tampoco (21 %) y en 92 días 2 % |
| NZ-WC | TAURANGA BAY |  | 34° | 273° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 66 %) y en 92 días 1 % |
| PA-BDT | DUMPERS |  | 121° | 45° | 79° | las olas casi nunca le entran de frente (0 % de las horas; la zona 79 %) y en 92 días 0 % |
| PA-PAC | PLAYA VENAO | sí | 235° | 212° | — | 0.9 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | GUANICO |  | 153° | 201° | 209° | 0.8 m de media, más del doble de la zona (0.3 m) |
| PA-PAC | CAMBUTAL |  | 183° | 214° | — | 1.1 m de media, más del doble de la zona (0.3 m) |
| PE-LIM | LA HERRADURA | sí | 290° | 215° | 238° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| PE-LIM | AGUA DULCE |  | 291° | 215° | 232° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 3 % |
| PE-LIM | CERRO AZUL |  | 327° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PE-LLB | PACASMAYO | sí | 316° | 224° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 44 %) y en 92 días 0 % |
| PE-LLB | CHICAMA | sí | 339° | 231° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 44 %) y en 92 días 0 % |
| PE-LLB | HUANCHACO | sí | 309° | 222° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 44 %) y en 92 días 0 % |
| PE-NOR | ZORRITOS |  | 347° | 246° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (11 %) y en 92 días 2 % |
| PE-NOR | CABO BLANCO | sí | 327° | 242° | 308° | las olas casi nunca le entran de frente (5 % de las horas) y a su zona tampoco (11 %) y en 92 días 4 % |
| PE-NOR | LOBITOS | sí | 311° | 229° | 311° | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (11 %) y en 92 días 1 % |
| PF-ISL | TEAVAPITI |  | 65° | 202° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (6 %) y en 92 días 0 % |
| PF-TAH | TIAHURA |  | 328° | 204° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 64 %) y en 92 días 0 % |
| PR-NW | CRASH BOAT |  | 231° | 6° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | INDICATORS |  | 279° | 4° | 281° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | DOMES | sí | 252° | 4° | 284° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | SANDY BEACH |  | 235° | 4° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | DOGMAN'S |  | 236° | 4° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | STEPS |  | 239° | 4° | 285° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | TRES PALMAS | sí | 236° | 4° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | MARIA'S |  | 233° | 4° | 286° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PR-NW | CÓRCEGA |  | 246° | 4° | 285° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PT-ALG | ZAVIAL |  | 173° | 289° | 278° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| PT-AZO | SANTA BÁRBARA | sí | 343° | 233° | — | las olas casi nunca le entran de frente (2 % de las horas) y a su zona tampoco (20 %) y en 92 días 1 % |
| PT-AZO | ALMOXARIFE |  | 91° | 292° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (20 %) y en 92 días 0 % |
| PT-MAD | MACHICO |  | 122° | 339° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PT-MAD | SEIXAL |  | 57° | 316° | 212° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PT-MAD | RIBEIRA DA JANELA |  | 56° | 316° | 212° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| PT-NOR | MATOSINHOS | sí | 181° | 298° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| RE-ALL | BOUCAN CANOT |  | 312° | 214° | 265° | las olas casi nunca le entran de frente (0 % de las horas; la zona 67 %) y en 92 días 0 % |
| RE-ALL | LES BRISANTS |  | 283° | 214° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 67 %) y en 92 días 1 % |
| RE-ALL | BARACHOIS |  | 325° | 125° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 67 %) y en 92 días 0 % |
| SV-LIB | PUNTA ROCA | sí | 147° | 212° | 183° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| SV-ORI | LAS FLORES | sí | 126° | 206° | 172° | las olas casi nunca le entran de frente (0 % de las horas; la zona 53 %) y en 92 días 1 % |
| TO-ALL | PASS LEFTS |  | 5° | 151° | 272° | las olas casi nunca le entran de frente (0 % de las horas; la zona 50 %) y en 92 días 0 % |
| TO-ALL | PASS RIGHTS |  | 5° | 151° | 272° | las olas casi nunca le entran de frente (0 % de las horas; la zona 50 %) y en 92 días 0 % |
| TT-ALL | MOUNT IRVINE |  | 280° | 68° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-CEN | PIRATE'S COVE |  | 175° | 272° | 256° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 3 % |
| US-CA-CEN | MORRO ROCK | sí | 8° | 270° | 231° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| US-CA-CEN | ANDREW MOLERA |  | 186° | 286° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 4 % |
| US-CA-LA | MALIBU | sí | 125° | 211° | 201° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-LA | SECOND POINT |  | 125° | 211° | 201° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-LA | THIRD POINT |  | 125° | 211° | 201° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-NOR | BIG RIVER BEACH |  | 209° | 294° | 292° | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 4 % |
| US-CA-NOR | NORTH JETTY |  | 19° | 305° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-CA-SB | SANDSPIT |  | 112° | 203° | 193° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-SC | STEAMER LANE | sí | 156° | 254° | 202° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 3 % |
| US-CA-SC | THE HOOK |  | 158° | 254° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 3 % |
| US-CA-SC | PLEASURE POINT | sí | 154° | 254° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 2 % |
| US-CA-SC | MORAN LAKE |  | 130° | 254° | 200° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 0 % |
| US-CA-SC | CAPITOLA |  | 157° | 254° | 199° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 3 % |
| US-CA-SC | LOVER'S POINT |  | 41° | 295° | 282° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 0 % |
| US-CA-SC | GHOST TREE | sí | 209° | 294° | 305° | las olas casi nunca le entran de frente (0 % de las horas; la zona 58 %) y en 92 días 0 % |
| US-CA-SD | LA JOLLA SHORES |  | 298° | 209° | 256° | las olas casi nunca le entran de frente (2 % de las horas; la zona 88 %) y en 92 días 1 % |
| US-CA-SD | MARINE STREET |  | 293° | 209° | 256° | las olas casi nunca le entran de frente (2 % de las horas; la zona 88 %) y en 92 días 1 % |
| US-CA-SD | BIRD ROCK |  | 0° | 209° | 256° | las olas casi nunca le entran de frente (0 % de las horas; la zona 88 %) y en 92 días 0 % |
| US-CA-SF | FORT POINT | sí | 330° | 219° | 258° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-SF | BAKER BEACH |  | 294° | 219° | 261° | las olas casi nunca le entran de frente (4 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-CA-SF | BOLINAS |  | 153° | 269° | 254° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-GULF | PADRE SEASHORE |  | 112° | 100° | — | 0.9 m de media, más del doble de la zona (0.5 m) |
| US-HI-KAU | HANALEI | sí | 287° | 15° | 22° | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 5 % |
| US-HI-KAU | KALAPAKI |  | 225° | 52° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 75 %) y en 92 días 0 % |
| US-HI-MAU | HONOLUA | sí | 297° | 35° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 55 %) y en 92 días 0 % |
| US-HI-OAS | CONCESSIONS |  | 245° | 159° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 2 % |
| US-HI-OAS | CANOES |  | 262° | 159° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 0 % |
| US-HI-OAS | QUEENS | sí | 260° | 159° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 0 % |
| US-HI-OAS | PUBLICS |  | 249° | 159° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 1 % |
| US-HI-OAS | CHINA WALLS |  | 255° | 138° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 54 %) y en 92 días 0 % |
| US-PNW | HOBUCK |  | 88° | 265° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-PNW | PORT ORFORD |  | 162° | 291° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-SE | OCRACOKE |  | 262° | 107° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ZA-EC-JB | BRUCE'S BEAUTIES | sí | 47° | 217° | 91° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (3 %) y en 92 días 0 % |
| ZA-EC-PE | HOBIE BEACH |  | 31° | 190° | 132° | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (23 %) y en 92 días 0 % |
| ZA-WC-CPT | LLANDUDNO | sí | 311° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-CPT | DUNGEONS | sí | 101° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-CPT | SUNSET REEF | sí | 310° | 232° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-CPT | LONG BEACH | sí | 344° | 231° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-CPT | KALK BAY REEF |  | 110° | 221° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 28 %) y en 92 días 5 % |
| ZA-WC-CPT | KOGEL BAY |  | 332° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-CPT | ROOI-ELS |  | 328° | 212° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 28 %) y en 92 días 0 % |
| ZA-WC-GR | INNER POOL | sí | 52° | 203° | 147° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 0 % |
| ZA-WC-GR | SANTOS |  | 50° | 203° | 147° | las olas casi nunca le entran de frente (0 % de las horas; la zona 93 %) y en 92 días 0 % |
| ZA-WC-WCO | ELANDS BAY | sí | 339° | 243° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | MELKBOS |  | 310° | 235° | — | las olas casi nunca le entran de frente (1 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |
| ZA-WC-WCO | LAMBERTS BAY |  | 320° | 237° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | JACOBSBAAI |  | 318° | 229° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 1 % |
| ZA-WC-WCO | YZERFONTEIN |  | 351° | 233° | — | las olas casi nunca le entran de frente (0 % de las horas) y a su zona tampoco (0 %) y en 92 días 0 % |

## Emblemáticos lejos de su ítem en Wikidata, GeoNames u OpenStreetMap

Ninguno.

## Emblemáticos sin fuente en Wikidata, GeoNames ni OpenStreetMap (revisar a mano)

AU-NSW-SYD/OURS, AU-VIC-SC/WINKIPOP, AU-WA-MR/MAIN BREAK, AU-WA-MR/NORTH POINT, CL-NOR/EL GRINGO, CR-GUA/WITCH'S ROCK, CR-OSA/PAVONES, ES-CN-E/EL QUEMAO, ES-CN-W/EL FRONTON, ES-CN-W/LA IZQUIERDA, FJ-MAM/CLOUDBREAK, FJ-MAM/RESTAURANTS, FJ-MAM/SWIMMING POOLS, ID-BAL-E/SHIPWRECKS, ID-JAV-E/MONEY TREES, ID-MEN/MACARONIS, ID-MEN/KANDUI LEFT, ID-MEN/RIFLES, ID-ROT/T-LAND, ID-SBW/SUPERSUCK, IE-NW/EASKEY, IE-SW/AILEEN'S, LK-E/WHISKEY POINT, MA-N/SAFI LE JARDIN, MV-NMA/PASTA POINT, MV-NMA/SULTANS, MV-NMA/HONKY'S, MV-NMA/COKES, MV-NMA/CHICKENS, MV-NMA/JAILBREAKS, MV-SOU/TIGER STRIPES, MV-SOU/BEACONS, MX-BCS/ZIPPERS, NA-ERO/SKELETON BAY, NZ-GIS/CENTRES, NZ-GIS/WHALES, NZ-GIS/THE ISLAND, NZ-KAI/MEATWORKS, NZ-NTL/SUPER TUBES, NZ-NTL/MUKIES 2, NZ-NTL/MUKIES 1, NZ-NTL/PEAKS, NZ-RAG/INDICATORS, PH-SIA/JACKING HORSE, SV-ORI/LAS FLORES, US-HI-BIG/BANYANS, US-HI-KAU/PK'S, US-HI-OAN/BACKDOOR, US-NE/RUGGLES, ZA-EC-JB/BRUCE'S BEAUTIES, ZA-WC-CPT/DUNGEONS, ZA-WC-CPT/SUNSET REEF

## Zonas

| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |
|---|---|---|---|
| AR-BAN | ncep_gfswave025 | 0.9 m | 93 % |
| AR-MDP | ncep_gfswave025 | 0.9 m | 69 % |
| AR-SUR | ncep_gfswave025 | 0.8 m | 62 % |
| AU-NSW-MN | ncep_gfswave025 | 1.4 m | 55 % |
| AU-NSW-NC | ncep_gfswave025 | 1.3 m | 57 % |
| AU-NSW-NR | ncep_gfswave025 | 1.4 m | 59 % |
| AU-NSW-SC | ncep_gfswave025 | 1.4 m | 63 % |
| AU-NSW-SYD | ncep_gfswave025 | 1.5 m | 55 % |
| AU-QLD-GC | ncep_gfswave025 | 1.0 m | 77 % |
| AU-QLD-SC | ncep_gfswave025 | 1.0 m | 86 % |
| AU-SA-EYR | ncep_gfswave025 | 1.3 m | 100 % |
| AU-SA | ecmwf_wam | 1.2 m | 90 % |
| AU-TAS | ncep_gfswave025 | 1.2 m | 38 % |
| AU-VIC-PI | ncep_gfswave025 | 1.3 m | 100 % |
| AU-VIC-SC | ncep_gfswave025 | 1.1 m | 13 % |
| AU-VIC-W | ncep_gfswave025 | 2.3 m | 91 % |
| AU-WA-GAS | ncep_gfswave025 | 1.4 m | 0 % |
| AU-WA-MR | ncep_gfswave025 | 2.7 m | 100 % |
| AU-WA-NW | ncep_gfswave025 | 1.9 m | 95 % |
| AU-WA-PER | ncep_gfswave025 | 1.8 m | 99 % |
| BB-ALL | ncep_gfswave016 | 1.1 m | 30 % |
| BR-BA | ncep_gfswave025 | 1.2 m | 93 % |
| BR-ES | ncep_gfswave025 | 1.1 m | 93 % |
| BR-NE-CE | ncep_gfswave016 | 1.0 m | 88 % |
| BR-NE-PE | ncep_gfswave016 | 1.0 m | 100 % |
| BR-NE-RN | ncep_gfswave016 | 0.9 m | 100 % |
| BR-NOR | ncep_gfswave016 | 1.3 m | 55 % |
| BR-RJ | ncep_gfswave025 | 0.9 m | 99 % |
| BR-RJL | ncep_gfswave025 | 1.2 m | 76 % |
| BR-RS-SUL | ncep_gfswave025 | 1.0 m | 99 % |
| BR-RS | ncep_gfswave025 | 1.3 m | 97 % |
| BR-SC-FLN | ncep_gfswave025 | 1.3 m | 86 % |
| BR-SC-NOR | ncep_gfswave025 | 0.9 m | 100 % |
| BR-SC-SUL | ncep_gfswave025 | 1.3 m | 87 % |
| BR-SP | ncep_gfswave025 | 0.9 m | 90 % |
| BS-ALL | ncep_gfswave016 | 1.8 m | 0 % |
| CA-BC-VI | ecmwf_wam | 1.5 m | 19 % |
| CA-NS | ncep_gfswave016 | 1.0 m | 47 % |
| CL-CEN | ncep_gfswave025 | 1.7 m | 2 % |
| CL-MAU | ncep_gfswave025 | 1.5 m | 91 % |
| CL-NOR | ncep_gfswave025 | 1.7 m | 97 % |
| CL-PIC | ncep_gfswave025 | 1.9 m | 18 % |
| CL-SUR | ncep_gfswave025 | 1.6 m | 100 % |
| CN-HAI | ncep_gfswave016 | 1.0 m | 17 % |
| CO-CAR | ncep_gfswave016 | 0.6 m | 95 % |
| CO-PAC | ncep_gfswave016 | 0.8 m | 100 % |
| CR-CAR | ncep_gfswave016 | 0.7 m | 100 % |
| CR-GUA | ncep_gfswave016 | 1.1 m | 100 % |
| CR-NIC | ncep_gfswave016 | 1.0 m | 100 % |
| CR-OSA | ncep_gfswave016 | 1.1 m | 48 % |
| CR-PAC | ncep_gfswave016 | 0.9 m | 100 % |
| CV-ALL | ncep_gfswave016 | 1.2 m | 0 % |
| DE-ALL | ncep_gfswave025 | 1.1 m | 88 % |
| DK-ALL | ncep_gfswave025 | 1.5 m | 81 % |
| DO-ALL | ncep_gfswave016 | 1.3 m | 100 % |
| EC-COS | ncep_gfswave016 | 0.8 m | 100 % |
| EC-GAL | ncep_gfswave016 | 1.2 m | 0 % |
| ES-AND | ncep_gfswave016 | 0.5 m | 99 % |
| ES-AST | ncep_gfswave016 | 1.8 m | 91 % |
| ES-CAN | ncep_gfswave016 | 1.8 m | 93 % |
| ES-CN-E | ncep_gfswave016 | 1.3 m | 86 % |
| ES-CN-W | ncep_gfswave016 | 1.1 m | 70 % |
| ES-GAL | ncep_gfswave016 | 2.2 m | 77 % |
| ES-PV | ncep_gfswave016 | 1.6 m | 90 % |
| FJ-MAM | ncep_gfswave025 | 0.4 m | 100 % |
| FJ-SOU | ncep_gfswave025 | 1.2 m | 87 % |
| FR-BRE | ncep_gfswave016 | 1.9 m | 97 % |
| FR-GIR | ncep_gfswave016 | 2.0 m | 96 % |
| FR-HOS | ncep_gfswave016 | 1.9 m | 97 % |
| FR-PBA | ncep_gfswave016 | 1.9 m | 100 % |
| FR-VEN | ncep_gfswave016 | 1.5 m | 92 % |
| GB-CON | ncep_gfswave016 | 2.3 m | 90 % |
| GB-DEV | ncep_gfswave016 | 1.9 m | 93 % |
| GB-NE | ncep_gfswave025 | 1.0 m | 49 % |
| GB-NIR | ecmwf_wam | 1.0 m | 65 % |
| GB-SCO | ncep_gfswave025 | 1.5 m | 34 % |
| GB-SOU | ncep_gfswave016 | 1.2 m | 74 % |
| GB-WAL | ncep_gfswave025 | 1.8 m | 81 % |
| GH-ALL | ncep_gfswave016 | 0.8 m | 11 % |
| GP-ALL | ncep_gfswave016 | 1.1 m | 0 % |
| GT-PAC | ncep_gfswave016 | 1.1 m | 100 % |
| ID-BAL-BUK | ncep_gfswave016 | 1.6 m | 0 % |
| ID-BAL-E | ncep_gfswave016 | 1.1 m | 0 % |
| ID-BAL-W | ncep_gfswave016 | 1.1 m | 100 % |
| ID-JAV-E | ncep_gfswave016 | 1.5 m | 0 % |
| ID-JAV-W | ncep_gfswave016 | 1.5 m | 0 % |
| ID-KRU | ncep_gfswave016 | 1.6 m | 0 % |
| ID-LOM | ncep_gfswave016 | 1.6 m | 13 % |
| ID-MEN | ncep_gfswave016 | 1.2 m | 0 % |
| ID-NIA | ncep_gfswave016 | 1.2 m | 0 % |
| ID-ROT | ncep_gfswave016 | 1.0 m | 100 % |
| ID-SBW | ncep_gfswave016 | 1.2 m | 31 % |
| ID-SMB | ncep_gfswave016 | 1.4 m | 100 % |
| IE-NW | ncep_gfswave025 | 2.1 m | 89 % |
| IE-SE | ncep_gfswave016 | 1.8 m | 62 % |
| IE-SW | ecmwf_wam | 1.7 m | 95 % |
| IN-E | ncep_gfswave016 | 0.9 m | 94 % |
| IN-W | ncep_gfswave016 | 0.8 m | 96 % |
| IS-ALL | ncep_gfswave025 | 2.8 m | 95 % |
| IT-ALL | ncep_gfswave016 | 0.7 m | 55 % |
| IT-SAR | ncep_gfswave016 | 1.0 m | 98 % |
| JP-CHI | ncep_gfswave016 | 1.7 m | 71 % |
| JP-IBA | ncep_gfswave016 | 1.3 m | 76 % |
| JP-IZU | ncep_gfswave016 | 1.2 m | 33 % |
| JP-KYU | ncep_gfswave016 | 1.4 m | 16 % |
| JP-SHK | ncep_gfswave016 | 1.5 m | 90 % |
| JP-SHO | ncep_gfswave016 | 1.0 m | 69 % |
| KR-ALL | ncep_gfswave016 | 1.0 m | 37 % |
| LK-E | ncep_gfswave016 | 1.4 m | 44 % |
| LK-S | ncep_gfswave016 | 1.3 m | 100 % |
| LR-ALL | ncep_gfswave016 | 0.8 m | 0 % |
| MA-N | ncep_gfswave016 | 1.3 m | 98 % |
| MA-S | ncep_gfswave016 | 1.2 m | 100 % |
| MA-TAG | ncep_gfswave016 | 0.8 m | 0 % |
| MG-ALL | ncep_gfswave025 | 1.8 m | 31 % |
| MQ-ALL | ncep_gfswave016 | 1.1 m | 71 % |
| MU-ALL | ncep_gfswave025 | 1.1 m | 85 % |
| MV-CEN | ncep_gfswave016 | 0.9 m | 1 % |
| MV-NMA | ncep_gfswave016 | 1.0 m | 100 % |
| MV-SMA | ncep_gfswave016 | 0.9 m | 18 % |
| MV-SOU | ncep_gfswave016 | 1.0 m | 61 % |
| MX-BCN | ecmwf_wam | 1.2 m | 92 % |
| MX-BCS-N | ncep_gfswave016 | 1.0 m | 49 % |
| MX-BCS | ncep_gfswave016 | 1.0 m | 95 % |
| MX-CAR | ncep_gfswave016 | 0.5 m | 27 % |
| MX-NAY | ncep_gfswave016 | 0.7 m | 0 % |
| MX-OAX | ncep_gfswave016 | 1.2 m | 100 % |
| MX-PAC | ncep_gfswave016 | 1.4 m | 97 % |
| MZ-INH | ncep_gfswave025 | 1.0 m | 45 % |
| MZ-S | ncep_gfswave025 | 1.5 m | 32 % |
| NA-ERO | ncep_gfswave025 | 1.6 m | 100 % |
| NI-NW | ncep_gfswave016 | 1.1 m | 100 % |
| NI-RIV | ncep_gfswave016 | 1.1 m | 100 % |
| NL-ALL | ncep_gfswave025 | 1.2 m | 66 % |
| NO-N | ncep_gfswave025 | 2.1 m | 43 % |
| NO-S | ncep_gfswave025 | 1.7 m | 80 % |
| NZ-AKL | ncep_gfswave025 | 2.0 m | 100 % |
| NZ-BOP | ncep_gfswave025 | 0.6 m | 73 % |
| NZ-GIS | ncep_gfswave025 | 1.1 m | 80 % |
| NZ-KAI | ncep_gfswave025 | 0.9 m | 56 % |
| NZ-NTL | ncep_gfswave025 | 0.9 m | 36 % |
| NZ-OTA | ncep_gfswave025 | 1.3 m | 22 % |
| NZ-RAG | ncep_gfswave025 | 1.7 m | 0 % |
| NZ-TAR | ncep_gfswave025 | 1.7 m | 21 % |
| NZ-WC | ncep_gfswave025 | 1.9 m | 66 % |
| NZ-WEL | ncep_gfswave025 | 1.5 m | 59 % |
| PA-BDT | ncep_gfswave016 | 0.8 m | 79 % |
| PA-PAC | ncep_gfswave016 | 0.3 m | 100 % |
| PE-LIM | ncep_gfswave025 | 1.9 m | 100 % |
| PE-LLB | ncep_gfswave016 | 1.3 m | 44 % |
| PE-NOR | ncep_gfswave016 | 0.9 m | 11 % |
| PE-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| PF-ISL | ncep_gfswave025 | 2.0 m | 6 % |
| PF-TAH | ncep_gfswave025 | 2.1 m | 64 % |
| PG-ALL | ncep_gfswave016 | 0.9 m | 72 % |
| PH-EAS | ncep_gfswave016 | 1.4 m | 89 % |
| PH-LUZ | ncep_gfswave016 | 0.9 m | 96 % |
| PH-SIA | ncep_gfswave016 | 1.2 m | 95 % |
| PR-N | ncep_gfswave016 | 1.1 m | 99 % |
| PR-NW | ncep_gfswave016 | 1.1 m | 0 % |
| PT-ALG | ncep_gfswave016 | 1.6 m | 100 % |
| PT-AZO | ncep_gfswave016 | 1.2 m | 20 % |
| PT-CEN | ncep_gfswave016 | 1.7 m | 100 % |
| PT-ERI | ncep_gfswave016 | 1.7 m | 99 % |
| PT-LIS | ncep_gfswave016 | 1.2 m | 78 % |
| PT-MAD | ncep_gfswave016 | 1.0 m | 0 % |
| PT-NOR | ncep_gfswave016 | 1.7 m | 100 % |
| PT-PEN | ncep_gfswave016 | 1.9 m | 100 % |
| RE-ALL | ncep_gfswave025 | 1.1 m | 67 % |
| SN-ALL | ncep_gfswave016 | 1.4 m | 100 % |
| SV-LIB | ncep_gfswave016 | 1.1 m | 100 % |
| SV-ORI | ncep_gfswave016 | 1.1 m | 53 % |
| TO-ALL | ncep_gfswave025 | 1.5 m | 50 % |
| TT-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| TW-E | ncep_gfswave016 | 1.9 m | 59 % |
| TW-NE | ncep_gfswave016 | 1.8 m | 77 % |
| US-CA-CEN | ecmwf_wam | 1.5 m | 83 % |
| US-CA-LA | ecmwf_wam | 0.9 m | 100 % |
| US-CA-NOR | ecmwf_wam | 1.7 m | 100 % |
| US-CA-OC | ecmwf_wam | 1.0 m | 100 % |
| US-CA-SB | ecmwf_wam | 0.8 m | 100 % |
| US-CA-SC | ecmwf_wam | 1.2 m | 58 % |
| US-CA-SD | ncep_gfswave016 | 0.8 m | 88 % |
| US-CA-SF | ecmwf_wam | 1.4 m | 100 % |
| US-FL-PAN | ecmwf_wam | 0.6 m | 60 % |
| US-FL | ncep_gfswave016 | 1.8 m | 100 % |
| US-GULF | ecmwf_wam | 0.5 m | 98 % |
| US-HI-BIG | ecmwf_wam | 1.0 m | 66 % |
| US-HI-KAU | ecmwf_wam | 1.8 m | 75 % |
| US-HI-MAU | ecmwf_wam | 1.6 m | 55 % |
| US-HI-OAN | ncep_gfswave016 | 1.5 m | 79 % |
| US-HI-OAS | ecmwf_wam | 1.1 m | 54 % |
| US-MID | ncep_gfswave025 | 0.9 m | 98 % |
| US-NE | ecmwf_wam | 0.7 m | 69 % |
| US-PNW | ecmwf_wam | 1.8 m | 100 % |
| US-SC-GA | ncep_gfswave016 | 0.9 m | 91 % |
| US-SE | ncep_gfswave025 | 1.3 m | 100 % |
| UY-CAN | ncep_gfswave025 | 0.7 m | 40 % |
| UY-MAL | ncep_gfswave025 | 1.0 m | 78 % |
| UY-ROC | ncep_gfswave025 | 1.2 m | 61 % |
| VE-ALL | ncep_gfswave016 | 0.5 m | 89 % |
| VN-ALL | ncep_gfswave016 | 0.7 m | 100 % |
| VU-ALL | ncep_gfswave025 | 1.3 m | 27 % |
| WS-ALL | ncep_gfswave025 | 1.9 m | 73 % |
| ZA-EC-JB | ncep_gfswave025 | 2.0 m | 3 % |
| ZA-EC-PE | ncep_gfswave025 | 2.1 m | 23 % |
| ZA-EC-WLD | ncep_gfswave025 | 1.8 m | 48 % |
| ZA-KZN-DBN | ncep_gfswave025 | 1.6 m | 62 % |
| ZA-KZN-N | ncep_gfswave025 | 1.6 m | 68 % |
| ZA-KZN-S | ncep_gfswave025 | 1.8 m | 53 % |
| ZA-WC-CPT | ncep_gfswave025 | 1.8 m | 28 % |
| ZA-WC-GR | ncep_gfswave025 | 1.7 m | 93 % |
| ZA-WC-WCO | ncep_gfswave025 | 1.6 m | 0 % |
