import praw
import dota_responses_account as account
import dota_responses_properties as properties
from responses_wiki import dota_wiki_parser as parser

__author__ = "Jonarzz"


def execute():
    r = account.get_account()
    responses_dict = parser.dictionary_from_file("dota_responses_1.1.txt")
    already_done = load_already_done()
    for submission in r.get_subreddit(properties.SUBREDDIT).get_new(limit=10):
        if submission.id in already_done:
            continue

        submission.replace_more_comments(limit=None, threshold=0)

        for comment in praw.helpers.flatten_tree(submission.comments):
            comment_text = prepare_comment(comment.body)
            for key in responses_dict:
                if comment_text == key:
                    comment.reply(responses_dict[key] + properties.COMMENT_ENDING)
                    print("DODANO: " + comment.id)
                    break

        already_done.append(submission.id)

    save_already_done(already_done)


def save_already_done(already_done):
    with open("already_done.txt", "w") as file:
        for item in already_done:
            file.write("%s " % item)


def load_already_done():
    with open("already_done.txt") as file:
        already_done = [i for i in file.read().split()]
        return already_done


def prepare_comment(comment):
    if comment[-1] in [".", "!"]:
        comment = comment[:-1]

    comment.strip()
    comment = comment.lower()

    return comment


execute()