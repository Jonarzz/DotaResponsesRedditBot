from parsers import css_parser, wiki_parser
from util.database.database import db_api

__author__ = 'MePsyDuck'


def first_run():
    """Method to be run first time to set up the database
    """
    db_api.drop_all_tables()
    db_api.create_all_tables()
    wiki_parser.populate_responses()
    css_parser.populate_heroes()


if __name__ == '__main__':
    first_run()
