"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/
"""

import json
import re
import string

import requests

from config import API_PATH, RESPONSES_CATEGORY, RESPONSES_REGEX, CATEGORY_API_PARAMS, URL_DOMAIN, FILE_API_PARAMS
from util.database.queries import db_api

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


def populate_responses():
    """Method that adds all the responses to database. Assumes responses and hero database are already built.
    hero_name is used commonly for both announcers, heroes and voice packs.
    """

    paths = pages_for_category(RESPONSES_CATEGORY)
    for path in paths:
        if is_hero_type(path):
            # path points to hero responses
            hero_name = get_hero_name(path)
        else:
            # path points to voice pack, announcer or shopkeeper responses
            hero_name = path

        response_link_list = create_responses_text_and_link_list(url_path=path)

        # Note: Save all responses to the db. Apply single word and common words filter on comments, not while saving
        # responses
        db_api.add_hero_and_responses(hero_name=hero_name, response_link_list=response_link_list)

    # TODO add support for custom responses
    # custom_responses = {}
    #
    # for response, link in custom_responses.items():
    #     db.add_response_to_table(response=response, link=link)


def pages_for_category(category_name):
    """Method that returns a list of page endings for a given Wiki category.

    :param category_name: returns all category members in json response from mediawiki API.
    """
    params = get_params_for_category(category_name)
    json_response = requests.get(url=API_PATH, params=params).text

    pages = []

    parsed_json = json.loads(json_response)
    for category_members in parsed_json['query']['categorymembers']:
        title = category_members['title']
        pages.append(title)

    return pages


def get_params_for_category(category):
    params = CATEGORY_API_PARAMS.copy()
    params['cmtitle'] = 'Category:' + category
    return params


def get_params_for_file(file):
    params = FILE_API_PARAMS.copy()
    params['titles'] = 'File:' + file
    return params


def is_hero_type(page):
    """Method to check if page belongs to a hero, creep-hero(Warlock's Golem). There's a few inconsistencies due to
    Gamepedia's naming such as Feast of Abscession being a hero type in spite of being voice pack same as Call of
    Bladeform Legacy and Mercurial's Call.

    :param page: Page name as string.
    :return: True if page belongs to hero else False
    """
    if '/Responses' in page:
        return True
    else:
        return False


def get_hero_name(hero_page):
    """Method that parses hero name from it's responses page

    :param hero_page: hero's responses page as string.
    :return: Hero name as parsed
    """
    return hero_page.split('/')[0]


def create_responses_text_and_link_list(url_path):
    """Method that for a given page url_path creates a list of tuple: (original_text, processed_text, link).

    :param url_path: path for the hero's responses as string
    :return: list in the form of (original_text, processed_text, link).
    """

    responses_list = []

    responses_source = requests.get(url=URL_DOMAIN + '/' + url_path, params={'action': 'raw'}).text

    r = re.compile(RESPONSES_REGEX)

    for response in r.finditer(responses_source):
        original_text = response['text']
        file = response['file']
        processed_text = clean_response_text(original_text)

        link = link_for_file(file)
        if link:
            responses_list.append((original_text, processed_text, link))

        # In some cases there's two links when there's arcana audio file available for the same response.
        file2 = response['file2']
        if file2:
            link2 = link_for_file(file2)
            responses_list.append((original_text, processed_text, link2))

    return responses_list

    # TODO move to custom rules in config
    # responses['one of my favourites'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/b/b6' \
    #                                     '/Invo_ability_invoke_01.mp3 '
    # responses['lolicon'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/a/a9/Arcwar_lasthit_04.mp3'
    # responses['ho ho ha ha'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/1/17/Snip_ability_shrapnel_03.mp3'
    #
    # responses['caw'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/f/f6/Phoenix_bird_last_hit.mp3'
    # responses['skree'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/a/a5/Phoenix_bird_attack.mp3'
    # responses['beep boop'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/4/4f/Wisp_Move04.mp3'
    # responses['boop'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/5/5f/Wisp_Move02.mp3'
    # responses['beep'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/5/54/Wisp_Move01.mp3'
    #
    # heroes['Phoenix'] = 'Phoenix'
    # heroes['Wisp'] = 'Io'


def clean_response_text(key):
    """Method that cleans the given response text.
    It:
    * removes anything between parenthesis
    * removes trailing and leading spaces
    * removes all punctuations
    * removes double spaces
    * changes to lowercase

    :param key: the key to be cleaned
    :return: cleaned key
    """

    if '(' in key and ')' in key:
        start_index = key.find('(')
        end_index = key.rfind(')') + 1
        key = key.replace(key[start_index:end_index], '')

    key = key.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    while '  ' in key:
        key = key.replace('  ', ' ')

    key = key.strip().lower()

    return key


def link_for_file(file):
    try:
        json_response = json.loads(requests.get(url=API_PATH, params=get_params_for_file(file)).text)
        pages = json_response['query']['pages']
        imageinfo = pages[next(iter(pages))]['imageinfo'][0]
        file_url = imageinfo['url']
        return file_url.split('?')[0]  # Remove file version
    except KeyError:
        return None
