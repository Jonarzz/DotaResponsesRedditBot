__author__ = "Jonarzz"

APP_ID = "WXwDT96-cCTBZQ"
APP_SECRET = "B145CjK0nzzLY0HEei-xZo-WUCg"
APP_URI = "http://127.0.0.1:65010/authorize_callback"
APP_REFRESH_CODE = "45040623-c8oiR2OTtb4nJWfxiovyS9XhjUg"
USER_AGENT = """A tool that finds a Dota 2-related comments with the game heroes\' responses and links to the proper
             audio sample from http://dota2.gamepedia.com/Category:Lists_of_responses (author: /u/Jonarz)"""
SUBREDDIT = "dota2"
SCOPES = "identity read save submit"

COMMENT_ENDING = "\n\n---\n*I am a bot. Question/problem? Ask my master: /u/Jonarz*\n\n*Description/changelog:* [GitHub](https://github.com/Jonarzz/DotaResponsesRedditBot)"

EXCLUDED_RESPONSES = ["thank you", "why not?", "glimmer cape", "hood of defiance", "mask of madness", "force staff", "armlet of mordiggian", "helm of the dominator", "veil of discord",
                      "shadow blade", "blade mail", "urn of shadows", "skull basher", "battle fury", "crimson guard", "eul's scepter", "eul's scepter of divinity", "scepter of divinity",
                      "ethereal blade", "black king bar", "diffusal blade", "lotus orb", "silver edge", "solar crest", "medallion of courage", "rod of atos", "shiva's guard",
                      "heaven's halberd", "sange and yasha", "monkey king bar", "orchid malevolence", "drum of endurance", "aghanim's scepter", "manta style", "eye of skadi", "hand of midas",
                      "vladimir's offering", "refresher orb", "linken's sphere", "assault cuirass", "divine rapier", "scythe of vyse", "sheep stick", "pipe of insight", "boots of travel",
                      "blink dagger", "moon shard", "guardian greaves", "octarine core", "heart of tarrasque", "abyssal blade", "abyssal underlord", "ancient apparition", "anti mage",
                      "bounty hunter", "centaur warrunner", "chaos knight", "crystal maiden", "dark seer", "death prophet", "dragon knight", "drow ranger", "earth spirit", "earth shaker",
                      "elder titan", "ember spirit", "faceless void", "keeper of the light", "legion commander", "lone druid", "naga siren", "nature's prophet", "natures prophet",
                      "night stalker", "nyx assassin", "ogre magi", "outworld destroyer", "phantom assassin", "phantom lancer", "queen of pain", "sand king", "shadow demon", "shadow fiend",
                      "skywrath mage", "skeleton king", "spirit breaker", "storm spirit", "templar assassin", "treant protector", "troll warlord", "vengeful spirit", "winter wyvern",
                      "witch doctor", "wraith king", "i agree", "my bad", "ha ha", "why not", "fair enough", "no way", "you're welcome", "very nice", "of course", "well deserved"]

KEYWORDS_DICT = {"dank" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/3/38/Erth_ability_echo_03.mp3",
                 "just do it" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/c/c4/Sven_move_07.mp3",
                 "beautiful": "http://hydra-media.cursecdn.com/dota2.gamepedia.com/c/c4/Luna_levelup_06.mp3",
                 "from the ghastly eyrie" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/a/ac/Pain_lose_04.mp3",
                 "sniper" : " http://hydra-media.cursecdn.com/dota2.gamepedia.com/1/17/Snip_ability_shrapnel_03.mp3",
                 "ppd" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/4/47/Necr_death_10.mp3",
                 "leafeator" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/e/e5/Necr_respawn_10.mp3",
                 "ur brother" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/6/63/Ogmag_respawn_05.mp3",
                 "your brother" : "http://hydra-media.cursecdn.com/dota2.gamepedia.com/6/63/Ogmag_respawn_05.mp3"}