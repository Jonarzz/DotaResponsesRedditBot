from util.str_utils import preprocess_text
import requests


def request_cargo_set(url):
    web_request = requests.get(url)
    web_json = web_request.json()
    SELECTED_EXCLUDED_RESPONSES = {}
    cargo_set = set()
    for objects in web_json['cargoquery']:
        cargo = preprocess_text(objects['title']['title'])
        if cargo not in  SELECTED_EXCLUDED_RESPONSES: 
            cargo_set.add(cargo)
    return cargo_set
