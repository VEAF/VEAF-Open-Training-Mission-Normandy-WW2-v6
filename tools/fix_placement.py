"""Déplace sur du terrain dégagé les groupes que la sonde DCS juge dans l'eau ou dans le décor.

Pour chaque groupe de véhicules (hors porteurs `#veafInterpreter` / `#command`, que VEAF replace lui-même au lancement) ou
statique dont une unité est « blocked » ou « water », cherche par anneaux croissants (100 m à 1 500 m) le point le plus proche
que DCS donne « terre » et « place libre », et le groupe entier y est décalé (set_group_properties). Statiques jugés sur
l'eau seulement : un bâtiment bloque son propre test (limitation disposition-getsimplezones-is-a-lottery).
Usage : python fix_placement.py [--apply]   (sans --apply : liste ce qu'il déplacerait)
Nécessite la mission d'arpentage lancée dans DCS et dcs-serve connecté (tools/dcs.py).
"""
import math
import sys
from collections import defaultdict

import probe_scenery as ps
from mcp import cat
from lib import M, xy
from probe_points import probe

sys.stdout.reconfigure(encoding="utf-8")


def carrier_groups():
    """Groupes dont une unité porte #command ou #veafInterpreter : VEAF les remplace au lancement (settleGroup)."""
    from paths import ROOT
    from veaf_mission_mcp.mission_folder import load_folder_mission
    m = load_folder_mission(ROOT).mission_content
    out = set()
    for co in m["coalition"].values():
        for c in ps.seq(co.get("country")):
            for g in ps.seq((c.get("vehicle") or {}).get("group")):
                if any("#command" in u["name"] or "#veafInterpreter" in u["name"] for u in ps.seq(g["units"])):
                    out.add(g["name"])
    return out


def judge():
    vehicles, statics = ps.collect()
    skip = carrier_groups()
    out = {}
    for code in ps.chunks(vehicles):
        out.update(kv.split("=") for kv in ps.exec_lua(code).split(";"))
    bad = defaultdict(list)
    for n, g, x, z in vehicles:
        if out.get(str(n)) in ("blocked", "water") and g not in skip:
            bad[g].append((out[str(n)], x, z))
    water = []
    for code in ps.chunks(statics):
        for kv in ps.exec_lua(code).split(";"):
            n, v = kv.split("=")
            if v in ("water", "shallow"):
                s = statics[int(n) - 1]
                water.append((s[1], s[2], s[3]))
    return bad, water


def find_clear(x, y, extra=()):
    """Point le plus proche (anneaux) où DCS dit terre + place libre ; les `extra` sont d'autres points du groupe à garder
    sur la terre libre avec le même décalage."""
    for r in range(100, 1600, 100):
        cands = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(0, 360, 30)]
        pts = [(cx + ex, cy + ey) for cx, cy in cands for ex, ey in [(0, 0), *extra]]
        res = probe(pts)
        k = len(extra) + 1
        for i, (cx, cy) in enumerate(cands):
            if all(v.startswith(("land:clear", "road:clear")) for v in res[i * k:(i + 1) * k]):
                return round(cx), round(cy)
    return None


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    bad, water = judge()
    todo = {g: (sorted({v for v, *_ in us}), us[0][1:], [(u[1] - us[0][1], u[2] - us[0][2]) for u in us[1:]]) for g, us in bad.items()}
    for g, x, z in water:
        todo.setdefault(g, (["water"], (x, z), []))
    for g, (why, (x, z), extra) in sorted(todo.items()):
        q = find_clear(x, z, extra)
        print(f"{g:55} {','.join(why):14} ({x},{z}) -> {q}")
        if apply and q:
            r = cat.run_action("set_group_properties", {"mission_path": M, "group_name": g, "move_to": xy(q)})
            print("   ", {k: v for k, v in r.items() if k in ("moved", "warnings", "durable")})
