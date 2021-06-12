from typing import Tuple

import flask

from app.services.index import IndexService
from app.models import User

index_blueprint = flask.Blueprint('index', __name__)


@index_blueprint.route('/')
def index() -> str:
    users: Tuple[User] = IndexService.get_all_users()

    return flask.render_template('index/index.jinja2', users=users)
