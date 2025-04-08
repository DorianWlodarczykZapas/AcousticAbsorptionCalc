from django.test import TestCase
from faker.contrib import pytest
from users.tests.factories import UserFactory

from .models import User

pytestmark = pytest.mark.django_db


class UserFactoryTest(TestCase):

    def test_create_single_object(self):
        user = UserFactory()

        self.assertIsInstance(user, User)
        self.assertEquals(User.objects.count(), 1)

    def test_create_batch_objects(self):
        UserFactory.create_batch(5)
        self.assertEquals(User.objects.count(), 5)

    def test_user_registration(client):
        response = client.post(
            "/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "password123",
                "password2": "password123",
            },
        )
        assert response.status_code == 302
