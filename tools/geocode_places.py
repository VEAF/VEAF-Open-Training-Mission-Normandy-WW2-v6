"""Géocode une fois les lieux réels dont la mission a besoin → tools/places.json (x/y DCS).

Relancer ajoute seulement les lieux absents. Chaque point est à relire : l'outil peut tomber sur un
homonyme (osm_type et nom affiché sont gardés pour ça).
"""
import json
import sys

from paths import ROOT  # noqa: F401  (met aussi le code VMCT sur sys.path)
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
PLACES = [
    # Tourisme : plages du Débarquement, Cotentin, Londres
    "Pointe du Hoc", "Omaha Beach", "Utah Beach", "Arromanches-les-Bains", "Pegasus Bridge", "Sainte-Mère-Église",
    "Batterie de Longues-sur-Mer", "Courseulles-sur-Mer", "Ouistreham", "Batterie de Merville", "Vierville-sur-Mer",
    "Normandy American Cemetery and Memorial", "Saint-Vaast-la-Hougue", "Phare de Gatteville", "Cherbourg-en-Cotentin",
    "Fort du Roule", "Mont-Saint-Michel", "Carentan", "Cap de la Hague", "Bayeux",
    "Tower Bridge", "Palace of Westminster", "St Paul's Cathedral", "London Eye", "Windsor Castle", "Stonehenge",
    "Dover Castle", "Beachy Head", "Portsmouth Historic Dockyard", "The Needles",
    # Front et profondeur
    "Villers-Bocage, Calvados", "Tilly-sur-Seulles", "Caen", "Caumont-l'Éventé", "Saint-Lô", "La Haye-du-Puits",
    "Falaise, Calvados", "Argentan", "Lisieux", "Vire Normandie", "Flers, Orne", "Mortain", "Avranches", "Coutances",
    "Évreux", "Rouen", "Elbeuf", "Le Havre", "Cap d'Antifer", "Étretat", "Fécamp", "Dieppe", "Honfleur",
    "Cap Gris-Nez", "Blockhaus d'Éperlecques", "Fort Tourgis", "Alderney", "La Roche-Guyon", "Mézidon-Canon",
    "Pont-l'Évêque, Calvados", "Dives-sur-Mer", "Saint-Valery-en-Caux", "Siracourt", "Mimoyecques",
    "Thury-Harcourt", "Vimoutiers", "Bernay, Eure", "Les Andelys", "Vernon, Eure",
]
out_path = ROOT / "tools" / "places.json"
places = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
cat = ActionCatalog()
register_default_actions(cat)
for q in PLACES:
    if q in places:
        continue
    try:
        r = cat.run_action("geocode", {"mission_path": str(ROOT), "query": q})
    except Exception as e:  # noqa: BLE001
        print("ERREUR", q, e)
        continue
    if not r.get("found"):
        print("INTROUVABLE", q)
        continue
    places[q] = {"x": round(r["xy"]["x"]), "y": round(r["xy"]["y"]), "osm": r.get("osm_type"), "name": r["display_name"][:90]}
    print(f"{q:28} {places[q]['x']:>8} {places[q]['y']:>8}  {places[q]['osm']:<14} {places[q]['name']}")
    out_path.write_text(json.dumps(places, indent=1, ensure_ascii=False), encoding="utf-8")
