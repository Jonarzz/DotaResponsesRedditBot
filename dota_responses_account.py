import praw
import dota_responses_properties as properties

__author__ = "Jonarzz"


def get_reddit():
    r = praw.Reddit(properties.USER_AGENT)
    r.set_oauth_app_info(properties.APP_ID, properties.APP_SECRET, properties.APP_URI)
    return r


def get_account():
    r = get_reddit()
    r.refresh_access_information(properties.APP_REFRESH_CODE)
    return r


def generate_access_code():
    r = get_reddit()
    url = r.get_authorize_url('uniqueKey', properties.SCOPES, True)
    import webbrowser
    webbrowser.open(url)


def print_access_information(access_code):
    r = get_reddit()
    access_information = r.get_access_information(access_code)
    print(access_information)
