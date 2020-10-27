from util.str_utils import preprocess_text
import requests


def request_hero_name_set():
    WEB_REQUEST = requests.get('https://dota2.gamepedia.com/api.php?' +
                                'action=cargoquery&tables=heroes&fields=title&where=game'+
                                '+IS+NULL&limit=500&format=json')
    WEB_JSON = WEB_REQUEST.json()
    SELECTED_HERO_RESPONSES = {}
    HERO_NAME_RESPONSES = set()
    for WEB_OBJECT in WEB_JSON['cargoquery']:
        HERO_ENTRIES = preprocess_text(WEB_OBJECT['title']['title'])
        if HERO_ENTRIES not in SELECTED_HERO_RESPONSES: 
            HERO_NAME_RESPONSES.add(HERO_ENTRIES)
    return (HERO_NAME_RESPONSES)
        
            
def request_item_name_set():
    WEB_REQUEST = requests.get('https://dota2.gamepedia.com/api.php?'+
                                'action=cargoquery&tables=items&fields='+
                                'title&where=game+IS+NULL&limit=500&format=json')
    WEB_JSON = WEB_REQUEST.json()
    SELECTED_ITEM_RESPONSES = {}
    ITEM_RESPONSES = set()
    for WEB_OBJECT in WEB_JSON['cargoquery']:
        ITEM_ENTRIES = preprocess_text(WEB_OBJECT['title']['title'])
        if ITEM_ENTRIES not in SELECTED_ITEM_RESPONSES: 
            ITEM_RESPONSES.add(ITEM_ENTRIES)
    return(ITEM_RESPONSES)