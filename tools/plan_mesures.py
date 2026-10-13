"""Mesures du front et des aérodromes (plan chiffré). Front du 6 juillet 1944 (approximatif, d'après la tenue des lieux)."""
import json, math, sys
from paths import ROOT  # noqa
from veaf_libs.coordinates import latlon_to_xy, xy_to_latlon
from veaf_mission_mcp.map_tools import list_airfields
sys.stdout.reconfigure(encoding="utf-8")
NM = 1852.0
TH = "Normandy"
FRONT_LL = [(49.37, -1.62), (49.30, -1.52), (49.30, -1.24), (49.22, -1.12), (49.12, -1.08), (49.09, -0.81), (49.10, -0.65),
            (49.18, -0.62), (49.18, -0.46), (49.20, -0.36), (49.28, -0.24), (49.30, -0.10)]
FRONT = [latlon_to_xy(TH, la, lo) for la, lo in FRONT_LL]
def d(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
L = sum(d(FRONT[i], FRONT[i+1]) for i in range(len(FRONT)-1))
print("front", round(L/NM, 1), "nm")
def dist_front(p):
    best = 1e18
    for i in range(len(FRONT)-1):
        a, b = FRONT[i], FRONT[i+1]
        t = max(0, min(1, ((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/max(1, (b[0]-a[0])**2+(b[1]-a[1])**2)))
        best = min(best, d(p, (a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1]))))
    return best
afs = list_airfields(theatre=TH)["airfields"]
for a in afs: a["p"] = (a["x"], a["y"])
xs = [a["x"] for a in afs]; ys = [a["y"] for a in afs]
print("airfields", len(afs), "x", min(xs), max(xs), "y", min(ys), max(ys))
for n in ["Tangmere", "Carpiquet", "Lessay", "Azeville", "Bazenville", "Beny-sur-Mer", "Evreux", "Abbeville Drucat", "Biggin Hill", "Manston", "Cretteville", "Maupertus"]:
    a = next(x for x in afs if x["name"] == n)
    print(n, "dist front", round(dist_front(a["p"])/NM, 1), "nm", "lat", round(a["lat"], 3), "lon", round(a["lon"], 3))
# classement géographique : Angleterre (lat > 50.5 ou ile de Wight) ; Normandie bleue = au nord de la ligne du front ; reste rouge
def side(a):
    lat, lon = a["lat"], a["lon"]
    if a["name"] in ("Meautis", "Cretteville"): return "BLUE"
    if lat >= 50.5 and lon < 1.6: return "BLUE"
    if lat >= 50.5: return "RED"
    if a["name"] in ("Jersey", "Guernsey", "Alderney"): return "RED"
    if lon > -0.15: return "RED"
    # point au nord de la ligne du front -> bleu
    px = a["p"]
    # signe du côté : on compare avec la latitude interpolée du front à la même longitude
    for i in range(len(FRONT_LL)-1):
        (la1, lo1), (la2, lo2) = FRONT_LL[i], FRONT_LL[i+1]
        if min(lo1, lo2) <= lon <= max(lo1, lo2) and lo1 != lo2:
            lat_f = la1 + (la2-la1)*(lon-lo1)/(lo2-lo1)
            return "BLUE" if lat >= lat_f else "RED"
    return "BLUE" if lat >= 49.3 else "RED"
for a in afs: a["side"] = side(a); a["df"] = dist_front(a["p"])/NM
for s in ("BLUE", "RED"):
    xs = sorted([a for a in afs if a["side"] == s], key=lambda a: a["df"])
    print(s, len(xs))
    print("; ".join(f'{a["name"]} {a["df"]:.0f}' for a in xs))
json.dump([{k: v for k, v in a.items() if k != "p"} for a in afs], open("airfields_side.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
