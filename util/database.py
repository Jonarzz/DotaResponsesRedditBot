"""Module used to perform database operations for the bot to use.
Needs operation optimisation and normalization in databases
"""

import psycopg2

from config import DB_URL
from util.logger import logger

__author__ = 'Jonarzz'

import datetime
import re

import config as properties
import urllib.parse as up


class DBUtil:
    conn = None

    def __init__(self):
        up.uses_netloc.append("postgres")
        url = up.urlparse(DB_URL)
        self.conn = psycopg2.connect(database=url.path[1:],
                                     user=url.username,
                                     password=url.password,
                                     host=url.hostname,
                                     port=url.port
                                     )
        self.conn.autocommit = True
        logger.info('Connected to database at ' + DB_URL)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            # logger.info('Closed connection to database at ' + DB_URL)

    # RESPONSES TABLE METHODS
    def create_responses_table(self):
        """Method that creates an table for response-link pairs.
        """

        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS responses '
                  '(response text, link text, hero_id integer, '
                  'UNIQUE (response,link, hero_id),'
                  'FOREIGN KEY (hero_id) REFERENCES heroes (id))')
        c.execute('CREATE INDEX idx_response ON responses(response)')
        c.close()

    def drop_responses_table(self):
        """Method that deletes the Postgres table for response-link pairs.
        """

        c = self.conn.cursor()
        c.execute('DROP TABLE IF EXISTS responses CASCADE')
        c.close()

    def add_response_to_table(self, response, link, hero="", hero_id=""):
        """Method that updates the responses with pairs of response-link.
        If response already exists, update the link, else add the response to the table.
        All parameters should be strings.

        :param response: response text.
        :param link: url to the response audio file.
        :param hero_id: hero id. Should be same as id in heroes database.
        """

        c = self.conn.cursor()

        c.execute('INSERT INTO responses(response, link, hero_id) VALUES(%s,%s,%s)'
                  'ON CONFLICT DO NOTHING',
                  (response, link, hero_id))
        c.close()

    def get_hero_id_by_response(self, response_url):
        """Method that returns the hero id to which the given response url belongs to.

        :param response_url: The url to the response.
        :return The hero id
        """

        c = self.conn.cursor()

        c.execute('SELECT hero_id FROM responses WHERE link = %s', (response_url,))
        result = c.fetchone()
        hero_id = result[0] if result else None
        c.close()

        return hero_id

    def get_link_for_response(self, response, hero_id=None):
        """Method that returns the link to the response. First tries to match with the given hero_id, otherwise returns
        random result.

        :param response: The plaintext response.
        :param hero_id: The hero's id.
        :return The link to the response and the hero_id
        """

        c = self.conn.cursor()

        if hero_id is not None:
            c.execute('SELECT link, hero_id FROM responses WHERE response = %s AND hero_id = %s', (response, hero_id))
        else:
            c.execute('SELECT link, hero_id FROM responses WHERE response = %s AND hero_id IS NOT NULL '
                      'ORDER BY hero_id DESC, RANDOM() LIMIT 1', (response,))

        result = c.fetchone()
        if result:
            link = result[0]
            hero_id = result[1]
        else:
            link, hero_id = None, None

        c.close()

        return link, hero_id

    # COMMENTS TABLE METHODS
    def create_comments_table(self):
        """Method that creates an table with ids of already checked comments.
        """

        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS comments (comment_id text, date date)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_comment_id ON comments(comment_id)')
        c.close()

    def drop_comments_table(self):
        """Method that deletes the table with ids of already checked comments.
        """

        c = self.conn.cursor()
        c.execute('DROP TABLE IF EXISTS comments CASCADE')
        c.close()

    def add_comment_to_table(self, comment_id):
        """Method that adds current time and Reddit comments to comments table by their id.
        :param comment_id: The id of comment on Reddit
        """

        c = self.conn.cursor()
        c.execute('INSERT INTO comments VALUES (%s, %s)', (comment_id, datetime.date.today()))
        c.close()

    def delete_old_comment_ids(self):
        """Method used to remove comments older than a period of time defined in the properties file
        (number corresponding to number of days).
        """

        c = self.conn.cursor()

        furthest_date = datetime.date.today() - datetime.timedelta(days=properties.NUMBER_OF_DAYS_TO_DELETE_COMMENT)

        c.execute("DELETE FROM comments WHERE date < %s", ([str(furthest_date)]))
        self.conn.execute("VACUUM")

        c.close()

    def check_if_comment_exists(self, comment_id):
        """Method that checks if the comment id given is already present in the comments table

        :param comment_id: The id of the comment on Reddit
        :return: True if the it is already present in table, else False
        """

        c = self.conn.cursor()

        c.execute('SELECT COUNT(*) FROM comments WHERE comment_id = %s', (comment_id,))
        count = c.fetchone()
        if count is not None:
            result = int(count[0]) > 0
        else:
            result = False

        c.close()

        return result

    # HEROES TABLE METHODS
    def create_heroes_table(self):
        """Method that creates a table for heroes and announcer packs
        """

        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS heroes'
                  '(id serial primary key, name text, img_dir text, css text,'
                  'UNIQUE(name))')
        c.execute('CREATE INDEX idx_hero_name ON heroes(name)')
        c.close()

    def drop_heroes_table(self):
        """Method that deletes the table for heroes and announcer packs
        """

        c = self.conn.cursor()
        c.execute('DROP TABLE IF EXISTS heroes CASCADE')

        c.close()

    def add_hero_to_table(self, name, img_dir="", css=""):
        """Method to add hero to the table. All parameters are strings.

        :param name: Hero's name
        :param img_dir: path to hero's image
        :param css: CSS for the flair
        """

        c = self.conn.cursor()

        c.execute('INSERT INTO heroes (name, img_dir, css) VALUES (%s,%s,%s)'
                  'ON CONFLICT(name) DO NOTHING',
                  (name, img_dir, css))

        c.close()

    def get_hero_id_from_table(self, name):
        """Method to get hero's id from table.

        :param name: Hero's name
        :return: Hero's id
        """

        c = self.conn.cursor()

        c.execute('SELECT id from heroes WHERE name = %s ', (name,))
        result = c.fetchone()
        hero_id = result[0] if result else None

        c.close()

        return hero_id

    def get_hero_name(self, hero_id):
        """Method to get hero's name from table.

        :param hero_id: Hero's id
        :return: Hero's name
        """

        c = self.conn.cursor()

        c.execute('SELECT name from heroes WHERE id = %s ', (hero_id,))
        result = c.fetchone()
        hero_name = result[0] if result else None

        c.close()

        return hero_name

    def get_hero_id_by_css(self, css):
        """Method to get hero_id from the table based on the flair css

        :param css: Hero's css as in r/DotA2 subreddit
        :return: Hero's id
        """

        c = self.conn.cursor()

        c.execute('SELECT id from heroes WHERE css = %s ', (css,))
        result = c.fetchone()
        hero_id = result[0] if result else None

        c.close()

        return hero_id

    def get_img_dir_by_id(self, hero_id):
        """Method to get image directory for hero's flair

        :param hero_id: Hero's id
        :return: The directory path to the image
        """

        c = self.conn.cursor()

        c.execute('SELECT img_dir from heroes WHERE id = %s ', (hero_id,))
        result = c.fetchone()
        img_dir = result[0] if result else None

        c.close()

        return img_dir

    def add_heroes_to_table(self):
        """Method to add heroes to the table with hero names and proper css classes names as taken
        from the DotA2 subreddit and hero flair images from the reddit directory. Every hero has its
        own id, so that it can be joined with the hero from responses table (Serves as Foreign Key).

        Note: Unused currently since flairs don't work in comments for new Reddit redesign.
        """

        c = self.conn.cursor()

        flair_file = open('flair.txt', 'r')
        hero_file = open('hero_names.txt', 'r')
        img_file = open('hero_img.txt', 'r')

        flair_match = re.findall('"flair flair\-([^ ]+)"', flair_file.read())
        hero_lines = hero_file.readlines()
        img_paths = img_file.readlines()

        for match in flair_match:
            hero_name = ''
            hero_css = ''
            hero_img_path = ''

            for hero_line in hero_lines:
                heroes_match = re.search(r'(.*?): (\w+)', hero_line)
                if match == heroes_match.group(2).lower():
                    hero_name = heroes_match.group(1)
                    hero_css = match
                    break

            for path in img_paths:
                path_match = re.search(r'\/hero\-([a-z]+)', path)
                if hero_name.lower().translate(str.maketrans("", "", " -'")) == path_match.group(1):
                    hero_img_path = path.strip()
                    break

            c.execute('INSERT INTO heroes(name, img_dir, css) VALUES (%s, %s, %s)'
                      'ON CONFLICT(name) DO NOTHING',
                      (hero_name, hero_img_path, hero_css))

        c.execute('UPDATE responses SET hero_id = (SELECT heroes.id FROM heroes WHERE responses.hero = heroes.name);')
        c.close()

    def create_all_tables(self):
        """Method that creates all used tables.
        """
        self.create_comments_table()
        self.create_heroes_table()
        self.create_responses_table()

    def drop_all_tables(self):
        """Method that deletes/drops all tables.
        """
        self.drop_comments_table()
        self.drop_heroes_table()
        self.drop_responses_table()
