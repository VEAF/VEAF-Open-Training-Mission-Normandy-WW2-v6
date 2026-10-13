"""Lot 15 : date, météo de base, bullseye commun et briefing DCS de la mission.

Le texte est composé depuis les données (fréquences DCS des aérodromes, zones, QRA), pas tapé.
`python gen_15_identite.py [suffixe]` : un lot d'identité se rejoue sans danger (set_* remplacent), d'où le suffixe de
nom de lot pour garder chaque passage.
Météo : une seule, celle de la mission (le serveur VEAF fixe météo et heure de chaque session, décision de David du
12/10/2026) ; une après-midi d'été normande plausible (METAR LFRK du 13/10/2026 en octobre : 28013KT 9999 FEW031 18/12 Q1025,
ramené à juillet : vent d'ouest-sud-ouest, 18 °C, quelques cumulus), avec une seule couche (un METAR n'en vole qu'une).
"""
import json
import sys

import gen_07_entrainement as e
from gen_09_qra_cap import CAPS, QRAS
from gen_10_joueurs import ARENA, SANCTUARIES
from gen_11_config import COMBAT_MISSIONS
from lib import BLUE_SLOTS, BULLSEYE, RED_SLOTS, ROOT, Batch, xy

_t = (ROOT / "tools/airfield_channels.json").read_text(encoding="utf-8")
CH = {a["name"]: a for a in json.loads(_t[_t.index("{"):])["candidates"]}
SHORT = {"Longues-sur-Mer": "Longues", "Beny-sur-Mer": "Bény", "Abbeville Drucat": "Abbeville", "Evreux": "Évreux"}

ZONE_COUNT = 16


def base(n):
    f = CH[n]["freqs"]
    return f"{SHORT.get(n, n)} (V{f['vhf']:.2f})"


def qras(side):
    return ", ".join(f"{q['name'].replace('QRA ', '')} ({q['radius'] / 1852:.0f} nm)" for q in QRAS
                     if q["side"]["coalition"] == side)


def beacons():
    out = []
    for _z, (title, _c, _r, _s), bs in e.TOUR:
        out.append(f"{title} : " + ", ".join(f"{code} {mhz:.1f}" for code, mhz, _p, _sub in bs))
    return " ; ".join(out)


SITUATION = f"""VEAF Open Training — Normandie (1944, 6 juillet).
D+30. La tête de pont alliée tient Cherbourg, le Cotentin jusqu'à Carentan et l'ouest de Caen ; l'Angleterre du sud est la base arrière. Le front, tracé à l'estime donc approximatif, court de la côte ouest du Cotentin, par Carentan, Saint-Lô, Caumont et Villers-Bocage, à Carpiquet et à l'Orne ; au-delà, la France jusqu'à Paris et au Pas-de-Calais, plus les îles Anglo-Normandes, est rouge. Bullseye commun : Saint-Lô.

BASES BLEUES (slots dynamiques, VHF) : {", ".join(base(n) for n in BLUE_SLOTS)}. Tangmere est la base mère.
SOUTIEN : pas de ravitailleur ni d'AWACS en 1944 ; rien n'est posé. Raids de B-17G, de Ju 88 : voir les missions à la demande. Radio : une seule radio VHF/AM (Guard 121.5, arène 125.0).

ENTRAÎNEMENT (menu F10 VEAF, zones, trois niveaux chacun) : A mitraillage dans le bocage du Cotentin, B bombardement à Salisbury, C antiflak à Aurigny.
TOURISME : visite aérienne en trois circuits, balises VHF/AM — {beacons()} — et un guide qui raconte chaque monument survolé sous 1 500 ft sol ; menu F10 « Tourisme » pour faire apparaître les véhicules d'époque.
COMBAT : {ZONE_COUNT} zones (front, radars et flak, convois, frappes dans la profondeur, bases aériennes, antinavire), chacune avec son briefing dans le menu. Missions à la demande : CAP rouges et bleues, raid de Ju 88 sur la baie de Seine, raid de Ju 88 sur Arromanches, escorte de B-17G sur Rouen, interception d'un Ju 88 de reconnaissance.
QRA rouges : {qras('red')} ; QRA bleues : {qras('blue')}. Décollage 90 s après l'entrée du premier intrus ; pas de couloir de QRA sur le Cotentin sud, la haute Seine, le bocage de Flers et d'Argentan.
JOUEURS CONTRE JOUEURS : libre hors des sanctuaires. Sanctuaire bleu : Angleterre du sud ({SANCTUARIES[0][3] // 1000} km) ; rouge : Évreux ({SANCTUARIES[1][3] // 1000} km). Un intrus y est détruit après 60 s ; un missile tiré sur un défenseur est détruit. Arène de {ARENA[1] // 1852} nm de rayon au nord de Cherbourg, slots en vol, canons seulement.

Plan radio, cartes et détail de chaque zone : voir les images du briefing et le README de la mission."""

BLUE_TASK = ("Tenir la tête de pont et frapper la France occupée : s'entraîner sur les champs de tir A, B et C, puis attaquer les zones "
             "de combat rouges. Tangmere est la base mère ; Bény, Bazenville et Picauville sont en première ligne, Maupertus "
             "tient Cherbourg.")
RED_TASK = (f"Tenir la Normandie. Bases rouges avec slots : {', '.join(base(n) for n in RED_SLOTS)}. "
            "Le sanctuaire bleu d'Angleterre détruit tout appareil rouge qui y entre.")

if __name__ == "__main__":
    b = Batch()
    b.act("set_mission_date", date="1944-07-06", start_time="09:00")
    b.act("set_weather", metar="LFRK 061300Z 25008KT 9999 SCT040 18/11 Q1016")
    for side in ("blue", "red"):
        b.act("set_bullseye", coalition=side, position=xy(BULLSEYE))
    b.act("set_briefing", sortie="VEAF Open Training — Normandie 1944", situation=SITUATION, blue_task=BLUE_TASK,
          red_task=RED_TASK)
    b.save(f"15-identite{('-' + sys.argv[1]) if len(sys.argv) > 1 else ''}.json")
    print(SITUATION)
