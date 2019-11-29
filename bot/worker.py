"""Main module of the Dota 2 subreddit Responses Bot.

The main body of the script is running in this file. The comments are loaded from the subreddit
and the script checks if the thing is a response from Dota 2. If it is, a proper thing is
prepared. The thing is posted as a reply to the original post on Reddit.

Proper logging is provided - saved to 2 files as standard output and errors.
"""
import string

from praw.models import Comment

import config
from bot import account
from util.caching import get_cache_api
from util.database.database import db_api
from util.logger import logger

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

    comment_stream = reddit.subreddit(config.SUBREDDIT).stream.comments(pause_after=-1)
    submission_stream = reddit.subreddit(config.SUBREDDIT).stream.submissions(pause_after=-1)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            process_thing(reddit, comment)
        for submission in submission_stream:
            if submission is None:
                break
            process_thing(reddit, submission)


def process_thing(reddit, thing):
    """Method used to check all the comments in a submission and add replies if they are responses.

    PRAW generates past ~100 comments on the first iteration. Then the loop only runs if there is a new thing added to
    the comments stream. This also means that once PRAW is up and running, after the initial comments list it won't
    generate any duplicate comments.

    However, just as a safeguard, Caching is used to store thing ids as they are processed for the first time.
    Otherwise, when the bot is restarted it might reply twice to same comments. If thing id is in the already present
    in the cache_api, then it is ignored, else processed and added to the cache_api.
    * Self comments are ignored.
    * It is prepared for comparision to the responses in dictionary.
    * If the thing is not on the excluded responses list (loaded from config) and if it is in the responses db or
    specific responses list, a reply thing is prepared and posted.
    """

    if cache_api.check(thing_id=thing.fullname):
        return

    # Ignore thyself
    if thing.author == reddit.user.me:
        return

    logger.debug("Found new thing: " + str(thing.fullname))

    processed_body = process_body(thing.body if isinstance(thing, Comment) else thing.title)

    # Don't reply to single word text (they're mostly common phrases).
    if ' ' not in processed_body:
        return

    if processed_body in config.EXCLUDED_RESPONSES:
        return

    if processed_body in config.CUSTOM_RESPONSES:
        do_custom_reply(thing=thing, custom_response=config.CUSTOM_RESPONSES[processed_body])

    if do_flair_specific_reply(thing, processed_body):
        return

    do_regular_reply(thing, processed_body)


def process_body(body_text):
    """Method used to clean the thing text. Logic is similar to clean_response_text on wiki parsers.
    * If thing contains a quote, the first quote is considered as the response_text.
    * Punctuation marks are replaced with space.
    * The response_text is turned to lowercase.
    * Converts multiple spaces into single space.

    Removed code to remove repeating letters in a thing because it does more harm than good - words like 'all',
    'tree' are stripped to 'al' and 'tre' which dont match with any responses.

    :param body_text: The thing body
    :return: Processed thing body
    """

    if '>' in body_text:
        lines = body_text.split('\n\n')
        for line in lines:
            if line.startswith('>'):
                body_text = line
                break

    body_text = body_text.translate(PUNCTUATION_TRANS)
    body_text = body_text.translate(WHITESPACE_TRANS)

    while '  ' in body_text:
        body_text = body_text.replace('  ', ' ')

    body_text = body_text.strip().lower()

    return body_text


def do_flair_specific_reply(thing, response):
    hero_id = db_api.get_hero_id_by_flair_css(flair_css=thing.author_flair_css_class)
    if hero_id:
        link, hero_id = db_api.get_link_for_response(
            processed_text=response, hero_id=hero_id)
        if link:
            reply = create_reply(thing=thing, response_url=link, hero_id=hero_id)
            thing.reply(reply)
            logger.info("Added: " + thing.fullname)
            return True


def do_regular_reply(thing, response):
    """Method to create response for given thing.
    In case of multiple matches, it used to sort responses in descending order of heroes, but now it's random.
    add_shitty_wizard_response was very similar to this, and hence has been merged

    :param thing: The thing/submission on reddit
    :param response: The plaintext processed thing body
    :return: None
    """

    link, hero_id = db_api.get_link_for_response(processed_text=response)

    if link and hero_id:
        img_dir = db_api.get_img_dir_by_id(hero_id=hero_id)

        thing.reply(create_reply(thing=thing, response_url=link, hero_id=hero_id, img=img_dir))

        logger.info("Replied to: " + thing.id)


def create_reply(thing, response_url, hero_id, img=None):
    """Method that creates a reply in reddit format.

    The message consists of a link the the response, the response itself, a warning about the sound
    and an ending added from the config file (post footer). Image is currently ignored due to new reddit not
    rendering flairs properly.
    """
    original_text = thing.body if isinstance(thing, Comment) else thing.title

    if img:
        hero_name = db_api.get_hero_name(hero_id)
        return "[{}]({}) (sound warning: {}){}".format(original_text, response_url, hero_name, config.COMMENT_ENDING)
    else:
        hero_name = db_api.get_hero_name(hero_id)
        return "[{}]({}) (sound warning: {}){}".format(original_text, response_url, hero_name, config.COMMENT_ENDING)
    #    return (
    #        "[]({}): [{}]({}) (sound warning: {}){}"
    #        .format(img, original_text, response_url, hero_name, config.COMMENT_ENDING)
    #        )


def do_custom_reply(thing, custom_response):
    original_text = thing.body if isinstance(thing, Comment) else thing.title

    reply = custom_response.format(original_text, config.COMMENT_ENDING)
    thing.reply(reply)


PUNCTUATION_TRANS = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
WHITESPACE_TRANS = str.maketrans(string.whitespace, ' ' * len(string.whitespace))
