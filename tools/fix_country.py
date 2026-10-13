"""Remplace `country germany` par `country thirdreich` dans les noms d'unités porteurs (#command, #veafInterpreter).

`Germany` (id 6) n'est dans aucun camp de cette mission : le spawn y prend le camp neutre (side=0), n'a pas de réseau Skynet par
défaut et s'arrête sur `networkName nil` (sonde en jeu du 13/10/2026). Le camp rouge a `Third Reich` (id 66), que le Lua appelle
THIRDREICH (`country.id`). Idempotent.
"""
import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

mission = load_folder_mission(paths.ROOT)
n = 0
for side in mission.mission_content["coalition"].values():
    for c in (side.get("country") or {}).values() if isinstance(side.get("country"), dict) else side.get("country") or []:
        for cat in ("vehicle", "static", "plane", "ship"):
            grp = (c.get(cat) or {}).get("group") or {}
            for g in (grp.values() if isinstance(grp, dict) else grp):
                us = g["units"]
                for u in (us.values() if isinstance(us, dict) else us):
                    if "country germany" in u["name"]:
                        u["name"] = u["name"].replace("country germany", "country thirdreich")
                        n += 1
print(n, "noms d'unités corrigés")
print(save_folder_mission(mission, paths.ROOT)["mission_file"])
