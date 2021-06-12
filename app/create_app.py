import os
import functools
import flask

from app import blueprints
from app import db
from app import login_manager


@functools.lru_cache
def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = b'\x1bwx\xa4fl\x1aP\x95[~\t\xcf\xd2\n\xa5'
    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB', 'db')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', '127.0.0.1')
    app.config['MONGODB_PORT'] = int(os.getenv('MONGODB_PORT', 27017))

    print(app.config)

    blueprints.setup(app)
    login_manager.init_app(app)
    db.init_app(app)

    return app
