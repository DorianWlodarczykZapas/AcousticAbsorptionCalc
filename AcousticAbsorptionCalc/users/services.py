from django.contrib.auth.hashers import check_password

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
