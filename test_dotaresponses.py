"""Module used to test dotaresponses module methods."""

import unittest

import dotaresponses
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser

__author__ = 'Jonarzz'


class DotaResponsesTest(unittest.TestCase):
    """Class used to test dotaresponses module.
    Inherits from TestCase class of unittest module."""

    def test_prepare_response(self):
        """Method that tests the prepare_response method from dotaresponses module.

        It checks whether the returned value is the same as the expected string.
        """
        self.assertEqual(dotaresponses.prepare_response("That's a great idea!!!"), "that's a great idea")
        self.assertEqual(dotaresponses.prepare_response("  WoNdErFuL  "), "wonderful")
        self.assertEqual(dotaresponses.prepare_response("How are you?"), "how are you?")
