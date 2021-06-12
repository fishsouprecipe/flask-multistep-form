# type: ignore

import flask_login

from app.db import db


class UserState(db.DynamicEmbeddedDocument):
    pass


class UserSettings(db.EmbeddedDocument):
    first_name = db.StringField()
    last_name = db.StringField()
    address_line_1 = db.StringField()
    address_line_2 = db.StringField()
    cell_phone_number = db.StringField()
    home_phone_number = db.StringField()


class User(flask_login.UserMixin, db.Document):
    username = db.StringField()
    hashed_password = db.StringField()
    settings = db.EmbeddedDocumentField(UserSettings, default=UserSettings)
    state = db.EmbeddedDocumentField(UserState, default=UserState)

    def get_id(self) -> str:
        return self.username
