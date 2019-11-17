"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/
"""

import json
import re
import string
import time

import requests

from config import API_PATH, RESPONSES_CATEGORY, RESPONSE_REGEX, CATEGORY_API_PARAMS, URL_DOMAIN, FILE_API_PARAMS, \
    FILES_PER_API_CALL, FILE_REGEX
from util.database.database import db_api
from util.logger import logger

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


def pages_for_category(category_name):
    """Method that returns a list of page endings for a given Wiki category.

    :param category_name: returns all category members in json response from mediawiki API.
    """
    params = get_params_for_category_api(category_name)
    json_response = requests.get(url=API_PATH, params=params).text

    pages = []

    parsed_json = json.loads(json_response)
    for category_members in parsed_json['query']['categorymembers']:
        title = category_members['title']
        pages.append(title)

    return pages


def get_params_for_category_api(category):
    params = CATEGORY_API_PARAMS.copy()
    params['cmtitle'] = 'Category:' + category
    return params


def get_params_for_files_api(files):
    params = FILE_API_PARAMS.copy()
    titles = 'File:' + '|File:'.join(files)
    params['titles'] = titles
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
    responses_source = requests.get(url=URL_DOMAIN + '/' + url_path, params={'action': 'raw'}).text

    responses_list = []
    file_and_text_list = []

    response_regex = re.compile(RESPONSE_REGEX)
    file_regex = re.compile(FILE_REGEX)

    for response in response_regex.finditer(responses_source):
        original_text = parse_response(response['text']).strip()
        if original_text == '':
            pass

        files_source = response['files']
        for file in file_regex.finditer(files_source):
            file_and_text_list.append([original_text, file['file']])

    file_and_link_dict = links_for_files(file_and_text_list)

    for original_text, file in file_and_text_list:
        processed_text = clean_response_text(original_text)
        if processed_text != '':
            try:
                link = file_and_link_dict[file]
                responses_list.append((original_text, processed_text, link))
            except KeyError:
                pass

    return responses_list


def parse_response(text):
    if '(broken file)' in text:
        return ''
    if 'versus (TI ' in text:
        return ''
    if 'sm2' in text:
        return ''

    regexps_empty_sub = [r'<!--.*?-->',  # Remove comments
                         r'{{resp\|(r|u|\d+|d\|\d+)}}',  # Remove response rarity
                         r'{{hero icon\|[a-z- \']+\|\d+px}}',  # Remove hero icon
                         r'{{item( icon)?\|[a-z0-9() \']+\|\d+px}}',  # Remove item icon
                         r'\[\[File:[a-z.,!\'() ]+\|\d+px\|link=[a-z,!\'() ]+]]',  # Remove Files
                         r'<small>\[\[#[a-z_\-\' ]+\|\'\'followup\'\']]</small>',
                         # Remove followup links in <small> tags
                         r'<small>\'\'[a-z0-9 /]+\'\'</small>',  # Remove text in <small> tags
                         ]
    for regex in regexps_empty_sub:
        text = re.sub(regex, '', text, flags=re.IGNORECASE)

    regexps_sub_text = [r'\[\[([a-zé().:\',\- ]+)]]',  # Replace links such as [[Shitty Wizard]]
                        r'\[\[[a-zé0-9().:\'/ ]+\|([a-zé().:\' ]+)]]',
                        # Replace links such as  [[Ancient (Building)|Ancients]] and [[:File:Axe|Axe]]
                        r'{{h\|([a-zé().:\' ]+)}}',  # Replace hero names
                        r'{{tooltip\|([a-z.!\'\-?,… ]+)\|[a-z.!\'\-?:,()/ ]+}}',  # Replace tooltips
                        r'{{note\|([a-z.!\'\-?, ]+)\|[a-z.!\'\-?,()/ ]+}}',  # Replace notes
                        ]
    for regex in regexps_sub_text:
        text = re.sub(regex, '\\1', text, flags=re.IGNORECASE)

    if any(escape in text for escape in ['[[', ']]', '{{', '}}', '|']):
        logger.warn('Response could not be processed : ' + text)

    return text


def clean_response_text(key):
    """Method that cleans the given response text.
    It:
    * removes trailing and leading spaces
    * removes all punctuations
    * removes all non-ascii characters (eg. ellipsis …)
    * removes double spaces
    * changes to lowercase

    :param key: the key to be cleaned
    :return: cleaned key
    """
    key = key.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    key = ''.join([i if ord(i) < 128 else ' ' for i in key])

    while '  ' in key:
        key = key.replace('  ', ' ')

    key = key.strip().lower()

    return key


def links_for_files(files_list):
    """
    Allows max 50 files(titles) at once : https://www.mediawiki.org/wiki/API:Query
    :param files_list:  list of [original_text, file]
    :return files_link_mapping: dict with file names and their links. dict['file'] = link
    """
    files_link_mapping = {}

    for batch in batches(files_list, FILES_PER_API_CALL):
        files_batch_list = [file for text, file in batch]

        files_from_to_mapping = {}

        http_response = requests.get(url=API_PATH, params=get_params_for_files_api(files_batch_list))
        json_response = json.loads(http_response.text)
        query = json_response['query']

        normalized = query['normalized']
        for mapping in normalized:
            from_file = mapping['from']
            to_file = mapping['to']
            files_from_to_mapping[to_file] = from_file

        pages = query['pages']
        for page_id, page in pages.items():
            title = page['title']  # Same as 'to' in 'normalized' entry
            try:
                imageinfo = page['imageinfo'][0]
                file_url = imageinfo['url'].split('?')[0]  # Remove file version
                files_link_mapping[files_from_to_mapping[title][5:]] = file_url
            except KeyError:
                logger.critical('File does not have a link : ' + title)

    return files_link_mapping


def batches(l, n):
    """Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]
