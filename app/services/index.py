from typing import Tuple

from app.models import User


class IndexService:
    @classmethod
    def get_all_users(cls) -> Tuple[User]:
        return tuple(User.objects())  # type: ignore
