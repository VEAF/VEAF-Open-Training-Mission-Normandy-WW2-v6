---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_OpenTraining_Normandy_ICAO_LFRK"
veaf.config.era = veaf.ERA.WW2
veaf.silenceAtcOnAllAirbases()
veaf.HideNamesFromSpawnedGroups = true

veaf.config.language = "fr"

-- ── Airfield channels of the mission's radio plan (src/presets.yaml, `bases`) ──────
if veafAirbases then
    veafAirbases.MissionChannels = {
        [4] = { alias = "Base-Maupertus", title = "Maupertus", uhf = 252.15, vhf = 120.35, fm = 40.6 },
        [8] = { alias = "Base-Lessay", title = "Lessay", uhf = 253.95, vhf = 121.85, fm = 42.1 },
        [12] = { alias = "Base-Deux Jumeaux", title = "Deux Jumeaux", uhf = 250.1, vhf = 118.15, fm = 38.55 },
        [15] = { alias = "Base-Azeville", title = "Azeville", uhf = 250.25, vhf = 118.35, fm = 38.7 },
        [16] = { alias = "Base-Picauville", title = "Picauville", uhf = 250.3, vhf = 118.4, fm = 38.75 },
        [18] = { alias = "Base-Longues-sur-Mer", title = "Longues-sur-Mer", uhf = 250.4, vhf = 118.55, fm = 38.85 },
        [19] = { alias = "Base-Carpiquet", title = "Carpiquet", uhf = 250.45, vhf = 118.6, fm = 38.9 },
        [20] = { alias = "Base-Bazenville", title = "Bazenville", uhf = 250.55, vhf = 118.7, fm = 39.0 },
        [22] = { alias = "Base-Beny-sur-Mer", title = "Beny-sur-Mer", uhf = 250.65, vhf = 118.8, fm = 39.1 },
        [26] = { alias = "Base-Evreux", title = "Evreux", uhf = 250.85, vhf = 119.0, fm = 39.3 },
        [30] = { alias = "Base-Tangmere", title = "Tangmere", uhf = 251.1, vhf = 119.3, fm = 39.55 },
        [32] = { alias = "Base-Argentan", title = "Argentan", uhf = 251.2, vhf = 119.4, fm = 39.65 },
        [38] = { alias = "Base-Vrigny", title = "Vrigny", uhf = 251.5, vhf = 119.7, fm = 39.95 },
        [44] = { alias = "Base-Beauvais-Tille", title = "Beauvais-Tille", uhf = 251.85, vhf = 120.05, fm = 40.3 },
        [45] = { alias = "Base-Cormeilles-en-Vexin", title = "Cormeilles-en-Vexin", uhf = 251.9, vhf = 120.1, fm = 40.35 },
        [46] = { alias = "Base-Creil", title = "Creil", uhf = 251.95, vhf = 120.15, fm = 40.4 },
        [51] = { alias = "Base-Fecamp-Benouville", title = "Fecamp-Benouville", uhf = 252.2, vhf = 120.4, fm = 40.65 },
        [55] = { alias = "Base-Triqueville", title = "Triqueville", uhf = 252.4, vhf = 120.6, fm = 40.85 },
        [58] = { alias = "Base-Stoney Cross", title = "Stoney Cross", uhf = 252.55, vhf = 120.75, fm = 41.0 },
        [60] = { alias = "Base-Ronai", title = "Ronai", uhf = 252.7, vhf = 120.9, fm = 41.1 },
        [61] = { alias = "Base-Rouen-Boos", title = "Rouen-Boos", uhf = 252.75, vhf = 120.95, fm = 41.15 },
        [62] = { alias = "Base-Deauville", title = "Deauville", uhf = 252.8, vhf = 121.0, fm = 41.2 },
        [64] = { alias = "Base-Flers", title = "Flers", uhf = 252.9, vhf = 121.1, fm = 41.3 },
        [67] = { alias = "Base-Beaumont-le-Roger", title = "Beaumont-le-Roger", uhf = 253.05, vhf = 121.25, fm = 41.45 },
        [71] = { alias = "Base-Biggin Hill", title = "Biggin Hill", uhf = 253.3, vhf = 134.8, fm = 41.7 },
        [72] = { alias = "Base-Manston", title = "Manston", uhf = 253.35, vhf = 118.25, fm = 41.75 },
        [75] = { alias = "Base-Abbeville Drucat", title = "Abbeville Drucat", uhf = 253.5, vhf = 118.05, fm = 41.9 },
        [76] = { alias = "Base-Saint-Omer Wizernes", title = "Saint-Omer Wizernes", uhf = 253.55, vhf = 121.55, fm = 41.95 },
    }
end

-- ── Global log level ─────────────────────────────────────────────────────────
veaf.ForcedLogLevel = "info"

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

-- One module's initialisation error must not take the others down (FIX-DEMO-MISSION-FINDINGS 02).
local function veafGuardedInit(name, initialize)
    local ok, err = xpcall(initialize, function(e)
        if debug and debug.traceback then
            return debug.traceback(tostring(e), 2)
        end
        return tostring(e)
    end)
    if not ok then
        veaf.loggers.get(veaf.Id):error("%s init failed: %s", name, err)
    end
end

veafGuardedInit("SECURITY", function()
if veafSecurity then
    veafSecurity.initialize()
end
end)

veafGuardedInit("RADIO", function()
if veafRadio then
    veafRadio.initialize(true)
end
end)

veafGuardedInit("SHORTCUTS", function()
if veafShortcuts then
    veafShortcuts.initialize()
end
end)

veafGuardedInit("NAMEDPOINTS", function()
if veafNamedPoints then
    veafNamedPoints.initialize({})
end
end)

veafGuardedInit("SPAWN", function()
if veafSpawn then
    veafSpawn.initialize()
end
end)

-- ── Combat ──

veaf.setConfig("CARRIER", "enable", false)

veafGuardedInit("CASMISSION", function()
if veafCasMission then
    veafCasMission.initialize()
end
end)

veafGuardedInit("TRANSPORTMISSION", function()
if veafTransportMission then
    veafTransportMission.initialize()
end
end)

veafGuardedInit("COMBATMISSION", function()
if veafCombatMission then
    veafCombatMission.addCapMission("CAP-Caen-Bf109", "CAP rouge Bf 109 K-4 — sud de Caen — 15 000 ft", "Deux Bf 109 K-4 patrouillent au sud de Caen, entre Falaise et Lisieux, à 15 000 ft. Canons et mitrailleuses seulement.", false, true)
    veafCombatMission.addCapMission("CAP-Cotentin-Fw190", "CAP rouge Fw 190 A-8 — Cotentin sud — 12 000 ft", "Deux Fw 190 A-8 patrouillent au sud du front du Cotentin, entre Coutances et Saint-Lô, à 12 000 ft. Canons seulement.", false, true)
    veafCombatMission.addCapMission("CAP-Seine-Fw190D9", "CAP rouge Fw 190 D-9 — vallée de la Seine — 22 000 ft", "Deux Fw 190 D-9, le chasseur le plus performant du camp rouge, patrouillent haut au-dessus de la Seine, entre Pont-Audemer et Rouen, à 22 000 ft. Canons seulement.", false, true)
    veafCombatMission.addCapMission("Raid-Ju88", "Raid rouge Ju 88 A-4 à intercepter — baie de Seine — 12 000 ft", "Quatre bombardiers Ju 88 A-4 tournent au-dessus de la baie de Seine, à 12 000 ft, prêts à frapper les plages : les intercepter. Armement défensif seulement tiré par les mitrailleurs.", false, true)
    veafCombatMission.addCapMission("CAP-TetedePont-P51D", "CAP bleue P-51D — tête de pont — 15 000 ft", "Deux P-51D patrouillent au large de la tête de pont, de Port-en-Bessin à Ouistreham, à 15 000 ft. Canons seulement.", false, true)
    veafCombatMission.addCapMission("CAP-Cotentin-Spitfire", "CAP bleue Spitfire LF IX — Cotentin — 12 000 ft", "Deux Spitfire LF Mk IX patrouillent au nord du Cotentin, de Cherbourg à Saint-Vaast, à 12 000 ft. Canons seulement.", false, true)
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Defense-Mulberry")
        :setFriendlyName("Défense — raid de Ju 88 sur le port artificiel d'Arromanches")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Six Ju 88 A-4 chargés de bombes, escortés de quatre Fw 190 A-8, partent de l'estuaire de la Seine vers le port artificiel d'Arromanches. Abattez les bombardiers avant le largage.
Échec si le port est bombardé (constaté par vous : la mission ne le vérifie pas).]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Bombardiers")
            :setGroups({"SC-Raid-Mulberry-Bombers"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Raid-Mulberry-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Escorte-B17")
        :setFriendlyName("Escorte — six B-17G sur les triages de Rouen")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Six B-17G décollés d'Angleterre vont bombarder la gare de triage de Rouen, par la Manche et la basse Seine. Des Fw 190 A-8 et des Bf 109 K-4 les attendent au-dessus de la Seine : escortez-les, de la côte à la cible.
Échec si un bombardier est abattu (constaté par vous : la mission ne le vérifie pas).]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Bombardiers")
            :setGroups({"SC-Escort-B17"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Chasseurs rouges")
            :setGroups({"SC-Escort-B17-Interceptors", "SC-Escort-B17-Interceptors-Bf109"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Interception-Reco")
        :setFriendlyName("Interception — Ju 88 de reconnaissance sur la tête de pont")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Un Ju 88 A-4 de reconnaissance, escorté de deux Bf 109 K-4, survole la tête de pont à 22 000 ft pour photographier les plages. Interceptez-le avant qu'il ne rentre : sa route passe au large de Courseulles, de Bayeux puis du Cotentin.]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Reconnaissance")
            :setGroups({"SC-Recce-Ju88"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Recce-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.initialize()
end
end)

veafGuardedInit("COMBATZONE", function()
if veafCombatZone then
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Bocage_Easy")
        :setFriendlyName("A1 Mitraillage bocage — facile")
        :setRadioGroupName("Entraînement appui rapproché")
        :setBriefing([[Champ de tir d'appui rapproché dans le bocage du Cotentin, à 6 nm à l'ouest d'Azeville : chars, blindés légers et camions immobiles en tir interdit, dépôts de carburant et casernement. À 11 nm du front, arrière bleu.
Position : bullseye 326°/27 nm (N49°30.000' W001°28.200').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Bocage_Medium")
        :setFriendlyName("A2 Mitraillage bocage — moyen")
        :setRadioGroupName("Entraînement appui rapproché")
        :setBriefing([[Champ de tir du bocage : un groupe blindé léger actif et de la flak légère de 20 mm (deux positions tirées au sort sur trois) en plus des cibles du niveau facile.
Position : bullseye 326°/27 nm (N49°30.000' W001°28.200').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Bocage_Hard")
        :setFriendlyName("A3 Mitraillage bocage — difficile")
        :setRadioGroupName("Entraînement appui rapproché")
        :setBriefing([[Champ de tir du bocage avec une défense courte portée réaliste : une batterie de flak de 37 mm (tirée au sort entre deux positions), de la flak de 20 mm et un second groupe blindé.
Position : bullseye 326°/27 nm (N49°30.000' W001°28.200').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Salisbury_Easy")
        :setFriendlyName("B1 Bombardement Salisbury — facile")
        :setRadioGroupName("Entraînement bombardement")
        :setBriefing([[Champ de tir de bombardement de la plaine de Salisbury, à 21 nm de Stoney Cross : bâtiments et véhicules fictifs immobiles en tir interdit (blockhaus, casernes, entrepôts, dépôt, gare). À 111 nm du front : aucun contact possible.
Position : bullseye 344°/130 nm (N51°12.000' W001°58.800').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Salisbury_Medium")
        :setFriendlyName("B2 Bombardement Salisbury — moyen")
        :setRadioGroupName("Entraînement bombardement")
        :setBriefing([[Champ de tir de Salisbury : de la flak légère de 20 mm, deux positions sur trois tirées au sort, en plus des cibles du niveau facile.
Position : bullseye 344°/130 nm (N51°12.000' W001°58.800').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Salisbury_Hard")
        :setFriendlyName("B3 Bombardement Salisbury — difficile")
        :setRadioGroupName("Entraînement bombardement")
        :setBriefing([[Champ de tir de Salisbury avec la flak lourde de l'époque : une batterie de pièces de 88 mm (tirée au sort entre deux positions) et une batterie de 37 mm en plus du niveau moyen.
Position : bullseye 344°/130 nm (N51°12.000' W001°58.800').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Aurigny_Easy")
        :setFriendlyName("C1 Antiflak Aurigny — facile")
        :setRadioGroupName("Entraînement antiflak")
        :setBriefing([[Site antiflak du fort Tourgis, à Aurigny, à 1 nm de la piste d'Aurigny et 30 nm de Maupertus : une batterie de flak moyenne (37 mm), à détruire. À 32 nm du front, en territoire rouge.
Position : bullseye 308°/58 nm (N49°43.398' W002°14.148').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Aurigny_Medium")
        :setFriendlyName("C2 Antiflak Aurigny — moyen")
        :setRadioGroupName("Entraînement antiflak")
        :setBriefing([[Site antiflak d'Aurigny : la flak lourde de 88 mm (une batterie sur deux positions) en plus de la batterie de 37 mm.
Position : bullseye 308°/58 nm (N49°43.398' W002°14.148').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Aurigny_Hard")
        :setFriendlyName("C3 Antiflak Aurigny — difficile")
        :setRadioGroupName("Entraînement antiflak")
        :setBriefing([[Site antiflak d'Aurigny en réseau : un radar d'alerte Freya, un radar de conduite de tir Würzburg, un télémètre et deux projecteurs guident la flak lourde et moyenne.
Position : bullseye 308°/58 nm (N49°43.398' W002°14.148').]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_TourPlages")
        :setFriendlyName("T1 Tourisme — Plages du Débarquement")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne « Plages du Débarquement », hors combat, à 3 nm de Longues-sur-Mer. Une balise radio VHF/AM à chaque site (SWD 130.0, GLD 130.5, OMA 131.0, UTH 131.5) ; survolez un monument à moins de 1 500 ft sol et un guide vous le raconte.
Position : bullseye 051°/23 nm (N49°21.000' W000°37.200').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_TourCotentin")
        :setFriendlyName("T2 Tourisme — Cotentin et Cherbourg")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne « Cotentin et Cherbourg », hors combat, à 2 nm de Maupertus. Une balise radio VHF/AM à chaque site (CHB 133.0, GAT 133.5, VAA 134.0) ; survolez un monument à moins de 1 500 ft sol et un guide vous le raconte.
Position : bullseye 334°/33 nm (N49°37.200' W001°27.000').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_TourAngleterre")
        :setFriendlyName("T3 Tourisme — Côte sud de l'Angleterre")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne « Côte sud de l'Angleterre », hors combat, à 19 nm de Stoney Cross. Une balise radio VHF/AM à chaque site (NDL 135.0, POR 135.5, BCH 136.0, DVR 136.5) ; survolez un monument à moins de 1 500 ft sol et un guide vous le raconte.
Position : bullseye 356°/101 nm (N50°48.000' W001°12.000').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_VillersBocage")
        :setFriendlyName("Z01 Front — Villers-Bocage")
        :setRadioGroupName("Front")
        :setBriefing([[Des chars allemands tiennent les hauteurs de Villers-Bocage, face à la poussée britannique : Panzer IV, Tiger et canons antichars en position, appuyés par de l'artillerie (composition illustrative). Détruire les blindés et les canons ; flak légère et moyenne pour la couverture.
Position : bullseye 095°/17 nm (N49°04.902' W000°39.348'). Base amie la plus proche : Bazenville, à 14 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CaenNord")
        :setFriendlyName("Z02 Front — Caen et Carpiquet")
        :setRadioGroupName("Front")
        :setBriefing([[La ligne de défense de la 12e SS Hitlerjugend au nord de Caen, autour de Carpiquet : Panzer IV, Tiger et automoteurs d'artillerie dans les ruines. Détruire les blindés et l'artillerie ; flak moyenne de 37 mm, sous la QRA de Caen.
Position : bullseye 079°/27 nm (N49°11.100' W000°24.600'). Base amie la plus proche : Beny-sur-Mer, à 7 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CotentinSud")
        :setFriendlyName("Z03 Front — La Haye-du-Puits et Lessay")
        :setRadioGroupName("Front")
        :setBriefing([[La ligne de défense allemande qui bloque le Cotentin, des marais de Lessay à La Haye-du-Puits : canons antichars, blindés légers et artillerie dans le bocage. Détruire les blindés et les canons ; flak moyenne. Aucune QRA ne couvre le Cotentin sud.
Position : bullseye 288°/17 nm (N49°12.600' W001°30.000'). Base amie la plus proche : Picauville, à 12 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Antifer")
        :setFriendlyName("Z04 Radars — station du cap d'Antifer")
        :setRadioGroupName("Flak et radars")
        :setBriefing([[La station radar du cap d'Antifer, sur la côte au nord du Havre : radar d'alerte avancée Freya et radars de conduite de tir Würzburg, protégés par de la flak lourde. Détruire les radars et réduire la flak.
Position : bullseye 053°/60 nm (N49°41.192' E000°09.875'). Base amie la plus proche : Beny-sur-Mer, à 33 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_GrisNez")
        :setFriendlyName("Z05 Radars — cap Gris-Nez")
        :setRadioGroupName("Flak et radars")
        :setBriefing([[Le cap Gris-Nez, au plus près des côtes anglaises : radars Freya et Würzburg, flak lourde et batterie côtière. Détruire les radars et réduire la flak ; la batterie côtière est une menace pour les navires, pas pour les avions.
Position : bullseye 042°/148 nm (N50°52.328' E001°35.023'). Base amie la plus proche : Manston, à 30 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiFalaise")
        :setFriendlyName("Z06 Convoi — Falaise vers Caen")
        :setRadioGroupName("Convois")
        :setBriefing([[Des renforts blindés quittent Falaise par la route de Caen. L'arrêter avant Caen ; deux Sd.Kfz 251 et un Puma l'escortent.
Position : bullseye 108°/37 nm (N48°54.745' W000°12.602'). Base amie la plus proche : Beny-sur-Mer, à 25 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiLisieux")
        :setFriendlyName("Z07 Convoi — Lisieux vers Caen")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi de ravitaillement roule de Lisieux vers Caen, par la route de Mézidon. Le détruire avant le front ; camions, tracteurs et un Sd.Kfz 251 d'escorte.
Position : bullseye 086°/51 nm (N49°08.399' E000°12.533'). Base amie la plus proche : Beny-sur-Mer, à 27 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiCoutances")
        :setFriendlyName("Z08 Convoi — Coutances vers La Haye-du-Puits")
        :setRadioGroupName("Convois")
        :setBriefing([[Des renforts quittent Coutances vers La Haye-du-Puits, le long du front du Cotentin. Les arrêter avant le front ; deux Sd.Kfz 251 et un Puma les escortent.
Position : bullseye 256°/15 nm (N49°03.671' W001°28.162'). Base amie la plus proche : Picauville, à 20 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_RocheGuyon")
        :setFriendlyName("Z09 Frappe — état-major de La Roche-Guyon")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Le quartier général du groupe d'armées B, dans le château de La Roche-Guyon, au bord de la Seine : bunkers, centre de transmissions, véhicules de commandement. Tout détruire ; flak moyenne et lourde. Hors des cercles de QRA.
Position : bullseye 088°/107 nm (N49°05.136' E001°37.650'). Base amie la plus proche : Beny-sur-Mer, à 82 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_TriageArgentan")
        :setFriendlyName("Z10 Frappe — gare de triage d'Argentan")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[La gare de triage d'Argentan, nœud ferroviaire qui alimente le front de Normandie : gare, entrepôts, réservoirs de carburant. Tout détruire ; flak moyenne.
Position : bullseye 116°/48 nm (N48°44.730' W000°00.900'). Base amie la plus proche : Beny-sur-Mer, à 37 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Eperlecques")
        :setFriendlyName("Z11 Frappe — blockhaus d'Éperlecques")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Le blockhaus d'Éperlecques, près de Saint-Omer : un énorme bunker de béton destiné au lancement des fusées V2, bâti en 1943 et déjà bombardé. Détruire le blockhaus et ses annexes ; flak lourde et moyenne, sous la QRA du Pas-de-Calais.
Position : bullseye 048°/160 nm (N50°48.498' E002°05.982'). Base amie la plus proche : Manston, à 43 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_DepotLisieux")
        :setFriendlyName("Z12 Frappe — dépôts d'essence de Lisieux")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Un dépôt de carburant de l'arrière du front, près de Lisieux (position illustrative) : réservoirs, pompes, entrepôts. Tout détruire ; flak moyenne.
Position : bullseye 086°/52 nm (N49°08.700' E000°13.800'). Base amie la plus proche : Beny-sur-Mer, à 27 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Triqueville")
        :setFriendlyName("Z13 OCA — base aérienne de Triqueville")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[La base aérienne de Triqueville, au sud de l'estuaire de la Seine : chasseurs au parking, hangars et carburant. Tout détruire au sol ; flak moyenne et lourde, sous la QRA de la Seine.
Position : bullseye 076°/63 nm (N49°20.158' E000°27.991'). Base amie la plus proche : Beny-sur-Mer, à 35 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_BeaumontLeRoger")
        :setFriendlyName("Z14 OCA — base aérienne de Beaumont-le-Roger")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[La base aérienne de Beaumont-le-Roger, à l'arrière du front : bombardiers et chasseurs au parking, hangars et carburant. Tout détruire au sol ; flak moyenne et lourde.
Position : bullseye 089°/75 nm (N49°05.767' E000°48.308'). Base amie la plus proche : Beny-sur-Mer, à 50 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_VedettesLeHavre")
        :setFriendlyName("Z15 Antinavire — vedettes lance-torpilles du Havre")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Les vedettes lance-torpilles (S-boote) basées au Havre, qui sortent attaquer les convois de la Manche, et la batterie côtière du cap de la Hève. Couler les vedettes ; flak de bord et batterie côtière (portée de 20 km environ pour les canons, sans menace pour les avions).
Position : bullseye 058°/50 nm (N49°31.800' E000°00.600'). Base amie la plus proche : Beny-sur-Mer, à 22 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiCotier")
        :setFriendlyName("Z16 Antinavire — convoi côtier vers Dieppe")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Un convoi de cargos escortés longe la côte du Havre vers Dieppe, avec deux vedettes lance-torpilles. Couler les cargos ; flak de bord sur les escorteurs.
Position : bullseye 047°/72 nm (N49°54.000' E000°18.000'). Base amie la plus proche : Beny-sur-Mer, à 46 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.GetZone("combatZone_Bocage_Medium"):addZoneElementsFromZoneNamed("combatZone_Bocage_Easy")
    veafCombatZone.GetZone("combatZone_Bocage_Hard"):addZoneElementsFromZoneNamed("combatZone_Bocage_Medium")
    veafCombatZone.GetZone("combatZone_Bocage_Hard"):addZoneElementsFromZoneNamed("combatZone_Bocage_Easy")
    veafCombatZone.GetZone("combatZone_Salisbury_Medium"):addZoneElementsFromZoneNamed("combatZone_Salisbury_Easy")
    veafCombatZone.GetZone("combatZone_Salisbury_Hard"):addZoneElementsFromZoneNamed("combatZone_Salisbury_Medium")
    veafCombatZone.GetZone("combatZone_Salisbury_Hard"):addZoneElementsFromZoneNamed("combatZone_Salisbury_Easy")
    veafCombatZone.GetZone("combatZone_Aurigny_Medium"):addZoneElementsFromZoneNamed("combatZone_Aurigny_Easy")
    veafCombatZone.GetZone("combatZone_Aurigny_Hard"):addZoneElementsFromZoneNamed("combatZone_Aurigny_Medium")
    veafCombatZone.GetZone("combatZone_Aurigny_Hard"):addZoneElementsFromZoneNamed("combatZone_Aurigny_Easy")
    veafCombatZone.initialize()
end
end)

veafGuardedInit("QRA", function()
if veafQraManager then
    veafQraManager.initialize()
    local QRA_Caen = VeafQRA:new()
        :setName("QRA Caen")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Caen")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Caen-Bf109", "QRA-Caen-Fw190A8"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Caen-Fw190D9x4", "QRA-Caen-Bf109x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Carpiquet")
        :start()
    local QRA_Seine = VeafQRA:new()
        :setName("QRA Seine")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Seine")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Seine-Fw190A8", "QRA-Seine-Bf109"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Seine-Fw190A8x4", "QRA-Seine-Fw190D9x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Triqueville")
        :start()
    local QRA_Pas_de_Calais = VeafQRA:new()
        :setName("QRA Pas-de-Calais")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-PasDeCalais")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-PdC-Bf109", "QRA-PdC-Fw190D9"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-PdC-Bf109x4", "QRA-PdC-Fw190A8x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Saint-Omer Wizernes")
        :start()
    local QRA_Solent = VeafQRA:new()
        :setName("QRA Solent")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-Solent")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Solent-Spitfire", "QRA-Solent-P51D"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Solent-Spitfirex4", "QRA-Solent-P51Dx4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Tangmere")
        :start()
    local QRA_T_te_de_pont = VeafQRA:new()
        :setName("QRA Tête de pont")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-TetedePont")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-TetedePont-P47D", "QRA-TetedePont-P51D"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-TetedePont-P47Dx4", "QRA-TetedePont-P51Dx4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Longues-sur-Mer")
        :start()
end
end)

-- ── Features ──

veafGuardedInit("GRASS", function()
if veafGrass then
    veafGrass.initialize()
end
end)

veafGuardedInit("MOVE", function()
if veafMove then
    veafMove.initialize()
end
end)

veafGuardedInit("SANCTUARY", function()
if veafSanctuary then
    veafSanctuary.initialize()
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Angleterre")
        if zone then
            zone:setName("Sanctuaire Angleterre du sud")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Evreux")
        if zone then
            zone:setName("Sanctuaire Évreux")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
end
end)

veafGuardedInit("WEATHER", function()
if veafWeather then
    veafWeather.initialize()
end
end)

veafGuardedInit("REMOTE", function()
if veafRemote then
    veafRemote.initialize()
end
end)

veafGuardedInit("AIRBASES", function()
if veafAirbases then
    veafAirbases.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("MARKERS", function()
if veafMarkers then
    veafMarkers.initialize()
end
end)

veafGuardedInit("TIME", function()
if veafTime then
    veafTime.initialize()
end
end)

veafGuardedInit("UNITS", function()
if veafUnits then
    veafUnits.initialize()
end
end)

veafGuardedInit("CACHE", function()
if veafCacheManager then
    veafCacheManager.initialize()
end
end)

veafGuardedInit("EVENTS", function()
if veafEventHandler then
    veafEventHandler.initialize()
end
end)

-- ── Core ──

veafGuardedInit("GROUNDAI", function()
if veafGroundAI then
    veafGroundAI.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("COMMANDS", function()
if veafCommands then
    veafCommands.initialize()
end
end)

-- ── Features ──

veafGuardedInit("INTERPRETER", function()
if veafInterpreter then
    veafInterpreter.initialize()
end
end)

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("ctld", "enable", false)
veaf.setConfig("csar", "enable", false)
veaf.setConfig("skynet", "enable", false)
veaf.setConfig("tum", "enable", false)
