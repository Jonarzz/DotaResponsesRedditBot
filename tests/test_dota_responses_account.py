"""Module used to test dota_responses_account module methods.
Removed extra tests because they were not testing any of our code logic.
This must've been tested by PRAW already.
"""

import unittest

import bot.account as account
import config

__author__ = 'Jonarzz'


class AccountTest(unittest.TestCase):
    """Class used to test dota_responses_account module.
    Inherits from TestCase class of unittest module.
    """

    def test_get_reddit(self):
        """Method testing get_reddit method from dota_responses_account module.

        The method tests if the OAuth info was provided, if the logging in was successful
        and if the client properties (app ID and secret) were passed properly to the Reddit API
        handler framework object.
        """
        reddit = account.get_account()

        self.assertTrue(reddit.has_oauth_app_info)
        self.assertFalse(reddit.is_logged_in())
        self.assertEqual(reddit.client_id, config.CLIENT_ID)
        self.assertEqual(reddit.client_secret, config.CLIENT_SECRET)
