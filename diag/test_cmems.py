"""Diagnostic run of validate/run.py with the cmems source on a few regions. The Toolbox download is
replaced by the public files of the same dataset (STAC/S3), only to test the parser and the matching here."""
import os, shutil, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "validate"))
import cmems, run
B = "https://s3.waw3-1.cloudferro.com/mdl-native-01/native/INSITU_GLO_PHYBGCWAV_DISCRETE_MYNRT_013_030/cmems_obs-ins_glo_phybgcwav_mynrt_na_irr_202311/"
UA = {"User-Agent": "surf-dawn-validation/1.0 (+https://github.com/scgm11/surf-dawn-data)"}
from concurrent.futures import ThreadPoolExecutor

def anon(paths, directory, log):
    os.makedirs(directory, exist_ok=True)
    def one(p):
        rel = p.split("cmems_obs-ins_glo_phybgcwav_mynrt_na_irr_202311/")[-1]
        dst = os.path.join(directory, p.rsplit("/", 1)[-1])
        if not os.path.exists(dst):
            with urllib.request.urlopen(urllib.request.Request(B + rel, headers=UA), timeout=300) as r, open(dst + ".part", "wb") as f:
                shutil.copyfileobj(r, f)
            os.replace(dst + ".part", dst)
        return dst
    with ThreadPoolExecutor(12) as ex:
        out = list(ex.map(one, paths))
    log("  cmems (diag): %d files" % len(paths))
    return out

cmems.download = anon
os.environ[cmems.ENV_USER] = os.environ[cmems.ENV_PASS] = "diag"
sys.argv = ["run.py", "--regions", "FR-HOS", "FR-GIR", "ES-PV", "GB-CON", "PT-CEN", "ES-CAN", "--sources", "mi", "cmems"]
run.main()
