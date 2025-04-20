from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from plans.factories import PlanFactory, UserPlanFactory
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


class TestPlanChangeViewUnauthorized(TestCase):
    def test_redirect_if_not_logged_in(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_type": "premium"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)


class TestPlanChangeViewMissingData(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_missing_plan_type(self):
        url = reverse("plans:change")
        response = self.client.post(url, {})
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("error", messages[0].tags)


class TestPlanChangeIdempotent(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory(type="base")
        self.client.force_login(self.user)
        self.user_plan = UserPlanFactory(user=self.user, plan=self.plan)

    def test_change_to_same_plan(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_type": "base"})
        messages = list(response.wsgi_request._messages)
        self.assertIn("Zmieniono plan", messages[0].message)
