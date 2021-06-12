# type: ignore

import flask_login

from app.db import db


class User(flask_login.UserMixin, db.Document):
    username = db.StringField()
    hashed_password = db.StringField()

    def get_id(self) -> str:
        return self.username
