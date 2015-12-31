# coding=UTF-8

"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/"""

import os
import re
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

__author__ = 'Jonarzz'


URL_BEGINNING = 'http://dota2.gamepedia.com/'
URL_API = ('api.php?action=query&list=categorymembers&cmlimit=max'
           '&cmprop=title&format=json&cmtitle=Category:')
CATEGORY = 'Lists_of_responses'

SCRIPT_DIR = os.path.dirname(__file__)


def generate_dictionaries(responses_filename, heroes_filename):
    """Method used to generate dictionaries for responses and hero names
    (short, used in urls matched with full names)."""
    responses, heroes = dictionary_of_responses(pages_for_category(CATEGORY))
    json.dump(responses, open(os.path.join(SCRIPT_DIR, responses_filename), "w"))
    json.dump(heroes, open(os.path.join(SCRIPT_DIR, heroes_filename), "w"))


def dictionary_from_file(filename):
    """Method used to load a dictionary from text file with given name
    (file contains JSON structure)."""
    with open(os.path.join(SCRIPT_DIR, filename)) as file:
        dictionary = json.load(file)
        return dictionary


def create_responses_list(soup):
    """Method that creates responses list for a given page payload in html."""
    list_of_responses = []

    for element in soup.find_all("li"):
        if "sm2_button" in str(element):
            list_of_responses.append(str(element))

    return list_of_responses


def dictionary_of_responses(pages_endings):
    """Method that creates two dictionaries - with the responses (response text - link to the file)
    and with hero names (short hero name used in Wiki files - long hero names).

    The dictionaries are created based on html body of a Wiki page related to the hero's responses.
    Each response and hero name is prepared to be saved: stripped (unnecesary words/characters) and
    turned to lowercase (only response text)."""
    responses = {}
    heroes = {}

    for ending in pages_endings:
        print(ending)
        page = page_to_parse(URL_BEGINNING + ending)
        soup = BeautifulSoup(page, "html.parser")

        list_of_responses = create_responses_list(soup)

        for element in list_of_responses:
            key = key_from_element(element)
            if " " not in key:
                continue
            value = value_from_element(element)

            short_hero = short_hero_name_from_url(value)
            hero = ending.replace('_', ' ')
            hero = hero.replace(' Pack', '')
            hero = hero.replace(' responses', '')

            if short_hero not in heroes:
                heroes[short_hero] = hero

            if key not in responses:
                responses[key] = value

    return responses, heroes


def page_to_parse(url):
    """Method used to open given url and return the received body (UTF-8 encoding)."""
    request = Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urlopen(request)
    return response.read().decode("UTF-8")


def pages_for_category(category_name):
    """Method that returns a list of page endings for a given Wiki category."""
    json_response = page_to_parse(URL_BEGINNING + URL_API + category_name)

    output = []

    parsed_json = json.loads(json_response)
    for categorymembers in parsed_json["query"]["categorymembers"]:
        for value in categorymembers.values():
            if isinstance(value, str) and '/' not in value:
                output.append(value.replace(" ", "_"))

    return output


def key_from_element(element):
    """Method that returns a key for a given element taken from parsed html body."""
    start_index = element.rfind("</a>") + 4
    end_index = element.find("</li>") - 1
    key = element[start_index:end_index]
    key = clean_key(key)
    return key


def substring_from_key(key, start_element, end_element, offset):
    """Method that takes a string and returns a substring of it with the position of start_element
    as start and the position of end_element + offset as end."""
    start_index = key.find(start_element)
    end_index = key.rfind(end_element) + offset
    return key.replace(key[start_index:end_index], "")


def clean_key(key):
    """Method that cleans the given key, so that it is a lowercase string with
    no dots or exclamation marks ending the string. Unnecessary spaces are removed. All html tags
    are removed as well."""
    if "<i>" and "</i>" in key:
        key = substring_from_key(key, "<i>", "</i>", 4)

    if "(" in key and ")" in key:
        key = substring_from_key(key, "(", ")", 1)

    key = key.strip(' .!')

    if key[-2:] == "--":
        key = key[:-2]

    key = key.replace("  ", " ").strip().lower()

    return key


def value_from_element(element):
    """Method that returns a value (url to the response) for a given element taken
    from parsed html body."""
    start_index = element.find("href=\"") + 6
    end_index = element.find("\" title")
    value = element[start_index:end_index]
    return value


def short_hero_name_from_url(url):
    """Method that returns a short hero name for the given url
    (taken from the filename on the Wiki server)."""
    search = re.search(r'\/(\w+?)_.+?\.mp3', url)
    if search:
        if search.group(1) == 'Dlc':
            search = re.search(r'\/(Dlc_\w+?)_.+?\.mp3', url)
            if search.group(1) == 'Dlc_tech':
                return 'Dlc_tech_ann'
        return search.group(1)


def ellipsis_to_three_dots(dictionary):
    """Method that replaces all ellipsis (…) with three dots (...) in the dictionary ketys."""
    newdict = {}

    for key in dictionary:
        newdict[key] = dictionary[key]
        if "…" in key:
            new = key.replace("…", "...")
            newdict[new] = newdict.pop(key)

    return newdict


# generate_dictionaries("dota_responses_1.3.txt", "heroes.txt")
# dictionary = dictionary_from_file("dota_responses_1.2.txt")
