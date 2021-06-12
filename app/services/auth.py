from typing import Optional

import flask_login
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.models import User


class AuthError(Exception): pass
class UserDoesNotExist(Exception): pass
class UsernameIsAlreadyOccupied(Exception): pass
class UserInvalidPassword(Exception): pass


class AuthService:
    @classmethod
    def create_user(cls, username: str, password: str) -> User:
        existing_user: Optional[User] = \
                User.objects(username=username).first()  # type: ignore

        if existing_user is not None:
            raise UsernameIsAlreadyOccupied

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            hashed_password=hashed_password,
        )

        user.save()

        return user

    @classmethod
    def authorize_user(cls, username: str, password: str) -> None:
        user: Optional[User] = \
                User.objects(username=username).first()  # type: ignore

        if user is None:
            raise UserDoesNotExist

        if not check_password_hash(user.hashed_password, password):
            raise UserInvalidPassword

        flask_login.login_user(user)

    @classmethod
    def logout_user(cls) -> None:
        flask_login.logout_user()
