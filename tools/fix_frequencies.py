"""Donne à chaque groupe d'avions une fréquence de groupe que sa radio sait accorder.

`add_air_group` écrit 251.0 MHz (modulation AM) sur tous les groupes : l'éditeur de DCS refuse d'enregistrer une mission dont un
groupe de joueurs a une fréquence hors de la plage de sa radio (« Invalid frequency 251 MHz », P-51D, Fw 190). Les radios de
1944 couvrent 38-156 MHz (P-51D 100-156, Fw 190 38.4-42.4). On prend la fréquence par défaut de l'appareil
(presets_injector/data/dcs-radio-specs.yaml, `human_radio.default_mhz`), puis une valeur dans la plage si le défaut n'en est pas.
Idempotent. Usage : python fix_frequencies.py [chemin du dossier ou .miz]  (par défaut le dossier de la mission)
"""
import sys

import yaml

import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
SPECS = yaml.safe_load((paths.VMCT_PY / "presets_injector" / "data" / "dcs-radio-specs.yaml").read_text(encoding="utf-8"))


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


def freq_for(unit_type):
    hr = (SPECS.get(unit_type) or {}).get("human_radio")
    if not hr:
        return None
    f = hr["default_mhz"]
    return f if hr["min_mhz"] <= f <= hr["max_mhz"] else round((hr["min_mhz"] + hr["max_mhz"]) / 2, 1)


def main():
    mission = load_folder_mission(paths.ROOT)
    m = mission.mission_content
    done = skipped = 0
    for side in m["coalition"].values():
        for country in seq(side.get("country")):
            for g in seq((country.get("plane") or {}).get("group")):
                f = freq_for(seq(g["units"])[0]["type"])
                if f is None:
                    skipped += 1
                    continue
                if g.get("frequency") != f:
                    g["frequency"], g["modulation"] = f, 0
                    done += 1
    print(done, "groupes corrigés,", skipped, "sans plage connue")
    print(save_folder_mission(mission, paths.ROOT)["mission_file"])


if __name__ == "__main__":
    main()
