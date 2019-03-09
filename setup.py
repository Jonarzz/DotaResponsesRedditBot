from responses_wiki.dota_wiki_parser import populate_responses
from util.database import DBUtil


def first_run():
    """Method to be run first time to set up all the databases
    """
    db = DBUtil()
    db.create_comments_database()
    db.create_heroes_database()
    db.create_responses_database()
    populate_responses()


if __name__ == '__main__':
    first_run()
