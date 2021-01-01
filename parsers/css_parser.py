"""Module to populate hero details from DotA 2 subreddit css.
"""

import json
import re

import requests
from rapidfuzz import process

from config import STYLESHEET_URL, FLAIR_REGEX, USER_AGENT
from util.database.database import db_api

__author__ = 'MePsyDuck'


def populate_heroes():
    """Method to update heroes in the Heroes table with hero names and proper css classes names as
    taken from the DotA2 subreddit and hero flair images from the reddit directory.

    Uses rapidfuzz for fuzzy matching of hero names to name found in `.flair-name` property in css.
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

        match, confidence, position = process.extractOne(flair_hero, hero_names)
        if confidence >= 90:
            db_api.update_hero(hero_name=match, img_path=img_path, flair_css=flair_css)
