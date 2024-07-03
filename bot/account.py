"""Module used to configure the connection to the Reddit API.
Removed old Code Flow auth in favor of Password Flow auth.
Reason: https://www.reddit.com/r/redditdev/comments/5fxlk8/praw_refresh_tokens/dantjyk/
"""

import praw

import config
from bot import bot_config

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


def get_account():
    """Method that provides the connection to Reddit API using OAuth.
        :return: Reddit instance.
    """
    return praw.Reddit(client_id=bot_config.CLIENT_ID, client_secret=bot_config.CLIENT_SECRET,
                       user_agent=config.USER_AGENT, username=bot_config.USERNAME, password=bot_config.PASSWORD)
