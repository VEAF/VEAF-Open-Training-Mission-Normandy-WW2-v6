"""Lot 16 : dessins F10 (add_map_drawing, pour qu'ils survivent au build).

Chaque zone a son contour à son rayon réel ET son étiquette ; ligne de front, sanctuaires, QRA, arène, circuits
touristiques. Étiquettes sur fond clair opaque (sans fond, l'action met du noir à moitié transparent et le texte sombre
devient illisible, Caucase 29/09/2026). Pas de trait en tirets : add_map_drawing n'écrit que du plein (VMCT
FIX-OPEN-TRAINING-CAUCASUS-FINDINGS ticket 03).
Couches : Common pour ce que les deux camps partagent (front, zones, sanctuaires, QRA, arène, circuits). Adapté de l'OT Sinaï.
"""
import gen_07_entrainement as e
import gen_08_zones as z
import sites as S
from gen_09_qra_cap import QRAS
from gen_10_joueurs import ARENA, SANCTUARIES
from lib import FRONT, Batch, xy

LABEL_BG = "0xffffffe0"
RED, BLUE, ORANGE, GREEN, MAGENTA, BROWN = "0xcc0000ff", "0x0040ccff", "0xe07000ff", "0x008000ff", "0xb000b0ff", "0x8b5a00ff"


def above(c, r, gap=800):
    return (c[0] + r + gap, c[1])


b = Batch()


def circle(layer, name, c, r, color, fill="0x00000000", thickness=3):
    b.act("add_map_drawing", layer=layer, shape="circle", name=name, position=xy(c), radius=r, color=color,
          fill_color=fill, thickness=thickness)


def label(layer, name, p, text, color, size=12):
    b.act("add_map_drawing", layer=layer, shape="textbox", name=name, position=xy(p), text=text, color=color,
          fill_color=LABEL_BG, font_size=size)


def build():
    b.act("add_map_drawing", layer="Common", shape="line", name="Front", points=[xy(q) for q in FRONT], color=RED,
          thickness=6)
    label("Common", "Front étiquette", (FRONT[len(FRONT) // 2][0] + 8000, FRONT[len(FRONT) // 2][1] - 14000),
          "FRONT du 6 juillet 1944 (approximatif)", RED, 14)

    # ── zones d'entraînement : un cercle et une étiquette par famille (niveaux imbriqués sur le même cercle) ──
    for zone, c, r, fname, *_ in e.zones():
        if not zone.endswith("_Easy"):
            continue
        fam = fname.split()[0][0]
        text = {"A": "A1-A3 Entraînement appui rapproché — bocage", "B": "B1-B3 Entraînement bombardement — Salisbury",
                "C": "C1-C3 Entraînement antiflak — Aurigny"}[fam]
        circle("Common", f"Zone {zone[:-5]}", c, r, ORANGE, "0xe0700018")
        label("Common", f"Zone {zone[:-5]} étiquette", above(c, r), text, ORANGE)

    # ── tourisme : les trois zones, les balises et les circuits ──
    for i, (zname, (title, c, r, side), beacons) in enumerate(e.TOUR, 1):
        circle("Common", f"Zone {zname}", c, r, BROWN, "0x8b5a0018")
        label("Common", f"Zone {zname} étiquette", above(c, r), f"T{i} Tourisme — {title}", BROWN)
        b.act("add_map_drawing", layer="Common", shape="line", name=f"Circuit T{i}",
              points=[xy(p) for code, mhz, p, sub in beacons], color=BROWN, thickness=2)
        for code, mhz, p, sub in beacons:
            label("Common", f"Balise {code} étiquette", (p[0] + 2500, p[1]), f"{code} VHF {mhz:.1f}", BROWN, 10)

    # ── vraies zones de combat ──
    for zone, c, r, fname, *_ in z.zones():
        circle("Common", f"Zone {zone}", c, r, RED, "0xcc000018")
        label("Common", f"Zone {zone} étiquette", above(c, r), fname, RED, 11)

    # ── QRA ──
    for q in QRAS:
        col = MAGENTA if q["side"]["coalition"] == "red" else BLUE
        circle("Common", f"QRA {q['name']}", q["center"], q["radius"], col, thickness=2)
        label("Common", f"QRA {q['name']} étiquette", (q["center"][0] + q["radius"] - 4000, q["center"][1]),
              f"{q['name']} ({round(q['radius'] / 1852)} nm)", col, 11)

    # ── sanctuaires ──
    for name, tz, c, r, side in SANCTUARIES:
        circle("Common", name, c, r, GREEN, "0x00800018", thickness=2)
        label("Common", f"{name} étiquette", (c[0] - r - 1500, c[1]), name, GREEN, 10)

    # ── arène ──
    circle("Common", "Arène cercle", ARENA[0], ARENA[1], GREEN, thickness=3)
    label("Common", "Arène étiquette", above(ARENA[0], ARENA[1], 3000), "ARÈNE joueurs contre joueurs (slots en vol)",
          GREEN, 14)


if __name__ == "__main__":
    build()
    b.save("16-dessins.json")
