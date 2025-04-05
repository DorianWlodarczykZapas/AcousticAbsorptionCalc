from django.test import TestCase

from .factories import UserFactory
from .models import User


class UserFactoryTest(TestCase):

    def test_create_single_object(self):
        user = UserFactory()

        self.assertIsInstance(user, User)
        self.assertEquals(User.objects.count(), 1)

    def test_create_batch_objects(self):
        UserFactory.create_batch(5)

        self.assertEquals(User.objets.count(), 5)
