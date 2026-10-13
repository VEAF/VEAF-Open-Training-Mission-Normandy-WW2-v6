"""Outils communs aux générateurs de lots (tools/gen_*.py), OT Normandie WW2.

Un générateur écrit un fichier de lot dans tools/batches/ ; `python tools/mcp.py batch <lot>` l'exécute sur le
catalogue d'actions de veaf-mission-mcp (code VMCT de develop). Un lot ne s'exécute qu'une fois.

Scénario : 6 juillet 1944 (D+30, date de la v5). Le bleu tient l'Angleterre du sud et la tête de pont normande, de
Cherbourg (tombé le 26-29 juin) à l'Orne ; le rouge tient le reste de la France, les îles Anglo-Normandes et le front
du Cotentin à Caen. Front tracé à l'estime d'après la tenue des lieux (Carentan, Saint-Lô, Caumont, Tilly,
Carpiquet, Orne) : approximatif, et dit tel dans le briefing.

Terre / mer : la grille d'altitude Normandy balayée dans DCS (`veaf-tools dcs terrain-sweep Normandy`) ; tant qu'elle
manque, `ground()` refuse et aucun placement au sol ne se génère.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT  # noqa: E402  (met aussi le code VMCT sur sys.path)
from veaf_libs.coordinates import latlon_to_xy, xy_to_latlon  # noqa: E402
from veaf_libs.terrain_elevation import grid_for_theatre  # noqa: E402

M = ROOT.as_posix()
THEATRE = "Normandy"

BLUE_US = dict(coalition="blue", country_id=2, country_name="USA")
BLUE_UK = dict(coalition="blue", country_id=4, country_name="UK")
BLUE_CA = dict(coalition="blue", country_id=8, country_name="Canada")
BLUE = BLUE_US
RED = dict(coalition="red", country_id=66, country_name="Third Reich")

_AF = json.loads((ROOT / "tools/airfields_side.json").read_text(encoding="utf-8"))
AIRFIELDS = {a["name"]: (a["x"], a["y"]) for a in _AF}
BLUE_ALL = [a["name"] for a in _AF if a["side"] == "BLUE"]
RED_ALL = [a["name"] for a in _AF if a["side"] == "RED"]

# Slots dynamiques bleus (11) : Tangmere (base mère), Stoney Cross, Biggin Hill, Manston (Angleterre, arrière) ;
# Maupertus (Cherbourg), Longues-sur-Mer, Deux Jumeaux, Azeville (milieu) ; Picauville, Bazenville, Beny-sur-Mer
# (avancées). Rouges (4) : Carpiquet (centre du front), Lessay (front ouest), Évreux (profondeur), Abbeville (nord).
BLUE_SLOTS = ["Tangmere", "Stoney Cross", "Biggin Hill", "Manston", "Maupertus", "Longues-sur-Mer", "Deux Jumeaux",
              "Azeville", "Picauville", "Bazenville", "Beny-sur-Mer"]
RED_SLOTS = ["Carpiquet", "Lessay", "Evreux", "Abbeville Drucat"]
BLUE_NO_SLOTS = [n for n in BLUE_ALL if n not in BLUE_SLOTS]
RED_NO_SLOTS = [n for n in RED_ALL if n not in RED_SLOTS]
MOTHER = "Tangmere"

# Front du 6 juillet 1944 (lat, lon) : de la côte ouest du Cotentin à l'embouchure de l'Orne
FRONT_LL = [(49.36, -1.64), (49.29, -1.53), (49.25, -1.30), (49.22, -1.15), (49.12, -1.09), (49.09, -0.81),
            (49.10, -0.65), (49.18, -0.62), (49.18, -0.46), (49.20, -0.36), (49.28, -0.24), (49.30, -0.10)]
FRONT = [tuple(round(c) for c in latlon_to_xy(THEATRE, la, lo)) for la, lo in FRONT_LL]

_GEO = json.loads((ROOT / "tools/places.json").read_text(encoding="utf-8"))
PLACES = {k: (v["x"], v["y"]) for k, v in _GEO.items()}
# Géocodage tombé sur un homonyme : coordonnées géographiques réelles
for _n, (_la, _lo) in {"Omaha Beach": (49.3722, -0.8767), "Gold Beach": (49.3400, -0.6200),
                       "Juno Beach": (49.3350, -0.4600)}.items():
    PLACES[_n] = tuple(round(c) for c in latlon_to_xy(THEATRE, _la, _lo))

# Bullseye commun : Saint-Lô, ville que les deux camps nomment, au milieu du front (ni zone ni base dessus)
BULLSEYE = PLACES["Saint-Lô"]


def nm(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1852


def km(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1000


def off(p, brg, m):
    """Point à `m` mètres de `p`, au relèvement `brg` (degrés vrais, x = nord, y = est)."""
    r = math.radians(brg)
    return (p[0] + m * math.cos(r), p[1] + m * math.sin(r))


def bearing(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def bullseye(p):
    """« 123°/45 nm » depuis le bullseye : cap = atan2(Δy, Δx)."""
    return f"{bearing(BULLSEYE, p):03.0f}°/{nm(BULLSEYE, p):.0f} nm"


def xy(p):
    return {"x": round(p[0]), "y": round(p[1])}


def ll(lat, lon):
    """Point DCS (x, y) d'une position géographique."""
    return tuple(round(c) for c in latlon_to_xy(THEATRE, lat, lon))


_GRID = None


def ground(x, y):
    global _GRID
    if _GRID is None:
        _GRID = grid_for_theatre(THEATRE)
        if _GRID is None:
            raise SystemExit("pas de grille d'altitude Normandy (veaf-tools dcs terrain-sweep Normandy)")
    return _GRID.elevation_at(x, y)


def _ring(p, r, n=12):
    return [p] + [(p[0] + r * math.cos(2 * math.pi * i / n), p[1] + r * math.sin(2 * math.pi * i / n))
                  for i in range(n)]


def is_land(p, margin=300):
    """Terre ferme : le point et un cercle de `margin` m autour sont au-dessus de 0 m (la mer vaut 0)."""
    return all((ground(*q) or 0) > 0 for q in _ring(p, margin))


def is_sea(p, margin=1000):
    return all((ground(*q) or 0) <= 0 for q in _ring(p, margin, 16))


def land(p, what, margin=300):
    if not is_land(p, margin):
        raise SystemExit(f"PAS SUR LA TERRE FERME (marge {margin} m) : {what} {p}")
    return p


def sea(p, what, margin=1500):
    if not is_sea(p, margin):
        raise SystemExit(f"PAS EN PLEINE MER (marge {margin} m) : {what} {p}")
    return p


def nearest_land(x, y, margin=300, step=100, max_r=6000):
    """Le point à terre le plus proche de (x, y), à `margin` m au moins de l'eau (anneaux croissants)."""
    if is_land((x, y), margin):
        return (x, y)
    r = step
    while r <= max_r:
        n = max(8, int(2 * math.pi * r / step))
        for i in range(n):
            a = 2 * math.pi * i / n
            p = (x + r * math.cos(a), y + r * math.sin(a))
            if is_land(p, margin):
                return (round(p[0]), round(p[1]))
        r += step
    return None


def spot(center, brg, dist, what, margin=150):
    """Point à `dist` m de `center` au relèvement `brg`, ramené sur la terre ferme la plus proche."""
    p = off(center, brg, dist)
    q = nearest_land(p[0], p[1], margin=margin)
    if q is None:
        raise SystemExit(f"pas de terre près de {what} {p}")
    return q


class Batch:
    def __init__(self):
        self.items = []

    def act(self, action, **params):
        self.items.append({"name": action, "params": {"mission_path": M, **params}})

    def save(self, name):
        path = ROOT / "tools/batches" / name
        if path.exists():
            raise SystemExit(f"{path.name} existe déjà : un lot ne se régénère pas après exécution (doublons)")
        path.write_text(json.dumps(self.items, indent=1, ensure_ascii=False), encoding="utf-8")
        print(len(self.items), "actions ->", path.relative_to(ROOT))


def cmd_unit(alias_cmd, carrier_type, tag, extra=""):
    """Faux porteur de zone : `#command="<alias ...>"` + balises de tirage + suffixe unique."""
    name = f'#command="{alias_cmd}"'
    if extra:
        name += " " + extra
    return {"type": carrier_type, "name": f"{name} #{tag}"}


def interp_unit(alias_cmd, carrier_type, tag):
    """Porteur permanent : `#veafInterpreter["<alias ...>"]` + suffixe unique."""
    return {"type": carrier_type, "name": f'#veafInterpreter["{alias_cmd}"] #{tag}'}


def seg_nm(p, a, b):
    """Distance (nm) du point p au segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy) / 1852


def dist_front_nm(p):
    return min(seg_nm(p, FRONT[i], FRONT[i + 1]) for i in range(len(FRONT) - 1))


def ddm(p):
    """« N49°11.051' W000°45.729' » (degrés, minutes décimales : ce que saisissent la plupart des avions)."""
    lat, lon = xy_to_latlon(THEATRE, *p)

    def one(v, pos, neg, w):
        h = pos if v >= 0 else neg
        v = abs(v)
        d = int(v)
        return f"{h}{d:0{w}d}°{(v - d) * 60:06.3f}'"
    return f"{one(lat, 'N', 'S', 2)} {one(lon, 'E', 'W', 3)}"


def position_text(p):
    return f"Position : bullseye {bullseye(p)} ({ddm(p)})."
