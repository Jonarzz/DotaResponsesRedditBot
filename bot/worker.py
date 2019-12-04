"""Main module of the Dota 2 subreddit Responses Bot.

The main body of the script is running in this file. The comments are loaded from the subreddit
and the script checks if the comment or submission is a response from Dota 2. If it is, a proper reply for response is
prepared. The response is posted as a reply to the original comment/submission on Reddit.

Proper logging is provided - saved to 2 files as standard output and errors.
"""

from praw.models import Comment

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

    comment_stream = reddit.subreddit(config.SUBREDDIT).stream.comments(pause_after=-1)
    submission_stream = reddit.subreddit(config.SUBREDDIT).stream.submissions(pause_after=-1)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            process_replyable(reddit, comment)
        for submission in submission_stream:
            if submission is None:
                break
            process_replyable(reddit, submission)


def process_replyable(reddit, replyable):
    """Method used to check all the comments in a submission and add replies if they are responses.

    PRAW generates past ~100 comments/submissions on the first iteration. Then the loop only runs if there is a new
    comment/submission added to the stream. This also means that once PRAW is up and running, after the initial comments
    list it won't generate any duplicate comments.

    However, just as a safeguard, Caching is used to store replyable ids as they are processed for the first time.
    Otherwise, when the bot is restarted it might reply twice to same comments. If replyable id is in the already present
    in the cache_api, then it is ignored, else processed and added to the cache_api.
    * Self comments are ignored.
    * It is prepared for comparision to the responses in dictionary.
    * If the replyable is not on the excluded responses list (loaded from config) and if it is in the responses db or
    specific responses list, a reply replyable is prepared and posted.

    :param reddit: The reddit account instance
    :param replyable: comment or submission
    :return: None
    """

    if cache_api.check(thing_id=replyable.fullname):
        return

    # Ignore thyself
    if replyable.author == reddit.user.me:
        return

    logger.debug("Found new replyable: " + str(replyable.fullname))

    processed_body = process_body(replyable.body if isinstance(replyable, Comment) else replyable.title)

    # Don't reply to single word text (they're mostly common phrases).
    if ' ' not in processed_body:
        return

    if processed_body in config.EXCLUDED_RESPONSES:
        return

    if processed_body in config.CUSTOM_RESPONSES:
        do_custom_reply(replyable=replyable, custom_response=config.CUSTOM_RESPONSES[processed_body])

    if try_flair_specific_reply(replyable, processed_body):
        return
    else:
        do_regular_reply(replyable, processed_body)


def process_body(body_text):
    """Method used to clean the replyable body text.
    If body text contains a quote, the first quote text is considered as the body text.

    Removed code to remove repeating letters in a body text because it does more harm than good - words like 'all',
    'tree' are stripped to 'al' and 'tre' which dont match with any responses.

    :param body_text: The replyable body text
    :return: Processed body text
    """

    if '>' in body_text:
        lines = body_text.split('\n\n')
        for line in lines:
            if line.startswith('>'):
                body_text = line
                break

    return preprocess_text(body_text)


def try_flair_specific_reply(replyable, processed_text):
    """Method that tries to add a author's flair specific reply to the comment/submission.

    :param replyable: The comment/submission on reddit
    :param processed_text: The processed body text
    :return: True if the replyable was replied to, else False.
    """
    hero_id = db_api.get_hero_id_by_flair_css(flair_css=replyable.author_flair_css_class)
    if hero_id:
        link, hero_id = db_api.get_link_for_response(processed_text=processed_text, hero_id=hero_id)
        if link:
            reply = create_reply(replyable=replyable, response_url=link, hero_id=hero_id)
            replyable.reply(reply)
            logger.info("Added: " + replyable.fullname)
            return True
    return False


def do_regular_reply(replyable, processed_text):
    """Method to create response for given replyable.
    In case of multiple matches, it used to sort responses in descending order of heroes, but now it's random.

    :param replyable: The comment/submission on reddit
    :param processed_text: The processed body text
    :return: None
    """

    link, hero_id = db_api.get_link_for_response(processed_text=processed_text)

    if link and hero_id:
        img_dir = db_api.get_img_dir_by_id(hero_id=hero_id)

        replyable.reply(create_reply(replyable=replyable, response_url=link, hero_id=hero_id, img=img_dir))

        logger.info("Replied to: " + replyable.id)


def create_reply(replyable, response_url, hero_id, img=None):
    """Method that creates a reply in reddit format.
    The reply consists of a link to the response audio file, the response itself, a warning about the sound
    and an ending added from the config file (post footer).
    
    TODO Image is currently ignored due to new reddit redesign not rendering flairs properly.

    :param replyable: The comment/submission on reddit
    :param response_url: The url to the response audio file
    :param hero_id: The hero_id to which the response belongs to.
    :param img: The img path to be used for reply.
    :return: The text for the comment reply.
    """
    original_text = replyable.body if isinstance(replyable, Comment) else replyable.title

    hero_name = db_api.get_hero_name(hero_id)
    return "[{}]({}) (sound warning: {}){}".format(original_text, response_url, hero_name, config.COMMENT_ENDING)


def do_custom_reply(replyable, custom_response):
    """Method to create a custom reply for specific cases that match the custom responses set.

    :param replyable: The comment/submission on reddit
    :param custom_response: The matching custom response
    :return: None
    """
    original_text = replyable.body if isinstance(replyable, Comment) else replyable.title

    reply = custom_response.format(original_text, config.COMMENT_ENDING)
    replyable.reply(reply)
