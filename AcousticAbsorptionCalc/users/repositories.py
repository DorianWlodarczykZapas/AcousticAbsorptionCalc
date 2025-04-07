from django.db import models

from .models import User


class UserRepository:
    @staticmethod
    def get_by_identifier(identifier):
        return User.objects.filter(
            models.Q(username=identifier) | models.Q(email=identifier)
        ).first()

    @staticmethod
    def create_user(user_data):
        password = user_data.pop("password", None)
        user = User(**user_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_user(user, updated_data):
        for key, value in updated_data.items():
            setattr(user, key, value)
        user.save()
        return user
