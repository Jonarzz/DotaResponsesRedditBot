"""Module used to test dotaresponses module methods."""

import unittest

import dotaresponses
import dota_responses_properties as properties

__author__ = 'Jonarzz'


class DotaResponsesTest(unittest.TestCase):
    """Class used to test dotaresponses module.
    Inherits from TestCase class of unittest module."""

    def test_create_reply(self):
        """Method that tests the create_reply method from dotaresponses module.

        It checks whether the returned value is the same as the expected string.
        """
        responses_dict = {'abc' : 'http://def.gh/Abad_a_.mp3', '123' : 'http://456.78/Noba_a_.mp3'}
        heroes_dict = {'Abad' : 'Abaddon', 'Noba' : 'Techies'}

        expected_output = ("[{}]({}) (sound warning: {}){}"
                           .format('abc', 'http://def.gh/Abad_a_.mp3', 'Abaddon',
                                   properties.COMMENT_ENDING)
                          )
        self.assertEqual(dotaresponses.create_reply(responses_dict, heroes_dict, 'abc', 'abc'),
                         expected_output)

        expected_output = ("[{}]({}) (sound warning: {}){}"
                           .format('123', 'http://456.78/Noba_a_.mp3', 'Techies',
                                   properties.COMMENT_ENDING)
                          )
        self.assertEqual(dotaresponses.create_reply(responses_dict, heroes_dict, '123', '123'),
                         expected_output)

    def test_prepare_response(self):
        """Method that tests the prepare_response method from dotaresponses module.

        It checks whether the returned value is the same as the expected string.
        """
        self.assertEqual(dotaresponses.prepare_response("That's a great idea!!!"),
                         "that's a great idea")
        self.assertEqual(dotaresponses.prepare_response("Wonderfullll"), "wonderful")
        self.assertEqual(dotaresponses.prepare_response("How are you?"), "how are you?")
