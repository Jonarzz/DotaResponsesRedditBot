# coding=UTF-8
import praw
import dota_responses_account as account
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser
import re

__author__ = "Jonarzz"


def execute():
    r = account.get_account()
    responses_dict = parser.dictionary_from_file("dota_responses_1.2.txt")
    already_done_comments = load_already_done_comments()

    for submission in r.get_subreddit(properties.SUBREDDIT).get_new(limit=100):
        add_comments(submission, already_done_comments, responses_dict)
    for submission in r.get_subreddit(properties.SUBREDDIT).get_hot(limit=25):
        add_comments(submission, already_done_comments, responses_dict)


def add_comments(submission, already_done_comments, responses_dict):
    submission.replace_more_comments(limit=None, threshold=0)

    for comment in praw.helpers.flatten_tree(submission.comments):
        if comment.id in already_done_comments:
            continue
        already_done_comments.append(comment.id)

        comment_text = prepare_comment(comment.body)

        if comment_text not in properties.EXCLUDED_RESPONSES:
            if comment_text in responses_dict:
                comment.reply(create_reply(responses_dict, comment_text))
                print("Added: " + comment.id)

    save_already_done_comments(already_done_comments)


def create_reply(responses_dict, key):
    upper_key = capitalize(key)
    return "[" + upper_key + "](" + responses_dict[key] + ") (sound warning)" + properties.COMMENT_ENDING


def uppercase(matchobj):
    return matchobj.group(0).upper()


def capitalize(s):
    return re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', uppercase, s)


def save_already_done_comments(already_done_comments):
    try:
        with open("already_done_comments.txt", "w") as file:
            for item in already_done_comments:
                file.write("%s " % item)
    except OSError:
        with open("F:\Python\DotaResponses\already_done_comments.txt", "w") as file:
            for item in already_done_comments:
                file.write("%s " % item)


def load_already_done_comments():
    with open("already_done_comments.txt") as file:
        already_done_comments = [i for i in file.read().split()]
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
        print("IndexError")

    return new_comment


while True:
    execute()

