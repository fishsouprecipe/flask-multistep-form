import functools
from typing import NamedTuple
from typing import Type
from typing import Tuple

from flask_wtf import FlaskForm

from app.contrib.fsm import State
from app.contrib.exc import NoStateAvailable
from app.forms.settings import FirstForm
from app.forms.settings import SecondForm
from app.forms.settings import ThirdForm

from .base import BaseStateGroup


class StepInfo(NamedTuple):
    section_name: str
    form_cls: Type[FlaskForm]
    template: str


class SettingsState(State):
    def __init__(
        self,
        *,
        step_info: StepInfo,
        prev_state_name=None,
        next_state_name=None,
    ) -> None:
        super().__init__(
            prev_state_name=prev_state_name,
            next_state_name=next_state_name,
        )
        self.step_info = step_info



class SettingsStateGroup(BaseStateGroup[SettingsState]):
    first_form = SettingsState(
        step_info=StepInfo(
            section_name='first-form',
            form_cls=FirstForm,
            template='settings/first-form.jinja2',
        ),
        next_state_name='second_form',
    )
    default_state = first_form
    second_form = SettingsState(
        step_info=StepInfo(
            section_name='second-form',
            form_cls=SecondForm,
            template='settings/second-form.jinja2',
        ),
        prev_state_name='first_form',
        next_state_name='third_form',
    )
    third_form = SettingsState(
        step_info=StepInfo(
            section_name='third-form',
            form_cls=ThirdForm,
            template='settings/third-form.jinja2',
        ),
        prev_state_name='second_form',
    )

