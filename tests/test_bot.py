"""Module used to test bot worker module methods.
"""

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
        """Method that tests the process_text method from worker module.
        """
        self.assertEqual(worker.process_text(
            "That's a great idea!!!"), "that s a great idea")
        self.assertEqual(worker.process_text("  WoNdErFuL  "), "wonderful")
        self.assertEqual(worker.process_text("How are you?"), "how are you")
        self.assertEqual(worker.process_text(
            "Isn't is good to have quotes?  you can add any response in quote and bot would still \n\n> reply to them"),
            "reply to them")
        self.assertEqual(worker.process_text(
            "> multiple quotes \n\n > but reply to \n\n > only first one"), "multiple quotes")

    def test_account(self):
        """Method used to test the Reddit instance returned by get_account()
        """
        reddit = account.get_account()
        self.assertEqual(reddit.user.me(), config.USERNAME)
