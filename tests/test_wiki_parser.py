"""Module used to test dota_wiki_parser module methods.
"""

import unittest

from config import RESPONSES_CATEGORY
from parsers import wiki_parser

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'


class WikiParserTest(unittest.TestCase):
    """Class used to test wiki_parser module.
    Inherits from TestCase class of unittest module.
    """

    def test_pages_to_parse(self):
        """Method testing pages_to_ppages_for_categoryarse method from wiki_parser module.
        The method checks if the requested response is consists of pages as expected.
        """
        pages = wiki_parser.pages_for_category(RESPONSES_CATEGORY)

        self.assertTrue(len(pages) > 150)
        self.assertTrue('Abaddon/Responses' in pages)
        self.assertTrue('Zeus/Responses' in pages)
