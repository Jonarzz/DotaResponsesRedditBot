"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/
"""

import json
import re
import string
from concurrent.futures import as_completed

import requests
from requests_futures.sessions import FuturesSession

from config import API_PATH, RESPONSES_CATEGORY, RESPONSE_REGEX, CATEGORY_API_PARAMS, URL_DOMAIN, FILE_API_PARAMS, \
    FILE_REGEX, MAX_HEADER_LENGTH, CHAT_WHEEL_SECTION_REGEX
from util.database.database import db_api
from util.logger import logger

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


def populate_responses():
    """Method that adds all the responses to database. Assumes responses and hero database are already built.
    hero_name is used commonly for both announcers, heroes and voice packs.
    """
    populate_hero_responses()
    populate_chat_wheel()


def populate_hero_responses():
    paths = pages_for_category(RESPONSES_CATEGORY)
    for path in paths:
        if is_hero_type(path):
            # path points to hero responses
            hero_name = get_hero_name(path)
        else:
            # path points to voice pack, announcer or shopkeeper responses
            hero_name = path

        responses_source = requests.get(url=URL_DOMAIN + '/' + path, params={'action': 'raw'}).text

        response_link_list = create_responses_text_and_link_list(responses_source=responses_source)
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


def create_responses_text_and_link_list(responses_source):
    """Method that for a given page url_path creates a list of tuple: (original_text, processed_text, link).

    :param responses_source: Mediawiki source
    :return: list in the form of (original_text, processed_text, link).
    """
    responses_list = []
    file_and_text_list = []

    response_regex = re.compile(RESPONSE_REGEX)
    file_regex = re.compile(FILE_REGEX)

    for response in response_regex.finditer(responses_source):
        original_text = parse_response(response['text'])
        if original_text == '':
            pass

        files_source = response['files']
        for file in file_regex.finditer(files_source):
            file_name = file['file'].replace('_', ' ').capitalize()
            file_and_text_list.append([original_text, file_name])

    files_list = [file for text, file in file_and_text_list]
    file_and_link_dict = links_for_files(files_list)

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
    # Special cases
    if '(broken file)' in text:
        return ''
    if 'versus (TI ' in text:
        return ''
    if 'Ceeeb' in text:
        return ''

    text = re.sub(r'…', '...', text)  # Replace ellipsis with three dots

    regexps_empty_sub = [r'<!--.*?-->',  # Remove comments
                         r'{{resp\|(r|u|\d+|d\|\d+)}}',  # Remove response rarity
                         r'{{hero icon\|[a-z- \']+\|\d+px}}',  # Remove hero icon
                         r'{{item( icon)?\|[a-z0-9() \']+\|\d+px}}',  # Remove item icon
                         r'\[\[File:[a-z.,!\'() ]+\|\d+px\|link=[a-z,!\'() ]+]]',  # Remove Files
                         r'<small>\[\[#[a-z_\-\' ]+\|\'\'followup\'\']]</small>',
                         # Remove followup links in <small> tags
                         r'<small>\'\'[a-z0-9 /]+\'\'</small>',  # Remove text in <small> tags
                         r'<ref>.*?</ref>',  # Remove text in <ref> tags
                         r'<nowiki>.*?</nowiki>',  # Remove text in <nowiki> tags
                         ]
    for regex in regexps_empty_sub:
        text = re.sub(regex, '', text, flags=re.IGNORECASE)

    regexps_sub_text = [r'\[\[([a-zé().:\',\- ]+)]]',  # Replace links such as [[Shitty Wizard]]
                        r'\[\[[a-zé0-9().:\'/ ]+\|([a-zé().:\' ]+)]]',
                        # Replace links such as  [[Ancient (Building)|Ancients]] and [[:File:Axe|Axe]]
                        # r'{{h\|([a-zé().:\' ]+)}}',  # Replace hero names
                        r'{{tooltip\|(.*?)\|.*?}}',  # Replace tooltips
                        r'{{note\|([a-z.!\'\-?, ]+)\|[a-z.!\'\-?,()/ ]+}}',  # Replace notes
                        ]
    for regex in regexps_sub_text:
        text = re.sub(regex, '\\1', text, flags=re.IGNORECASE)

    if any(escape in text for escape in ['[[', ']]', '{{', '}}', '|', 'sm2']):
        logger.warn('Response could not be processed : ' + text)

    return text.strip()


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

    while '  ' in key:
        key = key.replace('  ', ' ')

    key = key.strip().lower()

    return key


def links_for_files(files_list):
    """
    Allows max 50 files(titles) at once : https://www.mediawiki.org/wiki/API:Query
    :param files_list:  list of files
    :return files_link_mapping: dict with file names and their links. dict['file'] = link
    """

    files_link_mapping = {}
    futures = []
    empty_api_length = len(requests.get(url=API_PATH, params=get_params_for_files_api([])).url)

    with FuturesSession() as session:
        files_batch_list = []
        title_length = 0

        for file in files_list:
            if len(file) + 10 + title_length >= MAX_HEADER_LENGTH - empty_api_length:
                futures.append(session.get(url=API_PATH, params=get_params_for_files_api(files_batch_list)))
                title_length = len(file) + 10
                files_batch_list = [file]
            else:
                files_batch_list.append(file)
                title_length += len(file) + 10

        futures.append(session.get(url=API_PATH, params=get_params_for_files_api(files_batch_list)))

        for future in as_completed(futures):
            json_response = future.result().json()
            query = json_response['query']
            pages = query['pages']

            for page_id, page in pages.items():
                title = page['title']  # Same as 'to' in 'normalized' entry
                try:
                    imageinfo = page['imageinfo'][0]
                    file_url = imageinfo['url'].split('?')[0]  # Remove file version
                    files_link_mapping[title[5:]] = file_url
                except KeyError:
                    logger.critical('File does not have a link : ' + title)

    return files_link_mapping


def populate_chat_wheel():
    chat_wheel_source = requests.get(url=URL_DOMAIN + '/' + 'Chat_Wheel', params={'action': 'raw'}).text

    chat_wheel_regex = re.compile(CHAT_WHEEL_SECTION_REGEX, re.DOTALL | re.IGNORECASE)

    for match in chat_wheel_regex.finditer(chat_wheel_source):
        event = match['event']
        responses_source = match['source']
        response_link_list = create_responses_text_and_link_list(responses_source=responses_source)

        db_api.add_hero_and_responses(hero_name=event, response_link_list=response_link_list)
