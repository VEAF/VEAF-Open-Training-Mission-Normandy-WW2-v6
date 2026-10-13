"""Relève dans la mission tout ce que les cartes et les briefings affichent → tools/briefing_data.json.

Sources : mission.yaml (zones, QRA, sanctuaires, missions scénarisées), src/mission/mission (positions, routes, dessins F10
dont la ligne de front), src/mission/warehouses (camps et slots des aérodromes), src/presets.yaml (plan radio). Rien n'est
tapé à la main ici : relancer après tout changement de la mission.
"""
import json
import math

import yaml
from paths import ROOT, TOOLS  # noqa: F401  (met aussi VMCT sur sys.path)
from veaf_libs import coordinates as C
from veaf_mission_mcp.map_tools import list_airfields
from veaf_mission_mcp.mission_folder import load_folder_mission

NM = 1852.0
THEATRE = "Normandy"


def seq(t):
    """Une table Lua lue en Python : liste, ou dict à clés entières."""
    if t is None:
        return []
    if isinstance(t, list):
        return t
    return [t[k] for k in sorted(t, key=lambda k: int(k))]


def ddm(x, y):
    lat, lon = C.xy_to_latlon(THEATRE, x, y)

    def one(v, p, n, w):
        h = p if v >= 0 else n
        minutes = round(abs(v) * 60, 3)  # arrondi avant de séparer : jamais « 60.000' »
        d = int(minutes // 60)
        return f"{h}{d:0{w}d}°{minutes - d * 60:06.3f}'"
    return f"{one(lat, 'N', 'S', 2)} {one(lon, 'E', 'W', 3)}"


mission_obj = load_folder_mission(ROOT)
M = mission_obj.mission_content["mission"] if "mission" in mission_obj.mission_content else mission_obj.mission_content
WH = mission_obj.warehouses_content
Y = yaml.safe_load(open(ROOT / "mission.yaml", encoding="utf-8"))
MOD = Y["modules"]
BULL = {"x": M["coalition"]["blue"]["bullseye"]["x"], "y": M["coalition"]["blue"]["bullseye"]["y"]}


def be(x, y):
    """Relèvement vrai (quadrillage DCS : x nord, y est) et distance DEPUIS le bullseye."""
    dx, dy = x - BULL["x"], y - BULL["y"]
    if math.hypot(dx, dy) < NM:
        return "sur le bullseye"
    return f"{round((math.degrees(math.atan2(dy, dx)) + 360) % 360) % 360:03d}°/{round(math.hypot(dx, dy) / NM)} nm"


groups = []
for side, coal in M["coalition"].items():
    for country in seq(coal.get("country")):
        for cat in ("plane", "helicopter", "vehicle", "ship", "static"):
            for g in seq((country.get(cat) or {}).get("group")):
                groups.append((side, country["name"], cat, g))
units_by_name = {u["name"]: (side, u) for side, _, _, g in groups for u in seq(g["units"])}
by_name = {g["name"]: (side, country, cat, g) for side, country, cat, g in groups}

# ── aérodromes avec slots ────────────────────────────────────────────────────────────────
afs = {a["id"]: a for a in list_airfields(theatre=THEATRE)["airfields"]}
bases = []
for aid, w in (WH.get("airports") or {}).items():
    coal = str(w.get("coalition", "")).lower()
    if coal not in ("blue", "red") or not w.get("dynamicSpawn"):
        continue
    a = afs[int(aid)]
    bases.append({"name": a["name"], "side": coal, "x": round(a["x"]), "y": round(a["y"]), "be": be(a["x"], a["y"]),
                  "ddm": ddm(a["x"], a["y"])})
bases.sort(key=lambda b: (b["side"], b["name"]))

# ── CAP ──────────────────────────────────────────────────────────────────────────────────
caps = []
for side, _, cat, g in groups:
    if cat == "plane" and g["name"].startswith("OnDemand-"):
        pts = seq(g["route"]["points"])
        caps.append({"name": g["name"][len("OnDemand-"):], "side": side, "type": seq(g["units"])[0]["type"],
                     "a": {"x": pts[0]["x"], "y": pts[0]["y"]}, "b": {"x": pts[-1]["x"], "y": pts[-1]["y"]}})

# ── zones de trigger ─────────────────────────────────────────────────────────────────────
tz = {z["name"]: z for z in seq(M["triggers"]["zones"])}
zones = []
for z in MOD["COMBATZONE"]["combat_zones"]:
    t = tz[z["zone_name"]]
    zones.append({"key": z["zone_name"], "name": z.get("friendly_name", z["zone_name"]), "training": bool(z.get("training")),
                  "menu": z.get("radio_group_name"), "x": round(t["x"]), "y": round(t["y"]), "radius_nm": t["radius"] / NM,
                  "be": be(t["x"], t["y"]), "ddm": ddm(t["x"], t["y"]),
                  "briefing": z["briefing"].split("\nPosition :")[0],
                  "near": z["briefing"].split("Base amie la plus proche : ")[1].strip() if "Base amie la plus proche" in z["briefing"] else ""})

qra = []
for q in MOD["QRA"]["definitions"]:
    t = tz[q["trigger_zone"]]
    tiers = [{"n": tr["enemy_count"], "pick": tr.get("random_pick", 1),
              "types": [f"{len(seq(by_name[gname][3]['units']))} × {seq(by_name[gname][3]['units'])[0]['type']}" for gname in tr["groups"]]}
             for tr in q.get("groups_by_enemy_count") or []]
    qra.append({"name": q["name"], "side": q["coalition"].lower(), "x": round(t["x"]), "y": round(t["y"]),
                "radius_nm": round(t["radius"] / NM), "airport": q.get("airport_link"), "tiers": tiers,
                "ddm": ddm(t["x"], t["y"]), "be": be(t["x"], t["y"]), "delay": q.get("delay_before_activating", 0),
                "helos": bool(q.get("react_on_helicopters"))})

sanct = []
for s in MOD["SANCTUARY"]["sanctuary_zones"]:
    t = tz[s["trigger_zone"]]
    sanct.append({"name": s["name"], "side": s["coalition"].lower(), "x": t["x"], "y": t["y"],
                  "radius_nm": t["radius"] / NM, "radius_km": t["radius"] / 1000})

# ── dessins F10 : ligne de front, arène ──────────────────────────────────────────────────
front, arena = [], None
for layer in seq(M["drawings"]["layers"]):
    for o in seq(layer.get("objects")):
        if o["name"] == "Front":
            front.append([{"x": o["mapX"] + p["x"], "y": o["mapY"] + p["y"]} for p in seq(o["points"])])
        if o["name"] == "Arène cercle":
            arena = {"x": o["mapX"], "y": o["mapY"], "radius_nm": round(o["radius"] / NM), "be": be(o["mapX"], o["mapY"]),
                     "ddm": ddm(o["mapX"], o["mapY"])}
fronts_nm = [round(sum(math.hypot(a["x"] - b["x"], a["y"] - b["y"]) for a, b in zip(line, line[1:])) / NM) for line in front]

# ── défense aérienne permanente ──────────────────────────────────────────────────────────
ad = []
for side, country, cat, g in groups:
    u0 = seq(g["units"])[0]
    if "#veafInterpreter" in u0["name"]:
        alias = u0["name"].split('["', 1)[1].split(",")[0]
        ad.append({"name": g["name"].replace("AD ", ""), "side": side, "alias": alias, "x": u0["x"], "y": u0["y"]})
    elif u0["type"] in ("FuMG-401", "FuSe-65", "Allies_Director") and not g["name"].startswith("combatZone_"):
        ad.append({"name": g["name"], "side": side, "alias": "radar " + ", ".join(sorted({u["type"] for u in seq(g["units"])})),
                   "x": u0["x"], "y": u0["y"]})
for a in ad:
    a["ddm"], a["be"] = ddm(a["x"], a["y"]), be(a["x"], a["y"])

arena_slots = [{"group": g["name"], "side": side, "type": seq(g["units"])[0]["type"], "n": len(seq(g["units"])),
                "fl": round(seq(g["units"])[0]["alt"] / 0.3048 / 100)}
               for side, country, cat, g in groups if cat == "plane" and g["name"].startswith("Arène")]

# plan radio et canaux de base (src/presets.yaml)
P = yaml.safe_load(open(ROOT / "src" / "presets.yaml", encoding="utf-8"))
channels = {k: v["freqs"] for coll in P["channels_collection"].values() for k, v in coll.items()}
titles = {k: v.get("title", k) for coll in P["channels_collection"].values() for k, v in coll.items()}
radio = {side: {role: {int(n): (c["channel"] if isinstance(c, dict) else c) for n, c in lst.items()}
                for role, lst in roles.items()} for side, roles in P["channel_lists"].items()}
fw_channels = {int(k): v for k, v in P["radios_collection"]["red_radios"]["radio_fug16"]["channels"].items()}
for b in bases:
    b.update(channels.get(f"Base-{b['name']}", {}))

W = M["weather"]
weather = {"temperature": W["season"]["temperature"], "wind_from": (W["wind"]["atGround"]["dir"] + 180) % 360,
           "wind_ms": W["wind"]["atGround"]["speed"], "visibility_km": min(W["visibility"]["distance"], 10000) / 1000,
           "sky": f"quelques nuages à {round(W['clouds']['base'] / 0.3048, -2):,.0f} ft".replace(",", " ")}

# ── tourisme : balises (gen_07b_tourisme.py) à leur position dans la mission ─────────────
from gen_07b_tourisme import BEACONS  # noqa: E402

_pos = {}
for _side, _co in M["coalition"].items():
    for _c in seq(_co.get("country")):
        for _g in seq((_c.get("vehicle") or {}).get("group")):
            _pos[_g["name"]] = (_g["x"], _g["y"])
beacons = [{"code": code, "site": sub.split(" — ")[1], "mhz": mhz, "ddm": ddm(*_pos[f"Balise {code}"]),
            "be": be(*_pos[f"Balise {code}"]), "x": _pos[f"Balise {code}"][0], "y": _pos[f"Balise {code}"][1]}
           for code, mhz, p, sub, side in BEACONS if f"Balise {code}" in _pos]

D = {"name": Y["mission"]["name"], "date": M["date"], "start": M["start_time"],
     "bullseye": {**BULL, "ddm": ddm(BULL["x"], BULL["y"])}, "bases": bases, "farps": [], "support": [], "caps": caps,
     "carriers": [], "zones": zones, "qra": qra, "sanctuaries": sanct, "front": front, "arena_zone": arena, "ad": ad,
     "drones": [], "arena_slots": arena_slots, "radio": radio, "channels": channels, "titles": titles,
     "fw_channels": fw_channels, "weather": weather, "beacons": beacons, "fronts_nm": fronts_nm,
     "cap_missions": [{"name": c["group_name"], "menu": c.get("menu_name", c["group_name"]), "briefing": c.get("briefing", "")}
                      for c in Y.get("cap_missions") or []],
     "combat_missions": [{"name": c["friendly_name"], "briefing": c["briefing"]} for c in Y.get("combat_missions") or []]}
for c in caps:
    g = by_name["OnDemand-" + c["name"]][3]
    u0 = seq(g["units"])[0]
    cm = next(x for x in Y.get("cap_missions") or [] if x["group_name"] == c["name"])
    c.update(n=len(seq(g["units"])), fl=round(u0["alt"] / 0.3048 / 100), menu=cm.get("menu_name", c["name"]),
             briefing=cm.get("briefing", ""),
             mid_be=be((c["a"]["x"] + c["b"]["x"]) / 2, (c["a"]["y"] + c["b"]["y"]) / 2))
json.dump(D, open(TOOLS / "briefing_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"bases {len(bases)}, CAP {len(caps)}, zones {len(zones)}, QRA {len(qra)}, sanctuaires {len(sanct)}, front {len(front)} "
      f"({fronts_nm} nm), arène {'oui' if arena else 'NON'}, balises {len(beacons)}")
