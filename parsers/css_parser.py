import json
import re

import requests
from fuzzywuzzy import process

from config import STYLESHEET_URL, FLAIR_REGEX, USER_AGENT
from util.database.queries import db_api


def populate_heroes():
    """Method to add heroes to the table with hero names and proper css classes names as taken
    from the DotA2 subreddit and hero flair images from the reddit directory. Every hero has its
    own id, so that it can be joined with the hero from responses table (Serves as Foreign Key).
    Note: Unused currently since flairs don't work in comments for new Reddit redesign.
    """
    hero_names = db_api.get_all_hero_names()

    response = requests.get(STYLESHEET_URL, headers={'User-Agent': USER_AGENT})
    r = json.loads(response.text)
    stylesheet = r['data']['stylesheet']

    r = re.compile(FLAIR_REGEX)
    for flair in r.finditer(stylesheet):
        flair_css = flair['css_class']
        img_path = flair['img_path']
        flair_hero = img_path[6:]

        match, confidence = process.extractOne(flair_hero, hero_names)
        if confidence >= 90:
            db_api.update_hero(hero_name=match, img_path=img_path, flair_css=flair_css)
