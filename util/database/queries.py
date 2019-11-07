import datetime
import random
import urllib.parse as up

from pony.orm import db_session, commit

from config import NUMBER_OF_DAYS_TO_DELETE_COMMENT, DB_URL, DB_PROVIDER
from util.database.models import Responses, Comments, Heroes, db

__author__ = 'MePsyDuck'


class DatabaseAPI:
    def __init__(self):
        self.db = db
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

        self.db.generate_mapping(create_tables=True)

    # Responses table queries
    @db_session
    def add_response_to_table(self, response_text, response_link, hero_id):
        """Method that updates the responses with pairs of response-link.
        If response already exists, update the link, else add the response to the table.
        All parameters should be strings.

        :param response_text: response text.
        :param response_link: url to the response audio file.
        :param hero_id: hero id. Should be same as id in heroes database.
        """
        r = Responses(response_text=response_text, response_link=response_link, hero_id=hero_id)

    @db_session
    def get_link_for_response(self, response_text, hero_id=None):
        """Method that returns the link to the response_text. First tries to match with the given hero_id, otherwise returns
        random result.

        :param response_text: The plaintext response_text.
        :param hero_id: The hero's id.
        :return The link to the response_text and the hero_id
        """
        # TODO review
        responses = Responses.select(lambda r: r.response_text == response_text)

        if hero_id is not None:
            for response in responses:
                if response.hero_id == hero_id:
                    return response.response_link, response.hero_id
        else:
            response = random.choice(responses)
            return response.response_link, response.hero_id

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
        comment = Comments.select(lambda c: c.comment_id == comment_id)
        return comment is not None

    # Heroes table queries
    @db_session
    def add_hero_to_table(self, hero_name, img_path=None, flair_css=None):
        """Method to add hero to the table. All parameters are strings.

        :param hero_name: Hero's name
        :param img_path: path to hero's image
        :param flair_css: CSS for the flair
        """
        h = Heroes(hero_name=hero_name, img_path=img_path, flair_css=flair_css)

    @db_session
    def get_hero_id_from_table(self, hero_name):
        """Method to get hero's id from table.

        :param hero_name: Hero's name
        :return: Hero's id
        """
        h = Heroes.get(hero_name=hero_name)
        return h.id if h is not None else None

    @db_session
    def get_hero_name(self, hero_id):
        """Method to get hero's name from table.

        :param hero_id: Hero's id
        :return: Hero's name
        """
        h = Heroes[hero_id]
        return h.hero_name if h is not None else None

    @db_session
    def get_hero_id_by_css(self, flair_css):
        """Method to get hero_id from the table based on the flair css

        :param flair_css: Hero's css as in r/DotA2 subreddit
        :return: Hero's id
        """
        h = Heroes.get(flair_css=flair_css)
        return h.id if h is not None else None

    @db_session
    def get_img_dir_by_id(self, hero_id):
        """Method to get image directory for hero's flair

         :param hero_id: Hero's id
         :return: The directory path to the image
         """
        h = Heroes[hero_id]
        return h.img_path if h is not None else None

    @db_session
    def get_all_hero_names(self):
        heroes = Heroes.select()[:]
        return [hero.hero_name for hero in heroes]

    @db_session
    def update_hero(self, hero_name, img_path, flair_css):
        hero = Heroes.get(hero_name=hero_name)
        hero.img_path = img_path
        hero.img_path = flair_css

    def create_all_tables(self):
        self.db.create_tables()

    def drop_all_tables(self):
        self.db.drop_all_tables(with_all_data=True)

    @db_session
    def add_hero_and_responses(self, hero_name, response_link_dict):
        h = Heroes(hero_name=hero_name, img_path=None, flair_css=None)
        commit()

        for response, link in response_link_dict.items():
            r = Responses(response_text=response, response_link=link, hero_id=h.id)


db_api = DatabaseAPI()
