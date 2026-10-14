# Picos: controles por pico

Generado 2026-10-14 22:51 UTC por `tools/check_spots.py` (issue #7, §5.2, §5.4 y §5.8). 212 regiones, 2494 picos.

- **Orientación (§5.2):** olas de los últimos 14 días y los próximos 2 en el punto de olas de cada pico (el modelo de su zona). Se marca un pico al que las olas de al menos 0.3 m casi nunca le llegan a menos de 75° de hacia donde mira (menos del 5 % de las horas) mientras a su zona sí (al menos 25 %).
- **Temporada:** los marcados por la orientación se miran de nuevo con 92 días de olas; 33 dejaron de estarlo (en dos semanas no les tocaba su ventana de swell).
- **Vecinos (§5.4):** se marca un pico sin olas todo ese tiempo, o con más del doble de la altura media de su zona.
- **Emblemáticos (§5.8):** la posición contra Wikidata (el ítem más cercano con su nombre, hasta 6 km; si no tiene, OpenStreetMap): 289 bien (a menos de 1.5 km), 3 lejos, 23 lejos pero revisados a mano (el ítem es el pueblo, un hotel u otra ola: `checked` en la semilla), 77 sin fuente (revisar a mano), 0 sin respuesta.
- Open-Meteo: 35 pedidos, ~2086 llamadas de las 10.000 diarias gratuitas.

## Orientación probablemente del lado equivocado (4)

Mira a más de 135° de sus vecinos (a 30 km) y de las olas, y dada vuelta coincide con ellos: casi seguro se calculó del otro lado de una punta, una isla o una laguna. Se corrige con `facing=` en la semilla.

| Región | Pico | Mira a | Vecinos | Olas desde |
|---|---|---|---|---|
| AU-NSW-NR | THE PASS | 304° | 86° | 122° |
| AU-QLD-SC | FIRST POINT | 310° | 86° | 107° |
| ES-CN-E | PUNTA MUJERES | 128° | 321° | 344° |
| ZA-WC-GR | INNER POOL | 331° | 141° | 192° |

## Picos marcados (124)

Muchos son puntas y arrecifes donde la ola entra dando la vuelta (la orientación de la playa está bien y el semáforo del swell es conservador ahí); se revisan a mano.

| Región | Pico | Emblemático | Mira a | Olas desde | Vecinos | Por qué |
|---|---|---|---|---|---|---|
| AU-NSW-NR | THE PASS | sí | 304° | 122° | 86° | las olas casi nunca le entran de frente (1 % de las horas; la zona 82 %) y en 92 días 1 % |
| AU-QLD-SC | FIRST POINT | sí | 310° | 107° | 86° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| AU-QLD-SC | LITTLE COVE |  | 312° | 107° | 86° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| AU-SA-EYR | CAVES |  | 142° | 226° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-TAS | MARRAWAH |  | 314° | 232° | — | 3.2 m de media, más del doble de la zona (1.4 m) |
| AU-TAS | GREEN POINT |  | 61° | 232° | — | 3.2 m de media, más del doble de la zona (1.4 m); las olas casi nunca le entran de frente (0 % de las horas; la zona 53 %) y en 92 días 0 % |
| AU-VIC-PI | FOREST CAVES |  | 127° | 223° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-VIC-SC | BARWON BLUFF |  | 65° | 194° | 151° | las olas casi nunca le entran de frente (3 % de las horas; la zona 99 %) y en 92 días 1 % |
| AU-VIC-SC | LORNE POINT | sí | 43° | 226° | 159° | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 0 % |
| AU-WA-PER | STRICKLAND BAY | sí | 169° | 255° | 277° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| AU-WA-PER | STARK BAY |  | 163° | 255° | 276° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| BB-ALL | SANDY LANE |  | 262° | 33° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| BB-ALL | DRILL HALL |  | 259° | 33° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| BB-ALL | FREIGHTS BAY | sí | 255° | 98° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| BB-ALL | SURFERS POINT |  | 235° | 98° | 325° | las olas casi nunca le entran de frente (0 % de las horas; la zona 35 %) y en 92 días 0 % |
| BR-NE-CE | PARACURU |  | 334° | 74° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 100 %) y en 92 días 4 % |
| BR-NE-RN | PIPA | sí | 6° | 93° | 59° | las olas casi nunca le entran de frente (4 % de las horas; la zona 100 %) y en 92 días 2 % |
| BR-SP | PAÚBA |  | 273° | 158° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 1 % |
| BR-SP | CAMBURI |  | 261° | 157° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 3 % |
| BR-SP | ILHA COMPRIDA |  | 322° | 139° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CA-NS | HIRTLE'S BEACH |  | 19° | 161° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 54 %) y en 92 días 1 % |
| CL-NOR | LAS MACHAS |  | 324° | 221° | 279° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CO-PAC | HUINA |  | 312° | 231° | 225° | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-CAR | PUNTA UVA |  | 321° | 55° | 15° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-GUA | OLLIE'S POINT |  | 144° | 238° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| CR-GUA | PICO PEQUEÑO |  | 331° | 232° | 249° | las olas casi nunca le entran de frente (5 % de las horas; la zona 100 %) y en 92 días 2 % |
| CR-OSA | RIO CLARO |  | 311° | 218° | 245° | las olas casi nunca le entran de frente (0 % de las horas; la zona 71 %) y en 92 días 2 % |
| EC-COS | PUNTA CARNERO |  | 355° | 237° | 278° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| EC-GAL | MANGLECITO |  | 322° | 212° | 262° | las olas casi nunca le entran de frente (0 % de las horas; la zona 49 %) y en 92 días 0 % |
| ES-AND | BOLONIA |  | 191° | 73° | 227° | las olas casi nunca le entran de frente (3 % de las horas; la zona 41 %) y en 92 días 2 % |
| ES-CN-E | PUNTA MUJERES |  | 128° | 344° | 321° | las olas casi nunca le entran de frente (0 % de las horas; la zona 64 %) y en 92 días 0 % |
| ES-CN-E | FLAG BEACH |  | 88° | 343° | 275° | las olas casi nunca le entran de frente (1 % de las horas; la zona 64 %) y en 92 días 3 % |
| ES-CN-E | ROCKY POINT |  | 218° | 344° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 64 %) y en 92 días 0 % |
| ES-CN-W | LAS CANTERAS |  | 215° | 356° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 0 % |
| ES-CN-W | EL FRONTON | sí | 221° | 355° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 0 % |
| ES-CN-W | SARDINA |  | 215° | 355° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 0 % |
| ES-CN-W | EL CAMISON |  | 293° | 166° | — | las olas casi nunca le entran de frente (5 % de las horas; la zona 65 %) y en 92 días 2 % |
| ES-CN-W | PUNTA BLANCA |  | 293° | 166° | — | las olas casi nunca le entran de frente (5 % de las horas; la zona 65 %) y en 92 días 2 % |
| ES-PV | HONDARRIBIA |  | 59° | 309° | 330° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 5 % |
| FJ-MAM | CLOUDBREAK | sí | 220° | 209° | 254° | 1.0 m de media, más del doble de la zona (0.5 m) |
| FR-BRE | LE POULDU |  | 132° | 255° | 221° | las olas casi nunca le entran de frente (1 % de las horas; la zona 95 %) y en 92 días 3 % |
| FR-VEN | LA TRANCHE |  | 151° | 267° | 211° | las olas casi nunca le entran de frente (2 % de las horas; la zona 99 %) y en 92 días 0 % |
| ID-BAL-E | SANUR REEF | sí | 79° | 195° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| ID-BAL-E | MERTASARI |  | 64° | 195° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | SHIPWRECKS | sí | 327° | 197° | 120° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | LACERATIONS |  | 23° | 197° | 125° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-E | PLAYGROUNDS |  | 289° | 197° | 115° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-W | KUTA REEF |  | 295° | 195° | 238° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-BAL-W | HALFWAY KUTA |  | 312° | 195° | 237° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-LOM | MAWI |  | 0° | 207° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 0 % |
| ID-LOM | KUTA LOMBOK |  | 65° | 207° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 0 % |
| ID-LOM | GERUPUK | sí | 117° | 207° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 3 % |
| ID-LOM | DON DON |  | 0° | 207° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 0 % |
| ID-LOM | EKAS |  | 303° | 208° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 76 %) y en 92 días 0 % |
| ID-SBW | SCAR REEF | sí | 322° | 208° | 234° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| ID-SBW | SUPERSUCK | sí | 330° | 208° | 234° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| IE-NW | MULLAGHMORE | sí | 37° | 283° | 315° | las olas casi nunca le entran de frente (0 % de las horas; la zona 95 %) y en 92 días 0 % |
| IS-ALL | THORLAKSHOFN |  | 61° | 197° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 82 %) y en 92 días 0 % |
| JP-KYU | AOSHIMA |  | 236° | 96° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 50 %) y en 92 días 1 % |
| LK-E | ARUGAM BAY | sí | 22° | 182° | 123° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| MA-TAG | BOILERS | sí | 185° | 320° | 230° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | KILLER POINT | sí | 213° | 320° | 224° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | ANCHOR POINT | sí | 199° | 320° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | LA SOURCE |  | 189° | 320° | 226° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | HASH POINT | sí | 188° | 320° | 226° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | MYSTERIES |  | 199° | 320° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | AGADIR |  | 200° | 320° | 225° | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MA-TAG | ESSAOUIRA |  | 153° | 322° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 29 %) y en 92 días 0 % |
| MG-ALL | ANAKAO |  | 299° | 211° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 68 %) y en 92 días 2 % |
| MU-ALL | TAMARIN BAY |  | 317° | 203° | 206° | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| MX-BCS-N | SCORPION BAY | sí | 90° | 216° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 50 %) y en 92 días 0 % |
| MX-NAY | SAYULITA | sí | 353° | 227° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 52 %) y en 92 días 0 % |
| MX-OAX | MAZUNTE |  | 123° | 219° | 187° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| MZ-INH | BARRA |  | 14° | 107° | 104° | las olas casi nunca le entran de frente (0 % de las horas; la zona 84 %) y en 92 días 3 % |
| NA-ERO | SKELETON BAY | sí | 321° | 218° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| NZ-AKL | PORT WAIKATO |  | 358° | 243° | — | las olas casi nunca le entran de frente (2 % de las horas; la zona 100 %) y en 92 días 2 % |
| NZ-NTL | BAYLYS BEACH |  | 235° | 227° | — | 2.2 m de media, más del doble de la zona (1.1 m) |
| NZ-OTA | KARITANE | sí | 284° | 148° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 72 %) y en 92 días 0 % |
| NZ-OTA | WHAREAKEAKE | sí | 311° | 148° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 72 %) y en 92 días 0 % |
| NZ-OTA | ARAMOANA SPIT | sí | 353° | 148° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 72 %) y en 92 días 3 % |
| NZ-WC | TAURANGA BAY |  | 43° | 268° | — | las olas casi nunca le entran de frente (1 % de las horas; la zona 100 %) y en 92 días 1 % |
| PA-PAC | PLAYA ESTERO |  | 258° | 170° | 210° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PA-PAC | PLAYA VENAO | sí | 235° | 210° | — | 0.9 m de media, más del doble de la zona (0.4 m) |
| PA-PAC | GUANICO |  | 153° | 199° | 209° | 0.8 m de media, más del doble de la zona (0.4 m) |
| PA-PAC | CAMBUTAL |  | 183° | 212° | — | 1.1 m de media, más del doble de la zona (0.4 m) |
| PE-LIM | LA HERRADURA | sí | 336° | 217° | 232° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PE-LIM | CERRO AZUL |  | 327° | 226° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| PE-LLB | PACASMAYO | sí | 316° | 225° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 0 % |
| PE-LLB | CHICAMA | sí | 339° | 233° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 0 % |
| PE-LLB | HUANCHACO | sí | 309° | 225° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 98 %) y en 92 días 3 % |
| RE-ALL | BOUCAN CANOT |  | 307° | 208° | 258° | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 0 % |
| RE-ALL | BARACHOIS |  | 317° | 119° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 65 %) y en 92 días 0 % |
| TO-ALL | PASS LEFTS |  | 5° | 130° | 271° | las olas casi nunca le entran de frente (0 % de las horas; la zona 43 %) y en 92 días 0 % |
| TO-ALL | PASS RIGHTS |  | 5° | 130° | 271° | las olas casi nunca le entran de frente (0 % de las horas; la zona 43 %) y en 92 días 0 % |
| TT-ALL | MOUNT IRVINE |  | 280° | 82° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-SC | STEAMER LANE | sí | 130° | 255° | 201° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-CA-SC | PLEASURE POINT | sí | 130° | 255° | 198° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-CA-SC | MORAN LAKE |  | 130° | 255° | 198° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-CA-SC | LOVER'S POINT |  | 56° | 296° | 288° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-SD | LA JOLLA SHORES |  | 298° | 209° | 260° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 5 % |
| US-CA-SD | BIRD ROCK |  | 0° | 209° | 259° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-CA-SD | SOUTH MISSION |  | 349° | 209° | 264° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-FL | FERNANDINA |  | 251° | 92° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-FL | JENSEN BEACH |  | 227° | 72° | 216° | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-FL | STUART BEACH |  | 245° | 72° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-GULF | PADRE SEASHORE |  | 112° | 101° | — | 1.2 m de media, más del doble de la zona (0.6 m) |
| US-HI-BIG | RICHARDSONS |  | 330° | 69° | — | las olas casi nunca le entran de frente (4 % de las horas; la zona 100 %) y en 92 días 1 % |
| US-HI-OAS | CONCESSIONS |  | 284° | 175° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 0 % |
| US-HI-OAS | CANOES |  | 268° | 175° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 2 % |
| US-HI-OAS | QUEENS | sí | 268° | 175° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 96 %) y en 92 días 2 % |
| US-HI-OAS | CHINA WALLS |  | 255° | 160° | — | las olas casi nunca le entran de frente (3 % de las horas; la zona 96 %) y en 92 días 3 % |
| US-NE | BEACH HAVEN |  | 276° | 114° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 83 %) y en 92 días 0 % |
| US-PNW | HOBUCK |  | 88° | 273° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 0 % |
| US-PNW | PORT ORFORD |  | 162° | 305° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 100 %) y en 92 días 2 % |
| US-SE | SURF CITY PIER |  | 2° | 115° | — | las olas casi nunca le entran de frente (4 % de las horas; la zona 99 %) y en 92 días 2 % |
| ZA-WC-CPT | LLANDUDNO | sí | 335° | 234° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 0 % |
| ZA-WC-CPT | DUNGEONS | sí | 101° | 234° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 1 % |
| ZA-WC-CPT | SUNSET REEF | sí | 320° | 233° | — | las olas casi nunca le entran de frente (4 % de las horas; la zona 73 %) y en 92 días 5 % |
| ZA-WC-CPT | LONG BEACH | sí | 343° | 233° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 0 % |
| ZA-WC-CPT | KOGEL BAY |  | 332° | 215° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 0 % |
| ZA-WC-CPT | ROOI-ELS |  | 328° | 215° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 73 %) y en 92 días 0 % |
| ZA-WC-GR | INNER POOL | sí | 331° | 192° | 141° | las olas casi nunca le entran de frente (0 % de las horas; la zona 78 %) y en 92 días 0 % |
| ZA-WC-WCO | ELANDS BAY | sí | 339° | 245° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 27 %) y en 92 días 1 % |
| ZA-WC-WCO | YZERFONTEIN |  | 351° | 237° | — | las olas casi nunca le entran de frente (0 % de las horas; la zona 27 %) y en 92 días 0 % |

## Emblemáticos lejos de su ítem de Wikidata u OpenStreetMap

| Región | Pico | Distancia | Ítem |
|---|---|---|---|
| CO-CAR | PUERTO COLOMBIA | 5.3 km | [osm:relation/1335183](https://www.openstreetmap.org/relation/1335183) Puerto Colombia (10.99571, -74.9161) |
| ZA-KZN-DBN | CAVE ROCK | 4.6 km | [Q31511084](https://www.wikidata.org/wiki/Q31511084) Cave Rock (-29.87998, 31.05608) |
| BR-RJL | ITAÚNA | 1.7 km | [osm:node/651221993](https://www.openstreetmap.org/node/651221993) Itaúna (-22.93355, -42.47566) |

## Emblemáticos sin fuente en Wikidata ni OpenStreetMap (revisar a mano)

AU-NSW-SYD/OURS, AU-QLD-SC/DOUBLE ISLAND PT, AU-VIC-SC/WINKIPOP, AU-WA-MR/MAIN BREAK, AU-WA-MR/THE BOX, AU-WA-MR/NORTH POINT, CL-NOR/EL GRINGO, CR-GUA/WITCH'S ROCK, CR-OSA/PAVONES, DK-ALL/KLITMOLLER, ES-CN-E/EL QUEMAO, ES-CN-W/EL FRONTON, ES-CN-W/LA IZQUIERDA, FJ-MAM/CLOUDBREAK, FJ-MAM/RESTAURANTS, FJ-MAM/SWIMMING POOLS, FR-GIR/LACANAU CENTRALE, FR-HOS/LA NORD, FR-HOS/LES CULS NULS, ID-BAL-E/SHIPWRECKS, ID-JAV-E/MONEY TREES, ID-MEN/MACARONIS, ID-MEN/KANDUI LEFT, ID-MEN/RIFLES, ID-ROT/T-LAND, ID-SBW/SCAR REEF, ID-SBW/SUPERSUCK, IE-NW/EASKEY, IE-SW/AILEEN'S, JP-KYU/KISAKIHAMA, LK-E/WHISKEY POINT, MA-N/SAFI LE JARDIN, MA-TAG/KILLER POINT, MA-TAG/PANORAMAS, MV-NMA/PASTA POINT, MV-NMA/SULTANS, MV-NMA/HONKY'S, MV-NMA/COKES, MV-NMA/CHICKENS, MV-NMA/JAILBREAKS, MV-SOU/TIGER STRIPES, MV-SOU/BEACONS, MX-BCS/ZIPPERS, NA-ERO/SKELETON BAY, NZ-BOP/WHANGAMATA BAR, NZ-GIS/CENTRES, NZ-GIS/STOCK ROUTE, NZ-GIS/PINES, NZ-GIS/WHALES, NZ-KAI/MEATWORKS, NZ-NTL/SUPER TUBES, NZ-NTL/MUKIES 2, NZ-NTL/MUKIES 1, NZ-NTL/PEAKS, NZ-OTA/ARAMOANA SPIT, NZ-RAG/INDICATORS, PF-TAH/HA'APITI, PH-SIA/JACKING HORSE, PH-SIA/QUICKSILVER, PR-NW/WILDERNESS, PR-NW/TRES PALMAS, SV-ORI/LAS FLORES, TW-E/JINZUN HARBOR, US-CA-OC/UPPER TRESTLES, US-CA-OC/LOWER TRESTLES, US-CA-SB/C STREET, US-HI-BIG/HONOLI'I, US-HI-BIG/BANYANS, US-HI-KAU/PK'S, US-HI-MAU/HO'OKIPA, US-HI-OAN/BACKDOOR, US-NE/RUGGLES, US-PNW/SHORT SANDS, ZA-EC-JB/BRUCE'S BEAUTIES, ZA-WC-CPT/DUNGEONS, ZA-WC-CPT/SUNSET REEF, ZA-WC-GR/INNER POOL

## Zonas

| Región | Modelo | Altura media (mediana) | Olas de frente (mediana) |
|---|---|---|---|
| AR-BAN | ncep_gfswave025 | 1.4 m | 100 % |
| AR-MDP | ncep_gfswave025 | 1.5 m | 100 % |
| AR-SUR | ncep_gfswave025 | 1.1 m | 97 % |
| AU-NSW-MN | ncep_gfswave025 | 1.5 m | 72 % |
| AU-NSW-NC | ncep_gfswave025 | 1.4 m | 79 % |
| AU-NSW-NR | ncep_gfswave025 | 1.5 m | 82 % |
| AU-NSW-SC | ncep_gfswave025 | 1.5 m | 78 % |
| AU-NSW-SYD | ncep_gfswave025 | 1.6 m | 73 % |
| AU-QLD-GC | ncep_gfswave025 | 1.1 m | 80 % |
| AU-QLD-SC | ncep_gfswave025 | 1.1 m | 100 % |
| AU-SA-EYR | ncep_gfswave025 | 1.4 m | 100 % |
| AU-SA | ecmwf_wam | 1.4 m | 98 % |
| AU-TAS | ncep_gfswave025 | 1.4 m | 53 % |
| AU-VIC-PI | ncep_gfswave025 | 1.4 m | 100 % |
| AU-VIC-SC | ncep_gfswave025 | 1.4 m | 99 % |
| AU-VIC-W | ncep_gfswave025 | 2.7 m | 100 % |
| AU-WA-GAS | ncep_gfswave025 | 1.3 m | 16 % |
| AU-WA-MR | ncep_gfswave025 | 3.1 m | 97 % |
| AU-WA-NW | ncep_gfswave025 | 2.0 m | 100 % |
| AU-WA-PER | ncep_gfswave025 | 2.0 m | 100 % |
| BB-ALL | ncep_gfswave016 | 1.1 m | 35 % |
| BR-BA | ncep_gfswave025 | 1.1 m | 100 % |
| BR-ES | ncep_gfswave025 | 1.2 m | 100 % |
| BR-NE-CE | ncep_gfswave016 | 1.2 m | 100 % |
| BR-NE-PE | ncep_gfswave016 | 1.1 m | 100 % |
| BR-NE-RN | ncep_gfswave016 | 1.1 m | 100 % |
| BR-NOR | ncep_gfswave016 | 1.4 m | 26 % |
| BR-RJ | ncep_gfswave025 | 0.8 m | 100 % |
| BR-RJL | ncep_gfswave025 | 1.1 m | 95 % |
| BR-RS-SUL | ncep_gfswave025 | 1.3 m | 100 % |
| BR-RS | ncep_gfswave025 | 1.4 m | 100 % |
| BR-SC-FLN | ncep_gfswave025 | 1.4 m | 99 % |
| BR-SC-NOR | ncep_gfswave025 | 0.9 m | 100 % |
| BR-SC-SUL | ncep_gfswave025 | 1.4 m | 100 % |
| BR-SP | ncep_gfswave025 | 0.8 m | 100 % |
| BS-ALL | ncep_gfswave016 | 0.8 m | 11 % |
| CA-BC-VI | ecmwf_wam | 1.2 m | 24 % |
| CA-NS | ncep_gfswave016 | 1.1 m | 54 % |
| CL-CEN | ncep_gfswave025 | 1.6 m | 13 % |
| CL-MAU | ncep_gfswave025 | 1.6 m | 95 % |
| CL-NOR | ncep_gfswave025 | 1.5 m | 100 % |
| CL-PIC | ncep_gfswave025 | 1.8 m | 68 % |
| CL-SUR | ncep_gfswave025 | 1.7 m | 100 % |
| CN-HAI | ncep_gfswave016 | 0.8 m | 53 % |
| CO-CAR | ncep_gfswave016 | 0.8 m | 100 % |
| CO-PAC | ncep_gfswave016 | 0.8 m | 100 % |
| CR-CAR | ncep_gfswave016 | 0.8 m | 100 % |
| CR-GUA | ncep_gfswave016 | 1.2 m | 100 % |
| CR-NIC | ncep_gfswave016 | 1.1 m | 100 % |
| CR-OSA | ncep_gfswave016 | 1.1 m | 71 % |
| CR-PAC | ncep_gfswave016 | 1.0 m | 100 % |
| CV-ALL | ncep_gfswave016 | 1.2 m | 4 % |
| DE-ALL | ncep_gfswave025 | 1.1 m | 85 % |
| DK-ALL | ncep_gfswave025 | 1.4 m | 81 % |
| DO-ALL | ncep_gfswave016 | 1.0 m | 100 % |
| EC-COS | ncep_gfswave016 | 0.9 m | 100 % |
| EC-GAL | ncep_gfswave016 | 1.1 m | 49 % |
| ES-AND | ncep_gfswave016 | 0.6 m | 41 % |
| ES-AST | ncep_gfswave016 | 1.4 m | 100 % |
| ES-CAN | ncep_gfswave016 | 1.3 m | 100 % |
| ES-CN-E | ncep_gfswave016 | 1.3 m | 64 % |
| ES-CN-W | ncep_gfswave016 | 1.1 m | 65 % |
| ES-GAL | ncep_gfswave016 | 1.7 m | 96 % |
| ES-PV | ncep_gfswave016 | 1.2 m | 100 % |
| FJ-MAM | ncep_gfswave025 | 0.5 m | 100 % |
| FJ-SOU | ncep_gfswave025 | 1.3 m | 98 % |
| FR-BRE | ncep_gfswave016 | 1.2 m | 95 % |
| FR-GIR | ncep_gfswave016 | 1.4 m | 100 % |
| FR-HOS | ncep_gfswave016 | 1.4 m | 100 % |
| FR-PBA | ncep_gfswave016 | 1.4 m | 100 % |
| FR-VEN | ncep_gfswave016 | 0.9 m | 99 % |
| GB-CON | ncep_gfswave016 | 1.7 m | 99 % |
| GB-DEV | ncep_gfswave016 | 1.4 m | 92 % |
| GB-NE | ncep_gfswave025 | 0.8 m | 67 % |
| GB-NIR | ecmwf_wam | 1.0 m | 82 % |
| GB-SCO | ncep_gfswave025 | 1.5 m | 40 % |
| GB-SOU | ncep_gfswave016 | 0.7 m | 89 % |
| GB-WAL | ncep_gfswave025 | 1.5 m | 89 % |
| GH-ALL | ncep_gfswave016 | 0.9 m | 100 % |
| GP-ALL | ncep_gfswave016 | 1.1 m | 6 % |
| GT-PAC | ncep_gfswave016 | 1.2 m | 100 % |
| ID-BAL-BUK | ncep_gfswave016 | 1.8 m | 0 % |
| ID-BAL-E | ncep_gfswave016 | 1.2 m | 100 % |
| ID-BAL-W | ncep_gfswave016 | 1.2 m | 100 % |
| ID-JAV-E | ncep_gfswave016 | 1.5 m | 0 % |
| ID-JAV-W | ncep_gfswave016 | 1.6 m | 0 % |
| ID-KRU | ncep_gfswave016 | 1.9 m | 0 % |
| ID-LOM | ncep_gfswave016 | 1.8 m | 76 % |
| ID-MEN | ncep_gfswave016 | 1.2 m | 0 % |
| ID-NIA | ncep_gfswave016 | 1.3 m | 6 % |
| ID-ROT | ncep_gfswave016 | 0.9 m | 100 % |
| ID-SBW | ncep_gfswave016 | 1.5 m | 100 % |
| ID-SMB | ncep_gfswave016 | 1.5 m | 100 % |
| IE-NW | ncep_gfswave025 | 2.1 m | 95 % |
| IE-SE | ncep_gfswave016 | 1.5 m | 89 % |
| IE-SW | ecmwf_wam | 1.6 m | 98 % |
| IN-E | ncep_gfswave016 | 0.6 m | 100 % |
| IN-W | ncep_gfswave016 | 0.7 m | 100 % |
| IS-ALL | ncep_gfswave025 | 3.0 m | 82 % |
| IT-ALL | ncep_gfswave016 | 0.5 m | 80 % |
| IT-SAR | ncep_gfswave016 | 0.7 m | 76 % |
| JP-CHI | ncep_gfswave016 | 2.0 m | 99 % |
| JP-IBA | ncep_gfswave016 | 1.7 m | 99 % |
| JP-IZU | ncep_gfswave016 | 1.3 m | 90 % |
| JP-KYU | ncep_gfswave016 | 1.5 m | 50 % |
| JP-SHK | ncep_gfswave016 | 1.5 m | 93 % |
| JP-SHO | ncep_gfswave016 | 0.8 m | 83 % |
| KR-ALL | ncep_gfswave016 | 0.7 m | 40 % |
| LK-E | ncep_gfswave016 | 1.1 m | 83 % |
| LK-S | ncep_gfswave016 | 1.1 m | 100 % |
| LR-ALL | ncep_gfswave016 | 1.0 m | 0 % |
| MA-N | ncep_gfswave016 | 1.2 m | 100 % |
| MA-S | ncep_gfswave016 | 1.2 m | 100 % |
| MA-TAG | ncep_gfswave016 | 0.8 m | 29 % |
| MG-ALL | ncep_gfswave025 | 2.1 m | 68 % |
| MQ-ALL | ncep_gfswave016 | 1.1 m | 88 % |
| MU-ALL | ncep_gfswave025 | 1.4 m | 83 % |
| MV-CEN | ncep_gfswave016 | 0.8 m | 0 % |
| MV-NMA | ncep_gfswave016 | 0.8 m | 0 % |
| MV-SMA | ncep_gfswave016 | 0.7 m | 88 % |
| MV-SOU | ncep_gfswave016 | 1.0 m | 96 % |
| MX-BCN | ecmwf_wam | 1.2 m | 95 % |
| MX-BCS-N | ncep_gfswave016 | 1.3 m | 50 % |
| MX-BCS | ncep_gfswave016 | 1.6 m | 100 % |
| MX-CAR | ncep_gfswave016 | 0.9 m | 99 % |
| MX-NAY | ncep_gfswave016 | 1.4 m | 52 % |
| MX-OAX | ncep_gfswave016 | 1.6 m | 100 % |
| MX-PAC | ncep_gfswave016 | 2.1 m | 100 % |
| MZ-INH | ncep_gfswave025 | 1.1 m | 84 % |
| MZ-S | ncep_gfswave025 | 1.6 m | 84 % |
| NA-ERO | ncep_gfswave025 | 1.7 m | 100 % |
| NI-NW | ncep_gfswave016 | 1.0 m | 100 % |
| NI-RIV | ncep_gfswave016 | 1.1 m | 100 % |
| NL-ALL | ncep_gfswave025 | 1.0 m | 95 % |
| NO-N | ncep_gfswave025 | 1.9 m | 66 % |
| NO-S | ncep_gfswave025 | 1.9 m | 89 % |
| NZ-AKL | ncep_gfswave025 | 1.9 m | 100 % |
| NZ-BOP | ncep_gfswave025 | 0.7 m | 86 % |
| NZ-GIS | ncep_gfswave025 | 1.2 m | 66 % |
| NZ-KAI | ncep_gfswave025 | 1.1 m | 87 % |
| NZ-NTL | ncep_gfswave025 | 1.1 m | 2 % |
| NZ-OTA | ncep_gfswave025 | 1.3 m | 72 % |
| NZ-RAG | ncep_gfswave025 | 1.5 m | 2 % |
| NZ-TAR | ncep_gfswave025 | 1.4 m | 70 % |
| NZ-WC | ncep_gfswave025 | 1.5 m | 100 % |
| NZ-WEL | ncep_gfswave025 | 1.2 m | 62 % |
| PA-BDT | ncep_gfswave016 | 0.8 m | 100 % |
| PA-PAC | ncep_gfswave016 | 0.4 m | 100 % |
| PE-LIM | ncep_gfswave025 | 1.6 m | 100 % |
| PE-LLB | ncep_gfswave016 | 1.2 m | 98 % |
| PE-NOR | ncep_gfswave016 | 1.0 m | 60 % |
| PE-SUR | ncep_gfswave025 | 1.5 m | 100 % |
| PF-ISL | ncep_gfswave025 | 2.2 m | 25 % |
| PF-TAH | ncep_gfswave025 | 2.2 m | 81 % |
| PG-ALL | ncep_gfswave016 | 0.9 m | 70 % |
| PH-EAS | ncep_gfswave016 | 1.1 m | 99 % |
| PH-LUZ | ncep_gfswave016 | 0.6 m | 100 % |
| PH-SIA | ncep_gfswave016 | 1.0 m | 100 % |
| PR-N | ncep_gfswave016 | 0.8 m | 100 % |
| PR-NW | ncep_gfswave016 | 0.6 m | 2 % |
| PT-ALG | ncep_gfswave016 | 1.6 m | 100 % |
| PT-AZO | ncep_gfswave016 | 1.1 m | 22 % |
| PT-CEN | ncep_gfswave016 | 1.5 m | 100 % |
| PT-ERI | ncep_gfswave016 | 1.6 m | 100 % |
| PT-LIS | ncep_gfswave016 | 1.1 m | 97 % |
| PT-MAD | ncep_gfswave016 | 0.8 m | 20 % |
| PT-NOR | ncep_gfswave016 | 1.5 m | 100 % |
| PT-PEN | ncep_gfswave016 | 1.7 m | 96 % |
| RE-ALL | ncep_gfswave025 | 1.3 m | 65 % |
| SN-ALL | ncep_gfswave016 | 1.3 m | 89 % |
| SV-LIB | ncep_gfswave016 | 1.2 m | 100 % |
| SV-ORI | ncep_gfswave016 | 1.1 m | 100 % |
| TO-ALL | ncep_gfswave025 | 1.7 m | 43 % |
| TT-ALL | ncep_gfswave016 | 0.8 m | 100 % |
| TW-E | ncep_gfswave016 | 1.1 m | 93 % |
| TW-NE | ncep_gfswave016 | 0.9 m | 94 % |
| US-CA-CEN | ecmwf_wam | 1.4 m | 100 % |
| US-CA-LA | ecmwf_wam | 0.9 m | 100 % |
| US-CA-NOR | ecmwf_wam | 1.8 m | 100 % |
| US-CA-OC | ecmwf_wam | 1.0 m | 100 % |
| US-CA-SB | ecmwf_wam | 0.8 m | 100 % |
| US-CA-SC | ecmwf_wam | 1.1 m | 100 % |
| US-CA-SD | ncep_gfswave016 | 0.8 m | 100 % |
| US-CA-SF | ecmwf_wam | 1.3 m | 100 % |
| US-FL-PAN | ecmwf_wam | 0.7 m | 89 % |
| US-FL | ncep_gfswave016 | 0.7 m | 100 % |
| US-GULF | ecmwf_wam | 0.6 m | 99 % |
| US-HI-BIG | ecmwf_wam | 1.0 m | 100 % |
| US-HI-KAU | ecmwf_wam | 1.4 m | 100 % |
| US-HI-MAU | ecmwf_wam | 1.4 m | 100 % |
| US-HI-OAN | ncep_gfswave016 | 1.1 m | 96 % |
| US-HI-OAS | ecmwf_wam | 1.2 m | 96 % |
| US-MID | ncep_gfswave025 | 0.8 m | 89 % |
| US-NE | ecmwf_wam | 0.6 m | 83 % |
| US-PNW | ecmwf_wam | 1.5 m | 100 % |
| US-SC-GA | ncep_gfswave016 | 0.6 m | 98 % |
| US-SE | ncep_gfswave025 | 0.8 m | 99 % |
| UY-MAL | ncep_gfswave025 | 1.4 m | 100 % |
| UY-ROC | ncep_gfswave025 | 1.6 m | 92 % |
| VE-ALL | ncep_gfswave016 | 0.5 m | 100 % |
| VN-ALL | ncep_gfswave016 | 0.5 m | 99 % |
| VU-ALL | ncep_gfswave025 | 1.4 m | 46 % |
| WS-ALL | ncep_gfswave025 | 2.2 m | 100 % |
| ZA-EC-JB | ncep_gfswave025 | 2.5 m | 21 % |
| ZA-EC-PE | ncep_gfswave025 | 2.1 m | 74 % |
| ZA-EC-WLD | ncep_gfswave025 | 1.8 m | 85 % |
| ZA-KZN-DBN | ncep_gfswave025 | 1.8 m | 85 % |
| ZA-KZN-N | ncep_gfswave025 | 1.8 m | 98 % |
| ZA-KZN-S | ncep_gfswave025 | 1.9 m | 83 % |
| ZA-WC-CPT | ncep_gfswave025 | 2.2 m | 73 % |
| ZA-WC-GR | ncep_gfswave025 | 2.0 m | 78 % |
| ZA-WC-WCO | ncep_gfswave025 | 2.0 m | 27 % |
