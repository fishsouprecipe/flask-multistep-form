from typing import NamedTuple
from typing import List
from typing import Tuple
from typing import Dict
from typing import Type

import flask_wtf
import flask_login

from app.models import UserSettings


class SettingsError(Exception): pass
class FinalStateError(SettingsError): pass
class SectionNameIsAlreadyOccupied(SettingsError): pass


class State(NamedTuple):
    section_name: str
    form_cls: Type[flask_wtf.FlaskForm]
    template: str
    field_names: Tuple[str, ...]


class SettingsService:
    def __init__(self) -> None:
        self.states: List[State] = []
        self.states_dict: Dict[str, State] = {}

    @classmethod
    def get_user_settings(cls) -> UserSettings:
        user = flask_login.current_user

        user_settings = UserSettings.objects(  # type: ignore
                username=user.username).first()

        if user_settings is None:
            user_settings = UserSettings(username=user.username)
            user_settings.save()

        return user_settings

    def add(
        self,
        *,
        section_name: str,
        form_cls: Type[flask_wtf.FlaskForm],
        template: str,
        field_names: Tuple[str, ...],
    ) -> None:
        if section_name in self.states_dict:
            raise SectionNameIsAlreadyOccupied

        state = State(
            section_name=section_name,
            form_cls=form_cls,
            template=template,
            field_names=field_names,
        )

        self.states.append(state)
        self.states_dict[section_name] = state

    def get_current_state(self, user_settings: UserSettings) -> State:
        for state in self.states:
            for field_name in state.field_names:
                if getattr(user_settings, field_name) is None:
                    return state

        raise FinalStateError

    def get_state_by_section_name(self, section_name: str) -> State:
        return self.states_dict[section_name]


