from util.str_utils import preprocess_text
import requests


def request_cargo_set(url):
    web_request = requests.get(url)
    web_json = web_request.json()
    cargo_set = set()
    for objects in web_json['cargoquery']:
        cargo_set.add(preprocess_text(objects['title']['title']))
    return cargo_set
