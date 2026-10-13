"""Écrit src/waypoints.yaml : plans de vol des groupes joueurs, par catégorie et par camp jouable.

Le build ajoute lui-même le BULLSEYE (Saint-Lô) à chaque plan. Positions : champs d'entraînement et circuits touristiques de
tools/sites.py, arène de gen_10_joueurs.py. Plan bleu : les trois champs, les trois circuits et l'arène ; plan rouge : la
zone d'antiflak d'Aurigny (leur île), l'arène. Pas de plan hélicoptère : il n'y en a pas en 1944.
"""
import yaml

import sites as S
from gen_10_joueurs import ARENA
from lib import M

KT = 0.514444
WP = {
    "RNG_A": (S.A, 3000, 250), "RNG_B": (S.B, 8000, 220), "RNG_C": (S.C, 6000, 250),
    "TOUR_1": (S.T1_CENTER, 1500, 160), "TOUR_2": (S.T2_CENTER, 1500, 160), "TOUR_3": (S.T3_CENTER, 1500, 160),
    "ARENE": (ARENA[0], 15000, 250),
}
waypoints = {k: {"type": "Turning Point", "action": "Turning Point", "alt": round(ft * 0.3048), "alt_type": "BARO",
                 "speed": round(kt * KT, 1), "speed_type": "TAS", "x": round(p[0]), "y": round(p[1]), "name": k}
             for k, (p, ft, kt) in WP.items()}
settings = {
    "blue_planes": {"category": "plane", "coalition": "blue",
                    "waypoints": ["RNG_A", "RNG_B", "RNG_C", "TOUR_1", "TOUR_2", "TOUR_3", "ARENE"]},
    "red_planes": {"category": "plane", "coalition": "red", "waypoints": ["RNG_C", "ARENE"]},
}
HEADER = """# Plans de vol injectés dans les groupes joueurs (Open Training Normandie WW2) — écrit par tools/gen_13_waypoints.py.
# RNG_A/B/C = champs d'entraînement appui rapproché (Cotentin), bombardement (Salisbury) et antiflak (Aurigny) ;
# TOUR_1/2/3 = circuits touristiques (plages, Cotentin, côte sud de l'Angleterre) ; ARENE = arène de combat entre joueurs.
# Le build ajoute le BULLSEYE (Saint-Lô) à chaque plan.
"""
if __name__ == "__main__":
    with open(M + "/src/waypoints.yaml", "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump({"waypoints": waypoints, "settings": settings}, f, allow_unicode=True, sort_keys=False)
    print("waypoints.yaml :", len(waypoints), "points,", len(settings), "plans")
