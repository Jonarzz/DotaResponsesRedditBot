from parsers import parser_config
from util.str_utils import preprocess_text
from util.wiki_api import get_wiki_data


# TODO move away from cargoquery
def get_titles_from_cargo_tables(table):
    params = parser_config.CARGO_API_PARAMS.copy()
    params['tables'] = table

    json_response = get_wiki_data(params).json()
    cargo_set = set()
    try:
        for item in json_response['cargoquery']:
            cargo_set.add(preprocess_text(item['title']['title']))
    except KeyError:
        pass
    return cargo_set
