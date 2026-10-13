-- mission-script.lua
-- Mission-specific Lua code that cannot be generated from mission.yaml.
--
-- This file is loaded AFTER veaf-config.lua (which is generated automatically
-- from mission.yaml by the veaf-tools build command).
--
-- Put here:
--   - Custom shortcuts / aliases  (VeafAlias:new():...)
--   - Custom Lua helper functions
--   - Third-party script setup (CTLD, CSAR, …) that requires Lua code
--
-- Do NOT put here:
--   - Module initialization calls  → use mission.yaml (modules:)
--   - Mission identity             → use mission.yaml (mission:)
--   - QRA definitions              → use mission.yaml (modules.QRA)
--   - Combat/CAP missions          → use mission.yaml (combat_missions: / cap_missions:)
--   - Assets lists                 → use mission.yaml (modules.ASSETS.assets)

-- >>> guide touristique de la Normandie (écrit par tools/gen_07c_guide.py, ne pas éditer à la main)
do
  veafTourGuide = { seen = {} }
  veafTourGuide.monuments = {
    { x = -26691, z = 2839, r = 400, text = "Pegasus Bridge, à Bénouville, sur le canal de Caen à la mer. Dans la nuit du 5 au 6 juin 1944, des planeurs de la 6e division aéroportée britannique s'y posent à quelques mètres du pont et le prennent par surprise : c'est l'un des tout premiers actes du Jour J. L'emblème de la division, Pégase, a donné son nom au pont." },
    { x = -17177, z = -10924, r = 700, text = "Courseulles-sur-Mer, plage de Juno. Le 6 juin 1944, la 3e division d'infanterie canadienne y débarque : c'est le secteur canadien du Jour J, entre Gold à l'ouest et Sword à l'est." },
    { x = -16840, z = -22788, r = 900, text = "Arromanches-les-Bains, plage de Gold. Après le Jour J, les Alliés y assemblent un port artificiel, Mulberry B, dont les caissons de béton, les Phoenix, sont encore visibles en mer. Sans port en eau profonde, il fallait faire passer troupes et ravitaillement par les plages." },
    { x = -16814, z = -28037, r = 400, text = "Batterie de Longues-sur-Mer. Quatre canons de 150 mm sous casemates, face à la mer, qui menaçaient les plages de Gold et d'Omaha. Les canons sont toujours dans leurs casemates d'origine." },
    { x = -15204, z = -39874, r = 600, text = "Cimetière américain de Colleville-sur-Mer, au-dessus d'Omaha Beach. Le 6 juin 1944, les 1re et 29e divisions d'infanterie américaines y subissent les plus lourdes pertes de la journée. Plus de 9 000 soldats américains reposent ici." },
    { x = -11378, z = -49582, r = 500, text = "Pointe du Hoc. Le 6 juin 1944, les Rangers de Rudder escaladent ses falaises d'une trentaine de mètres pour détruire une batterie qui menaçait Utah et Omaha. Les cratères des bombardements navals et aériens marquent encore le sol." },
    { x = -10782, z = -62867, r = 700, text = "Utah Beach. Le 6 juin 1944, la 4e division d'infanterie américaine y débarque, un peu au sud de l'endroit prévu à cause du courant, et rencontre une résistance bien plus faible qu'à Omaha." },
    { x = -10616, z = -73446, r = 400, text = "Sainte-Mère-Église, l'une des premières communes libérées, dans la nuit du 5 au 6 juin 1944, par les 82e et 101e divisions aéroportées américaines. Le parachutiste John Steele y est resté accroché au clocher de l'église ; un mannequin y rappelle l'épisode." },
    { x = 13934, z = -94973, r = 600, text = "Fort du Roule, sur la colline qui domine Cherbourg : un fort du XIXe siècle équipé de blockhaus par la Wehrmacht. Cherbourg, grand port de la Manche, est pris par les Américains à la fin de juin 1944. Le fort abrite aujourd'hui le musée de la Libération." },
    { x = 19995, z = -70414, r = 500, text = "Phare de Gatteville, à la pointe de Barfleur : 75 m de haut, bâti entre 1829 et 1835, l'un des plus hauts phares de France. Il est monté par 365 marches." },
    { x = 9429, z = -70387, r = 800, text = "Saint-Vaast-la-Hougue, port ostréicole. Ses tours de la Hougue et de Tatihou, dessinées par Vauban, sont classées au patrimoine mondial de l'UNESCO depuis 2008. En 1692, la flotte française y fut détruite à la bataille de la Hougue." },
    { x = 22857, z = -119237, r = 800, text = "Cap de la Hague, la pointe nord-ouest du Cotentin, face à Aurigny. Le raz Blanchard, tout proche, est l'un des courants de marée les plus puissants d'Europe." },
    { x = 128303, z = -95552, r = 500, text = "Les Needles, trois piliers de craie à l'extrémité ouest de l'île de Wight, surmontés d'un phare construit en 1859. Une ancienne batterie de défense côtière du XIXe siècle domine la falaise." },
    { x = 144481, z = -62059, r = 1200, text = "Portsmouth, grande base de la Royal Navy. Son chantier historique garde le HMS Victory, le navire amiral de Nelson à Trafalgar en 1805, et le Mary Rose, navire de Henri VIII coulé en 1545 et renfloué en 1982. En 1944, le Solent est l'un des grands points de rassemblement de la flotte du Débarquement." },
    { x = 140446, z = 33238, r = 800, text = "Beachy Head, falaise de craie de 162 m au bout des Seven Sisters, la plus haute falaise de craie de Grande-Bretagne. Son phare rouge et blanc date de 1902 et se dresse au pied de la falaise." },
    { x = 188137, z = 106921, r = 1000, text = "Douvres. Le château de Douvres, la « clé de l'Angleterre », abrite dans ses tunnels le quartier général de l'opération Dynamo, l'évacuation de Dunkerque en 1940. En 1944, la région sert à une grande opération de déception : une armée fantôme, le FUSAG, y est censée préparer un débarquement dans le Pas-de-Calais." },
    { x = 185561, z = -113479, r = 400, text = "Stonehenge, cercle de pierres dressées de la plaine de Salisbury, commencé il y a environ 5 000 ans. La plaine est aussi, en 1944, un vaste terrain d'entraînement de l'armée britannique." },
    { x = -96750, z = -85827, r = 900, text = "Le Mont-Saint-Michel, îlot de granit surmonté d'une abbaye dont la première église remonte à 708. Ses marées comptent parmi les plus fortes d'Europe. Au 6 juillet 1944, vous le survolez en territoire rouge : il ne sera libéré que plus tard dans l'été." },
  }
  veafTourGuide.maxAgl = 457      -- 1 500 ft
  veafTourGuide.repeatAfter = 600 -- s
  function veafTourGuide.check()
    local now = timer.getTime()
    for _, side in pairs({ coalition.side.BLUE, coalition.side.RED }) do
      for _, unit in pairs(coalition.getPlayers(side) or {}) do
        if unit and unit:isExist() and unit:inAir() then
          local p = unit:getPoint()
          local agl = p.y - land.getHeight({ x = p.x, y = p.z })
          if agl < veafTourGuide.maxAgl then
            for i, m in ipairs(veafTourGuide.monuments) do
              local dx, dz = p.x - m.x, p.z - m.z
              if dx * dx + dz * dz < m.r * m.r then
                local key = unit:getName() .. '#' .. i
                local last = veafTourGuide.seen[key]
                if not last or now - last > veafTourGuide.repeatAfter then
                  veafTourGuide.seen[key] = now
                  trigger.action.outTextForGroup(unit:getGroup():getID(), m.text, 25)
                end
              end
            end
          end
        end
      end
    end
    return now + 2
  end
  timer.scheduleFunction(function(_, t) local ok, nxt = pcall(veafTourGuide.check) if ok then return nxt end env.error('veafTourGuide: ' .. tostring(nxt)) return t + 10 end, nil, timer.getTime() + 10)
end
-- <<< guide touristique de la Normandie
