"""Module used to test dota_responses_account module methods."""

import unittest

import dota_responses_account as account
import dota_responses_properties as properties

__author__ = 'Jonarzz'


class AccountTest(unittest.TestCase):
    """Class used to test dota_responses_account module.
    Inherits from TestCase class of unittest module."""

    def test_get_reddit(self):
        """Method testing get_reddit method from dota_responses_account module.

        The method tests if the OAuth info was provided, if the logging in was successful
        and if the client properties (app ID and secret) were passed properly to the Reddit API
        handler framework object.
        """
        reddit = account.get_reddit()

        self.assertTrue(reddit.has_oauth_app_info)
        self.assertFalse(reddit.is_logged_in())
        self.assertEqual(reddit.client_id, properties.APP_ID)
        self.assertEqual(reddit.client_secret, properties.APP_SECRET)

    def test_get_account(self):
        """Method testing get_account method from dota_responses_account module.

        The method tests if all the Reddit API scopes provided in properties file are applied
        to the Reddit API handler framework object.
        """
        reddit = account.get_account()
        scopes_list = properties.SCOPES.split(' ')

        self.assertIsNotNone(reddit.access_token)
        for scope in scopes_list:
            self.assertTrue(reddit.has_scope(scope))

    def test_generate_access_code(self):
        """Method testing generate_access_code method from dota_responses_account module.

        The method tests if the generated url that is opened in the web browser if the method
        is called without an argument (test value set as False) contains the required data loaded
        from the properties: Reddit API scopes, app URI, app ID.
        """
        prepared_uri = properties.APP_URI.replace(':', '%3A').replace('/', '%2F')
        url = account.generate_access_code(test=True)

        self.assertTrue(properties.SCOPES.replace(' ', '+') in url)
        self.assertTrue(prepared_uri in url)
        self.assertTrue(properties.APP_ID in url)

    def test_get_access_information(self):
        """Method testing get_access_information method from dota_responses_account module.

        The method tests only the wrong access code input as get_access_information method requires
        direct external interaction from the user.
        """

        self.assertEqual(account.get_access_information('123'), account.INVALID_CODE_ERR_MSG)
