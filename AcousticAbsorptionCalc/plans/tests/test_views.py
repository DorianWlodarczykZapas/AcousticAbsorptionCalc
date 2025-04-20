from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from plans.factories import PlanFactory
from users.factories import UserFactory

User = get_user_model()


class TestPlanChangeViewSuccess(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory(type="premium")
        self.client.force_login(self.user)

    def test_change_to_valid_plan(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_type": self.plan.type})
        self.assertRedirects(response, reverse("plans:list"))


class TestPlanChangeViewInvalidPlan(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_change_to_nonexistent_plan(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_type": "nonexistent"})
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("error", messages[0].tags)
