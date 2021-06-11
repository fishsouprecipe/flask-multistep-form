import flask

from .index import index_blueprint
from .auth import auth_blueprint
from .settings import settings_blueprint


def setup(app: flask.Flask) -> None:
    app.register_blueprint(index_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(settings_blueprint)


__all__ = (
    'index_blueprint',
    'auth_blueprint',
    'settings_blueprint',
    'setup',
)

