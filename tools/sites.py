"""Sites partagés par les générateurs : champs d'entraînement, circuits touristiques (positions géographiques réelles).

Aucune grille d'altitude ici : les positions sont de simples conversions lat/lon → x/y DCS.
Entraînement (3 familles x 3 niveaux, adaptées à 1944 : ni hélicoptère, ni SEAD) :
  A — appui rapproché (mitraillage) : bocage du Cotentin à 6 nm à l'ouest d'Azeville et 9 nm de Maupertus, arrière bleu, à 13 nm du front ;
  B — bombardement de précision : plaine de Salisbury (Imber), à 111 nm du front, à 21 nm de Stoney Cross ;
  C — antiflak : fort Tourgis, à Aurigny (rouge), à 32 nm du front et 30 nm de Maupertus.
Tourisme : trois circuits (plages du Débarquement, Cotentin, côte sud de l'Angleterre).
"""
from lib import ll

A = ll(49.50, -1.47)                  # CAS : bocage du Cotentin, à 6 nm à l'ouest d'Azeville
B = ll(51.20, -1.98)                  # bombardement : plaine de Salisbury
C = ll(49.7233, -2.2358)              # antiflak : fort Tourgis, Aurigny

# Circuits touristiques : balise (indicatif, MHz VHF/AM, lieu, sous-titre) ; la balise est posée au lieu indiqué.
T1_CENTER = ll(49.35, -0.62)          # centre de la zone « Plages du Débarquement » (Arromanches)
T1_BEACONS = [
    ("SWD", 130.0, ll(49.2437, -0.2745), "SWD — Sword et Pegasus Bridge"),
    ("GLD", 130.5, ll(49.3400, -0.6200), "GLD — Gold et Arromanches"),
    ("OMA", 131.0, ll(49.3593, -0.8564), "OMA — Omaha et Colleville"),
    ("UTH", 131.5, ll(49.4045, -1.1714), "UTH — Utah et Sainte-Mère-Église"),
]
T2_CENTER = ll(49.62, -1.45)          # Cotentin nord
T2_BEACONS = [
    ("CHB", 133.0, ll(49.6330, -1.6070), "CHB — Cherbourg et le fort du Roule"),
    ("GAT", 133.5, ll(49.6830, -1.2650), "GAT — phare de Gatteville"),
    ("VAA", 134.0, ll(49.5880, -1.2680), "VAA — Saint-Vaast-la-Hougue"),
]
T3_CENTER = ll(50.80, -1.20)          # côte sud de l'Angleterre (Solent)
T3_BEACONS = [
    ("NDL", 135.0, ll(50.6613, -1.5855), "NDL — les Needles"),
    ("POR", 135.5, ll(50.8000, -1.1060), "POR — Portsmouth"),
    ("BCH", 136.0, ll(50.7340, 0.2420), "BCH — Beachy Head"),
    ("DVR", 136.5, ll(51.1280, 1.3230), "DVR — Douvres"),
]
# Monuments du guide : (lat, lon, rayon m, texte) — en plus de l'indicatif de balise
