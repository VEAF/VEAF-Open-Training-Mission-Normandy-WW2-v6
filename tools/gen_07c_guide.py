"""Écrit le guide touristique de la Normandie dans src/scripts/mission-script.lua (bloc entre deux marqueurs, réécrit
à chaque passage : ce script se rejoue sans doublon).

Toutes les 2 s, le guide regarde les appareils des joueurs des deux camps ; quand l'un passe à moins de 1 500 ft
sol et à moins du rayon d'un monument, son groupe reçoit le texte du monument (une fois par appareil et par
monument, puis à nouveau après 10 min). Positions : coordonnées géographiques réelles (lat, lon).
Textes : connaissances générales, chiffres arrondis (articles Wikipédia en français des lieux) — à relire.
"""
from lib import M, ll

# (lat, lon, rayon m, texte). Coordonnées géographiques réelles, converties en x/y DCS.
# Textes : connaissances générales, chiffres arrondis ou omis quand ils sont discutés — à relire.
MONUMENTS = [
    # ── Circuit 1 : plages du Débarquement, de l'est à l'ouest ──
    (49.2437, -0.2745, 400,
     "Pegasus Bridge, à Bénouville, sur le canal de Caen à la mer. Dans la nuit du 5 au 6 juin 1944, des planeurs de la "
     "6e division aéroportée britannique s'y posent à quelques mètres du pont et le prennent par surprise : c'est l'un "
     "des tout premiers actes du Jour J. L'emblème de la division, Pégase, a donné son nom au pont."),
    (49.3335, -0.4590, 700,
     "Courseulles-sur-Mer, plage de Juno. Le 6 juin 1944, la 3e division d'infanterie canadienne y débarque : c'est le "
     "secteur canadien du Jour J, entre Gold à l'ouest et Sword à l'est."),
    (49.3400, -0.6220, 900,
     "Arromanches-les-Bains, plage de Gold. Après le Jour J, les Alliés y assemblent un port artificiel, Mulberry B, "
     "dont les caissons de béton, les Phoenix, sont encore visibles en mer. Sans port en eau profonde, il fallait "
     "faire passer troupes et ravitaillement par les plages."),
    (49.3417, -0.6942, 400,
     "Batterie de Longues-sur-Mer. Quatre canons de 150 mm sous casemates, face à la mer, qui menaçaient les plages "
     "de Gold et d'Omaha. Les canons sont toujours dans leurs casemates d'origine."),
    (49.3593, -0.8564, 600,
     "Cimetière américain de Colleville-sur-Mer, au-dessus d'Omaha Beach. Le 6 juin 1944, les 1re et 29e divisions "
     "d'infanterie américaines y subissent les plus lourdes pertes de la journée. Plus de 9 000 soldats américains "
     "reposent ici."),
    (49.3961, -0.9886, 500,
     "Pointe du Hoc. Le 6 juin 1944, les Rangers de Rudder escaladent ses falaises d'une trentaine de mètres pour "
     "détruire une batterie qui menaçait Utah et Omaha. Les cratères des bombardements navals et aériens marquent "
     "encore le sol."),
    (49.4045, -1.1714, 700,
     "Utah Beach. Le 6 juin 1944, la 4e division d'infanterie américaine y débarque, un peu au sud de l'endroit prévu "
     "à cause du courant, et rencontre une résistance bien plus faible qu'à Omaha."),
    (49.4082, -1.3171, 400,
     "Sainte-Mère-Église, l'une des premières communes libérées, dans la nuit du 5 au 6 juin 1944, par les 82e et 101e "
     "divisions aéroportées américaines. Le parachutiste John Steele y est resté accroché au clocher de l'église ; un "
     "mannequin y rappelle l'épisode."),
    # ── Circuit 2 : Cotentin ──
    (49.6329, -1.6075, 600,
     "Fort du Roule, sur la colline qui domine Cherbourg : un fort du XIXe siècle équipé de blockhaus par la "
     "Wehrmacht. Cherbourg, grand port de la Manche, est pris par les Américains à la fin de juin 1944. Le fort abrite "
     "aujourd'hui le musée de la Libération."),
    (49.6828, -1.2656, 500,
     "Phare de Gatteville, à la pointe de Barfleur : 75 m de haut, bâti entre 1829 et 1835, l'un des plus hauts "
     "phares de France. Il est monté par 365 marches."),
    (49.5878, -1.2686, 800,
     "Saint-Vaast-la-Hougue, port ostréicole. Ses tours de la Hougue et de Tatihou, dessinées par Vauban, sont "
     "classées au patrimoine mondial de l'UNESCO depuis 2008. En 1692, la flotte française y fut détruite à la "
     "bataille de la Hougue."),
    (49.7167, -1.9417, 800,
     "Cap de la Hague, la pointe nord-ouest du Cotentin, face à Aurigny. Le raz Blanchard, tout proche, est l'un "
     "des courants de marée les plus puissants d'Europe."),
    # ── Circuit 3 : côte sud de l'Angleterre ──
    (50.6613, -1.5855, 500,
     "Les Needles, trois piliers de craie à l'extrémité ouest de l'île de Wight, surmontés d'un phare construit en "
     "1859. Une ancienne batterie de défense côtière du XIXe siècle domine la falaise."),
    (50.8000, -1.1060, 1200,
     "Portsmouth, grande base de la Royal Navy. Son chantier historique garde le HMS Victory, le navire amiral de "
     "Nelson à Trafalgar en 1805, et le Mary Rose, navire de Henri VIII coulé en 1545 et renfloué en 1982. En 1944, "
     "le Solent est l'un des grands points de rassemblement de la flotte du Débarquement."),
    (50.7340, 0.2420, 800,
     "Beachy Head, falaise de craie de 162 m au bout des Seven Sisters, la plus haute falaise de craie de "
     "Grande-Bretagne. Son phare rouge et blanc date de 1902 et se dresse au pied de la falaise."),
    (51.1280, 1.3230, 1000,
     "Douvres. Le château de Douvres, la « clé de l'Angleterre », abrite dans ses tunnels le quartier général "
     "de l'opération Dynamo, l'évacuation de Dunkerque en 1940. En 1944, la région sert à une grande opération de "
     "déception : une armée fantôme, le FUSAG, y est censée préparer un débarquement dans le Pas-de-Calais."),
    (51.1789, -1.8262, 400,
     "Stonehenge, cercle de pierres dressées de la plaine de Salisbury, commencé il y a environ 5 000 ans. La plaine "
     "est aussi, en 1944, un vaste terrain d'entraînement de l'armée britannique."),
    # ── Hors circuit : en territoire rouge au 6 juillet 1944 ──
    (48.6360, -1.5110, 900,
     "Le Mont-Saint-Michel, îlot de granit surmonté d'une abbaye dont la première église remonte à 708. Ses marées "
     "comptent parmi les plus fortes d'Europe. Au 6 juillet 1944, vous le survolez en territoire rouge : il ne sera libéré que plus tard dans l'été."),
]

BEGIN = "-- >>> guide touristique de la Normandie (écrit par tools/gen_07c_guide.py, ne pas éditer à la main)"
END = "-- <<< guide touristique de la Normandie"


def lua_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def block():
    rows = []
    for lat, lon, r, text in MONUMENTS:
        x, y = ll(lat, lon)
        rows.append(f"    {{ x = {x}, z = {y}, r = {r}, text = {lua_str(text)} }},")
    return "\n".join([
        BEGIN,
        "do",
        "  veafTourGuide = { seen = {} }",
        "  veafTourGuide.monuments = {",
        *rows,
        "  }",
        "  veafTourGuide.maxAgl = 457      -- 1 500 ft",
        "  veafTourGuide.repeatAfter = 600 -- s",
        "  function veafTourGuide.check()",
        "    local now = timer.getTime()",
        "    for _, side in pairs({ coalition.side.BLUE, coalition.side.RED }) do",
        "      for _, unit in pairs(coalition.getPlayers(side) or {}) do",
        "        if unit and unit:isExist() and unit:inAir() then",
        "          local p = unit:getPoint()",
        "          local agl = p.y - land.getHeight({ x = p.x, y = p.z })",
        "          if agl < veafTourGuide.maxAgl then",
        "            for i, m in ipairs(veafTourGuide.monuments) do",
        "              local dx, dz = p.x - m.x, p.z - m.z",
        "              if dx * dx + dz * dz < m.r * m.r then",
        "                local key = unit:getName() .. '#' .. i",
        "                local last = veafTourGuide.seen[key]",
        "                if not last or now - last > veafTourGuide.repeatAfter then",
        "                  veafTourGuide.seen[key] = now",
        "                  trigger.action.outTextForGroup(unit:getGroup():getID(), m.text, 25)",
        "                end",
        "              end",
        "            end",
        "          end",
        "        end",
        "      end",
        "    end",
        "    return now + 2",
        "  end",
        "  timer.scheduleFunction(function(_, t) local ok, nxt = pcall(veafTourGuide.check) "
        "if ok then return nxt end env.error('veafTourGuide: ' .. tostring(nxt)) return t + 10 end, nil, "
        "timer.getTime() + 10)",
        "end",
        END,
    ])


if __name__ == "__main__":
    path = f"{M}/src/scripts/mission-script.lua"
    t = open(path, encoding="utf-8").read()
    if BEGIN in t:
        t = t[:t.index(BEGIN)] + t[t.index(END) + len(END):].lstrip("\n")
    t = t.rstrip("\n") + "\n\n" + block() + "\n"
    open(path, "w", encoding="utf-8").write(t)
    print(len(MONUMENTS), "monuments écrits dans", path)
