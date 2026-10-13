"""Lot 08 : les vraies zones de combat, dans la France occupée (training: false).

16 zones : front 3, flak et radars 2 (l'équivalent 1944 du SEAD), convois en mouvement 3, frappes dans la profondeur 4, OCA 2,
antinavire 2. Lieux réels (tools/places.json, geocode, ou coordonnées géographiques) ; chaque position est ramenée sur la
terre ferme (grille DCS) ; les navires sont contrôlés en pleine mer. Aucune zone n'est active au démarrage : check_portees.py
mesure la portée de chaque défense contre les bases amies.
Défense par les alias de VEAF d'époque (flak 20-88 mm, `-aaa`, `-samSR`, `-samLR`), blindés `-armor` (Pz IV, Tiger, Stug...),
groupes natifs pour l'artillerie, les convois et les navires.
Les routes des convois sont des tronçons du chemin par la route que DCS calcule (tools/roads.py) ; le lot 17 les a posées
(les convois du lot 08 étaient des points approximatifs entre deux villes), tous les points en « On Road ».
"""
import roads
from lib import (AIRFIELDS, BLUE_SLOTS, PLACES, RED, Batch, cmd_unit, land, ll, nm, off, position_text, sea, spot, xy)

A = AIRFIELDS
P = PLACES
GER = ", country thirdreich"


def g_fake(c, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    out = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(c, brg, dist, f"{tagbase}-{i}")
        out.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                    "units": [cmd_unit(alias + GER, carrier, f"{tagbase}-{i}", extra)]})
    return out


def g_native(c, name, brg, dist, units, route=None, patrol=False):
    p = spot(c, brg, dist, name)
    g = {"name": name, "position": xy(p), "keep_position": True, "units": units}
    if route:
        g["route"] = [xy(p)] + [xy(q) for q in route]
    if patrol:
        g["patrol"] = True
    return g


def s_items(c, items):
    """Statiques : (type, relèvement, distance)."""
    return [(typ, spot(c, brg, dist, typ)) for typ, brg, dist in items]


def near_blue(p):
    n = min(BLUE_SLOTS, key=lambda k: nm(p, A[k]))
    return f"Base amie la plus proche : {n}, à {nm(p, A[n]):.0f} nm."


def zones():
    Z = []

    def zone(name, c, r, fname, menu, text, groups, statics=(), side=RED, cat="vehicle", extra=()):
        Z.append((name, c, r, fname, menu, text, side, cat, groups, list(statics), list(extra)))

    # ── Front ────────────────────────────────────────────────────────────────
    C = spot(ll(49.0817, -0.6558), 0, 0, "Villers-Bocage")
    zone("combatZone_VillersBocage", C, 2500, "Z01 Front — Villers-Bocage", "Front",
         "Des chars allemands tiennent les hauteurs de Villers-Bocage, face à la poussée britannique : Panzer IV, Tiger et "
         "canons antichars en position, appuyés par de l'artillerie (composition illustrative). Détruire les blindés et les "
         "canons ; flak légère et moyenne pour la couverture.",
         g_fake(C, [("-armor, defense 2", "Pz_IV_H", 0, 800, ""), ("-armor, defense 1", "Pz_IV_H", 120, 900, ""),
                    ("-samSR", "flak37", 240, 700, ""), ("-aaa, defense 1", "flak38", 300, 1200, "")], "Z01")
         + [g_native(C, "Artillerie", 90, 1300, [{"type": "LeFH_18-40-105", "count": 4}]),
            g_native(C, "Antichars", 200, 900, [{"type": "Pak40", "count": 3}])],
         s_items(C, [("Bunker", 330, 1500), ("Bunker", 340, 1600)]))

    C = spot(ll(49.1850, -0.4100), 0, 0, "Caen nord")
    zone("combatZone_CaenNord", C, 2500, "Z02 Front — Caen et Carpiquet", "Front",
         "La ligne de défense de la 12e SS Hitlerjugend au nord de Caen, autour de Carpiquet : Panzer IV, Tiger et "
         "automoteurs d'artillerie dans les ruines. Détruire les blindés et l'artillerie ; flak moyenne de 37 mm, sous la "
         "QRA de Caen.",
         g_fake(C, [("-armor, defense 2", "Pz_IV_H", 30, 800, ""), ("-armor, defense 1", "Pz_IV_H", 150, 900, ""),
                    ("-samSR", "flak37", 270, 700, "")], "Z02")
         + [g_native(C, "Tigers", 330, 600, [{"type": "Tiger_I", "count": 2}]),
            g_native(C, "Artillerie", 210, 1200, [{"type": "Wespe124", "count": 3}])],
         s_items(C, [("Bunker", 0, 1300), ("Bunker", 20, 1400)]))

    C = spot(ll(49.2100, -1.5000), 0, 0, "Cotentin sud")
    zone("combatZone_CotentinSud", C, 2500, "Z03 Front — La Haye-du-Puits et Lessay", "Front",
         "La ligne de défense allemande qui bloque le Cotentin, des marais de Lessay à La Haye-du-Puits : canons "
         "antichars, blindés légers et artillerie dans le bocage. Détruire les blindés et les canons ; flak moyenne. Aucune "
         "QRA ne couvre le Cotentin sud.",
         g_fake(C, [("-armor, defense 1", "Sd_Kfz_251", 330, 800, ""), ("-armor, defense 2", "Pz_IV_H", 90, 900, ""),
                    ("-samSR", "flak37", 200, 600, "")], "Z03")
         + [g_native(C, "Antichars", 210, 1200, [{"type": "Pak40", "count": 4}]),
            g_native(C, "Artillerie", 120, 1400, [{"type": "LeFH_18-40-105", "count": 3}])],
         s_items(C, [("Bunker", 0, 400), ("Bunker", 120, 450), ("Bunker", 240, 420)]))

    # ── Flak et radars (l'équivalent 1944 du SEAD) ──────────────────────────
    C = spot(P["Cap d'Antifer"], 0, 0, "Antifer")
    zone("combatZone_Antifer", C, 2000, "Z04 Radars — station du cap d'Antifer", "Flak et radars",
         "La station radar du cap d'Antifer, sur la côte au nord du Havre : radar d'alerte avancée Freya et radars de "
         "conduite de tir Würzburg, protégés par de la flak lourde. Détruire les radars et réduire la flak.",
         g_fake(C, [("-samLR", "flak36", 180, 700, ""), ("-aaa, defense 2", "flak38", 90, 500, "")], "Z04")
         + [g_native(C, "Radars", 0, 0, [{"type": "FuMG-401", "count": 2}, {"type": "FuSe-65", "count": 2}])],
         s_items(C, [("Freya_Shelter_Brick", 300, 300), ("Freya_Shelter_Brick", 320, 350), ("Bunker", 40, 400)]))

    C = spot(ll(50.8700, 1.5800), 0, 800, "Gris-Nez")
    zone("combatZone_GrisNez", C, 2000, "Z05 Radars — cap Gris-Nez", "Flak et radars",
         "Le cap Gris-Nez, au plus près des côtes anglaises : radars Freya et Würzburg, flak lourde et batterie côtière. "
         "Détruire les radars et réduire la flak ; la batterie côtière est une menace pour les navires, pas pour les "
         "avions.",
         g_fake(C, [("-samLR", "flak36", 180, 700, ""), ("-samSR", "flak37", 90, 600, "")], "Z05")
         + [g_native(C, "Radars", 0, 0, [{"type": "FuMG-401", "count": 1}, {"type": "FuSe-65", "count": 2}])],
         s_items(C, [("SK_C_28_naval_gun", 270, 500), ("SK_C_28_naval_gun", 280, 560), ("Bunker", 320, 400)]))

    # ── Convois en mouvement (un groupe natif, route sur route) ──
    # Route = tronçon du chemin par la route que donne DCS (land.findPathOnRoads, relevé une fois par roads.py, gardé dans
    # tools/road_routes.json) ; tous les points, départ compris, sont sur la route.
    def convoy(name, fname, text, key, a, b, km0, km1, units):
        pts = roads.convoy_route(key, a, b, km0, km1)
        c = pts[0]
        zone(name, c, 1500, fname, "Convois", text, [g_native(c, "Convoi", 0, 0, units, route=pts[1:])])

    # Pas de DCA dans un convoi : toutes les pièces antiaériennes de 1944 ont une vitesse maximale de 0 dans DCS (mesuré en jeu le
    # 13/10/2026 : flak 18/30/36/37/38/41, Bofors, QF 3.7, M1 37 mm, M45) et freinent tout le groupe (5 m/s au lieu de 11) ;
    # l'escorte est faite de blindés légers (Sd.Kfz 251, Puma).
    convoy("combatZone_ConvoiFalaise", "Z06 Convoi — Falaise vers Caen",
           "Des renforts blindés quittent Falaise par la route de Caen. L'arrêter avant Caen ; deux Sd.Kfz 251 et un Puma "
           "l'escortent.",
           "falaise_caen", P["Falaise, Calvados"], ll(49.18, -0.36), 2, 31,
           [{"type": "Pz_IV_H", "count": 2}, {"type": "Sd_Kfz_251", "count": 2}, {"type": "Blitz_36-6700A", "count": 4},
            {"type": "Sd_Kfz_234_2_Puma", "count": 1}])
    convoy("combatZone_ConvoiLisieux", "Z07 Convoi — Lisieux vers Caen",
           "Un convoi de ravitaillement roule de Lisieux vers Caen, par la route de Mézidon. Le détruire avant le "
           "front ; camions, tracteurs et un Sd.Kfz 251 d'escorte.",
           "lisieux_caen", P["Lisieux"], ll(49.18, -0.36), 2, 43,
           [{"type": "Blitz_36-6700A", "count": 6}, {"type": "Sd_Kfz_7", "count": 2}, {"type": "Sd_Kfz_251", "count": 1}])
    convoy("combatZone_ConvoiCoutances", "Z08 Convoi — Coutances vers La Haye-du-Puits",
           "Des renforts quittent Coutances vers La Haye-du-Puits, le long du front du Cotentin. Les arrêter avant le front ; "
           "deux Sd.Kfz 251 et un Puma les escortent.",
           "coutances_hayedupuits", P["Coutances"], P["La Haye-du-Puits"], 2, 34,
           [{"type": "Sd_Kfz_251", "count": 2}, {"type": "Blitz_36-6700A", "count": 4}, {"type": "Kubelwagen_82", "count": 1},
            {"type": "Sd_Kfz_234_2_Puma", "count": 1}])

    # ── Frappes dans la profondeur ───────────────────────────────────────────
    C = spot(ll(49.0856, 1.6275), 0, 0, "La Roche-Guyon")
    zone("combatZone_RocheGuyon", C, 1200, "Z09 Frappe — état-major de La Roche-Guyon", "Frappes en profondeur",
         "Le quartier général du groupe d'armées B, dans le château de La Roche-Guyon, au bord de la Seine : bunkers, "
         "centre de transmissions, véhicules de commandement. Tout détruire ; flak moyenne et lourde. Hors des cercles de "
         "QRA.",
         g_fake(C, [("-samLR", "flak36", 200, 700, ""), ("-samSR", "flak37", 60, 500, "")], "Z09")
         + [g_native(C, "PC mobile", 300, 300,
                     [{"type": "Horch_901_typ_40_kfz_21", "count": 3}, {"type": "Kubelwagen_82", "count": 2}])],
         s_items(C, [(".Command Center", 0, 0), ("Bunker", 90, 200), ("Bunker", 180, 200), ("Bunker", 270, 200),
                     ("Military staff", 135, 250), ("Barracks 2", 45, 300)]))

    C = spot(ll(48.7455, -0.0150), 0, 0, "Argentan triage")
    zone("combatZone_TriageArgentan", C, 1500, "Z10 Frappe — gare de triage d'Argentan", "Frappes en profondeur",
         "La gare de triage d'Argentan, nœud ferroviaire qui alimente le front de Normandie : gare, entrepôts, "
         "réservoirs de carburant. Tout détruire ; flak moyenne.",
         g_fake(C, [("-samSR", "flak37", 200, 600, ""), ("-aaa, defense 2", "flak38", 20, 500, "")], "Z10"),
         s_items(C, [("Railway station", 0, 0), ("Warehouse", 40, 200), ("Warehouse", 60, 250), ("Warehouse", 90, 300),
                     ("Fuel tank", 200, 350), ("Fuel tank", 210, 400), ("Fuel tank", 220, 450)]))

    C = spot(ll(50.8083, 2.0997), 0, 0, "Eperlecques")
    zone("combatZone_Eperlecques", C, 1500, "Z11 Frappe — blockhaus d'Éperlecques", "Frappes en profondeur",
         "Le blockhaus d'Éperlecques, près de Saint-Omer : un énorme bunker de béton destiné au lancement des fusées V2, "
         "bâti en 1943 et déjà bombardé. Détruire le blockhaus et ses annexes ; flak lourde et moyenne, sous la QRA du "
         "Pas-de-Calais.",
         g_fake(C, [("-samLR", "flak36", 200, 800, ""), ("-samSR", "flak37", 60, 600, ""),
                    ("-aaa, defense 2", "flak38", 300, 500, "")], "Z11"),
         s_items(C, [("Bunker", 0, 0), ("Bunker", 40, 150), ("Hangar A", 90, 350), ("Hangar A", 110, 400),
                     ("Fuel tank", 200, 400), ("Military staff", 250, 300)]))

    C = spot(ll(49.1450, 0.2300), 0, 0, "Lisieux depot")
    zone("combatZone_DepotLisieux", C, 1500, "Z12 Frappe — dépôts d'essence de Lisieux", "Frappes en profondeur",
         "Un dépôt de carburant de l'arrière du front, près de Lisieux (position illustrative) : réservoirs, pompes, "
         "entrepôts. Tout détruire ; flak moyenne.",
         g_fake(C, [("-samSR", "flak37", 200, 500, ""), ("-aaa, defense 2", "flak38", 20, 400, "")], "Z12"),
         s_items(C, [("Fuel tank", 30, 150), ("Fuel tank", 60, 200), ("Fuel tank", 90, 150), ("Fuel tank", 120, 220),
                     ("Fuel tank", 150, 260), ("Pump station", 240, 120), ("Warehouse", 300, 200), ("Warehouse", 320, 260)]))

    # ── Bases aériennes (OCA) ────────────────────────────────────────────────
    C = spot(off(A["Triqueville"], 90, 600), 0, 0, "Triqueville")
    zone("combatZone_Triqueville", C, 1500, "Z13 OCA — base aérienne de Triqueville", "Bases aériennes",
         "La base aérienne de Triqueville, au sud de l'estuaire de la Seine : chasseurs au parking, hangars et carburant. "
         "Tout détruire au sol ; flak moyenne et lourde, sous la QRA de la Seine.",
         g_fake(C, [("-samSR", "flak37", 90, 900, ""), ("-samLR", "flak36", 270, 800, "")], "Z13"),
         s_items(C, [("FW-190A8", 0, 300), ("FW-190A8", 15, 340), ("Bf-109K-4", 40, 300), ("Bf-109K-4", 50, 340),
                     ("Hangar A", 330, 300), ("Fuel tank", 180, 400)]))

    C = spot(off(A["Beaumont-le-Roger"], 90, 600), 0, 0, "Beaumont-le-Roger")
    zone("combatZone_BeaumontLeRoger", C, 1500, "Z14 OCA — base aérienne de Beaumont-le-Roger", "Bases aériennes",
         "La base aérienne de Beaumont-le-Roger, à l'arrière du front : bombardiers et chasseurs au parking, hangars et "
         "carburant. Tout détruire au sol ; flak moyenne et lourde.",
         g_fake(C, [("-samSR", "flak37", 90, 900, ""), ("-samLR", "flak36", 270, 800, "")], "Z14"),
         s_items(C, [("Ju-88A4", 0, 300), ("Ju-88A4", 20, 380), ("Ju-88A4", 40, 300), ("FW-190A8", 60, 340),
                     ("Hangar A", 180, 300), ("Fuel tank", 200, 400)]))

    # ── Antinavire ───────────────────────────────────────────────────────────
    C = sea(ll(49.5300, 0.0100), "Le Havre mer", margin=2000)
    zone("combatZone_VedettesLeHavre", C, 6500, "Z15 Antinavire — vedettes lance-torpilles du Havre", "Antinavire",
         "Les vedettes lance-torpilles (S-boote) basées au Havre, qui sortent attaquer les convois de la Manche, et la "
         "batterie côtière du cap de la Hève. Couler les vedettes ; flak de bord et batterie côtière "
         "(portée de 20 km environ pour les canons, sans menace pour les avions).",
         [{"name": "Vedettes", "position": xy(C), "keep_position": True, "patrol": True,
           "units": [{"type": "Schnellboot_type_S130", "count": 4}], "route": [xy(C), xy(ll(49.58, -0.02))]}], cat="ship",
         extra=[("Batterie Hève", spot(ll(49.5100, 0.0750), 0, 0, "Hève", margin=200),
                 [{"type": "flak37", "count": 2}, {"type": "SK_C_28_naval_gun", "count": 2}])])

    C = sea(ll(49.9000, 0.3000), "convoi côtier", margin=3000)
    zone("combatZone_ConvoiCotier", C, 4000, "Z16 Antinavire — convoi côtier vers Dieppe", "Antinavire",
         "Un convoi de cargos escortés longe la côte du Havre vers Dieppe, avec deux vedettes lance-torpilles. Couler les "
         "cargos ; flak de bord sur les escorteurs.",
         [{"name": "Convoi", "position": xy(C), "keep_position": True, "patrol": True,
           "units": [{"type": "Dry-cargo ship-1", "count": 2}, {"type": "Dry-cargo ship-2", "count": 1},
                     {"type": "Schnellboot_type_S130", "count": 2}],
           "route": [xy(C), xy(ll(49.95, 0.55))]}], cat="ship")
    return Z


if __name__ == "__main__":
    b = Batch()
    for name, c, r, fname, menu, text, side, cat, groups, statics, extra in zones():
        if cat == "ship":
            sea(c, name, margin=1500)
        for g in groups:
            for q in g.get("route") or []:
                (sea if cat == "ship" else land)((q["x"], q["y"]), f"{name} route", 1000 if cat == "ship" else 100)
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": False,
              "briefing": f"{text}\n{position_text(c)} {near_blue(c)}"}
        b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **side,
              category=cat, combat_zone=cz)
        for i, (typ, p) in enumerate(statics, 1):
            b.act("add_group", **side, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
                  position=xy(p), units=[{"type": typ}], for_combat_zone=name, keep_position=True)
        for gname, p, units in extra:
            b.act("add_group", **side, category="vehicle", name=gname, position=xy(p), units=units,
                  for_combat_zone=name, keep_position=True)
        print(f"{fname:56} {round(c[0]):>8} {round(c[1]):>8}  r={r}")
    b.save("08-zones.json")
