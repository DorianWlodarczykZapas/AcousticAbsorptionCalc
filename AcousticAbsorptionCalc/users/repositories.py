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
        return User.objects.create(**user_data)
