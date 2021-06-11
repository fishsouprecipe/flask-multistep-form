import functools
import flask

from app import blueprints
from app import db
from app import login_manager


@functools.lru_cache
def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = b'\x1bwx\xa4fS\x1aP\x95[~\t\xcf\xd2\n\xa5'
    app.config['MONGODB_DB'] = 'db'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017

    blueprints.setup(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app
