"""Module used to perform database operations for the bot to use.
Needs operation optimisation and normalization in databases
"""

import psycopg2 as psycopg2

from config import DB_URL

__author__ = 'Jonarzz'

import datetime
import re

import config as properties


class DBUtil:
    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(DB_URL, sslmode='require')
        self.conn.autocommit = True

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    # RESPONSES DATABASE METHODS
    def create_responses_database(self):
        """Method that creates an SQLite database for response-link pairs.
        """

        c = self.conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS responses '
                  '(response text, link text, hero text, hero_id integer, '
                  'UNIQUE (response,link, hero, hero_id) ON CONFLICT IGNORE,'
                  'FOREIGN KEY (hero_id) REFERENCES heroes (id))')

        c.close()

    def add_response_to_database(self, response, link, hero="", hero_id=""):
        """Method that updates an SQLite database with pairs of response-link.
        If response already exists, update the link, else add the response to the table.
        All parameters should be strings.

        :param response: response text.
        :param link: url to the response audio file.
        :param hero: hero name.
        :param hero_id: hero id. Should be same as id in heroes database.
        """

        c = self.conn.cursor()

        c.execute('INSERT INTO responses(response, link, hero, hero_id) VALUES(?,?,?,?)',
                  (response, link, hero, hero_id))
        c.close()

    def get_hero_id_by_response(self, response_url):
        """Method that returns the hero id to which the given response url belongs to.

        :param response_url: The url to the response.
        :return The hero id
        """

        c = self.conn.cursor()

        c.execute('SELECT hero_id FROM responses WHERE link = ?', (response_url,))
        hero_id = c.fetchone()[0]
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
            c.execute('SELECT link, hero_id FROM responses WHERE response = ? AND hero_id = ?', (response, hero_id))
        else:
            c.execute('SELECT link, hero_id FROM responses WHERE response = ? AND hero_id IS NOT NULL '
                      'ORDER BY hero_id DESC, RANDOM() LIMIT 1', (response,))

        link = c.fetchone()[0]
        hero_id = c.fetchone()[1]
        c.close()

        return link, hero_id

    # COMMENTS DATABASE METHODS
    def create_comments_database(self):
        """Method that creates an SQLite database with ids of already checked comments.
        """

        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS comments (comment_id text, date date)')
        c.close()

    def add_comment_to_database(self, comment_id):
        """Method that adds current time and Reddit comments to database by their id.
        :param comment_id: The id of comment on Reddit
        """

        c = self.conn.cursor()
        c.execute('INSERT INTO comments VALUES (?, ?)', (comment_id, datetime.date.today()))
        c.close()

    def delete_old_comment_ids(self):
        """Method used to remove comments older than a period of time defined in the properties file
        (number corresponding to number of days).
        """

        c = self.conn.cursor()

        furthest_date = datetime.date.today() - datetime.timedelta(days=properties.NUMBER_OF_DAYS_TO_DELETE_COMMENT)

        c.execute("DELETE FROM comments WHERE date < ?", ([str(furthest_date)]))
        self.conn.execute("VACUUM")

        c.close()

    def check_if_comment_exists(self, comment_id):
        """Method that checks if the comment id given is already present in the database

        :param comment_id: The id of the comment on Reddit
        :return: True if the it is already present in database, else False
        """

        c = self.conn.cursor()

        c.execute('SELECT COUNT(*) FROM comments WHERE comment_id = ?', (comment_id,))
        result = int(c.fetchone()[0]) > 0

        c.close()

        return result

    # HEROES DATABASE METHODS
    def create_heroes_database(self):
        """Method that creates a database for heroes and announcer packs
        """

        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS heroes '
                  '(id integer primary key autoincrement, name text, img_dir text, css text,'
                  'UNIQUE (name) ON CONFLICT IGNORE)')

        c.close()

    def add_hero_to_database(self, name, img_dir="", css=""):
        """Method to add hero to the database. All parameters are strings.

        :param name: Hero's name
        :param img_dir: path to hero's image
        :param css: CSS for the flair
        """

        c = self.conn.cursor()

        c.execute('INSERT INTO heroes (name, img_dir, css) VALUES (?,?,?)',
                  (name, img_dir, css))

        c.close()

    def get_hero_id_from_database(self, name):
        """Method to get hero's id from database.

        :param name: Hero's name
        :return: Hero's id
        """

        c = self.conn.cursor()

        c.execute('SELECT id from heroes WHERE name = ? ', (name,))
        hero_id = c.fetchone()[0]

        c.close()

        return hero_id

    def get_hero_name(self, hero_id):
        """Method to get hero's name from database.

        :param hero_id: Hero's id
        :return: Hero's name
        """

        c = self.conn.cursor()

        c.execute('SELECT name from heroes WHERE id = ? ', (hero_id,))
        hero_name = c.fetchone()[0]

        c.close()

        return hero_name

    def get_hero_id_by_css(self, css):
        """Method to get hero_id from the database based on the flair css

        :param css: Hero's css as in r/DotA2 subreddit
        :return: Hero's id
        """

        c = self.conn.cursor()

        c.execute('SELECT id from heroes WHERE css = ? ', (css,))
        hero_id = c.fetchone()[0]

        c.close()

        return hero_id

    def get_img_dir_by_id(self, hero_id):
        """Method to get image directory for hero's flair

        :param hero_id: Hero's id
        :return: The directory path to the image
        """

        c = self.conn.cursor()

        c.execute('SELECT img_dir from heroes WHERE id = ? ', (hero_id,))
        img_dir = c.fetchone()[0]

        c.close()

        return img_dir

    def add_heroes_to_database(self):
        """Method to add heroes to the database with hero names and proper css classes names as taken
        from the DotA2 subreddit and hero flair images from the reddit directory. Every hero has its
        own id, so that it can be joined with the hero from responses database (Serves as Foreign Key).

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

            c.execute('INSERT INTO heroes(name, img_dir, css) VALUES (?, ?, ?)', (hero_name, hero_img_path, hero_css))

        c.execute('UPDATE responses SET hero_id = (SELECT heroes.id FROM heroes WHERE responses.hero = heroes.name);')
        c.close()

    def create_all_databases(self):
        """Method that creates all used databases
        """
        self.create_comments_database()
        self.create_heroes_database()
        self.create_responses_database()
