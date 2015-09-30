__author__ = "Jonarzz"

import praw
import dota_responses_account as account
import dota_responses_properties as properties

r = account.get_account()
for submission in r.get_subreddit(properties.SUBREDDIT).get_hot(limit=5):
    submission.replace_more_comments(limit=None, threshold=0)
    for comment in praw.helpers.flatten_tree(submission.comments):
        print(comment.body)
