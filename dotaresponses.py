# coding=UTF-8
import praw
import dota_responses_account as account
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser

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

        for key in responses_dict:
            if comment_text == key:
                if comment_text not in properties.EXCLUDED_RESPONSES:
                    comment.reply(responses_dict[key] + properties.COMMENT_ENDING)
                    print("Added: " + comment.id)
                    break

    save_already_done_comments(already_done_comments)


def save_already_done_comments(already_done_comments):
    with open("already_done_comments.txt", "w") as file:
        for item in already_done_comments:
            file.write("%s " % item)


def load_already_done_comments():
    with open("already_done_comments.txt") as file:
        already_done_comments = [i for i in file.read().split()]
        return already_done_comments


def prepare_comment(comment):
    if comment[-1] in [".", "!"]:
        comment = comment[:-1]

    comment.strip()
    comment = comment.lower()

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


