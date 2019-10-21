"""Main module of the Dota 2 subreddit Heroes Responses Bot.

The main body of the script is running in this file. The comments are loaded from the subreddit
and the script checks if the comment is a response from Dota 2. If it is, a proper comment is
prepared. The comment is posted as a reply to the original post on Reddit.

Proper logging is provided - saved to 2 files as standard output and errors.
"""
import string

import bot.account as account
import config
from util.caching import Cache
from util.database import DBUtil
from util.logger import logger

__author__ = 'Jonarzz'

db = DBUtil()
cache = Cache()


def execute():
    """Main method executing the script.

    It connects to an account, loads dictionaries from proper files (declared in config file).
    Afterwards it executes process_comments method with proper arguments passed.
    """

    reddit = account.get_account()
    logger.info('Connected to Reddit account' + config.USERNAME)

    comments = reddit.subreddit(config.SUBREDDIT).stream.comments()
    process_comments(reddit, comments)


def process_comments(reddit, comments):
    """Method used to check all the comments in a submission and add replies if they are responses.

    PRAW generates past ~100 comments on the first iteration. Then the loop only runs if there is a new comment added to
    the comments stream. This also means that once PRAW is up and running, after the initial comments list it won't
    generate any duplicate comments.

    However, just as a safeguard, Caching is used to store comment ids as they are processed for the first time.
    Otherwise, when the bot is restarted it might reply twice to same comments. If comment id is in the already present
    in the cache, then it is ignored, else processed and added to the cache.
    * Self comments are ignored.
    * It is prepared for comparision to the responses in dictionary.
    * If the comment is not on the excluded responses list (loaded from config) and if it is in the responses db or
    specific responses list, a reply comment is prepared and posted.
    """

    for comment in comments:

        if cache.check_comment(comment_id=comment.id):
            continue

        logger.debug("Found new comment: " + str(comment.id))

        # Ignore thyself
        if comment.author == reddit.user.me:
            continue

        clean_comment = parse_comment(comment.body)
        save_comment_id(comment.id)

        if clean_comment in config.EXCLUDED_RESPONSES:
            continue

        if add_flair_specific_response_and_return(comment, clean_comment):
            continue

        if clean_comment in SPECIFIC_RESPONSES_DICT:
            SPECIFIC_RESPONSES_DICT[clean_comment](comment, clean_comment)
            continue

        add_regular_response(comment, clean_comment)


def parse_comment(response):
    """Method used to clean the response. Logic is similar to clean_key on wiki parser.
    * If comment contains a quote, the first quote is considered as the response.
    * Punctuation marks are replaced  with space. 
    * The response is turned to lowercase.
    * Converts multiple spaces into single space.

    Commented out code to remove repeating letters in a comment because it does more harm than good - words like 'all',
    'tree' are stripped to 'al' and 'tre' which dont match with any responses.

    :param response: The comment body
    :return: Processed comment body
    """

    if '>' in response:
        lines = response.split('\n\n')
        for line in lines:
            if line.startswith('>'):
                response = line
                break

    response = response.translate(PUNCTUATION_TRANS)
    response = response.translate(WHITESPACE_TRANS)

    while '  ' in response:
        response = response.replace('  ', ' ')

    response = response.strip().lower()

    # i = 1
    # new_response = response
    #
    # try:
    #     while not response[-1].isalnum() and response[-1] == response[-1 - i]:
    #         new_response = new_response[:-1]
    #         i += 1
    # except IndexError:
    #     logger.error("IndexError in " + response)

    return response


def save_comment_id(comment_id):
    """Method that saves the comment id to the database"""
    db.add_comment_to_table(comment_id=comment_id)


def add_flair_specific_response_and_return(comment, response):
    hero_id = db.get_hero_id_by_css(css=comment.author_flair_css_class)
    if hero_id:
        link, hero_id = db.get_link_for_response(
            response=response, hero_id=hero_id)
        if link:
            comment.reply(create_reply(response_url=link,
                                       original_text=comment.body, hero_id=hero_id))
            logger.info("Added: " + comment.id)
            return True


def add_regular_response(comment, response):
    """Method to create response for given comment.
    In case of multiple matches, it used to sort responses in descending order of heroes, but now it's random.
    add_shitty_wizard_response was very similar to this, and hence has been merged

    :param comment: The comment on reddit
    :param response: The plaintext processed comment body
    :return: None
    """

    link, hero_id = db.get_link_for_response(response=response)

    if link and hero_id:
        img_dir = db.get_img_dir_by_id(hero_id=hero_id)

        if img_dir:
            comment.reply(create_reply(
                response_url=link, original_text=comment.body, hero_id=hero_id, img=img_dir))
        else:
            comment.reply(create_reply(response_url=link,
                                       original_text=comment.body, hero_id=hero_id))

        logger.info("Added: " + comment.id)


def create_reply(response_url, original_text, hero_id, img=None):
    """Method that creates a reply in reddit-post format.

    The message consists of a link the the response, the response itself, a warning about the sound
    and an ending added from the config file (post footer). Image is currently ignored due to new reddit not
    rendering flairs properly.
    """

    hero_name = db.get_hero_name(hero_id)
    logger.info(response_url + ' : ' + hero_name)

    # if img:
    #    return (
    #        "[]({}): [{}]({}) (sound warning: {}){}"
    #        .format(img, original_text, response_url, hero_name, config.COMMENT_ENDING)
    #        )
    # else:

    return "[{}]({}) (sound warning: {}){}".format(original_text, response_url, hero_name, config.COMMENT_ENDING)


def add_shitty_wizard_response(comment, response):
    """Method that creates a reply for 'shitty wizard' comments. Currently there's nothing different from regular
    responses.

    :param comment: The comment on reddit
    :param response: The plaintext processed comment body
    :return: None
    """
    add_regular_response(comment=comment, response=response)


def add_invoker_response(comment):
    comment.reply(create_reply_invoker_ending(
        config.INVOKER_RESPONSE_URL, config.INVOKER_IMG_DIR))
    logger.info("Added: " + comment.id)


def create_reply_invoker_ending(response_url, img_dir):
    return ("[]({}): [{}]({}) (sound warning: {})\n\n{}{}"
            .format(img_dir, config.INVOKER_RESPONSE, response_url, config.INVOKER_HERO_NAME,
                    config.INVOKER_ENDING, config.COMMENT_ENDING))


def add_sniper_response(comment):
    comment.reply(create_reply_sniper_ending(config.SNIPER_RESPONSE_URL, comment.body,
                                             config.SNIPER_IMG_DIR))
    logger.info("Added: " + comment.id)


def create_reply_sniper_ending(response_url, original_text, img_dir):
    return ("[]({}): [{}]({}) ({}){}"
            .format(img_dir, original_text, response_url, config.SNIPER_TRIGGER_WARNING, config.COMMENT_ENDING))


def prepare_specific_responses():
    output_dict = {}
    for response in config.INVOKER_BOT_RESPONSES:
        output_dict[response] = add_invoker_response
    output_dict["shitty wizard"] = add_shitty_wizard_response
    output_dict["ho ho ha ha"] = add_sniper_response
    return output_dict


SPECIFIC_RESPONSES_DICT = prepare_specific_responses()
PUNCTUATION_TRANS = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
WHITESPACE_TRANS = str.maketrans(string.whitespace, ' ' * len(string.whitespace))
