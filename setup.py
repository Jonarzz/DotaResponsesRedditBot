"""Module to be run first time to set up the database
* Drops all tables if the exist and creates them again.
* Populates responses from Gamepedia
* Populates heroes from Gamepedia and Dota 2 subreddit CSS.
"""
from parsers import css_parser, wiki_parser
from util.database.database import db_api

__author__ = 'MePsyDuck'

from util.logger import setup_logger


def first_run():
    db_api.drop_all_tables()
    db_api.create_all_tables()
    wiki_parser.populate_responses()
    css_parser.populate_heroes()


if __name__ == '__main__':
    setup_logger()
    first_run()
