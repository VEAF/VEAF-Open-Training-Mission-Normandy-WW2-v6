"""Portée de chaque défense permanente et de chaque zone face à ce qu'elle ne doit pas atteindre → docs/portees.md ; ligne VERDICT.

Portées DCS (list_unit_types, threat_range_m) : QF 3.7 pouces 9 000 m, M1 37 mm 5 700 m, flak 18/36/37/41 5 000 m, flak 38 2 500 m,
Bofors 2 000 m, quadruple M45 1 500 m. Une défense d'alias est mesurée à la portée de sa pièce la plus longue (alias `-samLR` et
`-samVLR` : QF 3.7 pouces côté bleu, flak 88 mm côté rouge ; `-samSR` : M1 37 mm / flak 37 ; `-aaa` : M45 / flak 38).
Règles (prompt VMCT §4.5, 4.6, 4.7) :
  1. aucune défense permanente (alias `#veafInterpreter`) ne couvre une base adverse avec slots ;
  2. aucune zone de combat réelle ne couvre une base amie avec slots, ni un champ d'entraînement ;
  3. une zone (active ou non) est mesurée avec la portée de sa pièce la plus longue (flak 88 mm rouge : 5 000 m).
"""
import sys

import gen_07_entrainement as e
import gen_08_zones as z
from lib import AIRFIELDS, BLUE_SLOTS, RED_SLOTS, ROOT, km, nm, xy  # noqa: F401
from gen_06_defense import SITES

sys.stdout.reconfigure(encoding="utf-8")
RANGE = {("blue", "-samLR"): 9000, ("blue", "-samVLR"): 9000, ("blue", "-samSR"): 5700, ("blue", "-aaa"): 1500,
         ("red", "-samLR"): 5000, ("red", "-samVLR"): 5000, ("red", "-samSR"): 5000, ("red", "-aaa"): 2500}
RED_ZONE_RANGE = 5000


def main():
    lines = ["# Portées des défenses", "", "Écrit par `tools/check_portees.py` ; distances en mètres, calculées sur les x/y de la mission.", "",
             "## Défenses permanentes face aux bases adverses avec slots", "",
             "| Défense | Camp | Portée | Base adverse la plus proche | Distance | Marge |", "|---|---|---|---|---|---|"]
    bad = 0
    for side, name, c, brg, dist, alias, kind, hdg in SITES:
        camp = side["coalition"]
        # position réelle posée dans la mission : centre + relèvement/distance (le placement a pu être décalé de quelques dizaines de mètres)
        from lib import off
        p = off(c, brg, dist)
        rng = RANGE[(camp, alias)]
        others = RED_SLOTS if camp == "blue" else BLUE_SLOTS
        n = min(others, key=lambda k: km(p, AIRFIELDS[k]))
        d = km(p, AIRFIELDS[n]) * 1000
        marge = d - rng
        bad += marge < 0
        lines.append(f"| {name} | {camp} | {rng} | {n} | {d:.0f} | {marge:+.0f} {'**ÉCHEC**' if marge < 0 else ''} |")
    lines += ["", "## Zones de combat réelles face aux bases bleues avec slots et aux champs d'entraînement", "",
              "| Zone | Plus proche | Distance | Marge |", "|---|---|---|---|"]
    train = {"A": e.A, "B": e.B, "C": e.C}
    for name, c, r, fname, menu, text, side, cat, groups, statics, extra in z.zones():
        targets = {f"base {k}": AIRFIELDS[k] for k in BLUE_SLOTS} | {f"champ {k}": v for k, v in train.items()}
        n, t = min(targets.items(), key=lambda kv: km(c, kv[1]))
        d = km(c, t) * 1000
        marge = d - r - RED_ZONE_RANGE
        bad += marge < 0
        lines.append(f"| {fname} | {n} | {d:.0f} | {marge:+.0f} {'**ÉCHEC**' if marge < 0 else ''} |")
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "portees.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"VERDICT: {'OK' if not bad else 'ÉCHEC'} ({bad} manquement(s))")


main()
