"""Module used to configure the connection to the Reddit API.
"""

import webbrowser

import praw

import config as properties

__author__ = 'Jonarzz'

INVALID_CODE_ERR_MSG = 'Invalid access code'


def get_reddit():
    """Method preparing the connection to Reddit API using OAuth."""
    return praw.Reddit(user_agent=properties.USER_AGENT, client_id=properties.APP_ID,
                       client_secret=properties.APP_SECRET, refresh_token=properties.APP_REFRESH_CODE,
                       redirect_uri=properties.APP_URI)


def get_account():
    """Method preparing the account using Reddit API."""
    reddit = get_reddit()
    return reddit


def generate_access_code(test=False):
    """Method used to generate the access code to Reddit API."""
    reddit = get_reddit()

    url = reddit.auth.url(state='uniqueKey', scopes=properties.SCOPES)
    if test:
        return url
    else:
        webbrowser.open(url)


def get_refresh_token(code):
    """Method that prints the account refresh token related to Reddit API.

    Requires the user to type in the code that can be obtained through the request to the redirect uri.
    :return: The obtained refresh token, if available, otherwise None.
    """
    reddit = get_reddit()
    return reddit.auth.authorize(code)


def get_scopes():
    """
    For read-only authorizations this should return {'*'}
    :return: A set of scopes included in the current authorization.
    """
    reddit = get_reddit()
    return reddit.auth.scopes()
