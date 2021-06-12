from typing import Generic
from typing import TypeVar
from flask_login import current_user

from app.contrib.fsm import DEFAULT_STATE_NAME
from app.contrib.fsm import StateGroup
from app.contrib.fsm import State

T = TypeVar('T', bound=State)


class BaseStateGroup(StateGroup[T], Generic[T]):
    __abstract__ = True

    @classmethod
    def set_active_state(cls, state: T) -> None:
        if current_user is None:
            raise ValueError

        setattr(
            current_user.state, cls.__group_name__, state.name) # type: ignore
        current_user.save()  # type: ignore

    @classmethod
    def get_active_state(cls) -> T:
        if current_user is None:
            raise ValueError

        try:
            active_state_name = getattr(
                    current_user.state, cls.__group_name__)  # type: ignore

        except AttributeError:
            active_state_name = DEFAULT_STATE_NAME

        return cls.__group_states__[active_state_name]
