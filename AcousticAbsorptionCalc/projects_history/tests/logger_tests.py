from django.test import TestCase
from users.models import User


class LoggerTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create(username="admin")
        self.user = User.objects.create(username="user")
