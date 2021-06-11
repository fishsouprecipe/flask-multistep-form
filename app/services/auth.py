from werkzeug import check_password_hash
from werkzeug import generate_password_hash

from app.models import User


class AuthService:
    @classmethod
    def create_user(cls, username: str, password: str) -> User:
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            hashed_password=hashed_password,
        )

        user.save()

        return user
