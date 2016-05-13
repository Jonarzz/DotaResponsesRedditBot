# coding=UTF-8

"""Module used to create dictionaries requited for the script to work.

Responses and urls to responses as mp3s are parsed from Dota 2 Wiki: http://dota2.gamepedia.com/"""

import os
import re
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import dota_responses_properties as properties

__author__ = 'Jonarzz'


URL_BEGINNING = 'http://dota2.gamepedia.com/'
URL_API = ('api.php?action=query&list=categorymembers&cmlimit=max'
           '&cmprop=title&format=json&cmtitle=Category:')
CATEGORY = 'Lists of responses'

SCRIPT_DIR = os.path.dirname(__file__)


def generate_dictionaries(responses_filename, heroes_filename, shitty_wizard_filename):
    """Method used to generate dictionaries for responses and hero names
    (short, used in urls matched with full names)."""
    responses, heroes, shitty_wizard = dictionary_of_responses(pages_for_category(CATEGORY))
    json.dump(responses, open(os.path.join(SCRIPT_DIR, responses_filename), "w"))
    json.dump(heroes, open(os.path.join(SCRIPT_DIR, heroes_filename), "w"))
    json.dump(shitty_wizard, open(os.path.join(SCRIPT_DIR, shitty_wizard_filename), "w"))


def dictionary_from_file(filename):
    """Method used to load a dictionary from text file with given name
    (file contains JSON structure)."""
    with open(os.path.join(SCRIPT_DIR, filename)) as file:
        dictionary = json.load(file)
        return dictionary
    
    
def create_responses_text_and_link_dict(ending):
    """Method that for a given page ending creates a dictionary of pairs: response text-link."""
    responses_dict = {}
    
    list_of_responses = create_list_of_responses(ending)
    
    for element in list_of_responses:
        key = response_text_from_element(element)
        if " " not in key:
            continue
            
        value = value_from_element(element)
        
        if key not in responses_dict:
            responses_dict[key] = value
    
    return responses_dict
                
def dictionary_of_responses(pages_endings):
    """Method that creates dictionaries - with the responses (response text - link to the file),
    with hero names (short hero name used in Wiki files - long hero names),
    with "shitty wizard" responses (hero name - link to the file).

    The dictionaries are created based on html body of a Wiki page related to the hero's responses.
    Each response and hero name is prepared to be saved: stripped (unnecesary words/characters) and
    turned to lowercase (only response text)."""
    responses = {}
    heroes = {}
    shitty_wizard = {}

    for ending in pages_endings:
        print(ending)
        list_of_responses = create_list_of_responses(ending)

        for element in list_of_responses:
            key = response_text_from_element(element)
            if " " not in key:
                continue
            value = value_from_element(element)

            short_hero = short_hero_name_from_url(value)
            hero = ending.replace('_', ' ')
            hero = hero.replace(' Pack', '')
            hero = hero.replace(' responses', '')

            if short_hero not in heroes:
                heroes[short_hero] = hero

            if key == "shitty wizard":
                if hero not in shitty_wizard:
                    shitty_wizard[hero] = value
            else:
                if key not in responses:
                    responses[key] = value

    responses['one of my favourites'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/b/b6/Invo_ability_invoke_01.mp3'
    responses['lolicon'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/a/a9/Arcwar_lasthit_04.mp3'
    responses['ho ho ha ha'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/1/17/Snip_ability_shrapnel_03.mp3'
    
    responses['caw'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/f/f6/Phoenix_bird_last_hit.mp3'
    responses['skree'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/a/a5/Phoenix_bird_attack.mp3'
    responses['beep boop'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/4/4f/Wisp_Move04.mp3'
    responses['boop'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/5/5f/Wisp_Move02.mp3'
    responses['beep'] = 'http://hydra-media.cursecdn.com/dota2.gamepedia.com/5/54/Wisp_Move01.mp3'
    
    heroes['Phoenix'] = 'Phoenix'
    heroes['Wisp'] = 'Io'
    
    return responses, heroes, shitty_wizard
    

def create_list_of_responses(ending):
    page = page_to_parse(URL_BEGINNING + ending)
    soup = BeautifulSoup(page, "html.parser")
    list_of_responses = []

    for element in soup.find_all("li"):
        if "sm2_button" in str(element):
            list_of_responses.append(str(element))
            
    return list_of_responses
    
    
def page_to_parse(url):
    """Method used to open given url and return the received body (UTF-8 encoding)."""
    request = Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urlopen(request)
    return response.read().decode("UTF-8")


def pages_for_category(category_name):
    """Method that returns a list of page endings for a given Wiki category."""
    category_name = category_name.replace(" ", "_")
    json_response = page_to_parse(URL_BEGINNING + URL_API + category_name)

    output = []

    parsed_json = json.loads(json_response)
    for categorymembers in parsed_json["query"]["categorymembers"]:
        for value in categorymembers.values():
            if isinstance(value, str) and '/' not in value:
                output.append(value.replace(" ", "_"))

    return output


def response_text_from_element(element):
    """Method that returns a key for a given element taken from parsed html body."""
    start_index = element.rfind("</a>") + 4
    end_index = element.find("</li>") - 1
    key = element[start_index:end_index]
    key = clean_key(key)
    return key


def clean_key(key):
    """Method that cleans the given key, so that it is a lowercase string with
    no dots or exclamation marks ending the string. All html tags are removed as well."""
    if "<i>" in key:
        start_index = key.find("<i>")
        end_index = key.rfind("</i>") + 4
        key = key.replace(key[start_index:end_index], "")

    if "(" in key and ")" in key:
        start_index = key.find("(")
        end_index = key.rfind(")") + 1
        key = key.replace(key[start_index:end_index], "")

    key = key.strip()

    try:
        if key[-1] in [".", "!"]:
            key = key[:-1]
    except IndexError:
        print("IndexError in: " + key)

    if key[-2:] == "--":
        key = key[:-2]

    key = key.replace("  ", " ")

    key = key.strip()
    key = key.lower()

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
            if search.group(1) == 'tech':
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


# generate_dictionaries(properties.RESPONSES_FILENAME, properties.HEROES_FILENAME, properties.SHITTY_WIZARD_FILENAME)
# dictionary = dictionary_from_file(properties.RESPONSES_FILENAME)
