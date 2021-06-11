from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name ', validators=[DataRequired()])


class BForm(FlaskForm):
    address_line_1 = StringField(
        'Address Line 1',
        validators=[DataRequired()]
    )
    address_line_2 = StringField(
        'Address Line 2',
        validators=[DataRequired()],
    )


class CForm(FlaskForm):
    cell_phone_number = StringField(
        'Cellphone Number',
        validators=[DataRequired()],
    )
    home_phone_number = StringField(
        'Home Phone Number',
        validators=[DataRequired()],
    )
