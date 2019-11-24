from datetime import datetime

from pony.orm import *

__author__ = 'MePsyDuck'

db = Database()


class Responses(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    processed_text = Required(str, 1000, index='idx_parsed_text')  # Stores the processed response text
    original_text = Required(str, 1000)  # Stores the original response text/ Unused currently, but may help in future.
    response_link = Required(str, unique=True)  # Link to the response text
    hero_id = Required('Heroes')  # The hero_id for hero whose response text this is


class Comments(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    comment_id = Required(str, unique=True)  # Comment id that are already processed
    process_datetime = Optional(datetime, default=lambda: datetime.utcnow())  # Datetime of processing the comment


class Heroes(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    hero_name = Required(str, unique=True)  # Hero's / Announcer pack's name
    img_path = Optional(str, nullable=True)  # Path to hero's flair image in reddit css
    flair_css = Optional(str, nullable=True)  # Class for hero in reddit css
    responses = Set(Responses)  # Relationship between Responses and Heroes table
