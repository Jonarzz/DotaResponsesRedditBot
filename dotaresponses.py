# coding=UTF-8

"""Main module of the Dota 2 subreddit Heroes Responses Bot.

The main body of the script is running in this file. The comments are loaded from the subreddit
and the script checks if the comment is a response from Dota 2. If it is, a proper comment is
prepared. The comment is posted as a reply to the original post on Reddit.

Proper logging is provided - saved to 2 files as standard output and errors.
"""

import traceback
import os
from datetime import datetime

import praw

import dota_responses_account as account
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser

__author__ = 'Jonarzz'


SCRIPT_DIR = os.path.dirname(__file__)


def execute():
    """Main method executing the script.

    It connects to an account, loads dictionaries from proper files (declared in properties file).
    Afterwards it executes add_comments method with proper arguments passed.
    """
    reddit_account = account.get_account()

    try:
        sticky = reddit_account.get_subreddit(properties.SUBREDDIT).get_sticky()
    except praw.errors.NotFound:
        sticky = None

    log('START')

    for submission in reddit_account.get_subreddit(properties.SUBREDDIT).get_new(limit=100):
        add_comments_to_submission(submission, sticky)

    for submission in reddit_account.get_subreddit(properties.SUBREDDIT).get_hot(limit=25):
        add_comments_to_submission(submission, sticky)


def add_comments_to_submission(submission, sticky):
    """Method that adds the bot replies to the comments in given submission."""
    if submission == sticky:
        return

    responses_dict = parser.dictionary_from_file(properties.RESPONSES_FILENAME)
    heroes_dict = parser.dictionary_from_file(properties.HEROES_FILENAME)
    already_done_comments = load_already_done_comments()

    add_comments(submission, already_done_comments, responses_dict, heroes_dict)


def log(message, error=False):
    """Method used to save messages to an proper (info/error) log file."""
    if error:
        with open(properties.ERROR_FILENAME, 'a') as file:
            file.write(str(datetime.now()) + '\n' + message + '\n')
    else:
        with open(properties.INFO_FILENAME, 'a') as file:
            file.write(str(datetime.now()) + '\n' + message + '\n')


def add_comments(submission, already_done_comments, responses_dict, heroes_dict):
    """Method used to check all the comments in a submission and add replies if they are responses.

    All comments are loaded. If comment ID is on the already_done_comments list, next comment
    is checked (further actions are ommited). If the comment wasn't analized before,
    it is prepared for comparision to the responses in dictionary. If the comment is not on the
    excluded responses list (loaded from properties) and if it is in the dictionary, a reply
    comment is prepared and posted.
    """
    submission.replace_more_comments(limit=None, threshold=0)

    for comment in praw.helpers.flatten_tree(submission.comments):
        if comment.id in already_done_comments:
            continue
        already_done_comments.append(comment.id)

        response = prepare_response(comment.body)

        if response not in properties.EXCLUDED_RESPONSES:
            if response in responses_dict:
                comment.reply(create_reply(responses_dict, heroes_dict, response, comment.body))
                log("Added: " + comment.id)

    save_already_done_comments(already_done_comments)


def create_reply(responses_dict, heroes_dict, key, orignal_text):
    """Method that creates a reply in reddit-post format.

    The message consists of a link the the response, the response itself, a warning about the sound
    and an ending added from the properties file (post footer).
    """
    response_url = responses_dict[key]
    short_hero_name = parser.short_hero_name_from_url(response_url)
    hero_name = heroes_dict[short_hero_name]

    return (
        "[{}]({}) (sound warning: {}){}"
        .format(orignal_text, response_url, hero_name, properties.COMMENT_ENDING)
        )


def save_already_done_comments(already_done_comments):
    """Method used to save a list of already done comment's IDs into a proper text file."""
    with open(os.path.join(SCRIPT_DIR, "already_done_comments.txt"), "w") as file:
        for item in already_done_comments:
            file.write("%s " % item)


def load_already_done_comments():
    """Method used to load a list of already done comments' IDs.

    Size of the already done comments list is kept at 25,000. If the list is bigger,
    IDs are removed from the start of the list (oldest go out first).
    """
    with open(os.path.join(SCRIPT_DIR, "already_done_comments.txt")) as file:
        already_done_comments = [i for i in file.read().split()]
        if len(already_done_comments) > 25000:
            already_done_comments = already_done_comments[-25000:]
        return already_done_comments


def prepare_response(response):
    """Method used to prepare  the response.

    Dots and exclamation marks are stripped. The response is turned to lowercase.
    Multiple letters ending the response are removed (e.g. ohhh->oh).
    """
    response = response.strip(" .!").lower()

    i = 1
    new_response = response
    try:
        while response[-1] == response[-1 - i]:
            new_response = new_response[:-1]
            i += 1
    except IndexError:
        log("IndexError", True)

    return new_response


if __name__ == '__main__':
    while True:
        try:
            execute()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            log(traceback.format_exc(), True)
            