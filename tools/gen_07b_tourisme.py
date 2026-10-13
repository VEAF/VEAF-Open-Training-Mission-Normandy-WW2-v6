"""Lot 07b : balises radio des trois circuits touristiques — sons fabriqués ici, émission VHF/AM en boucle.

Chaque balise répète son indicatif en morse (SWD, GLD, OMA, UTH, CHB, GAT, VAA, NDL, POR, BCH, DVR) sur une tonalité de
800 Hz : des fichiers WAV écrits par ce script dans tools/sons/ (aucun son emprunté), embarqués par add_sound. Fréquences
VHF 130.0-136.5, hors de la bande des tours (118.0-123.0, 132.45, 134.8) ; les appareils de 1944 n'ont qu'une radio VHF/AM.
Les balises sont permanentes : leur nom ne commence pas par celui d'une zone touristique, qui ne les capture donc pas.
Le guide (messages au survol des monuments) est du Lua dans src/scripts/mission-script.lua (gen_07c_guide.py).
"""
import math
import struct
import wave

import sites as S
from lib import BLUE_UK, BLUE_US, ROOT, Batch, spot, xy

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "G": "--.", "H": "....", "L": ".-..", "M": "--", "N": "-.",
         "O": "---", "P": ".--.", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--"}
RATE, TONE, DOT = 8000, 800, 0.1


def morse_wav(code, path):
    """Écrit l'indicatif `code` en morse (point 100 ms, trait 300 ms), suivi de 2 s de silence."""
    samples = []

    def tone(t):
        n = int(RATE * t)
        for i in range(n):
            env = min(1.0, i / 40, (n - i) / 40)   # attaque et relâche de 5 ms : pas de clic
            samples.append(int(12000 * env * math.sin(2 * math.pi * TONE * i / RATE)))

    def silence(t):
        samples.extend([0] * int(RATE * t))

    for letter in code:
        for sym in MORSE[letter]:
            tone(DOT if sym == "." else 3 * DOT)
            silence(DOT)
        silence(2 * DOT)
    silence(2.0)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    return len(samples) / RATE


BEACONS = ([(*b, BLUE_US) for b in S.T1_BEACONS] + [(*b, BLUE_US) for b in S.T2_BEACONS]
           + [(*b, BLUE_UK) for b in S.T3_BEACONS])   # indicatif, MHz, position, sous-titre, camp

if __name__ == "__main__":
    sons = ROOT / "tools/sons"
    sons.mkdir(exist_ok=True)
    b = Batch()
    for code, mhz, pos, sub, side in BEACONS:
        name = f"Balise {code}"
        wav = sons / f"balise-{code}.wav"
        dur = morse_wav(code, wav)
        p = spot(pos, 0, 0, name, margin=40)
        b.act("add_sound", sound_path=wav.as_posix())
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p),
              units=[{"type": "Willys_MB", "name": name}], keep_position=True)
        b.act("edit_route", group_name=name, operation="add_task", index=1, task="set_frequency",
              task_params={"frequency_mhz": mhz, "modulation": "AM"})
        b.act("edit_route", group_name=name, operation="add_task", index=1, task="transmit_message",
              task_params={"sound": wav.name, "loop": True, "duration_s": math.ceil(dur), "subtitle": sub})
        print(f"{name:12} {mhz} AM  {dur:.1f} s  {round(p[0])} {round(p[1])}")
    b.save("07b-tourisme.json")
