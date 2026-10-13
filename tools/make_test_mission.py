"""Construit la mission de test locale : profil LOCAL_TEST + game master + un P-51D en slot classique + dcs-bridge.

Les slots dynamiques ne fonctionnent qu'en multijoueur : un test en solo a besoin d'un slot `Client` classique.
Ces ajouts vont dans la COPIE DE TEST seulement, jamais dans les sources : le build serveur ne doit pas les gagner.

Usage (depuis le dossier de la mission, environnement poetry de VMCT) :
    poetry -C ../VEAF-Mission-Creation-Tools run python "$PWD/tools/make_test_mission.py"
Sortie : bridge/bridge-Normandy-OT.miz.
"""

import glob
import os
import shutil
import subprocess
import sys

from paths import ROOT
from mission_tools.miz_tools import read_miz, write_miz
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
BRIDGE_LUA = os.environ.get("BRIDGE_LUA", str(ROOT.parent / "VEAF-dcs-bridge" / "src" / "lua" / "dcs-bridge.lua"))
OUT = ROOT / "bridge" / "bridge-Normandy-OT.miz"
EXE = str(ROOT / "veaf-tools.exe")

# le build LOCAL_TEST réécrit src/scripts/veaf-config.lua (sécurité coupée, logs debug) : on garde la copie des
# sources et on la remet, pour qu'un commit après un test n'embarque jamais la configuration de test
CONFIG = ROOT / "src" / "scripts" / "veaf-config.lua"
config_before = CONFIG.read_bytes()
try:
    subprocess.run([EXE, "mission", "build", "--profile", "LOCAL_TEST"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
finally:
    CONFIG.write_bytes(config_before)
built = max(glob.glob(str(ROOT / "VEAF_OpenTraining_Normandy_ICAO_LFRK_2*.miz")), key=os.path.getmtime)
OUT.parent.mkdir(exist_ok=True)
shutil.copy(built, OUT)

# un game master par camp
miz = read_miz(OUT)
miz.mission_content["groundControl"]["roles"]["instructor"] = {"blue": 1, "red": 1, "neutrals": 0}
write_miz(miz, OUT)

# P-51D à Tangmere (base mère), au parking moteur chaud (parkings Normandy capturés le 13/10/2026) ; en vol sinon
catalog = ActionCatalog()
register_default_actions(catalog)
slot = dict(mission_path=str(OUT), coalition="blue", country_id=2, country_name="USA", name="TEST P-51D Tangmere",
            unit_type="P-51D", count=1, skill="Client", task="CAS")
try:
    print(catalog.run_action("add_air_group", dict(slot, start="parking-hot", airfield="Tangmere")))
except Exception as e:  # noqa: BLE001
    print("parking refusé, départ en vol :", e)
    print(catalog.run_action("add_air_group", dict(slot, start="air", position={"x": 150376, "y": -33743},
                                                   altitude_ft=5000, speed_kt=250)))

# fréquence de groupe que la radio du P-51D sait accorder (add_air_group écrit 251 MHz : l'éditeur refuse d'enregistrer)
miz = read_miz(OUT)
for coalition in miz.mission_content["coalition"].values():
    for country in (coalition.get("country") or {}).values() if isinstance(coalition.get("country"), dict) else coalition.get("country") or []:
        for grp in (country.get("plane") or {}).get("group", {}).values() if isinstance((country.get("plane") or {}).get("group"), dict) else (country.get("plane") or {}).get("group") or []:
            if grp["name"] == "TEST P-51D Tangmere":
                grp["frequency"], grp["modulation"] = 124.0, 0
write_miz(miz, OUT)

subprocess.run([EXE, "dcs", "inject-bridge", "--bridge-lua", BRIDGE_LUA, str(OUT)], cwd=ROOT, check=True)

# le build LOCAL_TEST a remplacé le .miz serveur du jour : le reconstruire, pour que la mission livrée reste celle du serveur
with open(ROOT / ".veaf-backups" / "build-serveur.log", "w", encoding="utf-8") as log:
    subprocess.run([EXE, "mission", "build"], cwd=ROOT, check=True, stdout=log, stderr=subprocess.STDOUT)
print("OK", OUT)
