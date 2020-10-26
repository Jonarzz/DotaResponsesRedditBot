"""Module in which the constants that are used by Dota Responses Bot are declared."""
import os
import json
import urllib.request

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'

# App config
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# Account config
USER_AGENT = 'Python:dota2_responses_bot:v3.0 by /u/Jonarz, maintained by /u/MePsyDuck'
SUBREDDIT = os.environ.get('SUBREDDIT', 'dota2')
USERNAME = os.environ.get('REDDIT_USERNAME')
PASSWORD = os.environ.get('REDDIT_PASSWORD')

# Parser config
URL_DOMAIN = 'http://dota2.gamepedia.com'
API_PATH = URL_DOMAIN + '/api.php'
RESPONSES_CATEGORY = 'Responses'
CATEGORY_API_PARAMS = {'action': 'query', 'list': 'categorymembers', 'cmlimit': 'max', 'cmprop': 'title',
                       'format': 'json', 'cmtitle': ''}
FILE_API_PARAMS = {'action': 'query', 'titles': '', 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json'}

STYLESHEET_URL = r'https://www.reddit.com/r/dota2/about/stylesheet.json'
FLAIR_REGEX = r'(?P<css_class>.flair-\w+),a\[href="(?P<img_path>/hero-\w+)"\]'
RESPONSE_REGEX = r'\*(?P<files>( <sm2>.*?</sm2>)+)(?P<text>(.*))'
CHAT_WHEEL_SECTION_REGEX = r'(=== (?P<event>The International \d+) ===)(?P<source>.+?)(?=\n=== [a-z0-9 ]+ ===\n)'
FILE_REGEX = r'( <sm2>(?P<file>[a-zA-Z0-9_. ]+)</sm2>)'

# Caching config
CACHE_PROVIDER = os.environ.get('CACHE_PROVIDER', 'memory')  # valid choices : redis, memory, db
CACHE_URL = os.environ.get('CACHE_URL',
                           os.path.join(os.getcwd(), 'cache.json'))  # file path in case of memory/file based caching

# DB config
DB_PROVIDER = os.environ.get('DATABASE_PROVIDER', 'sqlite')  # valid choices : sqlite, mysql, postgres
DB_URL = os.environ.get('DATABASE_URL', os.path.join(os.getcwd(), 'bot.db'))  # file path in case of sqlite

# Logging config
BOT_LOGGER = 'bot'
PRAW_LOGGER = 'prawcore'
LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s %(funcName)-20s %(levelname)-8s %(message)s'
LOG_DIR = 'logs'
INFO_FILENAME = 'info.log'
ERROR_FILENAME = 'error.log'
PRAW_FILENAME = 'praw.log'

CACHE_TTL = 5

# Responses config
# TODO confirm this keyword
UPDATE_REQUEST_KEYWORD = 'try '
COMMENT_ENDING = '''

---
Bleep bloop, I am a robot. *OP can reply with "Try hero_name" to update this with new hero*

[*^(Source)*](https://github.com/Jonarzz/DotaResponsesRedditBot) *^(|)* 
[*^(Suggestions/Issues)*](https://github.com/Jonarzz/DotaResponsesRedditBot/issues/new/choose) *^(|)* 
[*^(Maintainer)*](https://www.reddit.com/user/MePsyDuck/) *^(|)* 
[*^(Author)*](https://www.reddit.com/user/Jonarz/)
'''

# Key should be lowercase without special characters. Needs to be updated if links break (as links can be
# non-gamepedia links too)
# Value should have a placeholder for original text and replyable ending
CUSTOM_RESPONSES = {
    'ho ho ha ha': '[{}](https://gamepedia.cursecdn.com/dota2_gamepedia/1/17/Snip_ability_shrapnel_03.mp3)'
                   ' (trigger warning: Sniper){}',
    'turn up this guy is crazy as fuck he s gotta be on molly or some powder or something':
        '[{}](https://www.youtube.com/watch?v=CO3j9lUYFfo) (Donation warning: Arteezy){}'
}

# Only include responses for items, runes, heroes, > 100 count and common phrases.
# Hardcoded because then they can tweaked according to the needs.
# Drawback for this : need to update each time hero/item is added
FREQUENT_RESPONSES = {'denied', 'yes', 'not yet', 'no mana', 'not enough mana', 'i m not ready', 'out of mana',
                      'it s not time yet', 'ah', 'no', 'uh', 'ha ha', 'attack', 'haste', 'double damage', 'immortality',
                      'invisibility', 'illusion', 'regeneration', 'uh uh', 'ha', }

#Hero and item responses not hardcoded here
# Drawbacks: Can't be tweaked
#TODO incorperate an exclusion set
with urllib.request.urlopen('https://dota2.gamepedia.com/api.php?' +
                            'action=cargoquery&tables=heroes&fields=title&where=game'+
                            '+IS+NULL&limit=500&format=json') as url:
    HERO_NAME_RESPONSES = set()
    for i in json.loads(url.read().decode())['cargoquery']:
        i = i['title']['title']
        for c in ["'", "(", ")", ":", ",", "-"]: i = i.replace(c, " ")
        HERO_NAME_RESPONSES.add(i.lower())

with urllib.request.urlopen('https://dota2.gamepedia.com/api.php?'+
                            'action=cargoquery&tables=items&fields='+
                            'title&where=game+IS+NULL&limit=500&format=json') as url:
    ITEM_RESPONSES = set()
    for i in json.loads(url.read().decode())['cargoquery']:
        i = i['title']['title']
        for c in ["'", "(", ")", ":", ",", "-"]: i = i.replace(c, " ")
        ITEM_RESPONSES.add(i.lower())

# Add responses here as people report them. Taken from the old excluded responses list.
COMMON_PHRASE_RESPONSES = {'earth shaker', 'shut up', 'skeleton king', 'it begins', 'i am', 'exactly so', 'very nice',
                           'why not', 'much appreciated', 'well done', 'pit lord', 'outworld destroyer', 'I know right',
                           'aphotic shield', 'go outside', 'vladimir s offering', 'sheep stick', 'my bad',
                           "you're welcome", 'holy shit', 'are you okay', 'i agree', 'thank god', 'i like it', 'no way',
                           'fair enough', 'it worked', 'well deserved', 'he he he', 'how so', 'oh boy', 'very good',
                           'about time', 'are you kidding me', 'abyssal underlord', 'so beautiful', 'nice try',
                           'thank you so much', 'ah, nice', 'nice one', 'eul s scepter', 'thank you',
                           'scepter of divinity', 'at last', 'too soon', 'try again', 'i don t think so', 'try harder',
                           'well said', 'of course', 'got it', 'what happened', 'hey now', 'seems fair', 'that s right',
                           'all pick'}

EXCLUDED_RESPONSES = FREQUENT_RESPONSES | ITEM_RESPONSES | HERO_NAME_RESPONSES | COMMON_PHRASE_RESPONSES
