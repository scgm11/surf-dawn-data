"""Which Open-Meteo models a region uses (docs/formatos.md): its row of models.csv (chosen from the
validation against buoys, validation/models-suggested.csv, or by hand), else the default rule:
GFS-Wave 0.16° where it covers (15° S to 52.5° N), else 0.25°, and GFS for the wind. Uruguay,
Argentina, Santa Catarina and Rio Grande do Sul stay on GFS-Wave 0.25 + GFS, the models Windguru
shows there (issue #7): they are validated for information, never moved. One copy for
tools/build_zones.py and validate/."""
import csv
import os

from tools.lib import seeds

DEFAULT_WIND = "gfs_seamless"
FIXED_COUNTRIES = {"UY", "AR"}
FIXED_PREFIXES = ("BR-SC-", "BR-RS")          # Santa Catarina and Rio Grande do Sul
FIXED_MODELS = ("ncep_gfswave025", "gfs_seamless")
CSV = os.path.join(seeds.ROOT, "models.csv")


def is_fixed(code, country):
    return country in FIXED_COUNTRIES or code.startswith(FIXED_PREFIXES)


def default(code, country, lat):
    """[wave model, wind model] by the rule."""
    if is_fixed(code, country):
        return list(FIXED_MODELS)
    return ["ncep_gfswave016" if -15.0 <= lat <= 52.5 else "ncep_gfswave025", DEFAULT_WIND]


def read(path=None):
    """{region: [wave model, wind model]} of models.csv (empty when there is none)."""
    path = path or CSV
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["region"]: [r["wave"], r["wind"]] for r in csv.DictReader(f)}


def for_region(code, country, lat, rows):
    """The models of a region: its row of models.csv (rows = read()), else the rule."""
    return list(rows.get(code) or default(code, country, lat))
