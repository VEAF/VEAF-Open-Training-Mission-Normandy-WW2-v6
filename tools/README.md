# Outils de la mission

Scripts Python qui ont construit la mission et qui produisent ce qu'on ne tape pas à la main : le briefing, les cartes, la mission de test, les contrôles.
Ils importent le code Python de VMCT : par défaut le dépôt voisin `../VEAF-Mission-Creation-Tools` (branche `develop`), ou le dossier désigné par la variable `VMCT_PY` (le dossier `src/python/veaf-tools` d'un autre checkout).
Ils se lancent depuis `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
$PY = (poetry -C ..\..\VEAF-Mission-Creation-Tools env info -p) + "\Scripts\python.exe"
& $PY gather.py
```

Pipeline repris de l'OT Sinaï v6 (lui-même venu du Golfe Persique et des Mariannes), adapté à la Normandie de 1944.

## Construction (historique, à ne pas rejouer)

Chaque `gen_NN_*.py` écrit un lot d'actions `veaf-mission-mcp` dans `batches/`, que `mcp.py batch batches/<lot>.json` exécute dans le processus.
**Un lot ne se rejoue pas** : `add_group` ne dédoublonne pas, un second passage crée des doublons (les dessins F10, eux, sont refusés par nom).
Les lots au sol (06, 07, 07b, 08, 17) ont besoin de la grille d'altitude Normandy (`veaf-tools dcs terrain-sweep Normandy`) : `lib.spot()` et `lib.land()` ramènent chaque position sur la terre ferme et refusent sans elle.

| Script | Lot |
|---|---|
| `plan_mesures.py` | Mesure du front et classement des aérodromes (`airfields_side.json`) |
| `geocode_places.py` | Lieux réels (`places.json`) ; les homonymes hors du théâtre sont remplacés par leurs coordonnées dans `lib.py` |
| `gen_04_bases.py` | Camp des aérodromes, slots dynamiques |
| `gen_06_defense.py` | Défense aérienne permanente (`#veafInterpreter`), radars |
| `gen_07_entrainement.py` | Les 3 familles × 3 niveaux d'entraînement, et les trois zones touristiques |
| `gen_07b_tourisme.py` | Balises radio des circuits (sons morse écrits dans `sons/`) |
| `gen_07c_guide.py` | Guide touristique : bloc Lua de `src/scripts/mission-script.lua` (se rejoue sans doublon) |
| `gen_08_zones.py` | Les 16 vraies zones de combat |
| `gen_09_qra_cap.py`, `gen_09b_qra_piste.py` | QRA et CAP à la demande ; QRA refaites en décollage de la piste (parkings capturés) |
| `gen_10_joueurs.py` | Sanctuaires, arène, groupes des missions scénarisées |
| `gen_11_config.py` | `mission.yaml` : identité, profils, modules, SANCTUARY, `combat_missions:` (se rejoue) |
| `gen_12_presets.py`, `gen_13_waypoints.py`, `gen_14_slots_dynamiques.py` | `src/presets.yaml`, `src/waypoints.yaml`, `src/dynamic-slot-templates.yaml` |
| `gen_15_identite.py`, `gen_16_dessins.py` | Date, météo de base, bullseye, briefing DCS ; dessins F10 |
| `gen_17_convois.py` | Convois recalés sur les routes (`roads.py`, `road_routes.json`), vitesse 40 km/h |
| `inert_targets.py`, `ground_control_roles.py` | Cibles inertes (tir interdit, sans dispersion) ; rôles sans avion à 5 par camp |
| `fix_placement.py`, `probe_scenery.py`, `probe_points.py`, `roads.py`, `dcs.py` | Sondes DCS par le pont dcs-serve (terre, eau, décor, routes) |

## Après tout changement

| Script | Ce qu'il fait |
|---|---|
| `gather.py` | Relève dans la mission tout ce que le briefing affiche → `briefing_data.json` |
| `gen_readme.py` | Écrit `README.md` (le briefing des pilotes) et redessine les cartes par `gen_map.py` |
| `gen_map.py` | Carte générale `docs/carte.jpg` et zooms `docs/cartes/` sur fond OpenStreetMap (tuiles en cache dans `tiles/`), copiés dans `src/mission/l10n/DEFAULT/` et déclarés dans la mission |
| `check_portees.py` | Portée de chaque défense et de chaque zone face à ce qu'elle ne doit pas atteindre → `docs/portees.md` ; ligne `VERDICT` |
| `verify.py` | Contrôles du `.miz` construit (noms, slots, QRA, porteurs, images, météo, sécurité) ; ligne `VERDICT` |
| `make_test_mission.py` | Mission de test locale `bridge/bridge-Normandy-OT.miz` (LOCAL_TEST, game master, P-51D à Tangmere, dcs-bridge) |

Ordre : build serveur (`.\veaf-tools.exe mission build`), `gather.py`, `gen_readme.py`, rebuild serveur (les cartes sont dans le `.miz`), `check_portees.py`, `verify.py`.

Retours sur les outils VMCT : `retours-vmct.md`.
