"""Lot 06 : défense aérienne permanente des bases et des arrières (#veafInterpreter).

1944 : de la flak, pas de missile. Porteur = une pièce de la classe que génère l'alias (l'éditeur montre son cercle de portée),
nom unique. Portées DCS (list_unit_types, threat_range_m) : QF 3.7 pouces 9 000 m, M1 37 mm 5 700 m, flak 18/36/37/41 5 000 m,
flak 38 2 500 m, Bofors 2 000 m, quadruple M45 1 500 m. Aucune pièce moyenne ou lourde ne doit couvrir une base adverse avec
slots : aux bases avancées (Bény, Bazenville, Picauville, Carpiquet, Lessay) seulement `-samSR` et `-aaa`, posés du côté opposé
à la base adverse ; la flak lourde (`-samLR`, `-samVLR`) à l'arrière. Le contrôle des distances est check_portees.py.
Chaque emplacement est ramené sur la terre ferme (grille DCS).
Pas de radar d'alerte avancée côté bleu en alias (`-blue_ewr` est un FPS-117 moderne) : deux directeurs de tir (Allies_Director,
30 km) à la place ; côté rouge, des radars Freya (FuMG-401) et Würzburg (FuSe-65) en groupes natifs.
"""
from lib import AIRFIELDS, BLUE_UK, BLUE_US, PLACES, RED, Batch, interp_unit, land, ll, spot, xy

A = AIRFIELDS
# types de porteur : (SR, AAA, LR)
BLUE_T = {"sr": "M1_37mm", "aaa": "M45_Quadmount", "lr": "QF_37_AA"}
RED_T = {"sr": "flak37", "aaa": "flak38", "lr": "flak36"}

# (camp, nom de groupe, centre, relèvement, distance (m), alias, genre de porteur, cap)
SITES = [
    # ── Bleu, Angleterre : base mère et arrière ──
    (BLUE_UK, "AD Tangmere LR", A["Tangmere"], 20, 4000, "-samLR", "lr", 0),
    (BLUE_UK, "AD Tangmere SR", A["Tangmere"], 200, 2500, "-samSR", "sr", 0),
    (BLUE_UK, "AD Tangmere AAA", A["Tangmere"], 110, 1800, "-aaa", "aaa", 0),
    (BLUE_US, "AD Stoney Cross LR", A["Stoney Cross"], 330, 4000, "-samLR", "lr", 0),
    (BLUE_US, "AD Stoney Cross AAA", A["Stoney Cross"], 150, 1800, "-aaa", "aaa", 0),
    (BLUE_UK, "AD Biggin Hill LR", A["Biggin Hill"], 0, 4000, "-samLR", "lr", 0),
    (BLUE_UK, "AD Biggin Hill AAA", A["Biggin Hill"], 180, 1800, "-aaa", "aaa", 0),
    (BLUE_UK, "AD Manston LR", A["Manston"], 270, 4000, "-samLR", "lr", 0),
    (BLUE_UK, "AD Manston AAA", A["Manston"], 90, 1800, "-aaa", "aaa", 0),
    # ── Bleu, Cotentin et tête de pont : milieu ──
    (BLUE_US, "AD Maupertus LR", A["Maupertus"], 0, 4000, "-samLR", "lr", 0),
    (BLUE_US, "AD Maupertus AAA", A["Maupertus"], 180, 1800, "-aaa", "aaa", 0),
    (BLUE_US, "AD Azeville LR", A["Azeville"], 60, 4000, "-samLR", "lr", 0),
    (BLUE_US, "AD Azeville AAA", A["Azeville"], 250, 1800, "-aaa", "aaa", 0),
    (BLUE_US, "AD Deux Jumeaux SR", A["Deux Jumeaux"], 330, 3500, "-samSR", "sr", 0),
    (BLUE_US, "AD Deux Jumeaux AAA", A["Deux Jumeaux"], 150, 1800, "-aaa", "aaa", 0),
    (BLUE_US, "AD Longues LR", A["Longues-sur-Mer"], 0, 4000, "-samLR", "lr", 0),
    (BLUE_US, "AD Longues AAA", A["Longues-sur-Mer"], 270, 1800, "-aaa", "aaa", 0),
    # ── Bleu, bases avancées : courte portée seulement, côté opposé à l'ennemi ──
    (BLUE_US, "AD Picauville SR", A["Picauville"], 0, 3000, "-samSR", "sr", 0),
    (BLUE_US, "AD Picauville AAA", A["Picauville"], 60, 1800, "-aaa", "aaa", 0),
    (BLUE_UK, "AD Bazenville SR", A["Bazenville"], 0, 3000, "-samSR", "sr", 0),
    (BLUE_UK, "AD Bazenville AAA", A["Bazenville"], 300, 1800, "-aaa", "aaa", 0),
    (BLUE_US, "AD Beny SR", A["Beny-sur-Mer"], 0, 3000, "-samSR", "sr", 0),
    (BLUE_US, "AD Beny AAA", A["Beny-sur-Mer"], 60, 1800, "-aaa", "aaa", 0),
    # ── Bleu : points sensibles (flak lourde de zone) ──
    (BLUE_UK, "AD Portsmouth VLR", ll(50.80, -1.10), 0, 3000, "-samVLR", "lr", 0),
    (BLUE_US, "AD Mulberry Arromanches VLR", PLACES["Arromanches-les-Bains"], 0, 1500, "-samVLR", "lr", 0),
    (BLUE_US, "AD Cherbourg VLR", PLACES["Cherbourg-en-Cotentin"], 0, 2000, "-samVLR", "lr", 0),
    # ── Rouge : bases avancées (courte portée seulement) ──
    (RED, "AD Carpiquet SR", A["Carpiquet"], 150, 3000, "-samSR", "sr", 0),
    (RED, "AD Carpiquet AAA", A["Carpiquet"], 90, 1800, "-aaa", "aaa", 0),
    (RED, "AD Lessay SR", A["Lessay"], 180, 3000, "-samSR", "sr", 0),
    (RED, "AD Lessay AAA", A["Lessay"], 90, 1800, "-aaa", "aaa", 0),
    # ── Rouge : profondeur ──
    (RED, "AD Evreux LR", A["Evreux"], 90, 4000, "-samLR", "lr", 0),
    (RED, "AD Evreux SR", A["Evreux"], 270, 2500, "-samSR", "sr", 0),
    (RED, "AD Evreux AAA", A["Evreux"], 180, 1800, "-aaa", "aaa", 0),
    (RED, "AD Abbeville LR", A["Abbeville Drucat"], 90, 4000, "-samLR", "lr", 0),
    (RED, "AD Abbeville SR", A["Abbeville Drucat"], 270, 2500, "-samSR", "sr", 0),
    (RED, "AD Abbeville AAA", A["Abbeville Drucat"], 0, 1800, "-aaa", "aaa", 0),
    (RED, "AD Le Havre VLR", PLACES["Le Havre"], 0, 3000, "-samVLR", "lr", 0),
    (RED, "AD Rouen VLR", PLACES["Rouen"], 0, 3000, "-samVLR", "lr", 0),
    (RED, "AD Triqueville LR", A["Triqueville"], 0, 3500, "-samLR", "lr", 0),
    (RED, "AD Saint-Omer LR", A["Saint-Omer Wizernes"], 0, 3500, "-samLR", "lr", 0),
]

# Radars (groupes natifs, un par site) : (camp, nom, lieu, relèvement, distance, [(type, nombre)])
RADARS = [
    (RED, "EWR Honfleur", PLACES["Honfleur"], 0, 3000, [("FuMG-401", 1), ("FuSe-65", 1)]),
    (RED, "EWR Vimoutiers", PLACES["Vimoutiers"], 0, 3000, [("FuMG-401", 1)]),
    (RED, "EWR Argentan", PLACES["Argentan"], 270, 4000, [("FuMG-401", 1), ("FuSe-65", 1)]),
    (RED, "EWR Dieppe", PLACES["Dieppe"], 0, 3000, [("FuMG-401", 1), ("FuSe-65", 1)]),
    (BLUE_UK, "Director Tangmere", A["Tangmere"], 45, 5000, [("Allies_Director", 1)]),
    (BLUE_US, "Director Bayeux", PLACES["Bayeux"], 0, 3000, [("Allies_Director", 1)]),
]

if __name__ == "__main__":
    b = Batch()
    for side, name, c, brg, dist, alias, kind, hdg in SITES:
        carrier = (RED_T if side is RED else BLUE_T)[kind]
        p = spot(c, brg, dist, name, margin=300)
        land(p, name, margin=300)
        tag = name.replace("AD ", "").replace(" ", "-")
        country = ", country thirdreich" if side is RED else ", country usa"
        cmd = f"{alias}, hdg {hdg}{country}"
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p), keep_position=True,
              units=[interp_unit(cmd, carrier, tag)])
        print(f"{name:30} {round(p[0]):>8} {round(p[1]):>8}")
    for side, name, c, brg, dist, units in RADARS:
        p = spot(c, brg, dist, name, margin=300)
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p), keep_position=True,
              units=[{"type": t, "count": n} for t, n in units])
    b.save("06-defense.json")
