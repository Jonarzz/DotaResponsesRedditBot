from responses_wiki.dota_wiki_parser import populate_responses
from util.database import DBUtil


def first_run():
    """Method to be run first time to set up the database
    """
    db = DBUtil()
    db.drop_all_tables()
    db.create_all_tables()
    populate_responses()


if __name__ == '__main__':
    first_run()
