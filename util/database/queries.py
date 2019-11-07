import datetime
import urllib.parse as up

from pony.orm import db_session, Database

from config import NUMBER_OF_DAYS_TO_DELETE_COMMENT, DB_URL, DB_PROVIDER
from util.database.models import Responses, Comments, Heroes


class DBUtil:
    def __init__(self):
        self.db = Database()
        if DB_PROVIDER == 'sqlite':
            self.db.bind(provider='sqlite', filename=DB_URL, create_db=True)
        elif DB_PROVIDER == 'mysql':
            up.uses_netloc.append("mysql")
            url = up.urlparse(DB_URL)
            self.db.bind(provider='mysql', host=url.hostname, user=url.username, passwd=url.password, db=url.path[1:])
        elif DB_PROVIDER == 'postgres':
            up.uses_netloc.append("postgres")
            url = up.urlparse(DB_URL)
            self.db.bind(provider='postgres', user=url.username, password=url.password, host=url.hostname,
                         database=url.path[1:])
        else:
            self.db.bind(provider='sqlite', filename=':memory:')

    # Responses table queries
    @db_session
    def add_response_to_table(self, response, link, hero_id):
        """Method that updates the responses with pairs of response-link.
        If response already exists, update the link, else add the response to the table.
        All parameters should be strings.

        :param response: response text.
        :param link: url to the response audio file.
        :param hero_id: hero id. Should be same as id in heroes database.
        """
        r = Responses(response=response, link=link, hero_id=hero_id)

    @db_session
    def get_link_for_response(self, response, hero_id=None):
        """Method that returns the link to the response. First tries to match with the given hero_id, otherwise returns
        random result.

        :param response: The plaintext response.
        :param hero_id: The hero's id.
        :return The link to the response and the hero_id
        """
        responses = Responses.select(lambda r: r.response == response)
        # TODO
        if hero_id is not None:
            pass
        else:
            pass

    # Comments table queries
    @db_session
    def add_comment_to_table(self, comment_id):
        """Method that adds current time and Reddit comments to comments table by their id.
        :param comment_id: The id of comment on Reddit
        """
        c = Comments(comment_id=comment_id)

    @db_session
    def delete_old_comment_ids(self):
        """Method used to remove comments older than a period of time defined in the config file
        (number corresponding to number of days).
        """
        furthest_date = datetime.datetime.utcnow() - datetime.timedelta(days=NUMBER_OF_DAYS_TO_DELETE_COMMENT)

        Comments.select(lambda c: c.process_datetime < furthest_date).delete(bulk=True)

    @db_session
    def check_if_comment_exists(self, comment_id):
        """Method that checks if the comment id given is already present in the comments table

        :param comment_id: The id of the comment on Reddit
        :return: True if the it is already present in table, else False
        """
        c = Comments.select(lambda c: c.comment_id == comment_id)
        return c is not None

    # Heroes table queries
    @db_session
    def add_hero_to_table(self, name, img_dir=None, css=None):
        """Method to add hero to the table. All parameters are strings.

        :param name: Hero's name
        :param img_dir: path to hero's image
        :param css: CSS for the flair
        """
        h = Heroes(name=name, img_dir=img_dir, css=css)

    @db_session
    def get_hero_id_from_table(self, name):
        """Method to get hero's id from table.

        :param name: Hero's name
        :return: Hero's id
        """
        h = Heroes.get(name=name)
        return h.id if h is not None else None

    @db_session
    def get_hero_name(self, hero_id):
        """Method to get hero's name from table.

        :param hero_id: Hero's id
        :return: Hero's name
        """
        h = Heroes[hero_id]
        return h.name if h is not None else None

    @db_session
    def get_hero_id_by_css(self, css):
        """Method to get hero_id from the table based on the flair css

        :param css: Hero's css as in r/DotA2 subreddit
        :return: Hero's id
        """
        h = Heroes.get(css=css)
        return h.id if h is not None else None

    @db_session
    def get_img_dir_by_id(self, hero_id):
        """Method to get image directory for hero's flair

         :param hero_id: Hero's id
         :return: The directory path to the image
         """
        h = Heroes[hero_id]
        return h.img_dir if h is not None else None

    @db_session
    def add_heroes_to_table(self):
        # TODO get css from r/dota2 subreddit and update heroes table
        pass

    @db_session
    def create_all_tables(self):
        self.db.create_tables()

    @db_session
    def drop_all_tables(self):
        self.db.drop_all_tables(with_all_data=True)
