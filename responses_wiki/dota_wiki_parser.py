__author__ = "Jonarzz"

from urllib.request import Request
from urllib.request import urlopen
import json

URL_BEFORE_CATEGORY = "http://dota2.gamepedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:"
URL_AFTER_CATEGORY = "&cmlimit=max&cmprop=title&format=json"

def pages_for_category(category_name):
    """ Returns list of pages in given category.
    :return: List of pages in given category.
    """
    category_name = category_name.replace(" ", "_")

    request = Request(URL_BEFORE_CATEGORY + category_name + URL_AFTER_CATEGORY)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urlopen(request)
    json_response = response.read().decode("utf-8")

    output = []

    parsed_json = json.loads(json_response)
    for a in parsed_json["query"]["categorymembers"]:
        for b in a.values():
            if (type(b) is str and '/' not in b):
                output.append(b.replace(" ", "_"))

    return output

z = pages_for_category("Lists of responses")
print(z)