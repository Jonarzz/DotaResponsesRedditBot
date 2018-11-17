"""Module used to perform database operations for the bot to use.
Needs operation optimisation and normalization in databases
"""

__author__ = 'Jonarzz'

import datetime
import re
import sqlite3

import dota_responses_properties as properties


# RESPONSES DATABASE METHODS
def create_responses_database():
    """Method that creates an SQLite database for response-link pairs.
    """

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS responses '
              '(response text, link text, hero text, hero_id integer, '
              'UNIQUE (response,link, hero, hero_id) ON CONFLICT IGNORE,'
              'FOREIGN KEY (hero_id) REFERENCES heroes (id))')

    conn.commit()
    c.close()


def add_response_to_database(response, link, hero="", hero_id=""):
    """Method that updates an SQLite database with pairs of response-link.
    If response already exists, update the link, else add the response to the table.
    All parameters should be strings.

    :param response: response text.
    :param link: url to the response audio file.
    :param hero: hero name.
    :param hero_id: hero id. Should be same as id in heroes database.
    """

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()

    c.execute('INSERT INTO responses(response, link, hero, hero_id) VALUES(?,?,?,?)',
              (response, link, hero, hero_id))

    conn.commit()
    c.close()


# COMMENTS DATABASE METHODS
def create_comments_database():
    """Method that creates an SQLite database with ids of already checked comments.
    """

    conn = sqlite3.connect('comments.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS comments (comment_id text, date date)')

    conn.commit()
    c.close()


def add_comment_to_database(comment_id):
    """Method that adds current time and Reddit comments to database by their id.
    :param comment_id: The id of comment on Reddit
    """
    conn = sqlite3.connect('comments.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    c.execute('INSERT INTO comments VALUES (?, ?)', (comment_id, datetime.date.today()))

    conn.commit()
    c.close()


def delete_old_comment_ids():
    """Method used to remove comments older than a period of time defined in the properties file
    (number corresponding to number of days).
    """

    furthest_date = datetime.date.today() - datetime.timedelta(days=properties.NUMBER_OF_DAYS_TO_DELETE_COMMENT)

    conn = sqlite3.connect('comments.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE date < ?", ([str(furthest_date)]))
    conn.execute("VACUUM")
    conn.commit()
    c.execute('SELECT COUNT(*) FROM comments')
    num_of_ids = c.fetchone()[0]
    c.close()

    # TODO replace with logger
    print("COMMENTS DB CLR\nNumber of IDs: " + str(num_of_ids))


# HEROES DATABASE METHODS
def create_heroes_database():
    """Method that creates a database for heroes and announcer packs
    """

    conn = sqlite3.connect('heroes.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS heroes '
              '(id integer primary key autoincrement, name text, img_dir text, css text,'
              'UNIQUE (name) ON CONFLICT IGNORE)')

    conn.commit()
    c.close()


def add_hero_to_database(name, img_dir="", css=""):
    """Method to add hero to the database. All parameters are strings.

    :param name: Hero's name
    :param img_dir: path to hero's image
    :param css: CSS for the flair
    """

    conn = sqlite3.connect('heroes.db')
    c = conn.cursor()

    c.execute('INSERT INTO heroes (name, img_dir, css) VALUES (?,?,?)',
              (name, img_dir, css))

    conn.commit()
    c.close()


def get_hero_id_from_database(name):
    """Method to get hero's id in database

    :param name: Hero's name
    :return: Hero's id
    """

    conn = sqlite3.connect('heroes.db')
    c = conn.cursor()

    c.execute('SELECT id from heroes WHERE name = ? ', (name,))
    hero_id = c.fetchone()[0]

    conn.commit()
    c.close()

    return hero_id


def add_heroes_to_database():
    """Method to add heroes to the database with hero names and proper css classes names as taken
    from the DotA2 subreddit and hero flair images from the reddit directory. Every hero has its
    own id, so that it can be joined with the hero from responses database.

    Note: Unused currently since flairs don't work in comments for new Reddit redesign.
    """

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()

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
            heroes_match = re.search('(.*?): (\w+)', hero_line)
            if match == heroes_match.group(2).lower():
                hero_name = heroes_match.group(1)
                hero_css = match
                break

        for path in img_paths:
            path_match = re.search('\/hero\-([a-z]+)', path)
            if hero_name.lower().translate(str.maketrans("", "", " -'")) == path_match.group(1):
                hero_img_path = path.strip()
                break

        c.execute('INSERT INTO heroes(name, img_dir, css) VALUES (?, ?, ?)', (hero_name, hero_img_path, hero_css))
        conn.commit()

    c.execute('UPDATE responses SET hero_id = (SELECT heroes.id FROM heroes WHERE responses.hero = heroes.name);')
    conn.commit()
    c.close()


def create_all_databases():
    """Method that creates all used databases
    """
    create_comments_database()
    create_heroes_database()
    create_responses_database()
