from django.contrib.auth.hashers import check_password, make_password

from .models import User
from .repositories import UserRepository


class AuthService:
    @staticmethod
    def authenticate(identifier, password):
        user = UserRepository.get_by_identifier(identifier)
        if user and check_password(password, user.password_hash):
            return user
        return None


class UserService:
    @staticmethod
    def register_user(form):
        user = form.save()
        return user

    @staticmethod
    def update_user(self, user: User, data: dict):
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        new_password = data.get("new_password")
        if new_password:
            user.password_hash = make_password(new_password)

        user.save()
