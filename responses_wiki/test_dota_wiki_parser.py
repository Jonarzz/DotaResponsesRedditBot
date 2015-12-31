"""Module used to test dota_wiki_parser module methods."""

import unittest

import dota_wiki_parser as parser

__author__ = 'Jonarzz'


class AccountTest(unittest.TestCase):
    """Class used to test dota_wiki_parser module.
    Inherits from TestCase class of unittest module."""

    def test_dictionary_from_file(self):
        """Method testing dictionary_from_file method from dota_wiki_parser module.

        The method checks if the imported dictionary from .txt file with JSON content
        is the same as predefined dictionary in the test case.
        """
        resp_dict = {"abc" : "http://def.gh/Abad_a_.mp3", "123" : "http://456.78/Noba_a_.mp3"}
        hero_dict = {"Abad" : "Abaddon", "Noba" : "Techies"}

        self.assertEqual(parser.dictionary_from_file('test_responses_dict.txt'), resp_dict)
        self.assertEqual(parser.dictionary_from_file('test_heroes_dict.txt'), hero_dict)
