# coding=UTF-8

__author__ = 'Jonarzz'

"""Module used to transfer from usage of dictionaries to databases for the bot to use."""


import sqlite3
import os
import datetime
import re

from responses_wiki import dota_wiki_parser as parser
import dota_responses_properties as properties


SCRIPT_DIR = os.path.dirname(__file__)


def create_responses_database():
    """Method that creates an SQLite database with pairs response-link
    based on the JSON file with such pairs which was used before."""
    responses_dictionary = parser.dictionary_from_file(properties.RESPONSES_FILENAME)

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS responses (response text, link text, hero text, hero_id integer)')
    for key, value in responses_dictionary.items():
        c.execute("INSERT INTO responses(response, text) VALUES (?, ?)", (key, value))

    conn.commit()
    c.close()


def create_comments_database():
    """Method that creates an SQLite database with ids of already checked comments."""
    already_done_comments = load_already_done_comments()

    conn = sqlite3.connect('comments.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS comments (id text, date date)')
    for id in already_done_comments:
        c.execute("INSERT INTO comments VALUES (?, ?)", (id, datetime.date.today()))
    
    conn.commit()
    c.close()


def load_already_done_comments():
    """Method used to load a list of already done comments' IDs from a text file."""
    with open(os.path.join(SCRIPT_DIR, "already_done_comments.txt")) as file:
        already_done_comments = [i for i in file.read().split()]
        return already_done_comments
        
        
def delete_old_comment_ids():
    """Method used to remove comments older than a period of time defined in the properties file
    (number corresponding to number of days)."""
    furthest_date = datetime.date.today() - datetime.timedelta(days=properties.NUMBER_OF_DAYS_TO_DELETE_COMMENT)

    conn = sqlite3.connect('comments.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE date < ?", ([str(furthest_date)]))
    conn.commit()
    c.execute("SELECT Count(*) FROM comments")
    num_of_ids = c.fetchone()[0]
    c.close()

    print("COMMENTS DB CLR\nNumber of IDs: " + str(num_of_ids))
    
    
def add_hero_specific_responses():
    """Method that adds hero specific responses to the responses database."""
    database_connection = sqlite3.connect('responses.db')
    cursor = database_connection.cursor()
    
    for ending in parser.pages_for_category(parser.CATEGORY):
        print(ending)
        responses_dict = parser.create_responses_text_and_link_dict(ending)
        for key, value in responses_dict.items():
            cursor.execute("INSERT INTO responses VALUES (?, ?, ?)", (key, value, ending.replace('_', ' ').replace('responses', '').strip()))
        database_connection.commit()
    
    cursor.close()
    
    
def create_heroes_database():
    """Method that creates a database with hero names and proper css classes names as taken
    from the DotA2 subreddit and hero flair images from the reddit directory. Every hero has its
    own id, so that it can be joined with the hero from responses database."""
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS heroes (id integer primary key autoincrement, name text, img_dir text, css text)')

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
                
        c.execute("INSERT INTO heroes(name, img_dir, css) VALUES (?, ?, ?)", (hero_name, hero_img_path, hero_css))
        conn.commit()
    
    c.execute("UPDATE responses SET hero_id = (SELECT heroes.id FROM heroes WHERE responses.hero = heroes.name);");
    conn.commit()
    c.close()
           

if __name__ == '__main__':
    #create_responses_database()
    #create_comments_database()
    #add_hero_specific_responses()
    #create_heroes_database()
    delete_old_comment_ids()
    
