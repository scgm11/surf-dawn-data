"""Spot names as people write them: the distinctive part of a name ("PRAIA DO ROSA" -> "ROSA") and
comparison without case, accents or punctuation ("HO'OKIPA" is "Hoʻokipa", "T-LAND" is "T Land"). One
copy for tools/resolve_seeds.py, tools/check_spots.py, tools/lookup.py and tools/lib/geonames.py."""
import re
import unicodedata

PREFIXES = ["PRAIA DO ", "PRAIA DA ", "PRAIA DE ", "PRAIA ", "PLAYA DE ", "PLAYA DEL ", "PLAYA ", "BAHÍA DE ",
            "BAHÍA ", "BAIA ", "PUNTA DE ", "PUNTA ", "PONTA DO ", "PONTA DA ", "PONTA ", "CABO ", "PLAGE DE ",
            "PLAGE ", "PRAIA DOS ", "PRAIA DAS ", "BARRA DE ", "BARRA DO ", "BARRA ", "EL ", "LA ", "LOS ", "LAS ",
            "THE "]
SUFFIXES = [" BEACH", " POINT", " PT", " BAY", " REEF", " HEAD", " HEADS", " PIER", " RIGHT", " LEFT", " LEFTS",
            " RIGHTS", " BREAK", " INLET", " COVE"]
# a variant that is only one of these says nothing ("NORTH POINT" is not anything named "North...")
GENERIC = {"NORTH", "SOUTH", "EAST", "WEST", "MAIN", "BIG", "LITTLE", "OLD", "NEW", "BACK", "FRONT", "FIRST",
           "SECOND", "THIRD", "INNER", "OUTER", "UPPER", "LOWER", "SURF", "ISLAND", "SANTA", "SAN", "SÃO"}
SIDES = ["UPPER ", "LOWER ", "OUTER "]     # "UPPER TRESTLES" is a part of "Trestles" (the rest 6 letters or more)


APOSTROPHES = "'\u2019\u2018\u02bb\u02bc`\u00b4"      # ' ’ ‘ ʻ (Hawaiian ʻokina) ʼ ` ´


def fold(s):
    """Lower case without accents (punctuation kept: Overpass regexes are built from it)."""
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def key(s):
    """fold() without apostrophes, with other punctuation as spaces: the form names are compared in."""
    s = "".join(c for c in fold(s) if c not in APOSTROPHES)
    return " ".join(re.sub(r"[-_.,;:/()]", " ", s).split())


def variants(name):
    out = [name]
    n = name
    for p in PREFIXES:
        if n.startswith(p) and len(n) > len(p) + 2:
            out.append(n[len(p):])
            break
    for p in SIDES:
        if n.startswith(p) and len(n) >= len(p) + 6:
            out.append(n[len(p):])
    if re.search(r" \d$", n):                     # "MUKIES 2"
        out.append(n[:-2])
    for s in SUFFIXES:
        for v in list(out):
            if v.endswith(s) and len(v) > len(s) + 2:
                out.append(v[:-len(s)])
    for v in list(out):                             # "SHORT SANDS" is "Short Sand Beach"
        if " " in v and v.endswith("S") and not v.endswith("SS") and len(v.split()[-1]) >= 5:
            out.append(v[:-1])
    out = [out[0]] + [v for v in out[1:] if v.strip(" '.-") not in GENERIC]
    return list(dict.fromkeys(v.strip(" '.-") for v in out if len(v.strip()) >= 3))


def matches(label, names):
    """label (a place's name) contains one of the name variants, or one of them contains it."""
    f = key(label)
    return bool(f) and any(key(v) in f or (len(f) >= 4 and f in key(v)) for v in names)


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
        elif ch in " -." or ch in APOSTROPHES:
            out.append(".?")
        else:
            out.append(".")
    return "".join(out)
