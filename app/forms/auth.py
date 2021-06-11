from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo(
                'confirm_password',
                message='Entered passwords do not match',
            ),
        ]
    )
    confirm_password = StringField(
        'Confirm password',
        validators=[DataRequired()]
    )
