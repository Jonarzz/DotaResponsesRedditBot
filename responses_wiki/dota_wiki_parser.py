"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/
"""

import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from config import URL_DOMAIN, API_PATH, CATEGORY
from util.database import DBUtil

__author__ = 'Jonarzz'

db = DBUtil()


def create_responses_text_and_link_dict(url_path):
    """Method that for a given page url_path creates a dictionary of pairs: response text-link.

    :param url_path: path for the hero's url as string
    :return: dictionary in the form of dict['response'] = link
    """

    responses_dict = {}

    list_of_responses = create_list_of_responses(url_path)

    for element in list_of_responses:
        key = response_text_from_element(element)

        # ignores single word responses such as yeah, no, yes, victory etc.
        # would be better to filter using a custom ignored words dictionary
        if " " not in key:
            continue

        value = link_from_element(element)

        if key not in responses_dict:
            responses_dict[key] = value

    return responses_dict

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


def create_list_of_responses(ending):
    page = page_to_parse(URL_DOMAIN + ending)
    soup = BeautifulSoup(page, "html.parser")
    list_of_responses = []

    for element in soup.find_all("li"):
        if "sm2_button" in str(element):
            list_of_responses.append(str(element))

    return list_of_responses


def page_to_parse(url):
    """Method used to open given url and return the received body (UTF-8 encoding).
    URL can contain spaces, which need to be changed to underscores before sending request.

    :param url: URL to be parsed.
    :return: html response for the url
    """
    url = url.replace(" ", "_")
    request = Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urlopen(request)
    return response.read().decode("UTF-8")


def pages_for_category(category_name):
    """Method that returns a list of page endings for a given Wiki category.

    :param category_name: returns all category members in json response from gamepedia API.
    """
    json_response = page_to_parse(URL_DOMAIN + API_PATH + category_name)

    pages = []

    parsed_json = json.loads(json_response)
    for category_members in parsed_json['query']['categorymembers']:
        title = category_members['title']
        if isinstance(title, str):
            pages.append(title)

    return pages


def response_text_from_element(element):
    """Method that returns a plaintext for a given element taken from parsed html body. Removes all HTML tags as well.
    Works specifically with currently existing responses on Gamepedia.
    Note: Code can be replaced with older string manipulation equivalent if needed, but it could be unsafe for elements
    that contain <span> tags.

    :param element: The html code to be parsed for the response
    :return: plaintext clean response
    """
    soup = BeautifulSoup(element, 'html.parser')
    link = soup.find('a')
    if link:
        link.decompose()
    tooltip = soup.find('span')
    if tooltip:
        tooltip.decompose()
    key = clean_key(soup.get_text())
    return key


def clean_key(key):
    """Method that cleans the given key. It:
    * removes anything between parenthesis
    * removes trailing and leading spaces
    * removes the ending '.', '!' and '--'
    * removes double spaces
    * changes to lowercase

    :param key: the key to be cleaned
    :return: cleaned key
    """

    if "(" in key and ")" in key:
        start_index = key.find("(")
        end_index = key.rfind(")") + 1
        key = key.replace(key[start_index:end_index], "")

    key = key.strip()

    if len(key) > 1 and key[-1] in [".", "!"]:
        key = key[:-1]

    if len(key) > 2 and key[-2:] == "--":
        key = key[:-2]

    key = key.replace("  ", " ")

    key = key.strip()
    key = key.lower()

    return key


def link_from_element(element):
    """Method that returns a link (url to the response) for a given element taken
    from parsed html body.

    :param element: The html code to be parsed for the link
    :return: The url to the response
    """

    soup = BeautifulSoup(element, 'html.parser')
    link = soup.find('a').get('href')
    return link


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


def populate_responses():
    """Method that adds all the responses to database. Assumes responses and hero database are already built.
    hero_name is used commonly for both announcers, heroes and voice packs.
    """

    paths = pages_for_category(CATEGORY)
    for path in paths:
        if is_hero_type(path):
            # path points to hero responses
            hero_name = get_hero_name(path)
        else:
            # path points to voice pack, announcer or shopkeeper responses
            hero_name = path

        db.add_hero_to_table(name=hero_name)
        hero_id = db.get_hero_id_from_table(name=hero_name)
        response_link_dict = create_responses_text_and_link_dict(url_path=path)

        for response, link in response_link_dict.items():
            db.add_response_to_table(response=response, link=link, hero=hero_name, hero_id=hero_id)

    custom_responses = {}

    for response, link in custom_responses.items():
        db.add_response_to_table(response=response, link=link)
