# type: ignore

import flask_login

from app.db import db


class UserSettings(db.Document):
    username = db.StringField(required=True)
    first_name = db.StringField()
    last_name = db.StringField()
    address_line_1 = db.StringField()
    address_line_2 = db.StringField()
    cell_phone_number = db.StringField()
    home_phone_number = db.StringField()
