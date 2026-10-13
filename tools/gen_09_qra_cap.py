"""Lot 09 : QRA (rouges, et bleues puisque le rouge est jouable) et CAP à la demande.

QRA : cercle dans le territoire du camp qui défend, réponse graduée (une paire de chasseurs, puis quatre), un seul
groupe tiré au sort parmi des appareils différents, délai 90 s, pas de réaction aux hélicoptères (il n'y en a pas en
1944), pas de menu radio ouvert à tous. Départ en vol au-dessus de la base : Normandy n'a pas de données de parking dans
VMCT (describe_known_limitations, no-parking-data-outside-three-theatres).
  - rouges : Caen (cercle de 14 km décalé de 10 km au sud-est de Carpiquet : ni Bény ni Bazenville dedans), l'estuaire de la
    Seine (Triqueville, 22 km), le Pas-de-Calais (Saint-Omer, 30 km : le blockhaus d'Éperlecques et ses voisins) ;
  - bleues : le Solent (Tangmere, 25 km), la tête de pont (Longues-sur-Mer, 20 km décalé vers la mer).
  Couloirs libres côté rouge : tout le Cotentin sud (Lessay, Coutances), la Seine en amont de Rouen, le bocage (Flers,
  Argentan, Vire).
CAP rouges dans le territoire rouge, CAP bleues dans le territoire bleu (au-dessus de la tête de pont et de la Manche).
Armement : canons seulement pour les chasseurs (aucun emport nommé par DCS pour un appareil de module, et le template de
slot ne porte aucun pylône) ; Ju 88 et B-17G avec les emports relevés dans db.Units.lua (voir gen_10_joueurs.py).
"""
from gen_10_joueurs import JU88
from lib import AIRFIELDS, BLUE_UK, BLUE_US, RED, Batch, ll, off, xy

A = AIRFIELDS

CAEN_CENTER = off(A["Carpiquet"], 120, 10000)
QRAS = [
    dict(name="QRA Caen", side=RED, zone="QRA-Caen", center=CAEN_CENTER, radius=14000, airfield="Carpiquet",
         enemy="BLUE", levels=[
             (1, [("QRA-Caen-Bf109", "Bf-109K-4", 2), ("QRA-Caen-Fw190A8", "FW-190A8", 2)]),
             (3, [("QRA-Caen-Fw190D9x4", "FW-190D9", 4), ("QRA-Caen-Bf109x4", "Bf-109K-4", 4)])]),
    dict(name="QRA Seine", side=RED, zone="QRA-Seine", center=A["Triqueville"], radius=22000, airfield="Triqueville",
         enemy="BLUE", levels=[
             (1, [("QRA-Seine-Fw190A8", "FW-190A8", 2), ("QRA-Seine-Bf109", "Bf-109K-4", 2)]),
             (3, [("QRA-Seine-Fw190A8x4", "FW-190A8", 4), ("QRA-Seine-Fw190D9x4", "FW-190D9", 4)])]),
    dict(name="QRA Pas-de-Calais", side=RED, zone="QRA-PasDeCalais", center=A["Saint-Omer Wizernes"], radius=30000,
         airfield="Saint-Omer Wizernes", enemy="BLUE", levels=[
             (1, [("QRA-PdC-Bf109", "Bf-109K-4", 2), ("QRA-PdC-Fw190D9", "FW-190D9", 2)]),
             (3, [("QRA-PdC-Bf109x4", "Bf-109K-4", 4), ("QRA-PdC-Fw190A8x4", "FW-190A8", 4)])]),
    dict(name="QRA Solent", side=BLUE_UK, zone="QRA-Solent", center=A["Tangmere"], radius=25000, airfield="Tangmere",
         enemy="RED", levels=[
             (1, [("QRA-Solent-Spitfire", "SpitfireLFMkIX", 2), ("QRA-Solent-P51D", "P-51D", 2)]),
             (3, [("QRA-Solent-Spitfirex4", "SpitfireLFMkIX", 4), ("QRA-Solent-P51Dx4", "P-51D-30-NA", 4)])]),
    dict(name="QRA Tête de pont", side=BLUE_US, zone="QRA-TetedePont", center=off(A["Longues-sur-Mer"], 0, 4000),
         radius=20000, airfield="Longues-sur-Mer", enemy="RED", levels=[
             (1, [("QRA-TetedePont-P47D", "P-47D-30", 2), ("QRA-TetedePont-P51D", "P-51D", 2)]),
             (3, [("QRA-TetedePont-P47Dx4", "P-47D-40", 4), ("QRA-TetedePont-P51Dx4", "P-51D-30-NA", 4)])]),
]

# (nom, type, nombre, camp, a, b, altitude ft, kt, emport, menu, briefing)
CAPS = [
    ("CAP-Caen-Bf109", "Bf-109K-4", 2, RED, ll(48.98, -0.35), ll(49.00, 0.10), 15000, 260, None,
     "CAP rouge Bf 109 K-4 — sud de Caen — 15 000 ft",
     "Deux Bf 109 K-4 patrouillent au sud de Caen, entre Falaise et Lisieux, à 15 000 ft. Canons et mitrailleuses "
     "seulement."),
    ("CAP-Cotentin-Fw190", "FW-190A8", 2, RED, ll(49.05, -1.45), ll(49.10, -1.20), 12000, 250, None,
     "CAP rouge Fw 190 A-8 — Cotentin sud — 12 000 ft",
     "Deux Fw 190 A-8 patrouillent au sud du front du Cotentin, entre Coutances et Saint-Lô, à 12 000 ft. Canons "
     "seulement."),
    ("CAP-Seine-Fw190D9", "FW-190D9", 2, RED, ll(49.22, 0.55), ll(49.40, 1.00), 22000, 270, None,
     "CAP rouge Fw 190 D-9 — vallée de la Seine — 22 000 ft",
     "Deux Fw 190 D-9, le chasseur le plus performant du camp rouge, patrouillent haut au-dessus de la Seine, entre "
     "Pont-Audemer et Rouen, à 22 000 ft. Canons seulement."),
    ("Raid-Ju88", "Ju-88A4", 4, RED, ll(49.45, 0.30), ll(49.55, -0.10), 12000, 215, {"pylons": JU88},
     "Raid rouge Ju 88 A-4 à intercepter — baie de Seine — 12 000 ft",
     "Quatre bombardiers Ju 88 A-4 tournent au-dessus de la baie de Seine, à 12 000 ft, prêts à frapper les plages : "
     "les intercepter. Armement défensif seulement tiré par les mitrailleurs."),
    ("CAP-TetedePont-P51D", "P-51D", 2, BLUE_US, ll(49.45, -0.65), ll(49.42, -0.20), 15000, 260, None,
     "CAP bleue P-51D — tête de pont — 15 000 ft",
     "Deux P-51D patrouillent au large de la tête de pont, de Port-en-Bessin à Ouistreham, à 15 000 ft. Canons "
     "seulement."),
    ("CAP-Cotentin-Spitfire", "SpitfireLFMkIX", 2, BLUE_UK, ll(49.58, -1.30), ll(49.62, -0.85), 12000, 250, None,
     "CAP bleue Spitfire LF IX — Cotentin — 12 000 ft",
     "Deux Spitfire LF Mk IX patrouillent au nord du Cotentin, de Cherbourg à Saint-Vaast, à 12 000 ft. Canons "
     "seulement."),
]

if __name__ == "__main__":
    b = Batch()
    for q in QRAS:
        groups, levels = [], []
        ap = A[q["airfield"]]
        for count, members in q["levels"]:
            names = []
            for i, (gname, typ, n) in enumerate(members):
                groups.append({"name": gname, "units": [{"type": typ, "count": n}], "start": "air",
                               "position": xy((ap[0] + 1500 * i, ap[1] + 1500 * len(names))), "altitude_ft": 5000,
                               "speed_kt": 250, "airfield": q["airfield"]})
                names.append(gname)
            levels.append({"enemy_count": count, "groups": names, "random_pick": 1})
        side = q["side"]
        b.act("create_qra", name=q["name"], coalition=side["coalition"], country_id=side["country_id"],
              country_name=side["country_name"], trigger_zone=q["zone"], position=xy(q["center"]), radius=q["radius"],
              groups=groups, enemy_coalitions=[q["enemy"]],
              qra={"groups_by_enemy_count": levels, "delay_before_activating": 90, "delay_before_rearming": 600,
                   "react_on_helicopters": False, "airport_link": q["airfield"]})
    for name, typ, n, side, a, bb, alt, kt, loadout, menu, brief in CAPS:
        extra = loadout or {}
        b.act("create_cap_mission", mission_name=name, units=[{"type": typ, "count": n}], **side, position=xy(a),
              route=[{**xy(bb), "altitude_ft": alt}], altitude_ft=alt, speed_kt=kt,
              cap={"menu_name": menu, "briefing": brief}, **extra)
    b.save("09-qra-cap.json")
