import functools
from typing import Optional
from typing import List

from flask_wtf import FlaskForm
from flask_login import current_user

from app.models import UserSettings

from app.states.settings import SettingsState
from app.states.settings import SettingsStateGroup
from app.contrib.exc import NoStateAvailable
from app.contrib.fsm import DEFAULT_STATE_NAME

USER_SETTINGS_REQUIRED_FIELDS = (
    'first_name',
    'last_name',
    'address_line_1',
    'address_line_2',
    'cell_phone_number',
    'home_phone_number',
)


class SettingsService:
    @classmethod
    def get_all_states(cls) -> List[SettingsState]:
        return [
            state
            for name, state in SettingsStateGroup.__group_states__.items()
            if name != DEFAULT_STATE_NAME
        ]

    @classmethod
    def get_settings(cls) -> UserSettings:
        return current_user.settings  # type: ignore

    @classmethod
    def is_user_setting_filled(cls) -> bool:
        for field_name in USER_SETTINGS_REQUIRED_FIELDS:
            value = getattr(cls.get_settings(), field_name)

            if value is None:
                return False

        return True

    @classmethod
    def update_settings(cls, form: FlaskForm) -> None:
        for field_name, field in form._fields.items():  # type: ignore
            setattr(
                current_user.settings, field_name, field.data) # type: ignore

        current_user.save()  # type: ignore

    @classmethod
    @functools.lru_cache
    def _get_state_by_section_name(cls, section_name: str) -> SettingsState:
        for state in SettingsStateGroup.__group_states__.values():
            if state.step_info.section_name == section_name:
                return state

        raise NoStateAvailable

    @classmethod
    def get_state(
            cls, section_name: Optional[str] = None) -> SettingsState:
        if section_name is None:
            return SettingsStateGroup.get_active_state()

        return cls._get_state_by_section_name(section_name)

    @classmethod
    def get_form(cls, state: SettingsState) -> FlaskForm:
        settings: UserSettings = cls.get_settings()

        form = state.step_info.form_cls()

        for field_name, field in form._fields.items():  # type: ignore
            try:
                default_value = getattr(settings, field_name)

            except AttributeError:
                continue

            if default_value is not None:
                field.data = default_value

        return form
