from typing import cast

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import login_required

from app.contrib.exc import NoStateAvailable
from app.contrib.fsm import DEFAULT_STATE_NAME
from app.services.settings import SettingsService
from app.states.settings import SettingsState

settings_blueprint = Blueprint('settings', __name__)


@settings_blueprint.route('/settings/')
@login_required
def settings():
    state = SettingsService.get_state()

    if SettingsService.is_user_setting_filled():
        return render_template(
                'settings/settings.jinja2', states=SettingsService.get_all_states())


    return redirect(
        url_for('.settings_edit', section_name=state.step_info.section_name))

@settings_blueprint.route('/settings/<section_name>', methods=['GET', 'POST'])
@login_required
def settings_edit(section_name: str):
    state = SettingsService.get_state(section_name)
    form = SettingsService.get_form(state)

    if form.validate_on_submit():
        SettingsService.update_settings(form)

        try:
            redirect_url = request.args['next']

        except KeyError:
            try:
                next_state = cast(SettingsState, state.get_next_state())
                next_state.set_active()

            except NoStateAvailable:
                redirect_url = url_for('.settings')

            else:
                redirect_url = url_for(
                    '.settings_edit',
                    section_name=next_state.step_info.section_name,
                )

            return redirect(redirect_url)

    return render_template(state.step_info.template, form=form)
