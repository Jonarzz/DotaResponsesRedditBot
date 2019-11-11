"""Module in which the constants that are used by Dota Responses Bot are declared."""
import os

__author__ = 'Jonarzz'

# App config
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# Account config
USER_AGENT = "Reddit bot that replies DotA2 hero responses in comments. (by /u/MePsyDuck)"
SUBREDDIT = os.environ.get('SUBREDDIT', 'dota2')
USERNAME = os.environ.get('REDDIT_USERNAME')
PASSWORD = os.environ.get('REDDIT_PASSWORD')

# Parser config
URL_DOMAIN = 'http://dota2.gamepedia.com'
API_PATH = URL_DOMAIN + '/api.php'
CATEGORY_API_PARAMS = {'action': 'query', 'list': 'categorymembers', 'cmlimit': 'max', 'cmprop': 'title',
                       'format': 'json',
                       'cmtitle': ''}
FILE_API_PARAMS = {'action': 'query', 'titles': '', 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json'}
FILES_PER_API_CALL = 25
RESPONSES_CATEGORY = 'Responses'
STYLESHEET_URL = r'https://www.reddit.com/r/dota2/about/stylesheet.json'
FLAIR_REGEX = r'(?P<css_class>.flair-\w+),a\[href="(?P<img_path>/hero-\w+)"\]'
RESPONSES_REGEX = r'\* <sm2>(?P<file>[a-z0-9_.]+)</sm2> (<sm2>(?P<file2>[a-z0-9_.]+)</sm2> )?({{.+?}} )*(?P<text>(' \
                  r'.*)(\.|!|\?)) '

# External add-on config
DB_PROVIDER = os.getenv('DATABASE_PROVIDER', 'sqlite')  # valid choices : sqlite, mysql, postgres
DB_URL = os.environ.get('DATABASE_URL', ':memory:')
REDIS_URL = os.environ.get('REDIS_URL')

# Responses config
COMMENT_ENDING = """

---
Bleep bloop, I am a robot.

[*^(Source)*](https://github.com/MePsyDuck/DotaResponsesRedditBot) *^(|)* 
[*^(Suggestions/Issues)*](https://github.com/MePsyDuck/DotaResponsesRedditBot/issues) *^(|)* 
[*^(Contact)*](https://www.reddit.com/user/MePsyDuck/) *^(|)* 
[*^(Author)*](https://www.reddit.com/user/Jonarz/)
"""

# Logging config
BOT_LOG = 'bot'
PRAW_LOG = 'prawcore'
LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s %(funcName)-20s %(levelname)-8s %(message)s'
LOG_DIR = 'logs'
INFO_FILENAME = 'info.log'
ERROR_FILENAME = 'error.log'
PRAW_FILENAME = 'praw.log'

NUMBER_OF_DAYS_TO_DELETE_COMMENT = 5

INVOKER_BOT_RESPONSES = ['one of my favourites', 'one of my favorites', 'r/dota2smut', '/r/dota2smut', 'dota2smut']
INVOKER_RESPONSE = 'One of my favorites!'
INVOKER_RESPONSE_URL = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/b/b6/Invo_ability_invoke_01.mp3'
INVOKER_ENDING = '^^Thus ^^I ^^Invoke ^^Masturbation'
INVOKER_IMG_DIR = '/hero-invoker'
INVOKER_HERO_NAME = 'Dirty Invoker'

SNIPER_RESPONSE_URL = 'https://hydra-media.cursecdn.com/dota2.gamepedia.com/1/17/Snip_ability_shrapnel_03.mp3'
SNIPER_IMG_DIR = '/hero-sniper'
SNIPER_TRIGGER_WARNING = 'trigger warning: Sniper'

EXCLUDED_RESPONSES = ["thank you", "why not", "glimmer cape", "hood of defiance",
                      "mask of madness", "force staff", "armlet of mordiggian",
                      "helm of the dominator", "veil of discord", "shadow blade", "blade mail",
                      "urn of shadows", "skull basher", "battle fury", "crimson guard",
                      "eul s scepter", "eul s scepter of divinity", "scepter of divinity",
                      "ethereal blade", "black king bar", "diffusal blade", "lotus orb",
                      "silver edge", "solar crest", "medallion of courage", "rod of atos",
                      "shiva s guard", "heaven s halberd", "sange and yasha", "monkey king bar",
                      "orchid malevolence", "drum of endurance", "aghanim s scepter",
                      "manta style", "eye of skadi", "hand of midas", "vladimir s offering",
                      "refresher orb", "linken s sphere", "assault cuirass", "divine rapier",
                      "scythe of vyse", "sheep stick", "pipe of insight", "boots of travel",
                      "blink dagger", "moon shard", "guardian greaves", "octarine core",
                      "heart of tarrasque", "abyssal blade", "abyssal underlord",
                      "ancient apparition", "anti mage", "bounty hunter", "centaur warrunner",
                      "chaos knight", "crystal maiden", "dark seer", "death prophet",
                      "dragon knight", "drow ranger", "earth spirit", "earth shaker",
                      "elder titan", "ember spirit", "faceless void", "keeper of the light",
                      "legion commander", "lone druid", "naga siren", "nature s prophet",
                      "nature s prophet", "night stalker", "nyx assassin", "ogre magi",
                      "outworld destroyer", "phantom assassin", "phantom lancer", "queen of pain",
                      "sand king", "shadow demon", "shadow fiend", "skywrath mage",
                      "skeleton king", "spirit breaker", "storm spirit", "templar assassin",
                      "treant protector", "troll warlord", "vengeful spirit", "winter wyvern",
                      "witch doctor", "wraith king", "i agree", "my bad", "ha ha", "why not",
                      "fair enough", "no way", "you're welcome", "very nice", "of course",
                      "well deserved", "try again", "it worked", "nice try", "seems fair",
                      "that s right", "thank god", "thank you so much", "well said", "holy shit",
                      "so beautiful", "try harder", "go outside", "arc warden", "he he he",
                      "pit lord", "shut up", "how so", "hey now", "much appreciated",
                      "i don t think so", "I know right", "it begins", "too soon", "well done",
                      "i like it", "are you okay", "ah, nice", "about time", "very good",
                      "are you kidding me", "at last", "got it", "what happened", "oh boy",
                      "nice one", "i am", "exactly so", "aphotic shield", "ghost scepter",
                      "outworld devourer", "shadow shaman"]
