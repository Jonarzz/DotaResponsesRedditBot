from util.database import DBUtil
from wiki_parser.wiki_parser import populate_responses


def first_run():
    """Method to be run first time to set up the database
    """
    db = DBUtil()
    db.drop_all_tables()
    db.create_all_tables()
    populate_responses()


if __name__ == '__main__':
    first_run()
