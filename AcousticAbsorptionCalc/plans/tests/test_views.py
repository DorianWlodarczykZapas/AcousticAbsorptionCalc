from django.contrib.auth import get_user_model
from django.test import TestCase
from plans.factories import PlanFactory
from users.factories import UserFactory

User = get_user_model()


class TestPlanChangeViewSuccess(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory(type="premium")
        self.client.force_login(self.user)
