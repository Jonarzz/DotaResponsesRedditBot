import time

import requests
from ratelimit import sleep_and_retry, limits

from config import USER_AGENT
from parsers.parser_config import API_PATH

headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "User-Agent": USER_AGENT}


def get_page_source(page_title):
    response = get_wiki_data(
        params={'action': 'query', 'prop': 'revisions', 'titles': page_title, 'rvslots': '*', 'rvprop': 'content',
                'format': 'json'})
    response_json = response.json()

    pages = response_json['query']['pages']
    for _, page in pages.items():
        return page['revisions'][0]['slots']['main']['*']


@sleep_and_retry
@limits(calls=1, period=2)
def get_wiki_data(params, retries=0):
    if retries == 3:
        raise Exception(f'Exceeded max retries for params {params}')
    response = requests.get(url=API_PATH, params=params, headers=headers)

    if response.status_code == 429:
        wait_time = int(response.headers['Retry-After'])
        time.sleep(wait_time)
        return get_wiki_data(params, retries + 1)
    elif response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response
