# slug, title, year, platforms, credit, rawg slugs, avail, history, lineup
G = []
def A(slug, title, year, platforms, credit, rawg, avail, history, lineup):
    G.append({
        "slug": slug, "title": title, "year": str(year),
        "platforms": platforms, "credit": credit, "rawg": rawg,
        "avail": avail, "history": history, "lineup": lineup,
    })

# --- NES ---
A("super-mario-bros","Super Mario Bros.","1985",["NES"],"Nintendo",["super-mario-bros"],"nso",
  "A short, tough run through pipes, bricks, and castles that set the pattern for side-scrolling Mario.",
  "It is the NES game people mean by Mario, and the clearest start of the side-scrolling series in this catalog.")
A("super-mario-bros-2","Super Mario Bros. 2","1988",["NES"],"Nintendo",["super-mario-bros-2"],"nso",
  "The Western sequel lets a four-person cast pick up enemies and throw them, built from a different Japanese game.",
  "It sits between the original and Super Mario Bros. 3, and later returned inside Super Mario All-Stars.")
A("super-mario-bros-3","Super Mario Bros. 3","1988",["NES"],"Nintendo",["super-mario-bros-3"],"nso",
  "A world map, suits, and short stages turned Mario into a toy box you can wander.",
  "It is the third side-scrolling Mario on NES and a cornerstone of the 8-bit lineup.")
A("the-legend-of-zelda","The Legend of Zelda","1986",["NES"],"Nintendo",["the-legend-of-zelda"],"nso",
  "An open overworld of caves, tools, and dungeons you can approach in more than one order.",
  "It is the first Zelda, and the model for the series' mix of map, items, and bosses.")
A("zelda-ii-the-adventure-of-link","Zelda II: The Adventure of Link","1987",["NES"],"Nintendo",["zelda-ii-the-adventure-of-link","the-legend-of-zelda-2-the-adventure-of-link"],"nso",
  "Side-view combat and experience levels make this the odd Zelda, closer to an action RPG than the first game.",
  "It is the second NES Zelda, often cited when people talk about how far the series later swung back toward exploration.")
A("metroid","Metroid","1986",["NES"],"Nintendo",["metroid"],"nso",
  "Samus explores a hostile cavern where doors you cannot use yet are the point of the map.",
  "It is the first Metroid, and the template for the series' isolated upgrades and backtracking.")
A("kid-icarus","Kid Icarus","1986",["NES"],"Nintendo",["kid-icarus","kid-icarus-1986"],"nso",
  "Pit climbs out of the underworld with a weak bow that grows if you can keep your health up.",
  "It is the NES original that later handheld and 3DS games in the series look back to.")
A("excitebike","Excitebike","1984",["NES"],"Nintendo",["excitebike"],"nso",
  "A side-view dirt-bike race about temperature management as much as jumps.",
  "It is an early NES racer and a name Nintendo has kept alive in later Excite sequels.")
A("duck-hunt","Duck Hunt","1984",["NES"],"Nintendo",["duck-hunt"],"nso",
  "Light-gun shooting at ducks and clay pigeons, with a dog that comments on misses.",
  "It shipped with a huge number of NES bundles and stands for that light-gun era in this catalog.")
A("ice-climber","Ice Climber","1985",["NES"],"Nintendo",["ice-climber"],"nso",
  "Two climbers hammer through ice platforms toward a condor at the top of each mountain.",
  "It is a compact NES action game that stayed recognizable through later cameos.")
A("balloon-fight","Balloon Fight","1985",["NES"],"Nintendo",["balloon-fight"],"nso",
  "Flapping balloons keep you aloft while you pop rivals and dodge lightning.",
  "It is a small NES arcade-style game, often grouped with the console's early black-box lineup.")
A("mario-bros","Mario Bros.","1983",["NES"],"Nintendo",["mario-bros-1983","mario-bros"],"nso",
  "A single-screen cooperative game about bumping pests from below, before side-scrolling Mario.",
  "It is the arcade-born Mario Bros. on NES, not Super Mario Bros.")
A("dr-mario","Dr. Mario","1990",["NES"],"Nintendo",["dr-mario"],"nso",
  "Vitamin capsules fall into a bottle to clear colored viruses.",
  "It is the NES puzzle game that started the Dr. Mario line.")
A("punch-out","Punch-Out!!","1987",["NES"],"Nintendo",["punch-out","mike-tysons-punch-out","punch-out-1987"],"nso",
  "A pattern-based boxing career up a ladder of cartoon opponents, seen from behind Little Mac.",
  "It is the NES Punch-Out!!, the game most later entries in the series are measured against.")
A("mega-man-2","Mega Man 2","1988",["NES"],"Capcom",["mega-man-2"],"nso",
  "Eight robot masters can be challenged in any order, and their weapons answer one another.",
  "It is the Mega Man most players mean when they talk about the NES series.")
A("mega-man","Mega Man","1987",["NES"],"Capcom",["mega-man"],"nso",
  "The first robot-master gauntlet, harder and shorter than the sequel that made the formula famous.",
  "It opens the original Mega Man line on Nintendo's 8-bit console.")
A("castlevania","Castlevania","1986",["NES"],"Konami",["castlevania"],"nso",
  "Simon Belmont walks into Dracula's castle with a whip and very little room for error.",
  "It is the first Castlevania, and the start of Konami's long run on Nintendo hardware.")
A("castlevania-iii-draculas-curse","Castlevania III: Dracula's Curse","1989",["NES"],"Konami",["castlevania-iii-draculas-curse"],"nso",
  "Branching paths and partner characters expand the whip-and-castle formula.",
  "It is the late NES Castlevania, often treated as the peak of the 8-bit entries.")
A("contra","Contra","1988",["NES"],"Konami",["contra"],"nso",
  "A run-and-gun with two soldiers, spreading guns, and a famous cheat code culture around it.",
  "The NES version is the one that defined Contra for a generation of home players.")
A("kirbys-adventure","Kirby's Adventure","1993",["NES"],"HAL Laboratory / Nintendo",["kirbys-adventure"],"nso",
  "Kirby gains copy abilities here, turning inhaled enemies into powers across a long NES adventure.",
  "It is the NES follow-up to Dream Land and the game that set Kirby's copy-ability identity.")
A("ninja-gaiden","Ninja Gaiden","1988",["NES"],"Tecmo",["ninja-gaiden"],"nso",
  "Wall-clinging action cut with story scenes between stages.",
  "The NES trilogy starts here and is the version of Ninja Gaiden this catalog treats as the original home run.")
A("double-dragon","Double Dragon","1988",["NES"],"Technos",["double-dragon-1988","double-dragon"],"nso",
  "A side-scrolling brawler about punching through a gang to reach a kidnapped friend.",
  "The NES port is the home version many players met first.")
A("final-fantasy","Final Fantasy","1987",["NES"],"Square",["final-fantasy"],"nso",
  "A party of four jobs crosses a cursed world in menu-driven battles.",
  "It is the NES role-playing game that opened Square's Final Fantasy line.")
A("dragon-warrior","Dragon Warrior","1986",["NES"],"Chunsoft / Enix",["dragon-quest","dragon-warrior"],"nso",
  "A single hero walks a small kingdom, grinds levels, and talks to townspeople in a turn-based quest.",
  "North America met Dragon Quest under the Dragon Warrior name on NES.")
A("startropics","StarTropics","1990",["NES"],"Nintendo",["star-tropics","startropics"],"nso",
  "Mike Jones searches island dungeons with a yo-yo weapon and a letter that famously needed water.",
  "It is a late NES Nintendo adventure, cousin to Zelda but with its own island story.")
A("blaster-master","Blaster Master","1988",["NES"],"Sunsoft",["blaster-master"],"nso",
  "A tank explores caverns, then the driver hops out for tight overhead caves.",
  "It is one of the NES action games people still name when they talk about Sunsoft's 8-bit run.")
A("ghosts-n-goblins","Ghosts 'n Goblins","1986",["NES"],"Capcom",["ghosts-n-goblins"],"nso",
  "Arthur loses his armor in two hits on a graveyard march that expects you to finish twice.",
  "The NES port is the notoriously strict home version of Capcom's arcade game.")
A("mega-man-3","Mega Man 3","1990",["NES"],"Capcom",["mega-man-3"],"nso",
  "A slide move and a rival robot join the usual master-weapon loop.",
  "It is the third NES Mega Man, often ranked beside the second.")
A("battletoads","Battletoads","1991",["NES"],"Rare",["battletoads"],"nso",
  "A beat-em-up that changes vehicles and gimmicks every few stages, including a brutal speeder sequence.",
  "Rare's NES original is the Battletoads people mean, long before later reimaginings.")
A("teenage-mutant-ninja-turtles","Teenage Mutant Ninja Turtles","1989",["NES"],"Konami",["teenage-mutant-ninja-turtles"],"nso",
  "Four turtles share a life bar across an overhead map and side-view fights.",
  "It is the first NES TMNT game, distinct from the arcade-style sequel that followed.")
A("rc-pro-am","R.C. Pro-Am","1988",["NES"],"Rare",["rc-pro-am"],"nso",
  "Tiny radio-control cars race an overhead track and pick up better parts.",
  "It is Rare's NES racer, a step on the way to their later Nintendo sports and kart work.")
A("faxanadu","Faxanadu","1987",["NES"],"Hudson Soft / Falcom",["faxanadu"],"nso",
  "A side-view action RPG in a dying world tree, with stalls of gear and a password save.",
  "It is a cult NES adventure and one of the deeper action RPGs on the console.")
A("bionic-commando","Bionic Commando","1988",["NES"],"Capcom",["bionic-commando"],"nso",
  "A swinging arm replaces the jump button in a mission-based action game.",
  "The NES version is its own campaign, not a straight arcade port, and a Capcom staple of the era.")
A("river-city-ransom","River City Ransom","1989",["NES"],"Technos",["river-city-ransom"],"nso",
  "An open-town brawler where you spend recovered cash on stats and food.",
  "It is Technos on NES, in the same family as Double Dragon but closer to a small RPG.")
A("super-mario-bros-the-lost-levels","Super Mario Bros.: The Lost Levels","1986",["NES"],"Nintendo",["super-mario-bros-the-lost-levels","super-mario-bros-2-japan"],"nso",
  "The Japanese Super Mario Bros. 2 is a harsher remix of the first game, later titled The Lost Levels abroad.",
  "In this catalog it is the NES sibling of the original, not the Western throw-the-vegetables sequel.")


# --- SNES ---
A("super-mario-world","Super Mario World","1990",["SNES"],"Nintendo",["super-mario-world"],"nso",
  "A cape, a dinosaur friend, and a world map hide a lot of optional exits.",
  "It is the launch-era SNES Mario and the 16-bit standard the later 2D games answer.")
A("super-mario-world-2-yoshis-island","Super Mario World 2: Yoshi's Island","1995",["SNES"],"Nintendo",["super-mario-world-2-yoshis-island","yoshis-island"],"nso",
  "Yoshi carries baby Mario through crayon-drawn stages built around eggs and flutter jumps.",
  "It is the SNES Yoshi platformer, a spin on Mario World rather than a kart or party game.")
A("super-mario-all-stars","Super Mario All-Stars","1993",["SNES"],"Nintendo",["super-mario-all-stars"],"nso",
  "A 16-bit compilation of the NES Mario side-scrollers, redrawn and sold as one cartridge.",
  "It is how many SNES owners met the earlier Mario games, and it stays a compilation entry here, not a replacement for the NES pages.")
A("super-mario-kart","Super Mario Kart","1992",["SNES"],"Nintendo",["super-mario-kart"],"nso",
  "Mode 7 tracks, slippery handling, and items that still define the series.",
  "It is the SNES original, the first Mario Kart, not a later game that reused the cast.")
A("a-link-to-the-past","The Legend of Zelda: A Link to the Past","1991",["SNES"],"Nintendo",["the-legend-of-zelda-a-link-to-the-past"],"nso",
  "Two layered versions of the same kingdom, and dungeons that teach a tool and then test it.",
  "It is the SNES Zelda that later top-down games, including the 2013 handheld one, openly echo.")
A("super-metroid","Super Metroid","1994",["SNES"],"Nintendo",["super-metroid"],"nso",
  "Samus returns to a research station already going wrong and leaves only when the planet allows it.",
  "It is the 16-bit Metroid, widely treated as the series' high point before the GameCube Prime games.")
A("donkey-kong-country","Donkey Kong Country","1994",["SNES"],"Rare / Nintendo",["donkey-kong-country"],"nso",
  "Pre-rendered jungles, mine carts, and a partner who covers ground the other Kong cannot.",
  "Rare's first Donkey Kong Country is the SNES hit that restarted the ape as a platform-game lead.")
A("donkey-kong-country-2","Donkey Kong Country 2: Diddy's Kong Quest","1995",["SNES"],"Rare / Nintendo",["donkey-kong-country-2","donkey-kong-country-2-diddys-kong-quest"],"nso",
  "Diddy and Dixie rescue Donkey Kong through tighter stages and animal buddies.",
  "It is the second SNES Country game, often preferred by players who want harder levels.")
A("donkey-kong-country-3","Donkey Kong Country 3: Dixie Kong's Double Trouble!","1996",["SNES"],"Rare / Nintendo",["donkey-kong-country-3"],"nso",
  "Dixie and Kiddy search a northern world while the earlier heroes are missing.",
  "It closes the SNES Country trilogy, late in the console's life.")
A("f-zero","F-Zero","1990",["SNES"],"Nintendo",["f-zero"],"nso",
  "Futuristic hovercraft racing that showed off Mode 7 speed on a small roster of machines.",
  "It is the SNES original of a series that later went to Nintendo 64 and GameCube.")
A("pilotwings","Pilotwings","1990",["SNES"],"Nintendo",["pilotwings"],"nso",
  "Flight-school lessons in a hang glider, plane, and jet pack, graded by instructors.",
  "It is a launch-window SNES showcase, with a later Nintendo 64 sequel of its own.")
A("star-fox","Star Fox","1993",["SNES"],"Nintendo / Argonaut",["star-fox"],"nso",
  "On-rails space combat drawn with the Super FX chip, chatty wingmen included.",
  "It is the SNES original, distinct from the Nintendo 64 follow-up Star Fox 64.")
A("super-mario-rpg","Super Mario RPG","1996",["SNES"],"Square / Nintendo",["super-mario-rpg"],"nso",
  "Mario, Bowser, and Peach share a turn-based party in a story Square built with Nintendo.",
  "It is the SNES role-playing game. A separate 2023 remake has its own page in this catalog.")
A("earthbound","EarthBound","1994",["SNES"],"Ape / HAL Laboratory / Nintendo",["earthbound","mother-2"],"nso",
  "Ness and friends walk a modern America-like world, fighting with psychic powers and baseball bats.",
  "It is the SNES Mother game, the cult RPG later players met through reissues and the series' reputation.")
A("chrono-trigger","Chrono Trigger","1995",["SNES"],"Square",["chrono-trigger"],"nso",
  "A party time-travels through several eras, with battles that reward position as well as menus.",
  "Square's SNES RPG is the original release. Later ports exist, but this page is the 16-bit game.")
A("final-fantasy-vi","Final Fantasy VI","1994",["SNES"],"Square",["final-fantasy-vi","final-fantasy-iii"],"nso",
  "An ensemble casts magic against an empire, and the second half lets you choose who walks point.",
  "North America first knew it as Final Fantasy III on SNES. This page is that 16-bit game.")
A("secret-of-mana","Secret of Mana","1993",["SNES"],"Square",["secret-of-mana"],"nso",
  "Real-time weapon charging and drop-in co-op distinguish this Square action RPG.",
  "It is the SNES Mana game that reached the widest audience, between earlier and later series entries.")
A("kirby-super-star","Kirby Super Star","1996",["SNES"],"HAL Laboratory / Nintendo",["kirby-super-star"],"nso",
  "A collection of short Kirby games on one cartridge, including helper characters who copy abilities with you.",
  "It is the SNES Kirby anthology, later revisited on DS as Super Star Ultra.")
A("kirbys-dream-course","Kirby's Dream Course","1994",["SNES"],"HAL Laboratory / Nintendo",["kirbys-dream-course"],"nso",
  "Kirby is a golf ball, and copying an enemy on the green changes the shot.",
  "It is the odd SNES Kirby, a sports spin rather than a platformer.")
A("super-punch-out","Super Punch-Out!!","1994",["SNES"],"Nintendo",["super-punch-out"],"nso",
  "A taller, faster boxing career than the NES game, still built on learning each boxer's tell.",
  "It is the SNES Punch-Out!!, not the NES original and not the later Wii game.")
A("street-fighter-ii","Street Fighter II","1992",["SNES"],"Capcom",["super-street-fighter-ii","street-fighter-ii-the-world-warrior","street-fighter-ii"],"nso",
  "One-on-one fights with a roster of special moves, in the home version that lived in a lot of SNES collections.",
  "This page is the SNES era of Street Fighter II, not a PlayStation or arcade-only release.")
A("super-castlevania-iv","Super Castlevania IV","1991",["SNES"],"Konami",["super-castlevania-iv"],"nso",
  "A whip that swings in more directions and a castle redrawn for 16-bit hardware.",
  "It is the SNES Castlevania, a retelling rather than a straight port of the NES game.")
A("mega-man-x","Mega Man X","1993",["SNES"],"Capcom",["mega-man-x"],"nso",
  "A dash, a wall jump, and armored upgrades move Mega Man into a faster future setting.",
  "It opens the X series on SNES, separate from the numbered NES Mega Man games.")
A("illusion-of-gaia","Illusion of Gaia","1993",["SNES"],"Quintet / Enix",["illusion-of-gaia"],"nso",
  "A boy crosses ancient sites in an action RPG that changes form for combat.",
  "It is the middle game of Quintet's loose SNES trilogy with Soul Blazer and Terranigma.")
A("soul-blazer","Soul Blazer","1992",["SNES"],"Quintet / Enix",["soul-blazer"],"nso",
  "Freeing trapped souls rebuilds towns room by room in a top-down action RPG.",
  "It is the first of Quintet's SNES action RPGs published by Enix.")
A("terranigma","Terranigma","1995",["SNES"],"Quintet / Enix",["terranigma"],"nso",
  "A callow hero leaves an underworld village and has to rebuild the surface world.",
  "It is the last of Quintet's SNES action RPGs, released in Europe and Japan but not North America.")
A("harvest-moon","Harvest Moon","1996",["SNES"],"Pack-In-Video / Natsume",["harvest-moon"],"nso",
  "A short farming life: crops, livestock, and town relationships on a clock.",
  "It is the SNES original of the farming series later handhelds carried for years.")

# --- N64 ---
A("super-mario-64","Super Mario 64","1996",["Nintendo 64"],"Nintendo",["super-mario-64-1996","super-mario-64"],"n64",
  "Paintings in a castle open into sandbox courses where stars can be collected in almost any order.",
  "It is the Nintendo 64 Mario that set the pattern for 3D Mario. A limited Switch compilation later included it for a time.")
A("mario-kart-64","Mario Kart 64","1996",["Nintendo 64"],"Nintendo",["mario-kart-64-1996","mario-kart-64"],"n64",
  "Courses climb and drop in ways the SNES game could not, built for four players on one screen.",
  "It is the second Mario Kart and the living-room Nintendo 64 racer.")
A("ocarina-of-time","The Legend of Zelda: Ocarina of Time","1998",["Nintendo 64"],"Nintendo",["the-legend-of-zelda-ocarina-of-time"],"n64",
  "A rideable Hyrule and dungeons built around a small set of tools, with a lock-on camera for fights.",
  "It is the Nintendo 64 original, not the later 3DS revision, which has its own page.")
A("majoras-mask","The Legend of Zelda: Majora's Mask","2000",["Nintendo 64"],"Nintendo",["the-legend-of-zelda-majoras-mask"],"n64",
  "A three-day cycle over a doomed town, with masks that change how Link moves through it.",
  "It is the darker Nintendo 64 follow-up to Ocarina of Time. The 3DS version is a separate entry.")
A("star-fox-64","Star Fox 64","1997",["Nintendo 64"],"Nintendo",["star-fox-64","lylat-wars"],"n64",
  "Branching missions and voice chatter carry an on-rails shooter that replaced the SNES game's chip look.",
  "It is the Nintendo 64 Star Fox, later revisited as a 3DS remake.")
A("super-smash-bros","Super Smash Bros.","1999",["Nintendo 64"],"HAL Laboratory / Nintendo",["super-smash-bros"],"n64",
  "Nintendo characters knock each other off floating arenas in a four-player fighting game.",
  "It is the first Smash Bros., the Nintendo 64 original of a series that grew on every home console after.")
A("paper-mario","Paper Mario","2000",["Nintendo 64"],"Intelligent Systems / Nintendo",["paper-mario"],"n64",
  "A storybook Mario turns sideways for timed turn-based fights and partner puzzles.",
  "It is the Nintendo 64 start of Paper Mario, before the GameCube sequel and later spin-offs.")
A("mario-party","Mario Party","1998",["Nintendo 64"],"Hudson Soft / Nintendo",["mario-party"],"n64",
  "A board game of dice and minigames that assumes four people around one console.",
  "It opens the Mario Party series on Nintendo 64.")
A("mario-party-2","Mario Party 2","1999",["Nintendo 64"],"Hudson Soft / Nintendo",["mario-party-2"],"n64",
  "Costume boards and a larger minigame list refine the first party game.",
  "It is the second Nintendo 64 Mario Party, still built for the same shared-controller setup.")
A("f-zero-x","F-Zero X","1998",["Nintendo 64"],"Nintendo",["f-zero-x"],"n64",
  "A huge machine roster and a very high frame rate, with tracks that loop through silence more than scenery.",
  "It is the Nintendo 64 F-Zero, between the SNES original and the GameCube GX.")
A("wave-race-64","Wave Race 64","1996",["Nintendo 64"],"Nintendo",["wave-race-64"],"n64",
  "Jet-ski racing where the water itself is the obstacle, with buoys that judge your line.",
  "It is a Nintendo 64 launch-window racer, a showcase more than a character game.")
A("1080-snowboarding","1080 Snowboarding","1998",["Nintendo 64"],"Nintendo",["1080-snowboarding"],"n64",
  "Trick lines and timed courses on snow, with a later GameCube cousin in 1080 Avalanche.",
  "It is Nintendo's Nintendo 64 snowboard game.")
A("banjo-kazooie","Banjo-Kazooie","1998",["Nintendo 64"],"Rare",["banjo-kazooie"],"n64",
  "A bear and a bird collect notes and jiggies across themed worlds full of jokes.",
  "Rare's Nintendo 64 platformer sits beside Mario 64 in that generation's collect-a-thon shelf.")
A("banjo-tooie","Banjo-Tooie","2000",["Nintendo 64"],"Rare",["banjo-tooie"],"n64",
  "Larger connected worlds and new egg types continue Banjo and Kazooie's hunt.",
  "It is the Nintendo 64 sequel, still a Rare game from the studio's Nintendo years.")
A("goldeneye-007","GoldenEye 007","1997",["Nintendo 64"],"Rare",["goldeneye-007"],"n64",
  "Mission objectives and split-screen firefights made a movie license into a console shooter.",
  "It is Rare's Nintendo 64 GoldenEye, the one living rooms played, not a later reimagining.")
A("perfect-dark","Perfect Dark","2000",["Nintendo 64"],"Rare",["perfect-dark"],"n64",
  "A spy shooter with gadgets, bots, and a counter-operative mode beside the campaign.",
  "Rare's follow-up to GoldenEye on Nintendo 64, and the last big first-person game of that era from the studio.")
A("kirby-64-the-crystal-shards","Kirby 64: The Crystal Shards","2000",["Nintendo 64"],"HAL Laboratory / Nintendo",["kirby-64-the-crystal-shards"],"n64",
  "Copy abilities combine in pairs, which is the puzzle as much as the platforms.",
  "It is the Nintendo 64 Kirby, between the SNES games and the later handheld entries.")
A("pokemon-snap","Pokemon Snap","1999",["Nintendo 64"],"HAL Laboratory / Nintendo",["pokemon-snap"],"n64",
  "An on-rails photo safari scores you on how well you frame Pokemon, not on battles.",
  "It is the Nintendo 64 original. A much later Switch game, New Pokemon Snap, is its own entry.")
A("pokemon-stadium","Pokemon Stadium","1999",["Nintendo 64"],"Nintendo",["pokemon-stadium"],"n64",
  "3D battles on a console, plus minigames, for players who brought pocket-monster teams from Game Boy.",
  "It is the Nintendo 64 companion to the Game Boy Pokemon games, not a mainline handheld entry.")
A("mario-tennis","Mario Tennis","2000",["Nintendo 64"],"Camelot / Nintendo",["mario-tennis"],"n64",
  "Arcade tennis with Mario characters and a simple charge shot.",
  "Camelot's Nintendo 64 game opened a sports line that continued on later Nintendo systems.")
A("diddy-kong-racing","Diddy Kong Racing","1997",["Nintendo 64"],"Rare",["diddy-kong-racing"],"n64",
  "Kart, hovercraft, and plane races on one island hub, with a boss at the end of each world.",
  "Rare's Nintendo 64 racer, a rival to Mario Kart 64 in the same generation.")
A("yoshis-story","Yoshi's Story","1997",["Nintendo 64"],"Nintendo",["yoshis-story"],"n64",
  "A picture-book Yoshi game about eating fruit to clear short, scored pages.",
  "It is the Nintendo 64 Yoshi, softer and shorter than the SNES Yoshi's Island.")
A("pilotwings-64","Pilotwings 64","1996",["Nintendo 64"],"Nintendo / Paradigm",["pilotwings-64"],"n64",
  "Hang gliders, gyrocopters, and rocket belts over photoreal islands.",
  "It is the Nintendo 64 sequel to the SNES flight school, and a launch game for the console.")
A("mario-golf","Mario Golf","1999",["Nintendo 64"],"Camelot / Nintendo",["mario-golf"],"n64",
  "Approach shots and a small RPG-like mode sit under a Mario golf career.",
  "Camelot's Nintendo 64 golf game, paired in spirit with their tennis entry.")
A("mischief-makers","Mischief Makers","1997",["Nintendo 64"],"Treasure",["mischief-makers"],"n64",
  "A robot girl grabs enemies and shakes them, in a side-scroller from Treasure.",
  "It is a cult Nintendo 64 action game, not a Nintendo-made platformer.")
A("sin-and-punishment","Sin and Punishment","2000",["Nintendo 64"],"Treasure",["sin-and-punishment"],"n64",
  "An on-rails shooter with a stick-controlled aim, released in Japan and later noticed worldwide.",
  "Treasure's Nintendo 64 game. A Wii sequel followed years later.")
A("pokemon-puzzle-league","Pokemon Puzzle League","2000",["Nintendo 64"],"Nintendo",["pokemon-puzzle-league"],"n64",
  "Panel-matching puzzles skinned with the Pokemon anime cast.",
  "It is Nintendo's Nintendo 64 puzzle game in the Tetris Attack tradition, not a mainline Pokemon quest.")

# --- Game Boy ---
A("super-mario-land","Super Mario Land","1989",["Game Boy"],"Nintendo",["super-mario-land"],"nso",
  "A pocket platformer with its own enemies, vehicles, and ending, not a shrunken Super Mario Bros.",
  "It is Mario's first Game Boy outing and the start of the Land line.")
A("super-mario-land-2","Super Mario Land 2: 6 Golden Coins","1992",["Game Boy"],"Nintendo",["super-mario-land-2-6-golden-coins","super-mario-land-2"],"nso",
  "Mario reclaims his castle from Wario across six coins hidden in themed zones.",
  "It introduces Wario and is the second Game Boy Mario Land, bigger than the first.")
A("kirbys-dream-land","Kirby's Dream Land","1992",["Game Boy"],"HAL Laboratory / Nintendo",["kirbys-dream-land-1992","kirbys-dream-land"],"nso",
  "There is no copy ability yet. Kirby inhales, spits, and floats across five short lands.",
  "It is Kirby's first game, the Game Boy original before Adventure added copy powers.")
A("kirbys-dream-land-2","Kirby's Dream Land 2","1995",["Game Boy"],"HAL Laboratory / Nintendo",["kirbys-dream-land-2"],"nso",
  "Animal friends combine with copy abilities for puzzles the first Dream Land did not have.",
  "It is the second Game Boy Kirby, between Dream Land and the color sequel.")
A("pokemon-red","Pokemon Red","1996",["Game Boy"],"Game Freak / Nintendo",["pokemon-red"],"nso",
  "A trainer leaves a small town, fills a party, and aims at a league of gym leaders.",
  "This page is Pokemon Red, the 1996 Game Boy game. Blue and Yellow are separate entries. A later remake pair, FireRed and LeafGreen, is on Game Boy Advance.")
A("pokemon-blue","Pokemon Blue","1996",["Game Boy"],"Game Freak / Nintendo",["pokemon-blue"],"nso",
  "The paired version of Red, with a different roster of wild encounters and a different starter story beat.",
  "It is the other half of the 1996 Game Boy pair, not a sequel.")
A("pokemon-yellow","Pokemon Yellow","1998",["Game Boy"],"Game Freak / Nintendo",["pokemon-yellow"],"nso",
  "Pikachu follows on screen and the story leans on the anime's first season.",
  "It is the special Game Boy edition after Red and Blue, still the same generation of monsters.")
A("metroid-ii-return-of-samus","Metroid II: Return of Samus","1991",["Game Boy"],"Nintendo",["metroid-ii-return-of-samus"],"nso",
  "Samus hunts metroids down a vertical nest, with a save that was new for the series.",
  "It is the Game Boy Metroid. Samus Returns on 3DS and later games revisit this mission.")
A("wario-land","Wario Land: Super Mario Land 3","1994",["Game Boy"],"Nintendo",["wario-land-super-mario-land-3","wario-land"],"nso",
  "Wario hunts treasure with a shoulder charge, and the ending changes with how greedy you were.",
  "It is the first Wario Land, still numbered as a Mario Land game, on Game Boy.")
A("links-awakening","The Legend of Zelda: Link's Awakening (1993)","1993",["Game Boy"],"Nintendo",["the-legend-of-zelda-links-awakening-dx","the-legend-of-zelda-links-awakening"],"nso",
  "Link washes up on Koholint Island, which is not Hyrule, and tries to wake the Wind Fish.",
  "This page is the 1993 Game Boy game, including the later color DX edition as the same adventure. The 2019 Switch remake has its own page.")
A("tetris-game-boy","Tetris","1989",["Game Boy"],"Nintendo",["tetris-game-boy","tetris"],"nso",
  "Falling blocks on the handheld that came packed with an enormous number of Game Boys.",
  "This page is the Game Boy Tetris, the version that made the puzzle a portable habit, not a later theme-park edition.")
A("donk-kong-94","Donkey Kong","1994",["Game Boy"],"Nintendo",["donkey-kong-1994","donkey-kong-game-boy"],"nso",
  "The familiar girders are only the first four stages. After that it becomes a puzzle platformer with flips and handstands.",
  "It is the 1994 Game Boy Donkey Kong, not the 1981 arcade game and not Country.")

# --- GBC ---
A("pokemon-gold","Pokemon Gold","1999",["Game Boy Color"],"Game Freak / Nintendo",["pokemon-gold-version","pokemon-gold"],"gbc",
  "A western region, a day-night clock, and two new starter lines follow the first league.",
  "Gold is one half of the 1999 pair. Crystal revisits the same journey and has its own page. HeartGold on DS is a later remake.")
A("pokemon-silver","Pokemon Silver","1999",["Game Boy Color"],"Game Freak / Nintendo",["pokemon-silver-version","pokemon-silver"],"gbc",
  "The paired version of Gold, with legendary and version-exclusive differences.",
  "It is the other 1999 Game Boy Color edition, not a sequel and not the DS remake.")
A("pokemon-crystal","Pokemon Crystal","2000",["Game Boy Color"],"Game Freak / Nintendo",["pokemon-crystal-version","pokemon-crystal"],"gbc",
  "Crystal revisits Johto with animated battles and a story beat the Gold and Silver pair did not offer.",
  "It is the third version of the second generation, still a Game Boy Color game.")
A("oracle-of-ages","The Legend of Zelda: Oracle of Ages","2001",["Game Boy Color"],"Flagship / Nintendo",["the-legend-of-zelda-oracle-of-ages"],"gbc",
  "Time travel changes the map of Labrynna, with puzzles that depend on which era you stand in.",
  "It is one of two linked Game Boy Color Zeldas. Secrets connect it to Oracle of Seasons.")
A("oracle-of-seasons","The Legend of Zelda: Oracle of Seasons","2001",["Game Boy Color"],"Flagship / Nintendo",["the-legend-of-zelda-oracle-of-seasons"],"gbc",
  "A rod of seasons reshapes Holodrum, and the emphasis is action more than Ages' puzzles.",
  "It is the sibling Game Boy Color Zelda, meant to be played beside Oracle of Ages.")
A("wario-land-3","Wario Land 3","2000",["Game Boy Color"],"Nintendo",["wario-land-3"],"gbc",
  "Wario cannot die in the usual way. Getting crushed or burned is how new paths open.",
  "It is the Game Boy Color Wario Land, a puzzle-platformer more than a score attack.")
A("wario-land-2","Wario Land II","1998",["Game Boy Color"],"Nintendo",["wario-land-ii","wario-land-2"],"gbc",
  "Treasure and multiple endings matter more than a life counter.",
  "It straddles Game Boy and Game Boy Color. This catalog files the color-era release with the handheld's second generation of Wario.")
A("mario-tennis-gbc","Mario Tennis","2000",["Game Boy Color"],"Camelot / Nintendo",["mario-tennis-gb","mario-tennis-game-boy-color"],"gbc",
  "A role-playing story mode builds a tennis rookie between matches.",
  "Camelot's Game Boy Color game is the story-heavy sibling of the Nintendo 64 Mario Tennis.")
A("metal-gear-solid-gbc","Metal Gear Solid","2000",["Game Boy Color"],"Konami",["metal-gear-solid-2000","metal-gear-ghost-babel"],"gbc",
  "A stealth mission in the Metal Gear line, built for the handheld rather than ported scene for scene from the console game.",
  "It is Konami's Game Boy Color entry, known in Japan as Ghost Babel.")
A("shantae","Shantae","2002",["Game Boy Color"],"WayForward",["shantae"],"gbc",
  "A half-genie dances through towns and transformations on a late color cartridge.",
  "It is the Game Boy Color original of a series that continued long after the handheld ended.")
A("dragon-warrior-iii-gbc","Dragon Warrior III","2000",["Game Boy Color"],"Enix",["dragon-quest-iii","dragon-warrior-iii"],"gbc",
  "A class-changing party and a world that opens into a second map, in the color remake of an NES epic.",
  "This page is the Game Boy Color edition players used as the portable Dragon Quest III.")
A("pokemon-trading-card-game","Pokemon Trading Card Game","1998",["Game Boy Color"],"Hudson Soft / Nintendo",["pokemon-trading-card-game"],"gbc",
  "A campaign of card battles that teaches a deck, not a creature-collecting league.",
  "It is the Game Boy adaptation of the card game, adjacent to Red and Blue rather than a mainline sequel.")

# --- GBA ---
A("mario-kart-super-circuit","Mario Kart: Super Circuit","2001",["Game Boy Advance"],"Nintendo",["mario-kart-super-circuit"],"gba",
  "Flat, bright courses for a small screen, plus a cup list drawn from Super Mario Kart.",
  "It is the Game Boy Advance Kart, between the Nintendo 64 game and later handheld sequels.")
A("metroid-fusion","Metroid Fusion","2002",["Game Boy Advance"],"Nintendo",["metroid-fusion"],"gba",
  "A more guided Metroid that still hides upgrades off the path it marks for you.",
  "It launched beside Metroid Prime and is the handheld half of that return.")
A("metroid-zero-mission","Metroid: Zero Mission","2004",["Game Boy Advance"],"Nintendo",["metroid-zero-mission"],"gba",
  "A retelling of the first Metroid with a map, shinespark tricks, and a stealth ending the NES game did not have.",
  "It is the Game Boy Advance remake of the NES original, so it has its own page rather than replacing that entry.")
A("minish-cap","The Legend of Zelda: The Minish Cap","2004",["Game Boy Advance"],"Flagship / Nintendo",["the-legend-of-zelda-the-minish-cap"],"gba",
  "Towns and dungeons change scale when Link shrinks to the size of the Minish.",
  "It is a complete Game Boy Advance Zelda, not a port of an earlier console game.")
A("golden-sun","Golden Sun","2001",["Game Boy Advance"],"Camelot",["golden-sun"],"gba",
  "Djinn collectibles reshape both puzzles and a class system in a bright role-playing game.",
  "Camelot's first Golden Sun is the Game Boy Advance original. The Lost Age continues the same story.")
A("golden-sun-the-lost-age","Golden Sun: The Lost Age","2002",["Game Boy Advance"],"Camelot",["golden-sun-the-lost-age"],"gba",
  "A second party crosses the sea and links back to the first game's save.",
  "It is the direct sequel, still on Game Boy Advance, and the end of the story the first cartridge started.")
A("advance-wars","Advance Wars","2001",["Game Boy Advance"],"Intelligent Systems / Nintendo",["advance-wars"],"gba",
  "Turn-based army maps where each commanding officer bends the same units in a different way.",
  "It is the Game Boy Advance strategy game that introduced many players to the Wars series. A much later Switch collection revisits the early games.")
A("advance-wars-2","Advance Wars 2: Black Hole Rising","2003",["Game Boy Advance"],"Intelligent Systems / Nintendo",["advance-wars-2-black-hole-rising"],"gba",
  "A new enemy faction and more COs extend the map-by-map campaign.",
  "It is the second Game Boy Advance Advance Wars, not the DS Dual Strike.")
A("pokemon-ruby","Pokemon Ruby","2002",["Game Boy Advance"],"Game Freak / Nintendo",["pokemon-ruby-version","pokemon-ruby"],"gba",
  "A new region of contests, secret bases, and a weather-themed legendary.",
  "Ruby is one half of the 2002 pair. Emerald is the third version. Omega Ruby on 3DS is a later remake.")
A("pokemon-sapphire","Pokemon Sapphire","2002",["Game Boy Advance"],"Game Freak / Nintendo",["pokemon-sapphire-version","pokemon-sapphire"],"gba",
  "The paired version of Ruby, with a different legendary and version-exclusive teams.",
  "It is the other 2002 Game Boy Advance edition, not the 3DS remake.")
A("pokemon-emerald","Pokemon Emerald","2004",["Game Boy Advance"],"Game Freak / Nintendo",["pokemon-emerald-version","pokemon-emerald"],"gba",
  "The third Hoenn version, with a battle frontier and a story that uses both legendaries.",
  "It is the refined Game Boy Advance edition of the third generation.")
A("pokemon-firered","Pokemon FireRed","2004",["Game Boy Advance"],"Game Freak / Nintendo",["pokemon-firered-version","pokemon-fire-red"],"gba",
  "A remake of the 1996 Kanto journey, with the advance generation's mechanics and a post-game island.",
  "This page is the 2004 remake, not Pokemon Red. LeafGreen is the paired remake.")
A("pokemon-leafgreen","Pokemon LeafGreen","2004",["Game Boy Advance"],"Game Freak / Nintendo",["pokemon-leafgreen-version","pokemon-leaf-green"],"gba",
  "The paired remake of Blue, built to link with FireRed.",
  "It is the other 2004 Kanto remake on Game Boy Advance.")
A("mario-and-luigi-superstar-saga","Mario & Luigi: Superstar Saga","2003",["Game Boy Advance"],"AlphaDream / Nintendo",["mario-luigi-superstar-saga"],"gba",
  "Brothers share timed jumps and hammers in a comedy RPG set in a neighboring kingdom.",
  "It opens the Mario & Luigi series on Game Boy Advance. A 3DS remake exists as its own later entry.")
A("warioware-inc","WarioWare, Inc.: Mega Microgame$!","2003",["Game Boy Advance"],"Nintendo",["warioware-inc-mega-microgames","wario-ware-inc"],"gba",
  "Seconds-long microgames pile up until the speed is the joke.",
  "It is the first WarioWare, the Game Boy Advance original of a series that spread to every later Nintendo handheld and home console.")
A("wario-land-4","Wario Land 4","2001",["Game Boy Advance"],"Nintendo",["wario-land-4"],"gba",
  "A jewel hunt with a timer that starts only after you decide to escape the level.",
  "It is the Game Boy Advance Wario Land, louder and more animated than the color games.")
A("fire-emblem","Fire Emblem","2003",["Game Boy Advance"],"Intelligent Systems / Nintendo",["fire-emblem"],"gba",
  "Permadeath tactics on a grid, and the first Fire Emblem released in North America.",
  "It is the Game Boy Advance game simply titled Fire Emblem, known in Japan as The Blazing Blade.")
A("fire-emblem-the-sacred-stones","Fire Emblem: The Sacred Stones","2004",["Game Boy Advance"],"Intelligent Systems / Nintendo",["fire-emblem-the-sacred-stones"],"gba",
  "A smaller cast and a world map of optional fights distinguish this campaign.",
  "It is the other widely released Game Boy Advance Fire Emblem, separate from the first Western release.")
A("kirby-and-the-amazing-mirror","Kirby & the Amazing Mirror","2004",["Game Boy Advance"],"HAL Laboratory / Nintendo",["kirby-the-amazing-mirror"],"gba",
  "A maze of connected rooms and multiple Kirbys, closer to exploration than a straight stage list.",
  "It is the Game Boy Advance Kirby that plays least like a linear platformer.")
A("kirby-nightmare-in-dream-land","Kirby: Nightmare in Dream Land","2002",["Game Boy Advance"],"HAL Laboratory / Nintendo",["kirby-nightmare-in-dream-land"],"gba",
  "A remake of Kirby's Adventure with extra modes and cleaner sprites.",
  "This page is the Game Boy Advance remake. The NES Adventure remains its own entry.")
A("castlevania-aria-of-sorrow","Castlevania: Aria of Sorrow","2003",["Game Boy Advance"],"Konami",["castlevania-aria-of-sorrow"],"gba",
  "A future protagonist absorbs enemy souls in a castle you can map at your own pace.",
  "It is the Game Boy Advance Castlevania most often named with Symphony of the Night's explorative style.")
A("the-legend-of-zelda-a-link-to-the-past-four-swords","The Legend of Zelda: A Link to the Past & Four Swords","2002",["Game Boy Advance"],"Nintendo",["the-legend-of-zelda-a-link-to-the-past-four-swords"],"gba",
  "A portable Link to the Past shares a cartridge with a multiplayer Four Swords quest.",
  "It is the Game Boy Advance release, a reissue plus a new mode, not a replacement for the SNES page.")
A("final-fantasy-tactics-advance","Final Fantasy Tactics Advance","2003",["Game Boy Advance"],"Square",["final-fantasy-tactics-advance"],"gba",
  "Clan laws and a snow-globe world of jobs, built for short handheld maps.",
  "It is the Game Boy Advance tactics game, a spin on the earlier PlayStation Tactics rather than that game's port.")
A("mother-3","Mother 3","2006",["Game Boy Advance"],"Nintendo / Brownie Brown / HAL Laboratory",["mother-3"],"gba",
  "A rhythm-timed battle system and a story told in chapters, released in Japan and never officially localized at the time.",
  "It is the Game Boy Advance sequel to EarthBound, and the last Mother game.")

# --- GameCube ---
A("pikmin","Pikmin","2001",["GameCube"],"Nintendo",["pikmin"],"gc",
  "A tiny explorer directs plant-animal helpers to carry cargo before the day's sunlight ends.",
  "It is the GameCube original. Nintendo later collected the first two Pikmin games in an official Switch release. This page does not claim that collection's current listing.")
A("pikmin-2","Pikmin 2","2004",["GameCube"],"Nintendo",["pikmin-2"],"gc",
  "Debt collection replaces the strict day limit, and caves drop you into longer dungeons.",
  "It is the GameCube sequel. The later Switch collection pairs it with the first game.")
A("metroid-prime","Metroid Prime","2002",["GameCube"],"Retro Studios / Nintendo",["metroid-prime"],"gc",
  "First-person exploration of a ruined planet, with a scan visor and suits that reopen old rooms.",
  "It is the GameCube original. Metroid Prime Remastered on Switch is a separate page, not a replacement for this one.")
A("metroid-prime-2-echoes","Metroid Prime 2: Echoes","2004",["GameCube"],"Retro Studios / Nintendo",["metroid-prime-2-echoes"],"gc",
  "Light and dark worlds share a map, and ammunition is a resource the first Prime did not press as hard.",
  "It is the GameCube sequel, still a Retro Studios Metroid.")
A("super-mario-sunshine","Super Mario Sunshine","2002",["GameCube"],"Nintendo",["super-mario-sunshine"],"gc",
  "Mission-based tropical stages and a water pack that sprays, hovers, and cleans goop.",
  "It is the GameCube 3D Mario. A limited Switch compilation, Super Mario 3D All-Stars, included it for a time and is not treated here as a standing listing.")
A("legend-of-zelda-the-wind-waker","The Legend of Zelda: The Wind Waker","2002",["GameCube"],"Nintendo",["the-legend-of-zelda-the-wind-waker"],"gc",
  "A cartoon sea of islands, a conducting baton, and a boat that is the overworld.",
  "It is the GameCube original. Wind Waker HD on Wii U is a separate page.")
A("super-smash-bros-melee","Super Smash Bros. Melee","2001",["GameCube"],"HAL Laboratory / Nintendo",["super-smash-bros-melee"],"gc",
  "A faster Smash with wavedashing culture, trophies, and a much larger roster than the Nintendo 64 game.",
  "It is the GameCube Smash, the competitive center of the series for years.")
A("luigis-mansion","Luigi's Mansion","2001",["GameCube"],"Nintendo",["luigis-mansion"],"gc",
  "Luigi vacuums ghosts in a flashlight tour of a locked house, room by room.",
  "It is the GameCube launch game that started the Luigi's Mansion series. Later numbered games are sequels, not this mansion.")
A("animal-crossing","Animal Crossing","2001",["GameCube"],"Nintendo",["animal-crossing"],"gc",
  "A town on a real-time clock, neighbors who move away, and letters instead of a win screen.",
  "It is the first Animal Crossing released in the West, on GameCube. New Horizons and the handheld towns are separate games.")
A("paper-mario-the-thousand-year-door","Paper Mario: The Thousand-Year Door","2004",["GameCube"],"Intelligent Systems / Nintendo",["paper-mario-the-thousand-year-door"],"gc",
  "Stage-play battles and a rogue's gallery of partners under a cursed town.",
  "It is the GameCube Paper Mario. A 2024 Switch remake has its own page.")
A("f-zero-gx","F-Zero GX","2003",["GameCube"],"Amusement Vision / Nintendo",["f-zero-gx"],"gc",
  "Extremely fast tracks and a story mode of cruel license tests.",
  "It is the GameCube F-Zero, developed with Sega's Amusement Vision, and the last mainline game for a long time.")
A("pokemon-colosseum","Pokemon Colosseum","2003",["GameCube"],"Genius Sonority / Nintendo",["pokemon-colosseum"],"gc",
  "A snagged team of shadow Pokemon in a 3D desert story, not a traditional gym quest.",
  "It is a GameCube spin-off that uses the handheld creatures in a console campaign.")
A("pokemon-xd-gale-of-darkness","Pokemon XD: Gale of Darkness","2005",["GameCube"],"Genius Sonority / Nintendo",["pokemon-xd-gale-of-darkness"],"gc",
  "A follow-up campaign about purifying shadow Pokemon, with a deeper roster than Colosseum.",
  "It is the second GameCube Pokemon story RPG from Genius Sonority.")
A("super-mario-strikers","Super Mario Strikers","2005",["GameCube"],"Next Level Games / Nintendo",["super-mario-strikers"],"gc",
  "Arcade soccer with items and tackles that would not pass a referee.",
  "It is the GameCube original of the Strikers line. Later charged-up sequels are separate games.")
A("kirby-air-ride","Kirby Air Ride","2003",["GameCube"],"HAL Laboratory / Nintendo",["kirby-air-ride"],"gc",
  "A simple accelerator and a city mode where stats permanently change how you ride.",
  "It is the GameCube Kirby racer, unusual in the series for how little it explains itself.")
A("fire-emblem-path-of-radiance","Fire Emblem: Path of Radiance","2005",["GameCube"],"Intelligent Systems / Nintendo",["fire-emblem-path-of-radiance"],"gc",
  "Ike's mercenary company in a 3D tactics story with a laguz and beorc cast.",
  "It is the GameCube Fire Emblem. Radiant Dawn on Wii continues the same war.")
A("resident-evil-4","Resident Evil 4","2005",["GameCube"],"Capcom",["resident-evil-4"],"gc",
  "An over-the-shoulder shooter that debuted on GameCube before it spread to other hardware.",
  "This page is the 2005 GameCube original, not the later remake. It is here because the home debut was a Nintendo console.")
A("tales-of-symphonia","Tales of Symphonia","2003",["GameCube"],"Namco",["tales-of-symphonia"],"gc",
  "A real-time party RPG about a chosen one and a world split into two realms.",
  "The GameCube release is the original home version of this Tales story.")
A("eternal-darkness","Eternal Darkness: Sanity's Requiem","2002",["GameCube"],"Silicon Knights / Nintendo",["eternal-darkness-sanitys-requiem"],"gc",
  "A horror story told across centuries, with sanity effects that break the screen as well as the character.",
  "It is a Nintendo-published GameCube exclusive and a one-off, not a series entry with a sequel in this catalog.")
A("chibi-robo","Chibi-Robo!","2005",["GameCube"],"Skip Ltd. / Nintendo",["chibi-robo"],"gc",
  "A tiny robot cleans a house, earns happy points, and learns the family's problems at appliance scale.",
  "It is the GameCube original of a small Nintendo-published series.")
A("viewtiful-joe","Viewtiful Joe","2003",["GameCube"],"Clover Studio / Capcom",["viewtiful-joe"],"gc",
  "A side-scrolling brawler that slows time when the hero strikes a pose.",
  "It debuted on GameCube before other versions, which is why this catalog files it here.")
A("soulcalibur-ii","SoulCalibur II","2003",["GameCube"],"Namco",["soulcalibur-ii"],"gc",
  "Weapon fighters and a guest character, Link, in the GameCube edition of the 2002 fighter.",
  "This page is the GameCube version, kept because that edition's guest fighter is a Nintendo character. It is not a Nintendo-made game.")

# --- Wii ---
A("super-mario-galaxy","Super Mario Galaxy","2007",["Wii"],"Nintendo",["super-mario-galaxy"],"legacy",
  "Small planets with their own gravity, and a hub observatory between orchestral set pieces.",
  "It is the Wii 3D Mario. Super Mario Galaxy 2 is a different game. A limited Switch compilation included the first Galaxy for a time.")
A("super-mario-galaxy-2","Super Mario Galaxy 2","2010",["Wii"],"Nintendo",["super-mario-galaxy-2"],"legacy",
  "A sequel that returns to planetoids and adds Yoshi, with a world map instead of the first game's observatory story.",
  "It is its own Wii game, not a level pack inside the first Galaxy. This page does not claim a current re-release.")
A("wii-sports","Wii Sports","2006",["Wii"],"Nintendo",["wii-sports"],"legacy",
  "Tennis, bowling, baseball, golf, and boxing played with motion, and the pack-in that taught the Wii remote.",
  "It is the Wii launch sports game. Wii Sports Resort and Nintendo Switch Sports are separate entries.")
A("wii-sports-resort","Wii Sports Resort","2009",["Wii"],"Nintendo",["wii-sports-resort"],"legacy",
  "Swordplay, archery, and cycling on an island, built for the MotionPlus add-on.",
  "It is the Wii follow-up to Wii Sports, not the Switch sports game.")
A("wii-fit","Wii Fit","2007",["Wii"],"Nintendo",["wii-fit"],"legacy",
  "Balance-board exercises and a body-test score, sold as a fitness routine rather than a win-the-game campaign.",
  "It is the Wii original. Later Fit follow-ups are separate products.")
A("new-super-mario-bros-wii","New Super Mario Bros. Wii","2009",["Wii"],"Nintendo",["new-super-mario-bros-wii"],"legacy",
  "Four players share a side-scrolling map, with a midair spin carried over from the DS game's idea of 2D Mario.",
  "It is the Wii entry in the New Super Mario Bros. line, between the DS original and the Wii U game.")
A("super-smash-bros-brawl","Super Smash Bros. Brawl","2008",["Wii"],"Sora Ltd. / Nintendo",["super-smash-bros-brawl"],"legacy",
  "A large roster, a story mode called the Subspace Emissary, and stage hazards turned up.",
  "It is the Wii Smash, between Melee and the 3DS and Wii U games.")
A("mario-kart-wii","Mario Kart Wii","2008",["Wii"],"Nintendo",["mario-kart-wii"],"legacy",
  "Bikes, wheel-shaped shells, and online play in the Kart that sold with a plastic wheel.",
  "It is the Wii Mario Kart, not Mario Kart 8.")
A("xenoblade-chronicles","Xenoblade Chronicles","2010",["Wii"],"Monolith Soft / Nintendo",["xenoblade-chronicles"],"legacy",
  "A huge world on the bodies of two titans, with combat that auto-attacks while you time arts.",
  "It is the Wii original. Xenoblade Chronicles: Definitive Edition on Switch is a separate page.")
A("twilight-princess","The Legend of Zelda: Twilight Princess","2006",["Wii","GameCube"],"Nintendo",["the-legend-of-zelda-twilight-princess"],"legacy",
  "A wolf form, a darker Hyrule, and a launch-window Wii adventure that also shipped on GameCube.",
  "This one page covers both 2006 releases. Twilight Princess HD on Wii U is a separate remaster page.")
A("skyward-sword","The Legend of Zelda: Skyward Sword","2011",["Wii"],"Nintendo",["the-legend-of-zelda-skyward-sword"],"legacy",
  "A sky of islands above a surface you unlock in regions, played with motion sword swings.",
  "It is the Wii original. Skyward Sword HD on Switch is a separate page.")
A("metroid-prime-3-corruption","Metroid Prime 3: Corruption","2007",["Wii"],"Retro Studios / Nintendo",["metroid-prime-3-corruption"],"legacy",
  "Samus travels several planets while a corruption meter rewards and punishes hypermode.",
  "It is the Wii close of the original Prime trilogy.")
A("donkey-kong-country-returns","Donkey Kong Country Returns","2010",["Wii","Nintendo 3DS"],"Retro Studios / Nintendo",["donkey-kong-country-returns"],"legacy",
  "Mine carts, rocket barrels, and levels that expect both Kongs, in a return Retro built for Wii.",
  "This page is the Wii game, which also had a 3DS version. Donkey Kong Country Returns HD is a separate Switch page.")
A("kirbys-epic-yarn","Kirby's Epic Yarn","2010",["Wii"],"Good-Feel / HAL Laboratory / Nintendo",["kirbys-epic-yarn"],"legacy",
  "A yarn world where Kirby cannot die in the usual way, and the goal is beads and patches.",
  "It is the Wii Kirby by Good-Feel. A later 3DS port exists; this page is the Wii original.")
A("animal-crossing-city-folk","Animal Crossing: City Folk","2008",["Wii"],"Nintendo",["animal-crossing-city-folk","animal-crossing-lets-go-to-the-city"],"legacy",
  "A Wii town with a city you visit by bus, and voice chat that the series later dropped.",
  "It is the Wii Animal Crossing, between the GameCube original and the 3DS New Leaf.")
A("super-paper-mario","Super Paper Mario","2007",["Wii"],"Intelligent Systems / Nintendo",["super-paper-mario"],"legacy",
  "A side-scroller that flips into 3D, closer to an action game than the turn-based Paper Mario stories.",
  "It is the Wii Paper Mario, a departure from the GameCube Thousand-Year Door.")
A("punch-out-wii","Punch-Out!!","2009",["Wii"],"Next Level Games / Nintendo",["punch-out-wii","punch-out-2009"],"legacy",
  "A return to Little Mac's tells and glass jaws, with motion controls that can be turned down.",
  "It is the Wii Punch-Out!!, a revival of the NES career rather than a new sport.")
A("no-more-heroes","No More Heroes","2007",["Wii"],"Grasshopper Manufacture",["no-more-heroes"],"legacy",
  "An assassin ranks up by earning cash at odd jobs between motion-sword duels.",
  "It is the Wii original from Grasshopper Manufacture, a third-party game that became a series on Nintendo platforms.")
A("monster-hunter-tri","Monster Hunter Tri","2009",["Wii"],"Capcom",["monster-hunter-3","monster-hunter-tri"],"legacy",
  "Underwater fights and a village hub in the Monster Hunter that brought the series to a wide Nintendo audience.",
  "It is the Wii entry. Later portable Monster Hunter games are separate.")
A("fire-emblem-radiant-dawn","Fire Emblem: Radiant Dawn","2007",["Wii"],"Intelligent Systems / Nintendo",["fire-emblem-radiant-dawn"],"legacy",
  "Three armies and a huge cast continue the Path of Radiance war on Wii.",
  "It is the direct sequel to the GameCube Fire Emblem, and one of the largest games in the series.")
A("sin-and-punishment-star-successor","Sin & Punishment: Star Successor","2009",["Wii"],"Treasure",["sin-punishment-star-successor"],"legacy",
  "A sequel to the Nintendo 64 rail shooter, with a partner character and the same stick-aim idea.",
  "It is Treasure's Wii follow-up, not a remake of the 2000 game.")
A("the-last-story","The Last Story","2011",["Wii"],"Mistwalker / Nintendo",["the-last-story"],"legacy",
  "A mercenary band in a dying-magic city, with cover-based command battles.",
  "Mistwalker's late Wii RPG, published by Nintendo in the West, alongside that era's Xenoblade and Pandora's Tower.")

# --- Wii U ---
A("super-mario-3d-world","Super Mario 3D World","2013",["Wii U","Nintendo Switch"],"Nintendo",["super-mario-3d-world"],"legacy",
  "Clear courses, a cat suit, and a pace closer to 2D Mario than to the sandbox 3D games.",
  "This page covers the 2013 Wii U game and the later Switch edition, which adds Bowser's Fury as an extra story rather than a replacement.")
A("pikmin-3","Pikmin 3","2013",["Wii U"],"Nintendo",["pikmin-3"],"legacy",
  "Three captains split squads across a garden to bring fruit home before juice runs out.",
  "It is the Wii U Pikmin. Pikmin 3 Deluxe on Switch is a separate page.")
A("mario-kart-8","Mario Kart 8","2014",["Wii U"],"Nintendo",["mario-kart-8"],"legacy",
  "Anti-gravity tracks and a living-room roster on Wii U, before the Switch Deluxe edition.",
  "This page is the Wii U original. Mario Kart 8 Deluxe is its own Switch entry.")
A("splatoon","Splatoon","2015",["Wii U"],"Nintendo",["splatoon"],"legacy",
  "Teams shoot ink to claim ground, and the match ends when the paint does.",
  "It is the Wii U original of a series whose sequels, Splatoon 2 and Splatoon 3, are Switch games.")
A("super-smash-bros-for-wii-u","Super Smash Bros. for Wii U","2014",["Wii U"],"Bandai Namco / Sora Ltd. / Nintendo",["super-smash-bros-for-wii-u"],"legacy",
  "The home-console half of the pair that also shipped on 3DS, with larger stages.",
  "It is the Wii U Smash. The 3DS version is a separate page, and Ultimate on Switch is a later game.")
A("donkey-kong-country-tropical-freeze","Donkey Kong Country: Tropical Freeze","2014",["Wii U","Nintendo Switch"],"Retro Studios / Nintendo",["donkey-kong-country-tropical-freeze"],"legacy",
  "Cold-themed levels and a Dixie partner in the Country game Retro made after Returns.",
  "This page names both the 2014 Wii U original and the later Switch port of the same game.")
A("wind-waker-hd","The Legend of Zelda: The Wind Waker HD","2013",["Wii U"],"Nintendo",["the-legend-of-zelda-the-wind-waker-hd"],"legacy",
  "A higher-resolution sail across the same sea, with a quicker boat and the same cartoon look.",
  "It is the Wii U remaster. The 2002 GameCube original has its own page.")
A("twilight-princess-hd","The Legend of Zelda: Twilight Princess HD","2016",["Wii U"],"Nintendo",["the-legend-of-zelda-twilight-princess-hd"],"legacy",
  "The 2006 adventure rebuilt for a higher resolution, with amiibo extras that the original did not have.",
  "It is the Wii U remaster. The Wii and GameCube original is a different page.")
A("xenoblade-chronicles-x","Xenoblade Chronicles X","2015",["Wii U"],"Monolith Soft / Nintendo",["xenoblade-chronicles-x"],"legacy",
  "A frontier planet, a customizable avatar, and a transforming doll mech.",
  "It is the Wii U spin on Xenoblade, separate from the numbered Shulk story. A later Definitive Edition is its own page.")
A("bayonetta-2","Bayonetta 2","2014",["Wii U","Nintendo Switch"],"PlatinumGames / Nintendo",["bayonetta-2"],"legacy",
  "A spectacle fighter published by Nintendo, about a witch who uses her hair as a weapon.",
  "This page covers the Wii U original and the Switch version of the same game. Bayonetta 3 is a sequel.")
A("captain-toad-treasure-tracker","Captain Toad: Treasure Tracker","2014",["Wii U","Nintendo Switch"],"Nintendo",["captain-toad-treasure-tracker"],"legacy",
  "Diaphragm puzzles: rotate a small diorama and walk Toad to the star without jumping.",
  "It grew out of Super Mario 3D World levels. This page names the Wii U original and the Switch port.")
A("yoshis-woolly-world","Yoshi's Woolly World","2015",["Wii U"],"Good-Feel / Nintendo",["yoshis-woolly-world"],"legacy",
  "Yarn Yoshis unravel secrets in craft-textured stages.",
  "It is the Wii U Good-Feel game. A 3DS version with Poochy followed; this page is the home-console original.")
A("new-super-mario-bros-u","New Super Mario Bros. U","2012",["Wii U"],"Nintendo",["new-super-mario-bros-u"],"legacy",
  "A side-scrolling Mario that uses the GamePad for boost blocks when a second player wants them.",
  "It is the Wii U game. New Super Mario Bros. U Deluxe on Switch is a separate page.")
A("nintendo-land","Nintendo Land","2012",["Wii U"],"Nintendo",["nintendo-land"],"legacy",
  "A theme-park of attractions that show off the GamePad, from a ghost house to a Luigi mansion minigame.",
  "It is the Wii U launch compilation, a pack-in for many deluxe sets.")
A("super-mario-maker","Super Mario Maker","2015",["Wii U"],"Nintendo",["super-mario-maker"],"legacy",
  "A tool for building and sharing 2D Mario stages in the styles of several earlier games.",
  "It is the Wii U original. Super Mario Maker 2 on Switch is a sequel, not this tool.")
A("splatoon-note-star-fox-zero","Star Fox Zero","2016",["Wii U"],"Nintendo / PlatinumGames",["star-fox-zero"],"legacy",
  "A cockpit drawn on the GamePad and a TV view that does not always agree with it.",
  "It is the Wii U Star Fox, a retelling rather than Star Fox 64, and a late game for the console.")
A("paper-mario-color-splash","Paper Mario: Color Splash","2016",["Wii U"],"Intelligent Systems / Nintendo",["paper-mario-color-splash"],"legacy",
  "Paint restores a paper island, and battles are card-based rather than the old partner system.",
  "It is the Wii U Paper Mario, between Sticker Star and the Switch Origami King.")
A("the-wonderful-101","The Wonderful 101","2013",["Wii U"],"PlatinumGames / Nintendo",["the-wonderful-101"],"legacy",
  "A crowd of heroes forms a giant fist, sword, or gun when you draw the shape.",
  "It is the Wii U PlatinumGames game published with Nintendo. A later remastered edition exists; this page is the Wii U original.")
A("hyrule-warriors","Hyrule Warriors","2014",["Wii U"],"Omega Force / Team Ninja / Nintendo",["hyrule-warriors"],"legacy",
  "Musou crowds and Zelda characters on big battlefields, a crossover rather than a mainline quest.",
  "It is the Wii U original. Definitive Edition on Switch is a separate, expanded page.")

# --- DS ---
A("new-super-mario-bros","New Super Mario Bros.","2006",["Nintendo DS"],"Nintendo",["new-super-mario-bros"],"legacy",
  "A return to side-scrolling Mario on two screens, with a wall jump and a huge mushroom.",
  "It restarted 2D Mario on DS and led to the Wii, Wii U, and later Deluxe games.")
A("mario-kart-ds","Mario Kart DS","2005",["Nintendo DS"],"Nintendo",["mario-kart-ds"],"legacy",
  "Mission mode and online play on a handheld, with courses that use both screens for a map.",
  "It is the DS Mario Kart, between Super Circuit and Mario Kart 7.")
A("nintendogs","Nintendogs","2005",["Nintendo DS"],"Nintendo",["nintendogs"],"legacy",
  "A puppy you train with the touch screen and the microphone, on a real-time clock.",
  "It is the DS pet simulation that was a launch-era phenomenon. Later + Cats on 3DS is a sequel.")
A("animal-crossing-wild-world","Animal Crossing: Wild World","2005",["Nintendo DS"],"Nintendo",["animal-crossing-wild-world"],"legacy",
  "A pocket town you can visit online, smaller than the GameCube village and always in your bag.",
  "It is the DS Animal Crossing, between the GameCube original and City Folk.")
A("pokemon-diamond","Pokemon Diamond","2006",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-diamond-version","pokemon-diamond"],"legacy",
  "A Sinnoh journey with a physical-special split that changed how moves work.",
  "Diamond is one half of the 2006 pair. Platinum is the third version. Brilliant Diamond on Switch is a remake with its own page.")
A("pokemon-pearl","Pokemon Pearl","2006",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-pearl-version","pokemon-pearl"],"legacy",
  "The paired Sinnoh version, with a different legendary and a different wild roster.",
  "It is the other 2006 DS edition, not the Switch remake.")
A("pokemon-platinum","Pokemon Platinum","2008",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-platinum-version","pokemon-platinum"],"legacy",
  "The third Sinnoh version, with a distortion world and a fuller story.",
  "It is the refined DS edition of the fourth generation.")
A("pokemon-heartgold","Pokemon HeartGold","2009",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-heartgold-version","pokemon-heart-gold"],"legacy",
  "A remake of Gold in which a chosen Pokemon walks behind you and Johto leads into Kanto.",
  "This page is the 2009 DS remake, not Pokemon Gold.")
A("pokemon-soulsilver","Pokemon SoulSilver","2009",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-soulsilver-version","pokemon-soul-silver"],"legacy",
  "The paired remake of Silver, built to match HeartGold's walking companion and two regions.",
  "It is the other 2009 DS remake.")
A("pokemon-black","Pokemon Black","2010",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-black-version","pokemon-black"],"legacy",
  "A region that questions whether trainers should catch creatures at all, with seasons on the calendar.",
  "Black is one half of the 2010 pair. Black 2 is a sequel, not a third version.")
A("pokemon-white","Pokemon White","2010",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-white-version","pokemon-white"],"legacy",
  "The paired Unova version, with a different legendary and a city that changes after the story.",
  "It is the other 2010 DS edition.")
A("pokemon-black-2","Pokemon Black 2","2012",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-black-2","pokemon-black-version-2"],"legacy",
  "A direct sequel set two years later, which the series had not done for a paired edition before.",
  "It is the DS follow-up to Black, not a remake.")
A("pokemon-white-2","Pokemon White 2","2012",["Nintendo DS"],"Game Freak / Nintendo",["pokemon-white-2","pokemon-white-version-2"],"legacy",
  "The paired sequel to White, sharing Black 2's two-years-later Unova.",
  "It is the other 2012 DS sequel.")
A("phantom-hourglass","The Legend of Zelda: Phantom Hourglass","2007",["Nintendo DS"],"Nintendo",["the-legend-of-zelda-phantom-hourglass"],"legacy",
  "Touch-screen sailing and a temple you revisit on a timer, in a sequel to Wind Waker's sea.",
  "It is the DS Zelda that follows Link after The Wind Waker.")
A("spirit-tracks","The Legend of Zelda: Spirit Tracks","2009",["Nintendo DS"],"Nintendo",["the-legend-of-zelda-spirit-tracks"],"legacy",
  "A train replaces the boat, and Zelda is a spirit partner rather than a distant goal.",
  "It is the second DS Zelda in the Wind Waker's art style, and a different adventure from Phantom Hourglass.")
A("super-mario-64-ds","Super Mario 64 DS","2004",["Nintendo DS"],"Nintendo",["super-mario-64-ds"],"legacy",
  "Four characters replay the castle, with touch controls and extra stars the Nintendo 64 game did not have.",
  "It is the DS reworking. The 1996 Nintendo 64 game remains its own page.")
A("mario-luigi-bowsers-inside-story","Mario & Luigi: Bowser's Inside Story","2009",["Nintendo DS"],"AlphaDream / Nintendo",["mario-luigi-bowsers-inside-story"],"legacy",
  "Mario and Luigi explore Bowser's body while Bowser fights on the top screen.",
  "It is the DS Mario & Luigi. A 3DS remake later revisited it.")
A("mario-luigi-partners-in-time","Mario & Luigi: Partners in Time","2005",["Nintendo DS"],"AlphaDream / Nintendo",["mario-luigi-partners-in-time"],"legacy",
  "Adult brothers team with their baby selves across two screens.",
  "It is the DS follow-up to Superstar Saga.")
A("kirby-super-star-ultra","Kirby Super Star Ultra","2008",["Nintendo DS"],"HAL Laboratory / Nintendo",["kirby-super-star-ultra"],"legacy",
  "An expanded remake of the SNES Kirby Super Star, with extra games on the cart.",
  "This page is the DS edition. The SNES original has its own entry.")
A("kirby-canvas-curse","Kirby: Canvas Curse","2005",["Nintendo DS"],"HAL Laboratory / Nintendo",["kirby-canvas-curse"],"legacy",
  "You draw paths for a ball of Kirby instead of moving him directly.",
  "It is the DS Kirby built entirely around the touch screen.")
A("metroid-prime-hunters","Metroid Prime Hunters","2006",["Nintendo DS"],"Nintendo",["metroid-prime-hunters"],"legacy",
  "A bounty-hunter shooter on two screens, with local wireless fights.",
  "It is the DS Prime spin-off, not a numbered console sequel.")
A("the-world-ends-with-you","The World Ends with You","2007",["Nintendo DS"],"Square Enix / Jupiter",["the-world-ends-with-you"],"legacy",
  "Two-screen battles in Shibuya, fashion pins for powers, and a week-long deadline.",
  "It is the DS original. Later ports and a sequel exist; this page is the 2007 handheld game.")
A("chrono-trigger-ds","Chrono Trigger","2008",["Nintendo DS"],"Square Enix",["chrono-trigger-ds"],"legacy",
  "The SNES time-travel RPG on DS, with added scenes and a dual-screen map.",
  "This page is the 2008 DS edition. The SNES original remains a separate entry.")
A("phoenix-wright-ace-attorney","Phoenix Wright: Ace Attorney","2005",["Nintendo DS"],"Capcom",["phoenix-wright-ace-attorney","ace-attorney"],"legacy",
  "Courtroom objections and crime-scene searches, in the first Ace Attorney released widely on DS.",
  "It is Capcom's DS adventure that opened the series for many players outside Japan.")
A("professor-layton-and-the-curious-village","Professor Layton and the Curious Village","2007",["Nintendo DS"],"Level-5 / Nintendo",["professor-layton-and-the-curious-village"],"legacy",
  "A gentleman puzzle hunt wrapped in a village mystery.",
  "It is the first Layton game in the DS line, published by Nintendo in the West.")
A("elite-beat-agents","Elite Beat Agents","2006",["Nintendo DS"],"iNiS / Nintendo",["elite-beat-agents"],"legacy",
  "Touch-screen rhythm scenes about agents who fix lives by hitting marks on a song.",
  "It is the Western sibling of Ouendan, a DS rhythm game published by Nintendo.")
A("ghost-trick","Ghost Trick: Phantom Detective","2010",["Nintendo DS"],"Capcom",["ghost-trick-phantom-detective"],"legacy",
  "A dead man possesses objects to rewind the four minutes before a death.",
  "It is Shu Takumi's DS puzzle adventure, from the Ace Attorney director, and its own story.")
A("999-nine-hours-nine-persons-nine-doors","Nine Hours, Nine Persons, Nine Doors","2009",["Nintendo DS"],"Chunsoft",["nine-hours-nine-persons-nine-doors"],"legacy",
  "Escape-room puzzles on a sinking ship, with story branches that need more than one ending.",
  "It is the DS original of the Zero Escape series.")
A("rhythm-heaven","Rhythm Heaven","2008",["Nintendo DS"],"Nintendo",["rhythm-heaven"],"legacy",
  "Short rhythm scenes that use a tap, with a flick that the DS hardware made the joke.",
  "It is the DS Rhythm Heaven, between the GBA game that stayed in Japan and the later Wii and 3DS entries.")
A("advance-wars-dual-strike","Advance Wars: Dual Strike","2005",["Nintendo DS"],"Intelligent Systems / Nintendo",["advance-wars-dual-strike"],"legacy",
  "Two COs share a battle across both screens.",
  "It is the DS Advance Wars, the follow-up to the Game Boy Advance pair.")
A("dragon-quest-ix","Dragon Quest IX: Sentinels of the Starry Skies","2009",["Nintendo DS"],"Level-5 / Square Enix",["dragon-quest-ix-sentinels-of-the-starry-skies"],"legacy",
  "A class-changing party and street-pass guests in a huge handheld Dragon Quest.",
  "It is the DS mainline Dragon Quest, built for local play as much as a solo story.")
A("castlevania-dawn-of-sorrow","Castlevania: Dawn of Sorrow","2005",["Nintendo DS"],"Konami",["castlevania-dawn-of-sorrow"],"legacy",
  "Soma returns, and magic seals ask you to draw on the touch screen to finish a boss.",
  "It is the DS sequel to Aria of Sorrow.")

# Existing Switch / 3DS slugs that must stay stable
A("breath-of-the-wild","The Legend of Zelda: Breath of the Wild","2017",["Nintendo Switch","Wii U"],"Nintendo",["the-legend-of-zelda-breath-of-the-wild"],"switch",
  "Climbing, cooking, and a Hyrule you can cross without a set dungeon order.",
  "It launched on Wii U and Nintendo Switch in 2017. This one page names both. Tears of the Kingdom is the sequel and has its own page.")
A("tears-of-the-kingdom","The Legend of Zelda: Tears of the Kingdom","2023",["Nintendo Switch"],"Nintendo",["the-legend-of-zelda-tears-of-the-kingdom","the-legend-of-zelda-breath-of-the-wild-sequel"],"switch",
  "A changed Hyrule adds a sky, a depths, and a way to combine objects as you travel.",
  "It is the Switch sequel to Breath of the Wild, not a mode inside that game. RAWG has filed it under more than one slug; this page is the 2023 game.")
A("super-mario-odyssey","Super Mario Odyssey","2017",["Nintendo Switch"],"Nintendo",["super-mario-odyssey"],"switch",
  "Kingdoms are sandboxes full of optional moons, and a hat named Cappy does the possessing.",
  "It is a Nintendo Switch 3D Mario, not a port of Sunshine, Galaxy, or 64.")
A("mario-kart-8-deluxe","Mario Kart 8 Deluxe","2017",["Nintendo Switch"],"Nintendo",["mario-kart-8-deluxe"],"switch",
  "The Switch edition adds a revised battle mode, more characters, and later extra cups.",
  "It is not the same entry as the Wii U Mario Kart 8, which has its own page.")
A("animal-crossing-new-horizons","Animal Crossing: New Horizons","2020",["Nintendo Switch"],"Nintendo",["animal-crossing-new-horizons","animal-crossing-2019"],"switch",
  "You settle an island, invite neighbors, and decorate on the real-world calendar.",
  "It is the Switch Animal Crossing, not the GameCube, DS, Wii, or 3DS towns.")
A("metroid-dread","Metroid Dread","2021",["Nintendo Switch"],"MercurySteam / Nintendo",["metroid-dread"],"switch",
  "A side-view Metroid about slipping past threats you cannot beat yet, then coming back armed.",
  "It is a Switch original and the numbered follow-up to Fusion, developed with MercurySteam.")
A("a-link-between-worlds","The Legend of Zelda: A Link Between Worlds","2013",["Nintendo 3DS"],"Nintendo",["the-legend-of-zelda-a-link-between-worlds"],"legacy",
  "It revisits the shape of A Link to the Past, then lets Link become a painting and move along walls.",
  "It is a Nintendo 3DS Zelda. That system's digital catalog is closed, and this page does not invent a current listing.")
