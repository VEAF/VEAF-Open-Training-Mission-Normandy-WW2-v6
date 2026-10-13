"""Lot 07 : les 3 familles d'entraînement × 3 niveaux (facile ⊂ moyen ⊂ difficile, clé `includes:`), et les trois zones
touristiques.

Adaptées à 1944 (ni hélicoptère, ni SEAD) :
A — appui rapproché (mitraillage et roquettes), bocage du Cotentin à 6 nm à l'ouest d'Azeville : cibles inertes, puis flak
    légère, puis défense courte portée réaliste (flak de 20 à 37 mm, alias `-samSR`).
B — bombardement de précision, plaine de Salisbury (Imber), à 111 nm du front : bâtiments et véhicules inertes, puis flak
    légère, puis flak lourde (88 mm, 3,7 pouces : alias `-samLR`).
C — antiflak, fort Tourgis à Aurigny (rouge) : une batterie moyenne, puis la flak lourde en plus, puis radars (Freya,
    Würzburg), projecteurs et télémètre en réseau.
T — tourisme : trois circuits hors combat (training, non complétable) ; la zone F10 fait seulement apparaître des véhicules
    d'époque et quelques soldats ; les balises radio et le guide sont permanents (gen_07b, gen_07c).
Toutes les distances des briefings sont calculées ici, pas tapées.

Cibles inertes des niveaux faciles : groupes d'un véhicule nommés « Inert-… », rendus chauds, tir interdit et sans
dispersion par tools/inert_targets.py (aucune action MCP ne règle ROE ni dispersion).
"""
import sites as S
from lib import (AIRFIELDS, BLUE_SLOTS, BLUE_UK, BLUE_US, RED, Batch, cmd_unit, dist_front_nm, nm, position_text, spot,
                 xy)

A, B, C = S.A, S.B, S.C
GER = ", country thirdreich"


def inert(zone_center, items, prefix):
    """Groupes d'un véhicule, en couronne autour du centre : (type, relèvement, distance)."""
    groups = []
    for i, (typ, brg, dist) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{prefix}{i}")
        groups.append({"name": f"Inert-{typ.split()[0]}-{prefix}{i}", "position": xy(p), "keep_position": True,
                       "units": [{"type": typ, "count": 1}]})
    return groups


def fake(zone_center, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    groups = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{tagbase}-{i}")
        groups.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                       "units": [cmd_unit(alias + GER, carrier, f"{tagbase}-{i}", extra)]})
    return groups


def native(center, name, brg, dist, units):
    p = spot(center, brg, dist, name)
    return {"name": name, "position": xy(p), "keep_position": True, "units": units}


def nearest(p, names):
    n = min(names, key=lambda k: nm(p, AIRFIELDS[k]))
    return n, nm(p, AIRFIELDS[n])


def zones():
    stoney = nm(B, AIRFIELDS["Stoney Cross"])
    return [
        # ── A : appui rapproché ──
        ("combatZone_Bocage_Easy", A, 2500, "A1 Mitraillage bocage — facile", "Entraînement appui rapproché", None,
         inert(A, [("Pz_IV_H", 0, 600), ("Stug_III", 40, 800), ("Sd_Kfz_251", 80, 500), ("Sd_Kfz_251", 120, 700),
                   ("Blitz_36-6700A", 160, 600), ("Blitz_36-6700A", 200, 800), ("Sd_Kfz_7", 240, 600),
                   ("Horch_901_typ_40_kfz_21", 280, 500), ("Kubelwagen_82", 320, 700)], "A1-"),
         f"Champ de tir d'appui rapproché dans le bocage du Cotentin, à {nm(A, AIRFIELDS['Azeville']):.0f} nm à l'ouest "
         f"d'Azeville : chars, blindés légers et camions immobiles en tir interdit, dépôts de carburant et casernement. "
         f"À {dist_front_nm(A):.0f} nm du front, arrière bleu."),
        ("combatZone_Bocage_Medium", A, 2500, "A2 Mitraillage bocage — moyen", "Entraînement appui rapproché",
         "combatZone_Bocage_Easy",
         fake(A, [("-aaa, defense 1", "flak38", 210, 1200, '#spawngroup="A2AAA" #spawncount=2'),
                  ("-aaa, defense 1", "flak38", 270, 1100, '#spawngroup="A2AAA" #spawncount=2'),
                  ("-aaa, defense 1", "flak38", 150, 1300, '#spawngroup="A2AAA" #spawncount=2'),
                  ("-armor, defense 0", "Sd_Kfz_251", 330, 1500, "")], "A2"),
         "Champ de tir du bocage : un groupe blindé léger actif et de la flak légère de 20 mm (deux positions tirées au "
         "sort sur trois) en plus des cibles du niveau facile."),
        ("combatZone_Bocage_Hard", A, 2500, "A3 Mitraillage bocage — difficile", "Entraînement appui rapproché",
         "combatZone_Bocage_Medium",
         fake(A, [("-samSR", "flak37", 200, 1000, '#spawngroup="A3SR" #spawncount=1'),
                  ("-samSR", "flak37", 250, 1000, '#spawngroup="A3SR" #spawncount=1'),
                  ("-aaa, defense 2", "flak38", 220, 1500, ""),
                  ("-armor, defense 1", "Pz_IV_H", 300, 1700, "")], "A3"),
         "Champ de tir du bocage avec une défense courte portée réaliste : une batterie de flak de 37 mm (tirée au sort "
         "entre deux positions), de la flak de 20 mm et un second groupe blindé."),
        # ── B : bombardement de précision ──
        ("combatZone_Salisbury_Easy", B, 2500, "B1 Bombardement Salisbury — facile", "Entraînement bombardement", None,
         inert(B, [("Pz_IV_H", 0, 700), ("Tiger_I", 40, 900), ("Stug_III", 80, 600), ("Sd_Kfz_251", 120, 800),
                   ("Blitz_36-6700A", 160, 500), ("Blitz_36-6700A", 200, 700), ("Sd_Kfz_7", 240, 900),
                   ("Sd_Kfz_251", 280, 600)], "B1-"),
         f"Champ de tir de bombardement de la plaine de Salisbury, à {stoney:.0f} nm de Stoney Cross : bâtiments et "
         f"véhicules fictifs immobiles en tir interdit (blockhaus, casernes, entrepôts, dépôt, gare). À "
         f"{dist_front_nm(B):.0f} nm du front : aucun contact possible."),
        ("combatZone_Salisbury_Medium", B, 2500, "B2 Bombardement Salisbury — moyen", "Entraînement bombardement",
         "combatZone_Salisbury_Easy",
         fake(B, [("-aaa, defense 1", "flak38", 210, 1300, '#spawngroup="B2AAA" #spawncount=2'),
                  ("-aaa, defense 1", "flak38", 270, 1200, '#spawngroup="B2AAA" #spawncount=2'),
                  ("-aaa, defense 2", "flak38", 150, 1400, '#spawngroup="B2AAA" #spawncount=2')], "B2"),
         "Champ de tir de Salisbury : de la flak légère de 20 mm, deux positions sur trois tirées au sort, en plus des "
         "cibles du niveau facile."),
        ("combatZone_Salisbury_Hard", B, 2500, "B3 Bombardement Salisbury — difficile", "Entraînement bombardement",
         "combatZone_Salisbury_Medium",
         fake(B, [("-samLR", "flak36", 240, 1500, '#spawngroup="B3HVY" #spawncount=1'),
                  ("-samLR", "flak36", 300, 1500, '#spawngroup="B3HVY" #spawncount=1'),
                  ("-samSR", "flak37", 200, 1000, "")], "B3"),
         "Champ de tir de Salisbury avec la flak lourde de l'époque : une batterie de pièces de 88 mm (tirée au sort entre "
         "deux positions) et une batterie de 37 mm en plus du niveau moyen."),
        # ── C : antiflak ──
        ("combatZone_Aurigny_Easy", C, 1500, "C1 Antiflak Aurigny — facile", "Entraînement antiflak", None,
         fake(C, [("-samSR", "flak37", 0, 300, '#spawngroup="C1SR" #spawncount=1'),
                  ("-samSR", "flak37", 120, 400, '#spawngroup="C1SR" #spawncount=1')], "C1"),
         f"Site antiflak du fort Tourgis, à Aurigny, à {nm(C, AIRFIELDS['Alderney']):.0f} nm de la piste d'Aurigny et "
         f"{nm(C, AIRFIELDS['Maupertus']):.0f} nm de Maupertus : une batterie de flak moyenne (37 mm), à détruire. "
         f"À {dist_front_nm(C):.0f} nm du front, en territoire rouge."),
        ("combatZone_Aurigny_Medium", C, 1500, "C2 Antiflak Aurigny — moyen", "Entraînement antiflak",
         "combatZone_Aurigny_Easy",
         fake(C, [("-samLR", "flak36", 240, 500, '#spawngroup="C2HVY" #spawncount=1'),
                  ("-samLR", "flak36", 300, 500, '#spawngroup="C2HVY" #spawncount=1')], "C2"),
         "Site antiflak d'Aurigny : la flak lourde de 88 mm (une batterie sur deux positions) en plus de la batterie de "
         "37 mm."),
        ("combatZone_Aurigny_Hard", C, 1500, "C3 Antiflak Aurigny — difficile", "Entraînement antiflak",
         "combatZone_Aurigny_Medium",
         [native(C, "Radars", 60, 600, [{"type": "FuMG-401", "count": 1}, {"type": "FuSe-65", "count": 1}]),
          native(C, "Projecteurs", 200, 700,
                 [{"type": "Flakscheinwerfer_37", "count": 2}, {"type": "KDO_Mod40", "count": 1}])],
         "Site antiflak d'Aurigny en réseau : un radar d'alerte Freya, un radar de conduite de tir Würzburg, un télémètre "
         "et deux projecteurs guident la flak lourde et moyenne."),
    ]


# Statiques des niveaux faciles : ce qui ne vit pas (dépôts, bâtiments)
A1_STATICS = [("Fuel tank", 100, 1100), ("Fuel tank", 110, 1200), ("Barracks 2", 20, 1300)]
B1_STATICS = [("Bunker", 20, 400), ("Bunker", 50, 450), ("Barracks 2", 90, 600), ("Barracks 2", 100, 700),
              ("Warehouse", 140, 600), ("Warehouse", 150, 700), ("Fuel tank", 200, 900), ("Fuel tank", 210, 950),
              ("Railway station", 300, 1000)]

TOUR = [
    # nom de zone, (titre, centre, rayon, camp), balises
    ("combatZone_TourPlages", ("Plages du Débarquement", S.T1_CENTER, 1500, BLUE_US), S.T1_BEACONS),
    ("combatZone_TourCotentin", ("Cotentin et Cherbourg", S.T2_CENTER, 1500, BLUE_US), S.T2_BEACONS),
    ("combatZone_TourAngleterre", ("Côte sud de l'Angleterre", S.T3_CENTER, 1500, BLUE_UK), S.T3_BEACONS),
]


def tourism_text(title, center, beacons, blue_names):
    base, d = nearest(center, blue_names)
    cs = ", ".join(f"{code} {mhz:.1f}" for code, mhz, _p, _s in beacons)
    return (f"Visite aérienne « {title} », hors combat, à {d:.0f} nm de {base}. Une balise radio VHF/AM à chaque site "
            f"({cs}) ; survolez un monument à moins de 1 500 ft sol et un guide vous le raconte.")


def tourism_groups(center, side, i):
    """Véhicules et soldats d'époque au point central, bleus, hors combat."""
    car = "Willys_MB" if side is BLUE_US else "Bedford_MWD"
    return [{"name": f"Visiteurs-{i}-vehicules", "position": xy(spot(center, 90, 400, "visiteurs")),
             "keep_position": True, "units": [{"type": car, "count": 3}]},
            {"name": f"Visiteurs-{i}-groupe", "position": xy(spot(center, 60, 500, "groupe")), "keep_position": True,
             "units": [{"type": "soldier_wwii_us" if side is BLUE_US else "soldier_wwii_br_01", "count": 6}]}]


if __name__ == "__main__":
    b = Batch()
    for zone, c, r, fname, menu, inc, groups, text in zones():
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": True,
              "briefing": f"{text}\n{position_text(c)}"}
        if inc:
            cz["includes"] = [inc]
        b.act("create_combat_zone", zone_name=zone, position=xy(c), radius=r, groups=groups, **RED,
              category="vehicle", combat_zone=cz)
    for zname, statics, center in [("combatZone_Bocage_Easy", A1_STATICS, A), ("combatZone_Salisbury_Easy", B1_STATICS, B)]:
        for i, (typ, brg, dist) in enumerate(statics, 1):
            p = spot(center, brg, dist, f"{zname}-static-{i}")
            b.act("add_group", **RED, category="static", name=f"Static-{typ.strip('.').split()[0]}-{zname[11]}{i}",
                  position=xy(p), units=[{"type": typ}], for_combat_zone=zname, keep_position=True)
    for i, (zname, (title, center, r, side), beacons) in enumerate(TOUR, 1):
        text = tourism_text(title, center, beacons, BLUE_SLOTS)
        b.act("create_combat_zone", zone_name=zname, position=xy(center), radius=r,
              groups=tourism_groups(center, side, i), **side, category="vehicle",
              combat_zone={"friendly_name": f"T{i} Tourisme — {title}", "radio_group_name": "Tourisme",
                           "training": True, "completable": False,
                           "briefing": f"{text}\n{position_text(center)}"})
    b.save("07-entrainement.json")
