import os

from util.cargoquery_utils import get_titles_from_cargo_tables

# Account config
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
SUBREDDIT = os.environ.get('SUBREDDIT', 'dota2')
USERNAME = os.environ.get('REDDIT_USERNAME')
PASSWORD = os.environ.get('REDDIT_PASSWORD')

# Responses config
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
    'ho ho ha ha': '[{}](https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2f/Vo_sniper_snip_ability_shrapnel_03.mp3)'
                   ' (trigger warning: Sniper){}',
    'turn up this guy is crazy as fuck he s gotta be on molly or some powder or something': '[{}](https://www.youtube.com/watch?v=CO3j9lUYFfo) (Donation warning: Arteezy){}'}

# Only include responses for items, runes, heroes, > 100 count and common phrases.
# Hardcoded because then they can tweaked according to the needs.
# Drawback for this : need to update each time hero/item is added
FREQUENT_RESPONSES = {'denied', 'yes', 'not yet', 'no mana', 'not enough mana', 'i m not ready', 'out of mana',
                      'it s not time yet', 'ah', 'no', 'uh', 'ha ha', 'attack', 'haste', 'double damage', 'immortality',
                      'invisibility', 'illusion', 'regeneration', 'uh uh', 'ha', }

# Hero and item responses not hardcoded here
HERO_NAMES = get_titles_from_cargo_tables('heroes')
ITEM_NAMES = get_titles_from_cargo_tables('items')

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

EXCLUDED_RESPONSES = FREQUENT_RESPONSES | HERO_NAMES | ITEM_NAMES | COMMON_PHRASE_RESPONSES
