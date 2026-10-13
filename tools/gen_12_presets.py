"""Écrit src/presets.yaml (plan radio de la Normandie 1944), puis les canaux de base par set_airfield_channels.

Tous les appareils de 1944 (P-47, P-51, Spitfire, Mosquito, Bf 109, Fw 190) n'ont qu'une radio VHF/AM : ils lisent
`primary_2`, le rôle « radio unique des warbirds ». Les canaux ne portent donc que leur fréquence VHF.
Bande des tours (describe_airfield_channels, 13/10/2026) : VHF 118.0-123.0 (une tour tous les 50 kHz, plus 132.45 et
134.8), UHF 250.0-254.4 et FM 38.4-42.4 (inutilisés ici). Tout le reste est hors de cette bande : Guard 121.5 (dans la
bande, mais c'est Guard), arène 125.0, balises touristiques VHF 130.0-137.0.
Une radio tient 20 canaux : bleu = Guard, l'arène et les 11 bases bleues ; rouge = Guard, l'arène et 17 bases rouges.
Pas de FM ni d'UHF : aucun appareil de l'époque n'en a.
"""
import yaml

yaml.SafeDumper.ignore_aliases = lambda *a: True   # pas d'ancres YAML : chaque camp écrit sa liste

from lib import M, BLUE_SLOTS, RED_SLOTS
from mcp import cat

TACTICAL = [
    ("Guard", "Guard", {"uhf": 243, "vhf": 121.5}),
    ("Arene", "Arène — combat entre joueurs", {"vhf": 125.0}),
]
RED_MORE = ["Triqueville", "Rouen-Boos", "Beaumont-le-Roger", "Argentan", "Flers", "Saint-Omer Wizernes",
            "Fecamp-Benouville", "Deauville", "Beauvais-Tille", "Creil", "Cormeilles-en-Vexin", "Ronai", "Vrigny"]
BLUE_BASES = BLUE_SLOTS
RED_BASES = RED_SLOTS + RED_MORE


def _fw_channels():
    """Fréquences FM (38.4-42.4 MHz) des bases rouges, dans l'ordre de la liste rouge : ce que lit un Fw 190."""
    import json
    from lib import ROOT
    t = (ROOT / "tools/airfield_channels.json").read_text(encoding="utf-8")
    fm = {a["name"]: a["freqs"]["fm"] for a in json.loads(t[t.index("{"):])["candidates"]}
    return {i: fm[n] for i, n in enumerate(RED_BASES[:20], 1)}


def numbered(items):
    return {i: v for i, v in enumerate(items, 1)}


guard_vhf = {"title": "Guard/VHF", "channel": "Guard"}
FW_CHANNELS = _fw_channels()


def bases(names):
    return ["Base-" + b for b in names]


doc = {
    "channel_lists": {
        "blue": {"primary_2": numbered([guard_vhf, "Arene", *bases(BLUE_BASES)])},
        "red": {"primary_2": numbered([guard_vhf, "Arene", *bases(RED_BASES)[:18]])},
    },
    # Le Fw 190 n'accorde que 38.4-42.4 MHz (FuG 16 Z) : ses préréglages sont les fréquences FM des bases rouges.
    "presets_assignments": {"blue": {"helicopter": {"all": "none"}}, "red": {"helicopter": {"all": "none"},
                                                                              "plane": {"FW-190A8": "ww2_red_fug16",
                                                                                        "FW-190D9": "ww2_red_fug16"}}},
    "radios_collection": {"red_radios": {"radio_fug16": {"title": "FuG 16 Z", "type": "fm", "channels": FW_CHANNELS}}},
    "presets_collection": {"red_presets": {"ww2_red_fug16": {"title": "Red coalition - FuG 16 Z (Fw 190)",
                                                              "radios": {"radio_1": "radio_fug16"}}}},
    "channels_collection": {
        "tactical": {k: {"title": t, "freqs": f} for k, t, f in TACTICAL},
        "bases": {},
    },
}
HEADER = """# Plan radio de l'Open Training Normandie WW2 — écrit par tools/gen_12_presets.py, ne pas éditer à la main.
# Tous les appareils de 1944 n'ont qu'une radio VHF/AM (rôle primary_2). Hors bande des tours (VHF 118.0-123.0, 132.45,
# 134.8) : arène 125.0, balises touristiques VHF 130.0-137.0 (voir README). Guard 121.5.
# Les canaux d'aérodromes (collection `bases`) viennent de set_airfield_channels : fréquences DCS.
"""

if __name__ == "__main__":
    for side in ("blue", "red"):
        for name, lst in doc["channel_lists"][side].items():
            assert len(lst) <= 20, (side, name, len(lst))
    path = M + "/src/presets.yaml"
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=200)
    print(cat.run_action("set_airfield_channels", {"mission_path": M, "airfields": sorted(set(BLUE_BASES + RED_BASES))}))
