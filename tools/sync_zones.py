"""Réécrit modules.COMBATZONE de mission.yaml depuis gen_07_entrainement.py et gen_08_zones.py.

Les générateurs sont la source des noms, menus, inclusions et briefings ; un changement de texte n'a donc qu'à être fait là,
puis ce script remet mission.yaml d'accord. (Les positions sont recalculées avec la grille d'altitude : elle doit être présente.)
"""
import gen_07_entrainement as e
import gen_08_zones as z
from lib import BLUE_SLOTS, M, position_text
from mcp import cat

zones = []
for name, c, r, fname, menu, inc, groups, text in e.zones():
    cz = {"type": "zone", "zone_name": name, "friendly_name": fname, "radio_group_name": menu, "training": True}
    if inc:
        cz["includes"] = [inc]
    cz["briefing"] = f"{text}\n{position_text(c)}"
    zones.append(cz)
for i, (zname, (title, center, r, side), beacons) in enumerate(e.TOUR, 1):
    zones.append({"type": "zone", "zone_name": zname, "friendly_name": f"T{i} Tourisme — {title}",
                  "radio_group_name": "Tourisme", "training": True, "completable": False,
                  "briefing": f"{e.tourism_text(title, center, beacons, BLUE_SLOTS)}\n{position_text(center)}"})
for name, c, r, fname, menu, text, *_ in z.zones():
    zones.append({"type": "zone", "zone_name": name, "friendly_name": fname, "radio_group_name": menu,
                  "training": False, "briefing": f"{text}\n{position_text(c)} {z.near_blue(c)}"})
print(cat.run_action("set_mission_module", {"mission_yaml_path": M + "/mission.yaml", "module_id": "COMBATZONE",
                                             "value": {"enabled": True, "combat_zones": zones}}))
print(len(zones), "zones")
