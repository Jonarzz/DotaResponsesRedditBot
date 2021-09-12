import re
import string

import redditcleaner

PUNCTUATION_TRANS = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
WHITESPACE_TRANS = str.maketrans(string.whitespace, ' ' * len(string.whitespace))
LINK_PATTERN = re.compile(r'\[(.*?)]\s*\(.*?\)')
MULTIPLE_WHITESPACES_PATTERN = re.compile(r'\s+')


def preprocess_text(text):
    """Method for pre-processing the given response text.
    It:
    * replaces all punctuations with spaces
    * replaces all whitespace characters (tab, newline etc) with spaces
    * removes trailing and leading spaces
    * removes double spaces
    * changes to lowercase

    :param text: the text to be cleaned
    :return: cleaned text
    """

    text = text.translate(PUNCTUATION_TRANS)
    text = text.translate(WHITESPACE_TRANS)
    text = text.strip().lower()
    text = MULTIPLE_WHITESPACES_PATTERN.sub(' ', text)
    text = LINK_PATTERN.sub(r'\1', text)
    return text


def get_processed_hero_name(hero_name):
    """Method for pre-processing the given response text.
    Removes various keywords from the name, generally in case of announcer and voice packs.

    :param hero_name: The hero's original name
    :return: The hero's name after processing
    """

    processed_name = preprocess_text(hero_name)
    processed_name = processed_name.replace('announcer pack', '')
    processed_name = processed_name.replace('announcer', '')
    processed_name = processed_name.replace('mega kills', '')
    processed_name = processed_name.replace('bundle', '')
    processed_name = processed_name.replace('voice of', '')
    return processed_name


def get_formatted_text_for_reply(original_text):
    """Method to format the original text in comment/submission to be used in reply.
    Removes most of Reddit's markdown formatting.
    redditcleaner removes links as well, so those are handled separately first.

    :param original_text: The original text
    :return: The formatted text
    """
    text = LINK_PATTERN.sub(r'\1', original_text)
    text = redditcleaner.clean(text)
    return text
