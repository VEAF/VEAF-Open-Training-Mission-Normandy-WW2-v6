"""Lot 11 : configuration de mission.yaml — identité, profils, modules, SANCTUARY, missions scénarisées.
Se rejoue sans doublon (il écrit des blocs, il n'ajoute pas de groupes).

Époque 1944 : pas d'hélicoptère (CTLD et CSAR n'ont personne à servir), pas de porte-avions (CARRIER), ni ravitailleur ni AWACS
(ASSETS vide) : ces modules sont coupés, pas oubliés. Skynet est coupé (aucun SAM). Les alias de batterie doivent nommer un pays qui est dans un
camp de la mission : `country thirdreich` (Germany n'est dans aucun camp, le spawn prend alors le camp neutre et s'arrête sur
`networkName nil`, sonde en jeu du 13/10/2026 ; fix_country.py).
Pack « WWII Armour and Technics » (flak, blindés, véhicules, B-17G, Ju 88 A-4) : les actions MCP n'écrivent rien dans
`requiredModules` (vérifié : la table reste vide), donc un pilote qui n'a pas le pack charge la mission sans voir ces unités.
Météo : pas de variantes (le serveur VEAF fixe météo et heure, décision de David du 12/10/2026) ; une météo de base
plausible est posée par gen_15_identite.py.
"""
import sys
from pathlib import Path

from ruamel.yaml import YAML

from gen_10_joueurs import SANCTUARIES
from lib import M, ROOT

sys.stdout.reconfigure(encoding="utf-8")

COMBAT_MISSIONS = [
    {"name": "Defense-Mulberry", "friendly_name": "Défense — raid de Ju 88 sur le port artificiel d'Arromanches",
     "secured": False,
     "briefing": "Six Ju 88 A-4 chargés de bombes, escortés de quatre Fw 190 A-8, partent de l'estuaire de la Seine vers "
                 "le port artificiel d'Arromanches. Abattez les bombardiers avant le largage.\nÉchec si le port est "
                 "bombardé (constaté par vous : la mission ne le vérifie pas).",
     "elements": [{"name": "Bombardiers", "groups": ["SC-Raid-Mulberry-Bombers"], "scalable": False},
                  {"name": "Escorte", "groups": ["SC-Raid-Mulberry-Escort"], "scalable": True}]},
    {"name": "Escorte-B17", "friendly_name": "Escorte — six B-17G sur les triages de Rouen", "secured": False,
     "briefing": "Six B-17G décollés d'Angleterre vont bombarder la gare de triage de Rouen, par la Manche et la basse "
                 "Seine. Des Fw 190 A-8 et des Bf 109 K-4 les attendent au-dessus de la Seine : escortez-les, de la côte à la "
                 "cible.\nÉchec si un bombardier est abattu (constaté par vous : la mission ne le vérifie pas).",
     "elements": [{"name": "Bombardiers", "groups": ["SC-Escort-B17"], "scalable": False},
                  {"name": "Chasseurs rouges", "groups": ["SC-Escort-B17-Interceptors",
                                                          "SC-Escort-B17-Interceptors-Bf109"], "scalable": True}]},
    {"name": "Interception-Reco", "friendly_name": "Interception — Ju 88 de reconnaissance sur la tête de pont",
     "secured": False,
     "briefing": "Un Ju 88 A-4 de reconnaissance, escorté de deux Bf 109 K-4, survole la tête de pont à 22 000 ft pour "
                 "photographier les plages. Interceptez-le avant qu'il ne rentre : sa route passe au large de Courseulles, "
                 "de Bayeux puis du Cotentin.",
     "elements": [{"name": "Reconnaissance", "groups": ["SC-Recce-Ju88"], "scalable": False},
                  {"name": "Escorte", "groups": ["SC-Recce-Escort"], "scalable": True}]},
]

if __name__ == "__main__":
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    path = Path(M) / "mission.yaml"
    d = yaml.load(path.read_text(encoding="utf-8"))

    if "global_log_level" in d:
        d["global_log_level"] = "info"
    else:
        d.insert(0, "global_log_level", "info")
    mi = d["mission"]
    mi["name"] = "VEAF_OpenTraining_Normandy_ICAO_LFRK"
    mi.yaml_add_eol_comment("LFRK = Caen-Carpiquet, METAR vivant vérifié le 13/10/2026 ; Tangmere (base mère) n'en publie pas", "name")
    mi["era"] = "WW2"
    mi["language"] = "fr"
    mi["silence_atc_on_all_airbases"] = True
    mi["hide_names_from_spawned_groups"] = True
    mi.pop("third_party_mods", None)

    mods = d["modules"]
    mods["SKYNET"] = False
    mods["CTLD"] = False
    mods["CSAR"] = False
    mods["CARRIER"] = False
    mods["SANCTUARY"] = {"enabled": True, "sanctuary_zones": [
        {"name": n, "trigger_zone": z, "coalition": side, "delay_warning": 0, "delay_instant": 60,
         "protect_from_missiles": True} for n, z, c, r, side in SANCTUARIES]}

    d["pipeline"] = {"weather": False, "spawnable_aircrafts": False}
    d.yaml_add_eol_comment("pas de variantes météo (le serveur VEAF fixe météo et heure, David 12/10/2026) ; pas de catalogue d'avions à faire apparaître : il ne contient que des jets (aucun appareil de 1944)", "pipeline")
    d["profiles"] = {"LOCAL_TEST": {"global_log_level": "debug", "security": {"disabled": True},
                                    "mission": {"hide_names_from_spawned_groups": False}}}
    d["combat_missions"] = COMBAT_MISSIONS
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(d, f)
    print("mission.yaml écrit")

    v = ROOT / "src/versions.yaml"
    if v.exists():
        v.unlink()
        print("src/versions.yaml supprimé (pas de variantes)")
