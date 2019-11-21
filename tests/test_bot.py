"""Module used to test bot worker module methods."""

import unittest

import config
from bot import account
from bot import worker

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


class BotWorkerTest(unittest.TestCase):
    """Class used to test bot worker module.
    Inherits from TestCase class of unittest module.
    """

    def test_parse_comment(self):
        """Method that tests the parse_comment method from worker module.
        """
        self.assertEqual(worker.parse_comment(
            "That's a great idea!!!"), "that s a great idea")
        self.assertEqual(worker.parse_comment("  WoNdErFuL  "), "wonderful")
        self.assertEqual(worker.parse_comment("How are you?"), "how are you")
        self.assertEqual(worker.parse_comment(
            "Isn't is good to have quotes?  you can add your response in quote and bot would still \n\n> reply to them"),
            "reply to them")
        self.assertEqual(worker.parse_comment(
            "> multiple quotes \n\n > but reply to \n\n > only first one"), "multiple quotes")

    def test_account(self):
        reddit = account.get_account()
        self.assertEqual(reddit.user.me(), config.USERNAME)
