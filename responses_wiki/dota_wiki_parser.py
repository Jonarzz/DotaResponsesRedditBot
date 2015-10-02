# coding=UTF-8
from urllib.request import Request
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
import pprint

__author__ = "Jonarzz"

URL_BEGINNING = "http://dota2.gamepedia.com/"
URL_API = "api.php?action=query&list=categorymembers&cmlimit=max&cmprop=title&format=json&cmtitle=Category:"
CATEGORY = "Lists of responses"


def generate_json_with_responses_mapping(filename):
    dict = dictionary_of_responses(pages_for_category(CATEGORY))
    json.dump(dict, open(filename, "w"))


def dictionary_from_file(filename):
    dict = json.load(open(filename))
    return dict


def dictionary_of_responses(pages_endings):
    output = {}

    for ending in pages_endings:
        print(ending)
        page = page_to_parse(URL_BEGINNING + ending)
        soup = BeautifulSoup(page, "html.parser")
        list_of_responses = []

        for element in soup.find_all("li"):
            if "sm2_button" in str(element):
                list_of_responses.append(str(element))

        for element in list_of_responses:
            key = key_from_element(element)
            value = value_from_element(element)
            if key not in output:
                output[key] = value

    return output


def page_to_parse(url):
    request = Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urlopen(request)
    return response.read().decode("UTF-8")


def pages_for_category(category_name):
    category_name = category_name.replace(" ", "_")
    json_response = page_to_parse(URL_BEGINNING + URL_API + category_name)

    output = []

    parsed_json = json.loads(json_response)
    for a in parsed_json["query"]["categorymembers"]:
        for b in a.values():
            if type(b) is str and '/' not in b:
                output.append(b.replace(" ", "_"))

    return output


def key_from_element(element):
    start_index = element.rfind("</a>") + 4
    end_index = element.find("</li>") - 1
    key = element[start_index:end_index]
    key = clean_key(key)
    return key


def clean_key(key):
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

    key = key.strip()
    key = key.lower()

    return key


def value_from_element(element):
    start_index = element.find("href=\"") + 6
    end_index = element.find("\" title")
    value = element[start_index:end_index]
    return value


def ellipsis_to_three_dots(dict):
    newdict = {}

    for key in dict:
        newdict[key] = dict[key]
        if "…" in key:
            new = key.replace("…", "...")
            newdict[new] = newdict.pop(key)

    return newdict


# generate_json_with_responses_mapping("dota_responses.txt")
dictionary = dictionary_from_file("dota_responses_1.1.txt")
