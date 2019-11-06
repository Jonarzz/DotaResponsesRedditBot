from datetime import datetime

from pony.orm import *

db = Database()


class Responses(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    response = Required(str, 1000, index='idx_response')  # Stores the parsed response
    link = Required(str)  # Link to the response
    hero_id = Required('Heroes')  # The hero_id for hero whose response this is


class Comments(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    comment_id = Required(str, unique=True)  # Comment id that are already processed
    process_datetime = Optional(datetime, default=lambda: datetime.utcnow())  # Datetime of processing the comment


class Heroes(db.Entity):
    id = PrimaryKey(int, auto=True)  # Default db id column for pk
    name = Required(str, unique=True)  # Hero's / Announcer pack's name
    img_dir = Optional(str, nullable=True)  # Related to reddit css, currently unused due to reddit redesign
    css = Optional(str, nullable=True)  # Related to reddit css, currently unused due to reddit redesign
    responses = Set(Responses)  # Relationship between Responses and Heroes table


db.generate_mapping()
