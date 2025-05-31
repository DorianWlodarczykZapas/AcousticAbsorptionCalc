from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from plans.factories import PlanFactory, UserPlanFactory
from plans.models import UserPlan
from users.factories import UserFactory

User = get_user_model()


class TestPlanListView(TestCase):
    def test_get_plan_list(self):
        PlanFactory.create_batch(3)
        response = self.client.get(reverse("plans:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/plan_list.html")
        self.assertEqual(len(response.context["plans"]), 3)


class TestPlanChangeViewSuccess(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory(type="premium")
        self.client.force_login(self.user)

    def test_change_to_valid_plan(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_id": self.plan.id})

        self.assertRedirects(response, reverse("plans:list"))


class TestPlanChangeViewInvalidPlan(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_change_to_nonexistent_plan(self):
        url = reverse("plans:change")
        response = self.client.post(url, {"plan_id": 9999})
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


class TestPlanChangeMocked(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory(type="premium")
        self.client.force_login(self.user)

    @patch("plans.views.PlanService.change_user_plan")
    def test_mocked_service_call(self, mock_change):
        mock_change.return_value = None
        url = reverse("plans:change")
        self.client.post(url, {"plan_type": "premium"})
        mock_change.assert_called_once()


@patch("stripe.Webhook.construct_event")
def test_webhook_payment_succeeded_creates_userplan(self, mock_event):
    plan = PlanFactory()
    user = UserFactory(email="test@example.com")
    mock_event.return_value = {
        "type": "invoice.payment_succeeded",
        "data": {
            "object": {
                "customer_email": user.email,
                "metadata": {"plan_id": str(plan.id)},
            }
        },
    }

    response = self.client.post(
        "/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="valid_signature",
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(UserPlan.objects.filter(user=user, plan=plan).exists())
