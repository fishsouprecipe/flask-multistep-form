from typing import Optional

import flask
import flask_login

from app.services.settings import SettingsService
from app.services.settings import FinalStateError
from app.forms.settings import FirstForm
from app.forms.settings import SecondForm
from app.forms.settings import ThirdForm

settings_blueprint = flask.Blueprint('settings', __name__)

settings_service = SettingsService()
settings_service.add(
    section_name='first-form',
    form_cls=FirstForm,
    template='settings/first-form.jinja2',
    field_names=(
        'first_name',
        'last_name',
    ),
)

settings_service.add(
    section_name='second-form',
    form_cls=SecondForm,
    template='settings/second-form.jinja2',
    field_names=(
        'address_line_1',
        'address_line_2',
    ),
)

settings_service.add(
    section_name='third-form',
    form_cls=ThirdForm,
    template='settings/third-form.jinja2',
    field_names=(
        'cell_phone_number',
        'home_phone_number',
    ),
)

@settings_blueprint.route('/settings')
@settings_blueprint.route('/settings/<section_name>', methods=['GET', 'POST'])
@flask_login.login_required
def settings(section_name: Optional[str] = None):
    user_settings = settings_service.get_user_settings()

    if section_name is None:
        state = settings_service.get_current_state(user_settings)
        return flask.redirect(
                flask.url_for('.settings', section_name=state.section_name))

    state = settings_service.get_state_by_section_name(section_name)

    form = state.form_cls(**{
        field_name: getattr(user_settings, field_name)
        for field_name in state.field_names
    })

    if form.validate_on_submit():
        for field_name in state.field_names:
            field_value = getattr(form, field_name).data

            setattr(user_settings, field_name, field_value)

        user_settings.save()

        new_state = settings_service.get_current_state(user_settings)

        redirect_url = flask.url_for(
            endpoint='.settings',
            section_name=new_state.section_name,
        )

        return flask.redirect(redirect_url)

    return flask.render_template(state.template, form=form)
