# Retours pour VMCT — construction de l'OT Normandie WW2 v6 (13/10/2026)

Tenu au fil de la construction (prompt `new-open-training-mission.fr.md`, veaf-tools 6.29.0 installé par `scaffold_mission`, actions MCP sur VMCT `develop`).
Les constats sont écrits en tickets dans le dépôt VMCT : `.backlog/FIX-OPEN-TRAINING-NORMANDY-FINDINGS/` (15 tickets, anglais, format du backlog).

| # | Constat | Ticket |
|---|---|---|
| 1 | `list_payloads` ne connaît aucun avion de module WW2 ni les bombardiers IA (Ju 88 A-4, B-17G) ; les emports sont dans `CoreMods/*/UnitPayloads` et `db.Units.lua` | 01 |
| 2 | Avertissement « no weapons » faux pour un chasseur à canons ; `loadout_from` refuse un template sans pylône | 02 |
| 3 | Le catalogue `spawnables.yaml` livré injecte 51 jets modernes dans une mission WW2 | 03 |
| 4 | Tables WW2 de `veafCasMission` : infanterie moderne, Bradley | 04 |
| 5 | `list_shortcuts` sans époque ; pas d'alias WW2 pour Freya, Würzburg, artillerie | 05 |
| 6 | Le Fw 190 n'accorde que 38.4-42.4 MHz : pas de rôle de radio pour lui | 06 |
| 7 | Les templates rouges de slots dynamiques WW2 portent `gun: 0` (à mesurer en jeu) | 07 |
| 8 | Parkings Normandy capturés mais non livrés ; `capture-map --parking` n'écrit pas le format lu | 08 |
| 9 | `terrain-sweep` attend sans fin un `dcs-serve` mort et réécrit la clé d'une mission déjà ouverte | 09 |
| 10 | `describe_known_limitations` : 74 000 caractères, dépasse le résultat d'outil | 10 |
| 11 | `theatre-bounds.yaml` ne couvre que 4 théâtres : « Omaha Beach » géocodé en Iowa sans avertissement | 11 |
| 12 | Le prompt suppose un théâtre moderne (ravitailleurs, AWACS, hélicoptères, SAM) | 12 |
| 13 | `add_air_group` écrit 251 MHz sur tous les groupes : l'éditeur refuse d'enregistrer un groupe de joueurs P-51D ou Fw 190 (vu par David, 13/10) | 13 |
| 14 | Un alias `country germany` dans une mission Third Reich : Germany n'est dans aucun camp, le spawn est neutre et s'arrête sur `networkName nil`, les zones perdent leurs unités sans erreur de build (sonde en jeu) | 14 |
| 15 | Un convoi natif d'une zone roule à 5,1 m/s (10 nœuds) quelle que soit la vitesse de sa route (11,1 m/s écrit), mesuré en jeu ; la DCA de 1944 a une vitesse max de 0 et freine un convoi | 15, 04 |

Rappels, déjà signalés par les OT précédentes : `create_combat_zone` écrit 20 km/h et un premier point « Off Road » sur les routes de convoi (recalé ici par `tools/gen_17_convois.py`) ; la grille d'altitude n'est pas livrée ; `inject-bridge` attend « Entrée » même lancé par un script.
Pas VMCT : `land.findPathOnRoads` ne trouve aucune route depuis Vire (le réseau routier de la carte y est isolé) ; le convoi prévu est devenu Coutances – La Haye-du-Puits.
