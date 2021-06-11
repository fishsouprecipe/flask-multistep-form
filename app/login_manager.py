# type: ignore

import flask
import flask_login

from app.models import User

login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'


def init_app(app: flask.Flask) -> None:
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id) -> User:
    print(user_id)

    return None

    return User.objects(_id=user_id).first()
