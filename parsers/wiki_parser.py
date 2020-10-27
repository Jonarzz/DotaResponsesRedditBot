"""Module used to populate responses into the Responses table in database.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/
"""

import json
import re
import time
from concurrent.futures import as_completed

import requests
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3 import Retry

from config import API_PATH, RESPONSES_CATEGORY, RESPONSE_REGEX, CATEGORY_API_PARAMS, URL_DOMAIN, FILE_API_PARAMS, \
    FILE_REGEX, CHAT_WHEEL_SECTION_REGEX
from util.database.database import db_api
from util.logger import logger
from util.str_utils import preprocess_text

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


def populate_responses():
    """Method that adds all the responses to database. Assumes responses and hero database are already built.
    """
    populate_hero_responses()
    populate_chat_wheel()


def populate_hero_responses():
    """Method that populates hero responses (as well as Arcana voice packs and Announcer packs) from Gamepedia.
    First fetches all Pages in Responses category, then source for each page.
    Populates Responses table and Hero table from processed response, original response, link and hero name.
    """
    pages = pages_for_category(RESPONSES_CATEGORY)
    for page in pages:
        if is_hero_type(page):
            # page points to hero responses
            hero_name = get_hero_name(page)
        else:
            # page points to voice pack, announcer or shopkeeper responses
            hero_name = page

        responses_source = requests.get(url=URL_DOMAIN + '/' + page, params={'action': 'raw'}).text

        response_link_list = create_responses_text_and_link_list(responses_source=responses_source)
        # Note: Save all responses to the db. Apply single word and common words filter on comments and submission text
        # not while saving responses
        db_api.add_hero_and_responses(hero_name=hero_name, response_link_list=response_link_list)


def pages_for_category(category_name):
    """Method that returns a list of pages for a given Wiki category.

    :param category_name: returns all category members in json response from mediawiki API.
    :return: list of all `pages` in the given category.
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
    """Method to get `GET` parameters for querying MediaWiki for category details.

    :param category: category name to be passed in params.
    :return: GET parameters `params`
    """
    params = CATEGORY_API_PARAMS.copy()
    params['cmtitle'] = 'Category:' + category
    return params


def get_params_for_files_api(files):
    """Method to get `GET` parameters for querying MediaWiki for details for multiple files.
    Uses pipe character `|` to include multiple files. Currently MediaWiki limits number of files to 50.
    If files list is empty, leave `File` parameter empty.

    :param files: list of file names to be passed in params.
    :return: GET parameters `params`.
    """
    params = FILE_API_PARAMS.copy()
    if files:
        titles = 'File:' + '|File:'.join(files)
    else:
        titles = ''
    params['titles'] = titles
    return params


def is_hero_type(page):
    """Method to check if page belongs to a hero or creep-hero(Warlock's Golem).

    :param page: Page name as string.
    :return: True if page belongs to hero else False
    """
    return '/Responses' in page


def get_hero_name(hero_page):
    """Method that parses hero name from its responses page.
    Pages for heroes are in the form of `Hero name/Responses`. We need only the `Hero name` part for heroes.

    :param hero_page: hero's responses page as string.
    :return: Hero name as parsed
    """
    return hero_page.split('/')[0]


def create_responses_text_and_link_list(responses_source):
    """Method that for a given source of a hero's response page creates a list of tuple: (original_text, processed_text,
     link).
    Steps involved:
    * Use regex to find all lines containing mp3 files and responses.
    * Process it to get original response text and file name.
    * Create a list of files and get all the links for them by calling `links_for_files`.
    * Process original text to get processed response.
    * Add original response text, processed response text and file link to a list as a tuple.

    :param responses_source: Mediawiki source
    :return: list with tuples of (original_text, processed_text, link).
    """
    responses_list = []
    file_and_text_list = []

    response_regex = re.compile(RESPONSE_REGEX)
    file_regex = re.compile(FILE_REGEX)

    for response in response_regex.finditer(responses_source):
        original_text = parse_response(response['text'])
        if original_text is not None:
            files_source = response['files']
            for file in file_regex.finditer(files_source):
                file_name = file['file'].replace('_', ' ').capitalize()
                file_and_text_list.append([original_text, file_name])

    files_list = [file for text, file in file_and_text_list]
    file_and_link_dict = links_for_files(files_list)

    for original_text, file in file_and_text_list:
        processed_text = preprocess_text(original_text)
        if processed_text != '':
            try:
                link = file_and_link_dict[file]
                responses_list.append((original_text, processed_text, link))
            except KeyError:
                # Ignore files with no links to mp3 files. Happens to broken files and files undergoing migration.
                pass

    return responses_list


def parse_response(text):
    # Special cases
    if any(excluded_case in text for excluded_case in ['(broken file)', 'versus (TI ', 'Ceeeb']):
        return None

    text = re.sub(r'…', '...', text)  # Replace ellipsis with three dots

    regexps_empty_sub = [r'<!--.*?-->',  # Remove comments
                         r'{{resp\|(r|u|\d+|d\|\d+|rem)}}',  # Remove response rarity
                         r'{{hero icon\|[a-z- \']+\|\d+px}}',  # Remove hero icon
                         r'{{item( icon)?\|[a-z0-9() \']+\|\d+px}}',  # Remove item icon
                         r'\[\[File:[a-z.,!\'() ]+\|\d+px\|link=[a-z,!\'() ]+]]',  # Remove Files
                         r'<small>\[\[#[a-z0-9_\-\' ]+\|\'\'followup\'\']]</small>',
                         # Remove followup links in <small> tags
                         r'<small>\'\'[a-z0-9 /]+\'\'</small>',  # Remove text in <small> tags
                         r'<ref>.*?</ref>',  # Remove text in <ref> tags
                         r'<nowiki>.*?</nowiki>',  # Remove text in <nowiki> tags
                         ]
    for regex in regexps_empty_sub:
        text = re.sub(regex, '', text, flags=re.IGNORECASE)

    regexps_sub_text = [r'\[\[([a-zé().:\',\- ]+)]]',  # Replace links such as [[Shitty Wizard]]
                        r'\[\[[a-zé0-9().:\'/# ]+\|([a-zé().:\' ]+)]]',
                        # Replace links such as [[Ancient (Building)|Ancients]], [[:File:Axe|Axe]] and [[Terrorblade#Sunder|sundering]]
                        r'{{tooltip\|(.*?)\|.*?}}',  # Replace tooltips
                        r'{{note\|([a-z.!\'\-?, ]+)\|[a-z.!\'\-?,()/ ]+}}',  # Replace notes
                        ]
    for regex in regexps_sub_text:
        text = re.sub(regex, '\\1', text, flags=re.IGNORECASE)

    if any(escape in text for escape in ['[[', ']]', '{{', '}}', '|', 'sm2']):
        logger.warn('Response could not be processed : ' + text)
        return None

    return text.strip()


def links_for_files(files_list):
    """Method that queries MediaWiki API used by Gamepedia to return links to the files list passed.
    Does batch processing to avoid max number of files limit and header size limit.
    Used asynchronous requests for faster processing.
    Removes files version as we only need the latest one.

    MediaWiki allows max 50 files(titles) at once : https://www.mediawiki.org/wiki/API:Query.

    :param files_list: list of files
    :return files_link_mapping: dict with file names and their links. dict['file'] = link
    """

    # Method level constants
    max_title_list_length = 50
    file_title_prefix_length = len('%7CFile%3A')  # url encoded file title prefix '|File:'
    max_header_length = 1960  # max header length as found by trial and error

    files_link_mapping = {}
    futures = []
    empty_api_length = len(requests.Request('get', url=API_PATH, params=get_params_for_files_api([])).prepare().url)

    # To add retry in case of Status 429 : Too many requests
    with FuturesSession() as session:
        retries = 5
        status_forcelist = [429]
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            respect_retry_after_header=True,
            status_forcelist=status_forcelist,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        files_batch_list = []
        current_title_length = 0

        for file in files_list:
            file_name_len = file_title_prefix_length + len(file)
            # If header size overflows or the number of files reaches the limit specified by MediaWiki
            if file_name_len + current_title_length >= max_header_length - empty_api_length or \
                    len(files_batch_list) >= max_title_list_length:
                # Issue a request for current batch of files
                futures.append(session.get(url=API_PATH, params=get_params_for_files_api(files_batch_list)))

                # Reset files tracking variables
                files_batch_list = []
                current_title_length = 0

            files_batch_list.append(file)
            current_title_length += file_name_len

        if files_batch_list:
            futures.append(session.get(url=API_PATH, params=get_params_for_files_api(files_batch_list)))

        for future in as_completed(futures):
            json_response = future.result().json()

            # Even though response code maybe 200, the response may contain query execution error, hence another level of retries
            if 'error' in json_response:
                current_retry = 1
                while current_retry < retries and 'error' in json_response:
                    time.sleep(5)
                    json_response = requests.get(future.result().url).json()

                if current_retry == retries and 'error' in json_response:
                    logger.critical('MediaWiki API failed, max retries exceeded exiting ## last response : %s ## url : %s', current_retry, future.result().url, json_response)
                    return
                else:
                    logger.warn('MediaWiki API failed %s times ## url : %s', current_retry, future.result().url)

            query = json_response['query']
            pages = query['pages']

            for _, page in pages.items():
                title = page['title']
                try:
                    imageinfo = page['imageinfo'][0]
                    file_url = imageinfo['url'][:imageinfo['url'].index('.mp3') + len('.mp3')]  # Remove file version and trailing path
                    files_link_mapping[title[5:]] = file_url
                except KeyError:
                    logger.critical('File does not have a link : ' + title)

    return files_link_mapping


def populate_chat_wheel():
    """Method that populates chat wheel responses featured in The International yearly Battle Pass.
    Other chat wheel responses from events and Dota plus are not processed currently.
    """
    chat_wheel_source = requests.get(url=URL_DOMAIN + '/' + 'Chat_Wheel', params={'action': 'raw'}).text

    chat_wheel_regex = re.compile(CHAT_WHEEL_SECTION_REGEX, re.DOTALL | re.IGNORECASE)

    for match in chat_wheel_regex.finditer(chat_wheel_source):
        event = match['event']
        responses_source = match['source']
        response_link_list = create_responses_text_and_link_list(responses_source=responses_source)

        db_api.add_hero_and_responses(hero_name=event, response_link_list=response_link_list)
