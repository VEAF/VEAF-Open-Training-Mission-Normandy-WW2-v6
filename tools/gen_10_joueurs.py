"""Lot 10 : sanctuaires, arène de combat aérien, groupes des missions scénarisées.

Sanctuaires (cercles tirés de zones de déclenchement) :
  - bleu « Angleterre du sud » : 50 km autour de Portsmouth/Tangmere — la base mère, Ford, Funtington, le Solent et le
    circuit touristique de la côte sud ;
  - rouge « Évreux » : 25 km autour de la base d'Évreux, l'arrière rouge. Carpiquet, Lessay et Abbeville n'en ont pas :
    ils bloqueraient le front et le nord.
Arène : Manche, 40 nm au nord de Cherbourg, centre (75 000, -95 000), 20 nm de rayon, loin du front ; slots en vol des
deux camps, canons seulement (aucun appareil de 1944 ne tire de missile). Les bleus au sud, les rouges au nord.
Missions scénarisées (groupes en activation différée, déclarés dans `combat_missions:` de mission.yaml par gen_11) :
  - Défense : un raid de Ju 88 sur le port artificiel d'Arromanches, escorté de Fw 190 ;
  - Escorte : six B-17G vers les triages de Rouen, attendus par des Fw 190 et des Bf 109 ;
  - Interception : un Ju 88 de reconnaissance au-dessus de la tête de pont, escorté de deux Bf 109.
Chasseurs : canons seulement, sans pylône (DCS ne nomme aucun emport pour les appareils de module, list_payloads, et le
template de slot dynamique n'en porte pas). Bombardiers : emports relevés dans la base d'unités de l'installation DCS
(db.Units.lua) : Ju 88 A-4 = 2 SC 500 sous les ailes et 10 SC 50 en soute ; B-17G = 12 M64 (500 lb).
"""
from lib import AIRFIELDS, BLUE_UK, BLUE_US, PLACES, RED, Batch, ll, xy

SANCTUARIES = [
    ("Sanctuaire Angleterre du sud", "SANCT-Angleterre", ll(50.85, -0.95), 50000, "BLUE"),
    ("Sanctuaire Évreux", "SANCT-Evreux", AIRFIELDS["Evreux"], 25000, "RED"),
]

ARENA = ((75000, -95000), 37000)   # centre, rayon (20 nm)
ARENA_SLOTS = [
    # nom, camp, type, position (sud = bleu, nord = rouge), cap
    ("Arène bleue P-51D", BLUE_US, "P-51D", (55000, -96500), 0),
    ("Arène bleue Spitfire LF IX", BLUE_UK, "SpitfireLFMkIX", (55000, -93500), 0),
    ("Arène bleue P-47D", BLUE_US, "P-47D-30", (55000, -90500), 0),
    ("Arène rouge Fw 190 A-8", RED, "FW-190A8", (95000, -96500), 180),
    ("Arène rouge Fw 190 D-9", RED, "FW-190D9", (95000, -93500), 180),
    ("Arène rouge Bf 109 K-4", RED, "Bf-109K-4", (95000, -90500), 180),
]

ARROMANCHES = PLACES["Arromanches-les-Bains"]
ROUEN_TRIAGE = ll(49.4120, 1.0780)        # gare de triage de Sotteville-lès-Rouen
JU88 = {"1": {"CLSID": "SC_501_SC500"}, "2": {"CLSID": "{JU88A4TORP_10xSC50_on_InvCountedAttachmentPoints}"},
        "3": {"CLSID": "SC_501_SC500"}}
B17 = {"1": {"CLSID": "{12xM64}"}}
# Missions scénarisées : nom, camp, type, nombre, départ, altitude ft, kt, tâche, emport (pylons) ou None, points suivants
SCENARIO = [
    ("SC-Raid-Mulberry-Bombers", RED, "Ju-88A4", 6, ll(49.62, 0.45), 14000, 220, "Ground Attack", JU88,
     [ll(49.55, -0.20), ARROMANCHES]),
    ("SC-Raid-Mulberry-Escort", RED, "FW-190A8", 4, ll(49.64, 0.47), 15000, 260, "Escort", None,
     [ll(49.55, -0.20), ARROMANCHES]),
    ("SC-Escort-B17", BLUE_US, "B-17G", 6, ll(50.45, -0.15), 20000, 170, "Ground Attack", B17,
     [ll(49.95, 0.40), ROUEN_TRIAGE]),
    ("SC-Escort-B17-Interceptors", RED, "FW-190A8", 4, ll(49.50, 1.35), 20000, 260, "CAP", None,
     [ll(49.80, 0.75), ROUEN_TRIAGE]),
    ("SC-Escort-B17-Interceptors-Bf109", RED, "Bf-109K-4", 2, ll(49.48, 1.40), 21000, 260, "CAP", None,
     [ll(49.80, 0.75), ROUEN_TRIAGE]),
    ("SC-Recce-Ju88", RED, "Ju-88A4", 1, ll(49.60, 0.30), 22000, 215, "Reconnaissance", None,
     [ll(49.50, -0.60), ll(49.58, -1.25)]),
    ("SC-Recce-Escort", RED, "Bf-109K-4", 2, ll(49.62, 0.32), 23000, 240, "Escort", None,
     [ll(49.50, -0.60), ll(49.58, -1.25)]),
]

if __name__ == "__main__":
    b = Batch()
    for name, zone, c, r, side in SANCTUARIES:
        b.act("add_trigger_zone", name=zone, position=xy(c), radius=r)
    b.act("add_trigger_zone", name="Arene", position=xy(ARENA[0]), radius=ARENA[1])
    for name, side, typ, p, hdg in ARENA_SLOTS:
        b.act("add_air_group", **side, name=name, unit_type=typ, count=2, start="air", position=xy(p),
              altitude_ft=15000, speed_kt=250, heading_deg=hdg, skill="Client", task="CAP")
    for name, side, typ, n, p, alt, kt, task, pyl, route in SCENARIO:
        extra = {"pylons": pyl} if pyl else {}
        b.act("add_air_group", **side, name=name, unit_type=typ, count=n, start="air", position=xy(p),
              altitude_ft=alt, speed_kt=kt, task=task, skill="High", late_activation=True, **extra)
        for q in route:
            b.act("edit_route", group_name=name, operation="add", position=xy(q), altitude_ft=alt, speed_kt=kt)
    b.act("edit_route", group_name="SC-Raid-Mulberry-Bombers", operation="add_task", index=3, task="bombing",
          task_params={"position": xy(ARROMANCHES), "expend": "All", "attack_qty": 1})
    b.act("edit_route", group_name="SC-Escort-B17", operation="add_task", index=3, task="bombing",
          task_params={"position": xy(ROUEN_TRIAGE), "expend": "All", "attack_qty": 1})
    for esc, target in [("SC-Raid-Mulberry-Escort", "SC-Raid-Mulberry-Bombers"),
                        ("SC-Recce-Escort", "SC-Recce-Ju88")]:
        b.act("edit_route", group_name=esc, operation="add_task", index=1, task="escort",
              task_params={"group_name": target, "engagement_distance_nm": 15})
    b.save("10-joueurs.json")
