from util.str_utils import preprocess_text
import requests


def get_titles_from_cargo_tables(table):
    from config import API_PATH, CARGO_API_PARAMS

    params = CARGO_API_PARAMS.copy()
    params['tables'] = table

    json_response = requests.get(url=API_PATH, params=params).json()
    cargo_set = set()
    for item in json_response['cargoquery']:
        cargo_set.add(preprocess_text(item['title']['title']))
    return cargo_set
