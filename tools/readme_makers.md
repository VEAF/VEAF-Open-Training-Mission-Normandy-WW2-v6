## Pour les créateurs de mission

Ce dossier est une mission VEAF Mission Creation Tools v6 (`veaf-tools` 6.29.0). Sa source est `mission.yaml` et `src/` ; le `.miz` se construit, il ne s'édite pas.

Ce qui change par rapport à la v5 : l'époque (WW2, 6 juillet 1944), les camps (la tête de pont et l'Angleterre du sud bleues face à la France occupée rouge), des slots dynamiques sur 11 bases bleues et 4 rouges, seize vraies zones de combat, neuf zones d'entraînement adaptées à 1944, trois circuits touristiques, toutes les batteries posées par alias VEAF (`#veafInterpreter`), pas de variantes météo (le serveur VEAF fixe météo et heure). Ni Skynet, ni CTLD, ni CSAR, ni porte-avions, ni ravitailleur, ni AWACS : rien de tout cela n'existe en 1944.

### Construire

```powershell
.\veaf-tools.exe mission build                       # le .miz du serveur : sécurité active, logs info
.\veaf-tools.exe mission build --profile LOCAL_TEST  # sécurité coupée, logs debug, noms de groupes lisibles
```

### Fichiers

| Chemin | Rôle |
|---|---|
| `mission.yaml` | Identité, modules, zones de combat, QRA, CAP, sanctuaires, scénarios, profils |
| `src/mission/` | La mission DCS éclatée (groupes, zones de déclenchement, aérodromes, dessins F10, briefing, sons des balises) |
| `src/scripts/mission-script.lua` | Le guide touristique (messages au survol), écrit par `tools/gen_07c_guide.py` |
| `src/presets.yaml` | Plan radio (VHF pour tous, FM pour le Fw 190), canaux de base posés par `set_airfield_channels` |
| `src/dynamic-slot-templates.yaml` | Modèles de slots dynamiques : les neuf appareils de 1944 |
| `src/waypoints.yaml` | Plans de vol des groupes joueurs (champs, circuits, arène) |
| `tools/` | Les scripts qui ont construit la mission et qui produisent le briefing, les cartes et les contrôles (`tools/README.md`) |
| `docs/` | Carte générale, zooms, tableau des portées |

### Régénérer ce document

```powershell
$PY = (poetry -C ..\VEAF-Mission-Creation-Tools env info -p) + "\Scripts\python.exe"
cd tools
& $PY gather.py        # relève la mission → briefing_data.json
& $PY gen_readme.py    # écrit README.md et redessine les cartes
```

Les cartes sont dans le `.miz` : reconstruire après avoir régénéré.

### Limites connues

- Le front est tracé à l'estime, pas relevé d'une source : il est dit approximatif partout.
- Les chasseurs de 1944 n'ont pas d'emport nommé par DCS : QRA, CAP et arène volent aux canons (le canon est chargé). Les emports des bombardiers (Ju 88 A-4, B-17G) viennent de la base d'unités de l'installation DCS.
- Les modèles rouges de slots dynamiques livrés avec veaf-tools portent `gun: 0` : à confirmer en jeu que les Bf 109 et Fw 190 de slot ont bien leurs canons.
- Les dessins F10 et la présence des monuments touristiques dans le décor DCS ne se voient qu'en jeu.
- Le pack « WWII Armour and Technics » (flak, blindés, B-17G, Ju 88) n'est pas exigé (`requiredModules` reste vide) : un joueur qui ne l'a pas charge la mission sans voir ces unités.
