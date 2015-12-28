# coding=UTF-8
import praw
import dota_responses_account as account
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser
import re
import traceback
import os
from datetime import datetime

__author__ = "Jonarzz"


script_dir = os.path.dirname(__file__)


def execute():
    r = account.get_account()
    responses_dict = parser.dictionary_from_file(properties.RESPONSES_FILENAME)
    heroes_dict = parser.dictionary_from_file(properties.HEROES_FILENAME)
    already_done_comments = load_already_done_comments()
    
    try:
        sticky = r.get_subreddit(properties.SUBREDDIT).get_sticky()
    except praw.errors.NotFound:
        sticky = None

    log_stuffz('START')
    
    for submission in r.get_subreddit(properties.SUBREDDIT).get_new(limit=100):
        if submission == sticky:
            continue
        add_comments(submission, already_done_comments, responses_dict, heroes_dict)
        
    for submission in r.get_subreddit(properties.SUBREDDIT).get_hot(limit=25):
        if submission == sticky:
            continue
        add_comments(submission, already_done_comments, responses_dict, heroes_dict)


def log_error(e):
    with open("error.log", 'a') as f:
        f.write(str(datetime.now()) + '\n' + e + '\n')
    return


def log_stuffz(e):
    with open("stuffz.log", 'a') as f:
        f.write(str(datetime.now()) + '\n' + e + '\n')
    return


def add_comments(submission, already_done_comments, responses_dict, heroes_dict):
    submission.replace_more_comments(limit=None, threshold=0)

    for comment in praw.helpers.flatten_tree(submission.comments):
        if comment.id in already_done_comments:
            continue
        already_done_comments.append(comment.id)

        comment_text = prepare_comment(comment.body)

        if comment_text not in properties.EXCLUDED_RESPONSES:
            if comment_text in responses_dict:
                comment.reply(create_reply(responses_dict, heroes_dict, comment_text))
                log_stuffz("Added: " + comment.id)

    save_already_done_comments(already_done_comments)


def create_reply(responses_dict, heroes_dict, key):
    upper_key = capitalize(key)
    response_url = responses_dict[key]
    short_hero_name = parser.short_hero_name_from_url(response_url)
    hero_name = heroes_dict[short_hero_name]
    
    return "[" + upper_key + "](" + response_url + ") (sound warning: " + hero_name + ")" + properties.COMMENT_ENDING


def uppercase(matchobj):
    return matchobj.group(0).upper()


def capitalize(s):
    return re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)


def save_already_done_comments(already_done_comments):
    with open(os.path.join(script_dir, "already_done_comments.txt"), "w") as file:
        for item in already_done_comments:
            file.write("%s " % item)


def load_already_done_comments():
    with open(os.path.join(script_dir, "already_done_comments.txt")) as file:
        already_done_comments = [i for i in file.read().split()]
        if len(already_done_comments) > 25000:
            already_done_comments = already_done_comments[-25000:]
        return already_done_comments


def prepare_comment(comment):
    comment = comment.strip(" .!").lower()

    i = 1
    new_comment = comment
    try:
        while comment[-1] == comment [-1 - i]:
            new_comment = new_comment[:-1]
            i += 1
    except IndexError:
        log_error("IndexError")

    return new_comment


    

if __name__ == '__main__':
    while True:
        try:
            execute()
        except:
            log_error(traceback.format_exc())
            pass

