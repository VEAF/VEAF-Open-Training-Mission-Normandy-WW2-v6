"""Lot 04 : camp de chaque aérodrome et slots dynamiques.

Bleu avec slots (11) : Tangmere (base mère), Stoney Cross, Biggin Hill, Manston en Angleterre (arrière) ; Maupertus,
Longues-sur-Mer, Deux Jumeaux, Azeville (milieu) ; Picauville, Bazenville, Beny-sur-Mer (avancées).
Bleu sans slots : les autres terrains d'Angleterre du sud et de la tête de pont. Rouge avec slots : Carpiquet (centre du
front), Lessay (front ouest), Évreux (profondeur), Abbeville Drucat (nord) ; les autres terrains rouges sans slots.
Aucun aérodrome neutre : tout le théâtre est tenu par l'un des deux camps (îles Anglo-Normandes rouges).
Pas de FARP : aucun hélicoptère n'existe en 1944.
"""
from lib import BLUE_NO_SLOTS, BLUE_SLOTS, RED_NO_SLOTS, RED_SLOTS, Batch

if __name__ == "__main__":
    b = Batch()
    for n in BLUE_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue")
    for n in BLUE_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue", dynamic_spawn=False)
    for n in RED_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red")
    for n in RED_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red", dynamic_spawn=False)
    b.save("04-bases.json")
