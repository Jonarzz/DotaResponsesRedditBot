import re
import string

PUNCTUATION_TRANS = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
WHITESPACE_TRANS = str.maketrans(string.whitespace, ' ' * len(string.whitespace))


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
    text = re.sub(' +', ' ', text)
    return text
