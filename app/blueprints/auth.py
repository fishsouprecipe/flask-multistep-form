import flask
import flask_login

from app.forms.auth import LoginForm
from app.forms.auth import RegisterForm

auth_blueprint = flask.Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        return flask.redirect(flask.url_for('index.index'))

    return flask.render_template('auth/login.jinja2', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout_handler():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register_handler():
    form = RegisterForm()

    if form.validate_on_submit():

        return flask.redirect(flask.url_for('.login'))

    return flask.render_template('auth/register.jinja2', form=form)
