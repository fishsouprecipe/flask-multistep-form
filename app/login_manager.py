from typing import Optional

import flask
import flask_login

from app.models import User

login_manager = flask_login.LoginManager()


def init_app(app: flask.Flask) -> None:
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(username: str) -> Optional[User]:
    return User.objects(username=username).first()  # type: ignore


login_manager.login_view = 'auth.login'  # type: ignore
