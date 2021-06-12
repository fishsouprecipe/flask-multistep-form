import flask
import flask_login

from app.forms.auth import LoginForm
from app.forms.auth import RegisterForm
from app.services.auth import AuthService
from app.services.auth import UserDoesNotExist
from app.services.auth import UsernameIsAlreadyOccupied
from app.services.auth import UserInvalidPassword

auth_blueprint = flask.Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('index.index'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            AuthService.authorize_user(
                form.username.data,
                form.password.data,
            )

        except UserDoesNotExist:
            form.username.errors = ('User does not exist',)

        except UserInvalidPassword:
            form.username.errors = ('Invalid user password',)

        else:
            return flask.redirect(flask.url_for('index.index'))

    return flask.render_template('auth/login.jinja2', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    AuthService.logout_user()

    return flask.redirect(flask.url_for('index.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('index.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            AuthService.create_user(
                form.username.data,
                form.password.data,
            )

        except UsernameIsAlreadyOccupied:
            form.username.errors = ('Username is already occupied',)

        else:
            return flask.redirect(flask.url_for('.login'))

    return flask.render_template('auth/register.jinja2', form=form)
