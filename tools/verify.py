"""Contrôles du .miz construit (section 8 du prompt Open Training), lus avec le lecteur de VMCT, jamais par texte.

Usage (depuis tools/, Python de l'environnement poetry de VMCT) : python verify.py [fichier.miz ...]
Sans argument : le .miz de base le plus récent. Finit sur une ligne VERDICT.
"""
import collections
import glob
import os
import re
import sys
import zipfile

import yaml

sys.stdout.reconfigure(encoding="utf-8")
from lib import BLUE_SLOTS, RED_SLOTS  # noqa: E402
from mission_tools.miz_tools import read_miz  # noqa: E402
from paths import ROOT, VMCT_PY  # noqa: E402
from veaf_mission_mcp.map_tools import list_airfields  # noqa: E402

SPECS = yaml.safe_load((VMCT_PY / "presets_injector" / "data" / "dcs-radio-specs.yaml").read_text(encoding="utf-8"))
UNITS_DB = yaml.safe_load(open(VMCT_PY / "veaf_libs" / "data" / "veaf-units.yaml", encoding="utf-8"))
AF = {a["id"]: a for a in list_airfields(theatre="Normandy")["airfields"]}
WANTED_SLOTS = {"blue": set(BLUE_SLOTS), "red": set(RED_SLOTS)}
EXPECTED = {"zones": 28, "QRA": 5, "CAP": 6, "sanctuaires": 2}   # mission.yaml : 9 entraînement + 3 tourisme + 16 réelles
FAILS = []
SHAPE_REQUIRED = {".Command Center", ".Ammunition depot"}


def fail(msg):
    FAILS.append(msg)
    print("  ÉCHEC :", msg)


def seq(v):
    if v is None:
        return []
    if isinstance(v, dict):
        return [v[k] for k in sorted(v, key=lambda k: int(k))]
    return list(v)


def groups(m):
    for side, co in m["coalition"].items():
        for c in seq(co.get("country")):
            for cat in ("plane", "helicopter", "vehicle", "ship", "static"):
                for g in seq((c.get(cat) or {}).get("group")):
                    yield side, c.get("name"), cat, g


ALIAS_TYPES = {}
for _g in UNITS_DB["groups"]:
    _types = {(u["type"] if isinstance(u, dict) else u) for u in _g.get("units") or []}
    for _a in _g.get("aliases", []):
        ALIAS_TYPES[_a.lower()] = _types
# alias de commande → groupe(s) que VEAF génère ; les alias dynamiques (-aaa, -samSR, -samLR, -samVLR, -armor) tirent des
# groupes `generateAirDefenseGroup-<CAMP>-WW2-<n>` : on vérifie que le porteur est du type d'une pièce de ces groupes
DYN = {"-aaa": (1, 2), "-samSR": (2, 3), "-samLR": (4, 5), "-samVLR": (5, 5)}


def dyn_types(alias, side):
    lo, hi = DYN[alias]
    s = "BLUE" if side == "blue" else "RED"
    out = set()
    for n in range(lo - 1, hi + 2):   # tirage ±1
        out |= ALIAS_TYPES.get(f"generateairdefensegroup-{s.lower()}-ww2-{max(0, min(5, n))}", set())
    return out


def check(path):
    print(f"\n===== {os.path.basename(path)}")
    miz = read_miz(path)
    m = miz.mission_content
    m = m.get("mission", m)
    gnames, unames, gid, uid = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    interp = []
    n_air = 0
    for side, country, cat, g in groups(m):
        gnames[g["name"]] += 1
        gid[g["groupId"]] += 1
        for u in seq(g["units"]):
            unames[u["name"]] += 1
            uid[u["unitId"]] += 1
            if cat in ("plane", "helicopter") and not g.get("dynSpawnTemplate"):
                n_air += 1
                p0 = (seq(g["route"]["points"]) or [{}])[0]
                grounded = p0.get("linkUnit") or p0.get("airdromeId") or str(p0.get("type", "")).startswith("TakeOff")
                if (u.get("alt") or 0) <= 0 and not grounded:
                    fail(f"altitude <= 0 : {g['name']}")
                if not (u.get("payload") or {}).get("fuel"):
                    fail(f"sans carburant : {g['name']}")
                spec = (SPECS.get(u["type"]) or {}).get("radios")
                if spec and not any(r_["min_mhz"] <= (g.get("frequency") or 0) <= r_["max_mhz"] for r0 in spec for r_ in r0["ranges"]):
                    fail(f"fréquence de groupe hors plage de la radio : {g['name']} {g.get('frequency')} MHz ({u['type']})")
                if not (u.get("payload") or {}).get("gun"):
                    fail(f"sans munitions de canon : {g['name']}")
                for pyl in seq((u.get("payload") or {}).get("pylons")):
                    if "'" in str(pyl.get("CLSID", "")):
                        fail(f"CLSID mal formé dans {g['name']} : {pyl.get('CLSID')}")
                if u["type"] in ("Ju-88A4", "B-17G") and g["name"].startswith("SC-") and g["name"] != "SC-Recce-Ju88" \
                        and not (u.get("payload") or {}).get("pylons"):
                    fail(f"bombardier sans bombes : {g['name']}")
            if cat == "static" and not u.get("category"):
                fail(f"statique sans category : {g['name']}")
            if cat == "static" and not u.get("shape_name") and u["type"] in SHAPE_REQUIRED:
                fail(f"statique sans shape_name : {g['name']} ({u['type']})")
            if "#veafInterpreter" in u["name"]:
                interp.append((side, g, u))
        if g["name"].startswith("QRA-") and seq(seq(g["route"]["points"])[0].get("task", {}).get("params", {}).get("tasks")):
            fail(f"QRA avec une tâche sur son point : {g['name']}")
        if g["name"].startswith("QRA-") and not g.get("lateActivation"):
            fail(f"QRA sans activation différée : {g['name']}")
        if g["name"].startswith("QRA-"):
            t0 = str((seq(g["route"]["points"]) or [{}])[0].get("type", ""))
            if not t0.startswith("TakeOff"):
                fail(f"QRA qui ne décolle pas de la piste : {g['name']} ({t0})")
        if "-Convoi" in g["name"] and "Cotier" not in g["name"]:
            acts = [p.get("action") for p in seq(g["route"]["points"])]
            if any(a != "On Road" for a in acts):
                fail(f"convoi hors route (un point au moins) : {g['name']} {acts}")
    dups = [n for n, c in gnames.items() if c > 1] + [n for n, c in unames.items() if c > 1]
    print(f"  groupes {sum(gnames.values())}, unités {sum(unames.values())}, avions non-slot {n_air} ; doublons de nom "
          f"{dups[:5]} ; doublons d'id {sum(1 for c in gid.values() if c > 1)} / {sum(1 for c in uid.values() if c > 1)}")
    if dups or any(c > 1 for c in gid.values()) or any(c > 1 for c in uid.values()):
        fail("noms ou identifiants en double")

    dyn = collections.defaultdict(set)
    for k, a in (miz.warehouses_content.get("airports") or {}).items():
        if isinstance(a, dict) and a.get("dynamicSpawn"):
            dyn[str(a.get("coalition", "")).lower()].add(AF[int(k)]["name"])
    for side in ("blue", "red"):
        if dyn[side] != WANTED_SLOTS[side]:
            fail(f"slots dynamiques {side} : en trop {sorted(dyn[side] - WANTED_SLOTS[side])}, manquants "
                 f"{sorted(WANTED_SLOTS[side] - dyn[side])}")
    print(f"  slots dynamiques : bleu {len(dyn['blue'])}, rouge {len(dyn['red'])}, autres {sorted(k for k in dyn if k not in ('blue', 'red'))}")

    # porteurs #veafInterpreter : du type d'une pièce que génère l'alias
    for side, g, u in interp:
        alias = re.search(r'#veafInterpreter\["(-[\w]+)', u["name"]).group(1)
        if alias in DYN and u["type"] not in dyn_types(alias, side):
            fail(f"porteur {g['name']} : {u['type']} n'est pas une pièce que génère {alias} ({side})")
    print(f"  #veafInterpreter : {len(interp)} porteurs")

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        cfg = next((n for n in names if n.endswith("veaf-config.lua")), None)
        txt = z.read(cfg).decode("utf-8") if cfg else ""
        pics = [n for n in names if n.startswith("l10n/DEFAULT/carte") and n.endswith(".jpg")]
    counts = {k: len(re.findall(p, txt)) for k, p in {"zones": r"veafCombatZone\.AddZone", "QRA": r"VeafQRA:new\(\)",
                                                       "CAP": r"addCapMission\(",
                                                       "sanctuaires": r"VeafSanctuaryZone:new\(\)|addZoneFromTriggerZone\("}.items()}
    sec = [ln.strip() for ln in txt.splitlines() if "SecurityDisabled" in ln][:1]
    lvl = [ln.strip() for ln in txt.splitlines() if "ForcedLogLevel" in ln][:1]
    print(f"  veaf-config.lua : {counts} ; sécurité {sec} ; log {lvl}")
    for k, v in EXPECTED.items():
        if counts[k] != v:
            fail(f"veaf-config.lua : {counts[k]} {k}, {v} attendus")
    test = "bridge" in os.path.basename(path) or "LOCAL_TEST" in os.path.basename(path)
    disabled = any("= true" in s for s in sec)
    if disabled != test:
        fail(f"sécurité {'coupée' if disabled else 'active'} dans un build {'de test' if test else 'serveur'}")
    if m.get("requiredModules"):
        fail(f"requiredModules non vide : {m['requiredModules']}")
    pb, pn, pr = seq(m.get("pictureFileNameB")), seq(m.get("pictureFileNameN")), seq(m.get("pictureFileNameR"))
    print(f"  images : {len(pics)} dans le .miz, B {len(pb)}, N {len(pn)}, R {len(pr)}")
    if pr or len(pb) != len(pics) or pb != pn:
        fail("images de briefing mal listées")
    w = m["weather"]
    st = m.get("start_time", 0)
    print(f"  météo : clouds {w.get('clouds')}, température {w.get('season', {}).get('temperature')}, vent au sol "
          f"{w.get('wind', {}).get('atGround')}, départ {st // 3600:02d}:{st % 3600 // 60:02d}, date {m.get('date')}")
    c = w.get("clouds", {})
    if c.get("density", 0) > 0 and (c.get("base") or 0) < 300:
        fail(f"nuages au sol : base {c.get('base')} m")
    return {}


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        base = glob.glob(str(ROOT / "VEAF_OpenTraining_Normandy_ICAO_LFRK_2*.miz"))
        paths = [max(base, key=os.path.getmtime)] if base else []
    for p in paths:
        check(p)
    print(f"\nVERDICT : {'OK' if not FAILS else f'{len(FAILS)} échec(s)'}")
