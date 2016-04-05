# coding=UTF-8

__author__ = 'Jonarzz'

"""Module used to transfer from usage of dictionaries to databases for the bot to use."""


import sqlite3
import os
import datetime

from responses_wiki import dota_wiki_parser as parser
import dota_responses_properties as properties


SCRIPT_DIR = os.path.dirname(__file__)


def create_responses_database():
    """Method that creates an SQLite database with pairs response-link
    based on the JSON file with such pairs which was used before."""
    responses_dictionary = parser.dictionary_from_file(properties.RESPONSES_FILENAME)

    conn = sqlite3.connect('responses.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS responses (response text, link text)')
    for key, value in responses_dictionary.items():
        c.execute("INSERT INTO responses VALUES (?, ?)", (key, value))

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
    c.close()
    

if __name__ == '__main__':
    #create_responses_database()
    #create_comments_database()
    delete_old_comment_ids()
