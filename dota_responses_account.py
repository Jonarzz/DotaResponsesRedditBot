"""Module used to configure the connection to the Reddit API."""

import webbrowser

import praw

import dota_responses_properties as properties

__author__ = 'Jonarzz'


INVALID_CODE_ERR_MSG = 'Invalid access code'


def get_reddit():
    """Method preparing the connection to Reddit API using OAuth."""
    return praw.Reddit(user_agent=properties.USER_AGENT, client_id=properties.APP_ID, client_secret=properties.APP_SECRET, refresh_token=properties.APP_REFRESH_CODE)


def get_account():
    """Method preparing the account using Reddit API."""
    reddit = get_reddit()
    return reddit


def generate_access_code(test=False):
    """Method used to generate the access code to Reddit API."""
    reddit = get_reddit()
    url = reddit.get_authorize_url('uniqueKey', properties.SCOPES, True)
    if test:
        return url
    else:
        webbrowser.open(url)


def get_access_information(access_code):
    """Method that prints the account access information related to Reddit API.

    Requires the user to type in the access_code that can be retrieved by attaching the account
    connected to the Reddit API to the user's Reddit account. The code is provided in a link after
    accepting the requirements (provided in the script scope in the properties).
    """
    reddit = get_reddit()
    try:
        access_information = reddit.get_access_information(access_code)
    except praw.errors.OAuthInvalidGrant:
        return INVALID_CODE_ERR_MSG
    else:
        return access_information
 

# print(get_access_information)
