"""Lot 17 : les trois convois recalés sur les routes (le lot 08 les avait posés sur des points approximatifs).

Retire les trois zones de convoi et leurs groupes du lot 08 (y compris leurs entrées de mission.yaml : aucune action MCP ne les
retire), puis les recrée avec les routes de gen_08_zones (tronçons du chemin par la route de DCS). Le troisième convoi change
de trajet : Vire n'a pas de chemin par la route vers le front dans DCS (land.findPathOnRoads rend rien), il devient
Coutances – La Haye-du-Puits. Ensuite, `python gen_17_convois.py post` met tous les points en « On Road » et la vitesse à
40 km/h (create_combat_zone écrit 20 km/h sans le dire, retour VMCT) en réécrivant la table de la mission.
"""
import sys
from pathlib import Path

from ruamel.yaml import YAML

import gen_08_zones as z
from lib import M, Batch, land, position_text, xy

OLD = ["combatZone_ConvoiFalaise", "combatZone_ConvoiLisieux", "combatZone_ConvoiCoutances"]   # 2e passage : sans DCA
SPEED_MS = 11.1   # 40 km/h


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


def post():
    import paths
    from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission
    mission = load_folder_mission(paths.ROOT)
    m = mission.mission_content
    for name, *_ in [x for x in z.zones() if x[0].startswith("combatZone_Convoi") and x[0] != "combatZone_ConvoiCotier"]:
        g = next(g for s in m["coalition"].values() for c in s.get("country") or []
                 for g in (c.get("vehicle") or {}).get("group") or [] if g["name"] == f"{name}-Convoi")
        for p in seq(g["route"]["points"]):
            p["action"], p["type"], p["speed"] = "On Road", "Turning Point", SPEED_MS
            p["speed_locked"] = True
        print(name, len(seq(g["route"]["points"])), "points On Road,", round(SPEED_MS * 3.6), "km/h")
    print(save_folder_mission(mission, paths.ROOT)["mission_file"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "post":
        post()
        sys.exit()
    yaml = YAML()
    yaml.width = 4096
    path = Path(M) / "mission.yaml"
    d = yaml.load(path.read_text(encoding="utf-8"))
    cz = d["modules"]["COMBATZONE"]["combat_zones"]
    before = len(cz)
    cz[:] = [e for e in cz if e.get("zone_name") not in OLD]
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(d, f)
    print("mission.yaml :", before - len(cz), "entrées de convoi retirées")

    b = Batch()
    for name in OLD:
        b.act("remove_group", group_name=f"{name}-Convoi")
        b.act("edit_zone", zone_name=name, remove=True)
    for name, c, r, fname, menu, text, side, cat, groups, statics, extra in z.zones():
        if not name.startswith("combatZone_Convoi") or name == "combatZone_ConvoiCotier":
            continue
        for g in groups:
            for q in g.get("route") or []:
                land((q["x"], q["y"]), f"{name} route", 50)
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": False,
              "briefing": f"{text}\n{position_text(c)} {z.near_blue(c)}"}
        b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **side,
              category=cat, combat_zone=cz)
    b.save("17b-convois.json")
