from typing import Optional

import flask
import flask_login

from app.forms.settings import AForm
from app.forms.settings import BForm
from app.forms.settings import CForm

settings_blueprint = flask.Blueprint('settings', __name__)

@settings_blueprint.route('/settings')
@settings_blueprint.route('/settings/<section_name>')
@flask_login.login_required
def settings(section_name: Optional[str] = None):
    if section_name is not None:
        return ''

    form = 666
    print(section_name)

    if form % 3 == 0:
        f = AForm()

    elif form % 2 == 0:
        f = BForm()

    else:
        f = CForm()

    return flask.render_template('form.jinja2', f=f, my_blood='aoeu')
