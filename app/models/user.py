# type: ignore

import flask_login

from app.db import db


class User(db.Document, flask_login.UserMixin):
    username = db.StringField(required=True)
    hashed_password = db.StringField(required=True)
