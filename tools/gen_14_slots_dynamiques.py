"""Écrit src/dynamic-slot-templates.yaml : le catalogue livré (published/ de la release installée), réduit aux appareils de
1944 de chaque camp.

Bleu : P-47D-30, P-47D-40, P-51D, P-51D-30, Spitfire LF Mk IX, Mosquito FB VI. Rouge : Bf 109 K-4, Fw 190 A-8, Fw 190 D-9.
Retirés : tout le reste (jets, Corsair, TF-51D biplace d'après-guerre, I-16 et La-7 soviétiques) et les hélicoptères (aucun
n'existe en 1944). Aucun mod : les neuf appareils sont des modules officiels de DCS.
"""
import yaml

from lib import M
from paths import ROOT

SRC = ROOT / "published/src/defaults/mission-folder/src/dynamic-slot-templates.yaml"
KEEP = {"blue": {"P-47D-30", "P-47D-40", "P-51D", "P-51D-30-NA", "SpitfireLFMkIX", "MosquitoFBMkVI"},
        "red": {"Bf-109K-4", "FW-190A8", "FW-190D9"}}
if __name__ == "__main__":
    d = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    kept = dropped = 0
    for fam in ("airplanes", "helicopters"):
        for side, cs in d[fam]["coalitions"].items():
            for c, gs in cs.items():
                for n in list(gs):
                    u = gs[n]["units"][1] if isinstance(gs[n]["units"], dict) else gs[n]["units"][0]
                    if fam == "airplanes" and u["type"] in KEEP[side]:
                        kept += 1
                    else:
                        del gs[n]
                        dropped += 1
    HEADER = """# Open Training Normandie WW2 (6 juillet 1944) : catalogue livré par veaf-tools 6.29.0, réduit par
# tools/gen_14_slots_dynamiques.py aux appareils de 1944 de chaque camp (bleu : P-47D, P-51D, Spitfire LF IX, Mosquito ;
# rouge : Bf 109 K-4, Fw 190 A-8 et D-9), sans hélicoptère. Ce fichier n'est donc plus vide : le catalogue livré n'est plus
# lu, une mise à jour de veaf-tools n'y ajoute rien.
"""
    with open(M + "/src/dynamic-slot-templates.yaml", "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False, width=200)
    print(kept, "modèles gardés,", dropped, "retirés")
