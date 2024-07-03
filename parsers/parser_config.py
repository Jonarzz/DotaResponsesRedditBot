# Parser config
API_PATH = 'https://liquipedia.net/dota2/api.php'
RESPONSES_CATEGORY = 'Responses'
CATEGORY_API_PARAMS = {'action': 'query', 'list': 'categorymembers', 'cmlimit': 'max', 'cmprop': 'title',
                       'format': 'json', 'cmtitle': ''}
FILE_API_PARAMS = {'action': 'query', 'titles': '', 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json'}
CARGO_API_PARAMS = {'action': 'cargoquery', 'tables': '', 'fields': 'title', 'where': 'game IS NULL', 'limit': '500',
                    'format': 'json'}
STYLESHEET_URL = r'https://www.reddit.com/r/dota2/about/stylesheet.json'
FLAIR_REGEX = r'(?P<css_class>.flair-\w+),a\[href="(?P<img_path>/hero-\w+)"\]'
RESPONSE_REGEX = r'\*(?P<files>( <ab>.*?</ab>)+)(?P<text>(.*))'
FILE_REGEX = r'( <ab>(?P<file>[a-zA-Z0-9_. ]+)</ab>)'
TI_SECTION_CHAT_WHEEL_REGEX = r'(=== (?P<event>The International \d+) ===)(?P<source>.+?)(?=\n=== [a-z0-9 ]+ ===\n)'
AGHS_LAB_SECTION_CHAT_WHEEL_REGEX = r'(=== Sounds ===)(?P<source>.+?)(?=\n=== [a-z0-9 ]+ ===\n)'
SUPPORTERS_CLUB_TEAM_SECTION_REGEX = r'(==\s*{{Team\|(?P<team>.*?)}}\s*==(?P<source>.+?)(?=(==\s*{{Team\|.*?}}\s*==)|({{TeamNav}})))'
TI_TALENT_SECTION_REGEX = r'(==\s*Talents\s*==(?P<source>.+?)==\s*(.*?)\s*==)'
TI_TALENT_REGEX = r"\|\s*'''(?P<talent_tag>.*?)'''\s*\|\|\s*(?P<name>.*?)\s*\|\|\s*(?P<portrait>.*?)\s*\|\|\s*(?P<autograph>.*?)\s*\|\|" \
                  r"\s*<ab>(?P<file>.*?)</ab>(?P<text>.*)"
