"""Module used to configure the connection to the Reddit API."""

import praw

import dota_responses_properties as properties

__author__ = "Jonarzz"


def get_reddit():
    """Method preparing the connection to Reddit API using OAuth."""
    reddit = praw.Reddit(properties.USER_AGENT)
    reddit.set_oauth_app_info(properties.APP_ID, properties.APP_SECRET, properties.APP_URI)
    return reddit


def get_account():
    """Method preparing the account using Reddit API."""
    reddit = get_reddit()
    reddit.refresh_access_information(properties.APP_REFRESH_CODE)
    return reddit


def generate_access_code():
    """Method used to generate the access code to Reddit API."""
    reddit = get_reddit()
    url = reddit.get_authorize_url('uniqueKey', properties.SCOPES, True)
    import webbrowser
    webbrowser.open(url)


def print_access_information(access_code):
    """Method that prints the account access information related to Reddit API."""
    reddit = get_reddit()
    access_information = reddit.get_access_information(access_code)
    print(access_information)
