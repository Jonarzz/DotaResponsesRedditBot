"""Main module of the Dota 2 subreddit Responses Bot.

The main body of the script is running in this file. The comments are loaded from the subreddit
and the script checks if the comment or submission is a response from Dota 2. If it is, a proper reply for response is
prepared. The response is posted as a reply to the original comment/submission on Reddit.
"""
import time

from praw.exceptions import APIException
from praw.models import Comment
from prawcore import ServerError

import config
from bot import account
from util.caching import get_cache_api
from util.database.database import db_api
from util.logger import logger
from util.str_utils import preprocess_text

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'

cache_api = get_cache_api()


def work():
    """Main method executing the script.

    It connects to an account, loads dictionaries from proper files (declared in config file).
    Afterwards it executes process_comments method with proper arguments passed.
    """

    reddit = account.get_account()
    logger.info('Connected to Reddit account : ' + config.USERNAME)

    while True:
        # Streams need to be restarted when they throw exception
        comment_stream = reddit.subreddit(config.SUBREDDIT).stream.comments(pause_after=-1)
        submission_stream = reddit.subreddit(config.SUBREDDIT).stream.submissions(pause_after=-1)
        try:
            for comment in comment_stream:
                if comment is None:
                    break
                process_replyable(reddit, comment)
            for submission in submission_stream:
                if submission is None:
                    break
                process_replyable(reddit, submission)
        except ServerError as e:
            logger.critical("Reddit server is down : " + str(e))
            time.sleep(120)
        except APIException as e:
            logger.critical("API Exception occurred : " + str(e))
            time.sleep(60)


def process_replyable(reddit, replyable):
    """Method used to check all the comments in a submission and add replies if they are responses.

    PRAW generates past ~100 comments/submissions on the first iteration. Then the loop only runs if there is a new
    comment/submission added to the stream. This also means that once PRAW is up and running, after the initial comments
    list it won't generate any duplicate comments.

    However, just as a safeguard, Caching is used to store replyable ids as they are processed for the first time.
    Otherwise, when the bot is restarted it might reply twice to same comments. If replyable id is in the already present
    in the cache_api, then it is ignored, else processed and added to the cache_api.
    * Self comments are ignored.
    * It is prepared for comparison to the responses in dictionary.
    * If the replyable is not on the excluded responses list (loaded from config) and if it is in the responses db or
    specific responses list, a reply replyable is prepared and posted.

    :param reddit: The reddit account instance
    :param replyable: comment or submission
    :return: None
    """

    if cache_api.exists(thing_id=replyable.fullname):
        return

    # Ignore thyself
    if replyable.author == reddit.user.me():
        return

    logger.info("Found new replyable: " + replyable.fullname)

    processed_text = process_text(replyable.body if isinstance(replyable, Comment) else replyable.title)

    # TODO make use of assignment expression for all below
    if is_excluded_response(processed_text):
        pass
    elif is_custom_response(processed_text):
        add_custom_reply(replyable, processed_text)
    elif is_hero_specific_response(processed_text):
        add_hero_specific_reply(replyable, processed_text)
    elif is_flair_specific_response(replyable, processed_text):
        add_flair_specific_reply(replyable, processed_text)
    else:
        add_regular_reply(replyable, processed_text)


def process_text(text):
    """Method used to clean the replyable body/title text.
    If text contains a quote, the first quote text is considered as the text.

    Removed code to remove repeating letters in a text because it does more harm than good - words like 'all', 'tree'
    are stripped to 'al' and 'tre' which dont match with any responses.

    :param text: The replyable body/title text
    :return: Processed text
    """
    hero_name = None
    if '>' in text:
        text = get_quoted_text(text)
    if '::' in text:
        hero_name, text = text.split('::', 1)
        hero_name = hero_name.strip() + '::'

    return (hero_name or '') + preprocess_text(text)


def get_quoted_text(text):
    """Method used to get quoted text.
    If body/title text contains a quote, the first quote is considered as the text.

    :param text: The replyable text
    :return: The first quote in the text. If no quotes are found, then the entire text is returned
    """
    lines = text.split('\n\n')
    for line in lines:
        if line.startswith('>'):
            return line[1:]
    return text


def is_excluded_response(text):
    """Method to check if the given body/title is in excluded responses set.
    Also return False for single word text (they're mostly common phrases).

    :param text: The processed body/title text
    :return: True if text is an excluded response, else False
    """
    return ' ' not in text or text in config.EXCLUDED_RESPONSES


def is_custom_response(text):
    """Method to check if given body/title text is in custom response set.

    :param text: The body/title text
    :return: True if text is a custom response, else False
    """
    return text in config.CUSTOM_RESPONSES


def add_custom_reply(replyable, body):
    """Method to create a custom reply for specific cases that match the custom responses set.

    :param replyable: The comment/submission on reddit
    :param body: The processed body/title text
    :return: None
    """
    custom_response = config.CUSTOM_RESPONSES[body]
    original_text = replyable.body if isinstance(replyable, Comment) else replyable.title

    reply = custom_response.format(original_text, config.COMMENT_ENDING)
    replyable.reply(reply)
    logger.info("Replied to: " + replyable.fullname)


def is_hero_specific_response(text):
    """Method that checks if response for specified hero name and text exists.

    :param text: The processed body/title text
    :return: True if the response for specified hero was found, else False
    """
    if '::' in text:
        hero_name, text = text.split('::', 1)

        if not hero_name or not text:
            return False

        hero_id = db_api.get_hero_id_by_name(hero_name=hero_name)
        if hero_id:
            link, _ = db_api.get_link_for_response(processed_text=text, hero_id=hero_id)
            if link:
                return True
    return False


def add_hero_specific_reply(replyable, text):
    """Method to add a hero specific reply to the comment/submission.

    :param replyable: The comment/submission on reddit
    :param text: The processed body/title text
    :return: None
    """
    hero_name, text = text.split('::', 1)
    hero_id = db_api.get_hero_id_by_name(hero_name=hero_name)
    link, _ = db_api.get_link_for_response(processed_text=text, hero_id=hero_id)
    create_and_add_reply(replyable=replyable, response_url=link, hero_id=hero_id)


def is_flair_specific_response(replyable, text):
    """Method that checks if response for hero in author's flair and text exists.

    :param replyable: The comment/submission on reddit
    :param text: The processed body/title text
    :return: True if the response for author's flair's hero was found, else False
    """
    hero_id = db_api.get_hero_id_by_flair_css(flair_css=replyable.author_flair_css_class)
    if hero_id:
        link, _ = db_api.get_link_for_response(processed_text=text, hero_id=hero_id)
        if link:
            return True
    return False


def add_flair_specific_reply(replyable, text):
    """Method to add a author's flair specific reply to the comment/submission.

    :param replyable: The comment/submission on reddit
    :param text: The processed body/title text
    :return: None
    """
    hero_id = db_api.get_hero_id_by_flair_css(flair_css=replyable.author_flair_css_class)
    link, _ = db_api.get_link_for_response(processed_text=text, hero_id=hero_id)
    create_and_add_reply(replyable=replyable, response_url=link, hero_id=hero_id)


def add_regular_reply(replyable, text):
    """Method to create response for given replyable.
    In case of multiple matches, it used to sort responses in descending order of heroes and get the first one,
    but now it's random.

    :param replyable: The comment/submission on reddit
    :param text: The processed body/title text
    :return: None
    """

    link, hero_id = db_api.get_link_for_response(processed_text=text)

    if link and hero_id:
        create_and_add_reply(replyable=replyable, response_url=link, hero_id=hero_id)


def create_and_add_reply(replyable, response_url, hero_id):
    """Method that creates a reply in reddit format and adds the reply to comment/submission.
    The reply consists of a link to the response audio file, the response itself, a warning about the sound
    and an ending added from the config file (post footer).
    
    Image is currently ignored due to new reddit redesign not rendering flairs properly.

    :param replyable: The comment/submission on reddit
    :param response_url: The url to the response audio file
    :param hero_id: The hero_id to which the response belongs to.
    :return: The text for the comment reply.
    """
    original_text = replyable.body if isinstance(replyable, Comment) else replyable.title
    original_text = original_text.strip()

    if '>' in original_text:
        original_text = get_quoted_text(original_text).strip()
    if '::' in original_text:
        original_text = original_text.split('::', 1)[1].strip()

    hero_name = db_api.get_hero_name(hero_id)
    reply = "[{}]({}) (sound warning: {}){}".format(original_text, response_url, hero_name, config.COMMENT_ENDING)
    replyable.reply(reply)
    logger.info("Replied to: " + replyable.fullname)
