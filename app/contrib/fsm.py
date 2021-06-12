from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Type
from typing import Optional
from typing import Tuple
from typing import Dict
from typing import cast

from .utils import is_dunder
from .utils import camel_case_to_snake_case
from .exc import NoStateAvailable

DEFAULT_STATE_NAME = 'default_state'
GROUP_STATES = '__group_states__'
ABSTRACT_NAME = '__abstract__'
GROUP_NAME = '__group_name__'


class State:
    name: Optional[str]
    group: Optional[Type['StateGroup']]
    prev_state_name: Optional[str]
    next_state_name: Optional[str]

    def __init__(
        self,
        *,
        prev_state_name=None,
        next_state_name=None,
    ) -> None:
        self.prev_state_name = prev_state_name
        self.next_state_name = next_state_name
        self.name = None
        self.group = None

    def set_active(self) -> None:
        assert self.group is not None
        self.group.set_active_state(self)

    def get_prev_state(self) -> 'State':
        if self.prev_state_name is None:
            raise NoStateAvailable(f'No prev state for {self!r}')

        assert self.group is not None

        try:
            prev_state = getattr(self.group, self.prev_state_name)

        except AttributeError:
            raise NoStateAvailable(
                'State named '
                f'{getattr(self, GROUP_NAME)}:{self.prev_state_name} '
                'does not exist'
            )

        return prev_state

    def get_next_state(self) -> 'State':
        if self.next_state_name is None:
            raise NoStateAvailable(f'No next state for {self!r}')

        assert self.group is not None

        try:
            next_state = getattr(self.group, self.next_state_name)

        except AttributeError:
            raise NoStateAvailable(
                'State named '
                f'{getattr(self, GROUP_NAME)}:{self.next_state_name} '
                'does not exist'
            )

        return next_state

    def is_active(self) -> bool:
        assert self.group is not None
        return self is self.group.get_active_state()

    def __repr__(self) -> str:
        return f'{getattr(self.group, GROUP_NAME)}:{self.name}'


class StateGroupMeta(type):
    def __new__(
        mcs,
        cls_name: str,
        bases: Tuple[type, ...],
        namespace: Dict,
        **kwargs: Any,
    ) -> type:

        states: Dict[str, State] = {}

        for name, value in namespace.items():
            if is_dunder(name):
                continue

            if isinstance(value, State):
                states[name] = value

        is_abstract = namespace.get(ABSTRACT_NAME, False)

        if not is_abstract and DEFAULT_STATE_NAME not in states:
            raise ValueError(
                'Not abstract state groups must contain default state named '
                f'{DEFAULT_STATE_NAME!r}'
            )


        cls = cast(
            'StateGroup',
            super().__new__(mcs, cls_name, bases, namespace, **kwargs)
        )

        for state_name, state in states.items():
            state.group = cls
            state.name = state_name

        setattr(cls, GROUP_NAME, camel_case_to_snake_case(cls_name))
        setattr(cls, GROUP_STATES, states)

        return cls

T = TypeVar('T', bound=State)


class StateGroup(Generic[T], metaclass=StateGroupMeta):
    if TYPE_CHECKING:
        __abstract__: bool
        __group_name__: str
        __group_states__: Dict[str, T]

    __abstract__ = True

    @classmethod
    def set_active_state(cls, state: T) -> None:
        raise NotImplementedError

    @classmethod
    def get_active_state(cls) -> None:
        raise NotImplementedError

    @classmethod
    def get_default_state(cls) -> None:
        return getattr(cls, DEFAULT_STATE_NAME)
