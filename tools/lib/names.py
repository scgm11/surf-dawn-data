"""Spot names as people write them: the distinctive part of a name ("PRAIA DO ROSA" -> "ROSA") and
comparison without case or accents. One copy for tools/resolve_seeds.py (OpenStreetMap) and
tools/check_spots.py (Wikidata)."""
import unicodedata

PREFIXES = ["PRAIA DO ", "PRAIA DA ", "PRAIA DE ", "PRAIA ", "PLAYA DE ", "PLAYA DEL ", "PLAYA ", "BAHÍA DE ",
            "BAHÍA ", "BAIA ", "PUNTA DE ", "PUNTA ", "PONTA DO ", "PONTA DA ", "PONTA ", "CABO ", "PLAGE DE ",
            "PLAGE ", "PRAIA DOS ", "PRAIA DAS ", "BARRA DE ", "BARRA DO ", "BARRA ", "EL ", "LA ", "LOS ", "LAS ",
            "THE "]
SUFFIXES = [" BEACH", " POINT", " BAY", " REEF", " HEAD", " HEADS", " PIER", " RIGHT", " LEFT", " LEFTS",
            " RIGHTS", " BREAK", " INLET", " COVE"]


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def variants(name):
    out = [name]
    n = name
    for p in PREFIXES:
        if n.startswith(p) and len(n) > len(p) + 2:
            out.append(n[len(p):])
            break
    for s in SUFFIXES:
        for v in list(out):
            if v.endswith(s) and len(v) > len(s) + 2:
                out.append(v[:-len(s)])
    return list(dict.fromkeys(v.strip(" '.-") for v in out if len(v.strip()) >= 3))


def matches(label, names):
    """label (a place's name) contains one of the name variants, or one of them contains it."""
    f = fold(label)
    return bool(f) and any(fold(v) in f or (len(f) >= 4 and f in fold(v)) for v in names)


def regex(v):
    """An Overpass regex for v that ignores accents (case is ignored by the query flag)."""
    alts = {"a": "[aáàâãä]", "e": "[eéèêë]", "i": "[iíìîï]", "o": "[oóòôõö]", "u": "[uúùûü]",
            "c": "[cç]", "n": "[nñ]", "y": "[yý]"}
    out = []
    for ch in fold(v):
        if ch in alts:
            out.append(alts[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in " -'.":
            out.append(".?")
        else:
            out.append(".")
    return "".join(out)
