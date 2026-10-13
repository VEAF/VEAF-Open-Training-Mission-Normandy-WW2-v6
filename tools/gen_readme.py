"""Écrit README.md, le briefing des pilotes, depuis tools/briefing_data.json, et redessine les cartes (gen_map.py).

Lancer gather.py avant : toutes les valeurs viennent du dossier de la mission, rien n'est tapé ici à part le contexte et les
consignes. Construit comme le README de l'Open Training Sinaï v6, adapté à 1944.
"""
import json
import math

import gen_07c_guide as guide
import gen_map
from paths import ROOT, TOOLS

D = json.load(open(TOOLS / "briefing_data.json", encoding="utf-8"))
gen_map.render()

side = {"blue": "Bleu", "red": "Rouge"}
ADL = {"-samLR": "flak lourde (88 mm, 3,7 in)", "-samVLR": "flak lourde de zone", "-samSR": "flak moyenne (37 mm)",
       "-aaa": "flak légère (20 mm, 40 mm)"}
NAME = {"Bf-109K-4": "Bf 109 K-4", "FW-190A8": "Fw 190 A-8", "FW-190D9": "Fw 190 D-9", "P-51D": "P-51D",
        "P-51D-30-NA": "P-51D-30", "P-47D-30": "P-47D-30", "P-47D-40": "P-47D-40", "SpitfireLFMkIX": "Spitfire LF Mk IX",
        "Ju-88A4": "Ju 88 A-4", "B-17G": "B-17G"}
BASE_MERE = "Tangmere"
ZOOM = {s: (f"docs/cartes/carte_{i:02d}_{s}.jpg", t) for i, (s, t, _) in enumerate(gen_map.ZOOMS, 1)}
md = []
w = md.append


def c(v):
    return f"`{v}`"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(x).replace("|", "/") for x in r) + " |" for r in rows]
    return "\n".join(out)


def zooms(*slugs):
    """Les cartes zoomées d'une section, deux par ligne, chacune cliquable (une seule : pleine largeur)."""
    if len(slugs) == 1:
        w(f"![{ZOOM[slugs[0]][1]}]({ZOOM[slugs[0]][0]})")
        w("")
        return
    cells = [f'<td width="50%"><a href="{ZOOM[s][0]}"><img src="{ZOOM[s][0]}" alt="{ZOOM[s][1]}"></a><br>'
             f'<sub>{ZOOM[s][1]}</sub></td>' for s in slugs]
    w("<table>" + "".join("<tr>" + "".join(cells[k:k + 2]) + "</tr>" for k in range(0, len(cells), 2)) + "</table>")
    w("")


date, start, bu = D["date"], D["start"], D["bullseye"]
w("# VEAF Open Training — Normandie (6 juillet 1944)")
w("")
w("Mission d'entraînement ouverte des serveurs VEAF, sur la carte **Normandy** de DCS, au 6 juillet 1944 : trente jours après le "
  "Débarquement. Ce document est le briefing complet : bases, zones, QRA, CAP, radio, météo. Les positions sont données en "
  "coordonnées (degrés, minutes décimales) et en relèvement/distance depuis le bullseye (relèvement vrai, nautiques).")
w("")
w(table(["Mission", "Date", "Heure de base", "Bullseye (bleu et rouge)", "Météo", "ATC"],
        [[c(D["name"]), f'{date["Day"]:02d}/{date["Month"]:02d}/{date["Year"]}',
          f'{start // 3600:02d}:{start % 3600 // 60:02d} (heure de la carte)', f'Saint-Lô · {c(bu["ddm"])}',
          "celle du serveur VEAF", "coupé sur tous les aérodromes"]]))
w("")
w("**Sommaire** : [Situation](#situation) · [Carte](#carte) · [Bases](#bases) · [Soutien](#soutien) · "
  "[Entraînement](#entraînement) · [Tourisme](#tourisme) · [Zones de combat](#zones-de-combat) · "
  "[Missions scénarisées](#missions-scénarisées) · [QRA](#qra) · [CAP à la demande](#cap-à-la-demande) · "
  "[Combat entre joueurs](#combat-entre-joueurs) · [Défense aérienne](#défense-aérienne) · [Plan radio](#plan-radio) · "
  "[Météo et heures](#météo-et-heures) · [Commandes utiles](#commandes-utiles) · [Pour les créateurs de mission](#pour-les-créateurs-de-mission)")
w("")
w("## Situation")
w("")
w("D+30. La tête de pont alliée tient Cherbourg (tombé les 26-29 juin), le Cotentin jusqu'à Carentan et l'ouest de Caen ; "
  "l'Angleterre du sud est la base arrière. Le front, tracé à l'estime donc **approximatif** "
  f"({D['fronts_nm'][0]} nm), court de la côte ouest du Cotentin, par Carentan, Saint-Lô, Caumont et Villers-Bocage, à Carpiquet "
  "et à l'Orne. Au-delà, la France jusqu'à Paris et au Pas-de-Calais, plus les îles Anglo-Normandes, est rouge. Le bullseye "
  "commun est Saint-Lô, au milieu du front.")
w("")
w("La version 5 n'avait que quatre zones de combat et trois bases à slots bleues ; la v6 en compte "
  f"{sum(1 for z in D['zones'] if not z['training'])}, "
  f"{sum(1 for b in D['bases'] if b['side'] == 'blue')} bases bleues et {sum(1 for b in D['bases'] if b['side'] == 'red')} "
  "rouges à slots, des QRA, des CAP, des scénarios et trois circuits touristiques.")
w("")
w("Zones de combat, missions et scénarios se pilotent par le menu radio F10 (*Zones de combat*, *Missions de combat*).")
w("")
w("## Carte")
w("")
w("![Carte de la mission](docs/carte.jpg)")
w("")
w("Cartes zoomées, reprises dans les sections qu'elles illustrent : "
  + " · ".join(f"[{t.split(' : ')[0]}]({f})" for f, t in ZOOM.values()) + ".")
w("")
w("Carrés : bases avec slots (bleu / rouge). Pointillés : CAP à la demande. Cercles pleins : QRA. Pastilles vertes : entraînement "
  "(A appui rapproché, B bombardement, C antiflak). Pastilles marron T : circuits touristiques ; triangles marron : leurs "
  "balises. Pastilles rouges numérotées : zones de combat. Cercles en tirets : sanctuaires et arène. Fond OpenStreetMap ; la "
  "ligne de front est approximative. Le briefing DCS montre cette carte puis les zooms (flèches sous l'image, molette pour "
  "grossir) ; la carte F10 porte les mêmes dessins : front, zones, QRA, sanctuaires, circuits et arène.")
w("")
w("## Bases")
w("")
rows = []
for b in D["bases"]:
    here = [ADL.get(a["alias"], a["alias"]) for a in D["ad"]
            if a["side"] == b["side"] and abs(a["x"] - b["x"]) < 9000 and abs(a["y"] - b["y"]) < 9000]
    rows.append([f'**{b["name"]}**' + (" (base mère)" if b["name"] == BASE_MERE else ""), side[b["side"]], c(b["ddm"]) if "ddm" in b else "",
                 c(b["be"]), c(b.get("vhf", "—")), " + ".join(dict.fromkeys(here)) or "—"])
w(table(["Base", "Camp", "Position", "Bullseye", "VHF", "Défense"], rows))
w("")
w("Slots dynamiques, démarrage moteur chaud, carburant et munitions illimités : bleus P-47D, P-51D, Spitfire LF IX et Mosquito ; "
  "rouges Bf 109 K-4 et Fw 190 A-8 et D-9. Les autres aérodromes de chaque camp lui appartiennent, sans slots : côté bleu les "
  "terrains d'Angleterre du sud et de la tête de pont, côté rouge ceux de la France occupée et des îles Anglo-Normandes. "
  "Aucun aérodrome neutre. Fréquences : celles que DCS donne à chaque tour (ATC coupé).")
w("")
zooms("plages", "cotentin", "solent", "kent")
w("## Soutien")
w("")
w("Il n'y a ni ravitailleur ni AWACS en 1944 : aucun n'est posé, aucun n'est annoncé. Pas de FARP ni d'hélicoptère non plus. Le "
  "soutien est celui de l'époque : des bases proches du front, la radio VHF, et les vols de bombardiers des scénarios "
  "(B-17G, Ju 88). Les bases de la tête de pont sont à quelques minutes du front ; l'Angleterre est à 80-135 nm.")
w("")
w("## Entraînement")
w("")
w("Loin du front ou à l'arrière, à quelques minutes d'une base. Trois niveaux par famille, chacun comprenant ceux d'en dessous. "
  "**Activez un seul niveau par famille à la fois.** Les cibles des niveaux faciles sont des véhicules immobiles, en tir "
  "interdit : chauds au pod, inertes.")
w("")
for fam, label in (("Bocage", "A — Appui rapproché : bocage du Cotentin (à l'ouest d'Azeville)"),
                   ("Salisbury", "B — Bombardement : plaine de Salisbury (Angleterre)"),
                   ("Aurigny", "C — Antiflak : fort Tourgis (Aurigny, île rouge)")):
    lv = [z for z in D["zones"] if z["key"].startswith(f"combatZone_{fam}_")]
    z0 = lv[0]
    w(f"### {label}")
    w("")
    w(f'{c(z0["ddm"])} · bullseye {c(z0["be"])} · rayon {z0["radius_nm"]:.1f} nm · menu F10 « {z0["menu"]} »')
    w("")
    for z in lv:
        w(f'- **{z["name"]}** — {z["briefing"]}')
    w("")
w("## Tourisme")
w("")
w("Trois circuits aériens, hors combat, avec une balise radio VHF/AM à chaque site (elle répète son indicatif en morse) et un guide "
  "qui parle à tout appareil d'un joueur passant sous 1 500 ft sol au-dessus d'un monument : un message par monument, renouvelé "
  "après 10 minutes. La zone F10 *Tourisme* fait seulement apparaître des véhicules d'époque et quelques soldats ; les balises "
  "et le guide sont permanents. La présence des monuments dans le décor DCS est à confirmer en jeu.")
w("")
for z in (z for z in D["zones"] if z["key"].startswith("combatZone_Tour")):
    w(f'### {z["name"]}')
    w("")
    w(f'{c(z["ddm"])} · bullseye {c(z["be"])} · menu F10 « {z["menu"]} »')
    w("")
    w(z["briefing"].split("\n")[0])
    w("")
    key = {"Plages": "SWD", "Cotentin": "CHB", "Angleterre": "NDL"}[z["key"].replace("combatZone_Tour", "")]
    first = next(i for i, b in enumerate(D["beacons"]) if b["code"] == key)
    n = {"SWD": 4, "CHB": 3, "NDL": 4}[key]
    w(table(["Balise", "Site", "VHF/AM", "Position"],
            [[f'**{x["code"]}**', x["site"], c(f'{x["mhz"]:.1f}'), c(x["ddm"])] for x in D["beacons"][first:first + n]]))
    w("")
zooms("plages", "cotentin", "solent")
w("Le guide connaît aussi, hors circuit, le Mont-Saint-Michel (en territoire rouge au 6 juillet), Stonehenge, Douvres et "
  "Portsmouth. Monuments du guide : " + ", ".join(m[3].split(".")[0].split(",")[0] for m in guide.MONUMENTS) + ".")
w("")
w("## Zones de combat")
w("")
w("Les numéros renvoient à la carte. Chaque zone s'active par le menu F10 *Zones de combat*, qui redonne son briefing et sa "
  "position. Une partie des sites change d'une activation à l'autre (batteries tirées au sort, groupes blindés tirés au sort).")
w("")
zooms("seine", "calais")
for menu in ("Front", "Flak et radars", "Convois", "Frappes en profondeur", "Bases aériennes", "Antinavire"):
    w(f"### {menu}")
    w("")
    for z in D["zones"]:
        if z["training"] or z["menu"] != menu:
            continue
        w(f'**{z["name"]}** — {c(z["ddm"])} · bullseye {c(z["be"])}')
        w("")
        w(f'{z["briefing"]} Base amie la plus proche : {z["near"]}')
        w("")
w("## Missions scénarisées")
w("")
for cm in D["combat_missions"]:
    w(f'- **{cm["name"]}** — {cm["briefing"]}'.replace("\n", " "))
w("")
w("À lancer par le menu F10 *Missions de combat*. Elles n'ont pas de condition de réussite automatique : ce sont les pilotes "
  "qui jugent.")
w("")
w("## QRA")
w("")
w(table(["QRA", "Défend", "Centre", "Bullseye", "Rayon", "Base", "Réponse"],
        [[f'**{q["name"]}**', side[q["side"]], c(q["ddm"]), c(q["be"]), c(f'{q["radius_nm"]} nm'), q["airport"],
          "<br>".join(f'dès {t["n"]} intrus : {t["pick"]} vol parmi ' + ", ".join(
              f'{x.split(" × ")[0]} × {NAME.get(x.split(" × ")[1], x.split(" × ")[1])}' for x in t["types"])
                      for t in q["tiers"])] for q in D["qra"]]))
w("")
delay = D["qra"][0]["delay"]
w(f"Les chasseurs décollent de la piste {delay} s après l'entrée du premier intrus dans le cercle ; les hélicoptères (il n'y en a pas "
  "en 1944) ne comptent pas. Couloirs sans QRA rouge : le Cotentin sud (Lessay, Coutances), la haute Seine au-delà de Rouen, "
  "le bocage de Flers, d'Argentan et de Vire. Les bases bleues les plus proches du front (Bény, Bazenville) sont hors des "
  "cercles rouges.")
w("")
w("## CAP à la demande")
w("")
w(table(["Mission", "Camp", "Appareils", "Niveau", "Bullseye (milieu)", "Description"],
        [[f'**{x["menu"]}**', side[x["side"]], f'{x["n"]} × {NAME.get(x["type"], x["type"])}', c(f'FL{x["fl"]:03d}'),
          c(x["mid_be"]), x["briefing"]] for x in D["caps"]]))
w("")
w("À lancer par le menu F10 *Missions de combat*.")
w("")
w("## Combat entre joueurs")
w("")
w("Des joueurs volent des deux côtés. Le combat entre joueurs est **permis sur le théâtre et dans l'arène, interdit dans les "
  "sanctuaires** : l'Angleterre du sud côté bleu (Tangmere, Ford, Funtington, le Solent et son circuit touristique) ; Évreux "
  "côté rouge. Carpiquet, Lessay et Abbeville n'en ont pas : leurs abords, et le front, sont les plus disputés. Un pilote du "
  "camp adverse y est prévenu dès l'entrée, puis détruit au bout de 60 s, et les missiles tirés sur un appareil qui s'y trouve "
  "sont détruits. Les limites sont tracées sur la carte F10.")
w("")


def centre_be(z):
    dx, dy = z["x"] - D["bullseye"]["x"], z["y"] - D["bullseye"]["y"]
    return f"{round((math.degrees(math.atan2(dy, dx)) + 360) % 360) % 360:03d}°/{round(math.hypot(dx, dy) / 1852)} nm"


w(table(["Sanctuaire", "Protège", "Centre (bullseye)", "Rayon"],
        [[z["name"].replace("Sanctuaire ", ""), side[z["side"]], c(centre_be(z)), c(f'{z["radius_km"]:.1f} km')]
         for z in D["sanctuaries"]]))
w("")
az = D["arena_zone"]
w("### Arène")
w("")
w(f'Dans la Manche, au nord de Cherbourg : {c(az["ddm"])} · bullseye {c(az["be"])} · rayon {az["radius_nm"]} nm. Slots en '
  "départ en vol (15 000 ft), bleus au sud, rouges au nord, face à face, **canons seulement** : aucun appareil de 1944 ne "
  "tire de missile. Fréquence commune 125.0.")
w("")
zooms("arene")
rows = [[side[a["side"]], NAME.get(a["type"], a["type"]), f'{a["n"]} appareils', c(f'FL{a["fl"]:03d}')] for a in D["arena_slots"]]
w(table(["Camp", "Appareil", "Slot", "Départ"], rows))
w("")
w("## Défense aérienne")
w("")
w("De la flak, pas de missile. Défense permanente des deux camps : flak légère et moyenne sur chaque base avec slots, flak "
  "lourde à l'arrière et sur les points sensibles (Portsmouth, le port artificiel d'Arromanches, Cherbourg, Le Havre, Rouen), "
  "radars d'alerte avancée Freya et Würzburg côté rouge, directeurs de tir côté bleu. Aux bases de première ligne (Bény, "
  "Bazenville, Picauville, Carpiquet, Lessay), seulement de la courte portée, posée du côté opposé à la base adverse. Aucune "
  "défense permanente ne couvre une base adverse avec slots (portées DCS, `docs/portees.md`). Chaque zone de combat a en plus "
  "sa propre défense, décrite dans sa fiche.")
w("")
for sd in ("blue", "red"):
    w(f"**{side[sd]}** :")
    w("")
    w(table(["Site", "Système", "Position", "Bullseye"],
            [[a["name"], ADL.get(a["alias"], a["alias"]), c(a["ddm"]), c(a["be"])] for a in D["ad"] if a["side"] == sd]))
    w("")
w("## Plan radio")
w("")
w("Tous les appareils de 1944 n'ont qu'une radio VHF/AM (SCR-522, TR 1143, FuG 16) : Guard 121.5, arène 125.0, puis les "
  "bases, dont les fréquences sont celles que DCS donne à chaque tour. Les balises touristiques sont en VHF 130.0-136.5, hors "
  "de la bande des tours (118.0-123.0, 132.45 et 134.8).")
w("")
for sd in ("blue", "red"):
    rows = []
    for k, v in sorted(D["radio"][sd]["primary_2"].items(), key=lambda kv: int(kv[0])):
        mhz = D["channels"].get(v, {}).get("vhf")
        if mhz is None:
            continue
        rows.append([c(k), D["titles"].get(v, v).replace("Base-", ""), c(mhz)])
    w(f"### {side[sd]} (VHF)")
    w("")
    w(table(["Canal", "Nom", "MHz"], rows))
    w("")
w("### Rouge, Fw 190 (FM 38.4-42.4 MHz)")
w("")
w("Le Fw 190 n'accorde que 38.4-42.4 MHz (FuG 16 Z) : ses préréglages sont les fréquences FM des bases rouges, dans l'ordre "
  "de la liste VHF rouge sans Guard ni l'arène.")
w("")
bases_red = [v for k, v in sorted(D["radio"]["red"]["primary_2"].items(), key=lambda kv: int(kv[0])) if v.startswith("Base-")]
w(table(["Canal", "Base", "MHz"], [[c(k), D["titles"].get(bases_red[int(k) - 1], "").replace("Base-", ""), c(m)]
                                    for k, m in sorted(D["fw_channels"].items())]))
w("")
w("## Météo et heures")
w("")
wx = D["weather"]
w(f'La mission démarre le {date["Day"]:02d}/{date["Month"]:02d}/{date["Year"]} à {start // 3600:02d}:{start % 3600 // 60:02d} '
  f'(heure de la carte), {wx["sky"]}, {wx["temperature"]:.0f} °C, vent du {wx["wind_from"]:03.0f}° à '
  f'{wx["wind_ms"] * 1.944:.0f} kt. **Sur les serveurs VEAF, c\'est le serveur qui fixe la météo et l\'heure de chaque '
  "session** : la mission n'a pas de variantes météo.")
w("")
w("## Commandes utiles")
w("")
w("- `-cas` : fait apparaître une cible CAS aléatoire au marqueur.")
w("- `-point <nom>` : nomme un point de la carte.")
w("- `-smoke`, `-light`, `-signal` : fumigène, éclairage, fusée.")
w("- Les alias qui posent du matériel moderne (`-sa6`, `-hawk`, `-patriot`…) ne conviennent pas à 1944 : préférez `-aaa`, `-samSR`, "
  "`-samLR`, `-armor`.")
w("")
w("Rôles sans avion : 5 slots par camp pour chaque rôle (Game Master, commandant tactique, JTAC, observateur), et un "
  "pilote peut prendre la main sur les véhicules au sol. Le menu F10 VEAF reste vide pour un Game Master : il n'a pas de "
  "groupe, et les commandes sécurisées ne sont posées que groupe par groupe (VMCT #128, limite de DCS).")
w("")
w(open(TOOLS / "readme_makers.md", encoding="utf-8").read())
open(ROOT / "README.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print(f"VERDICT : README.md écrit ({sum(len(x) for x in md)} caractères), cartes redessinées")
