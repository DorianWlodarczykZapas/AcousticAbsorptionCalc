from unittest import TestCase
from unittest.mock import patch

from django.test import Client
from django.urls import reverse
from plans.models import Plan, User


class PlanListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Plan.objects.create(
            name="Base",
            price=10,
            billing_period="monthly",
            max_projects=1,
            max_rooms_per_project=1,
            description="test",
        )

    def test_plan_list_view(self) -> None:
        response = self.client.get(reverse("plan_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("plans", response.context)
        self.assertTemplateUsed(response, "plans/plan_list.html")


class CreateCheckoutSessionViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="secret"
        )
        self.plan = Plan.objects.create(
            name="Pro",
            price=50,
            billing_period="monthly",
            max_projects=10,
            max_rooms_per_project=5,
            description="desc",
        )

    @patch("plans.services.StripeService.create_checkout_session")
    def test_redirects_to_stripe_checkout(self, mock_create_session) -> None:
        mock_create_session.return_value = type(
            "obj", (object,), {"url": "https://stripe.test/session"}
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("create_checkout_session"), data={"plan_id": self.plan.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://stripe.test/session")
