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


class TestCreateCheckoutSessionView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.plan = PlanFactory()
        self.client.force_login(self.user)

    @patch("plans.services.StripeService.create_checkout_session")
    def test_create_checkout_session_success(self, mock_checkout_session):
        mock_checkout_session.return_value.url = "https://stripe-session-url.com"

        response = self.client.post(
            reverse("plans:create_checkout_session"), {"plan_id": self.plan.id}
        )

        self.assertRedirects(response, "https://stripe-session-url.com")
        mock_checkout_session.assert_called_once()

    def test_create_checkout_session_without_plan_id(self):
        response = self.client.post(reverse("plans:create_checkout_session"))

        self.assertEqual(response.status_code, 404)


class TestStripeWebhookView(TestCase):
    def setUp(self):
        self.user = UserFactory(email="test@example.com")
        self.plan = PlanFactory()

    @patch("stripe.Webhook.construct_event")
    def test_webhook_creates_userplan(self, mock_construct_event):
        # Arrange
        mock_construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer_email": self.user.email,
                    "metadata": {"plan_id": str(self.plan.id)},
                }
            },
        }

        response = self.client.post(
            reverse("plans:stripe_webhook"),
            data=b"{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="valid_signature",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            UserPlan.objects.filter(
                user=self.user, plan=self.plan, is_active=True
            ).exists()
        )

    @patch("stripe.Webhook.construct_event")
    def test_webhook_invalid_user(self, mock_construct_event):
        # Arrange
        mock_construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer_email": "nonexistent@example.com",
                    "metadata": {"plan_id": str(self.plan.id)},
                }
            },
        }

        response = self.client.post(
            reverse("plans:stripe_webhook"),
            data=b"{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="valid_signature",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserPlan.objects.filter(plan=self.plan).exists())

    @patch("stripe.Webhook.construct_event")
    def test_webhook_invalid_signature(self, mock_construct_event):
        mock_construct_event.side_effect = Exception("Invalid signature")

        response = self.client.post(
            reverse("plans:stripe_webhook"),
            data=b"{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="invalid_signature",
        )

        self.assertEqual(response.status_code, 400)


class TestPaymentSuccessView(TestCase):
    def setUp(self):
        self.user = UserFactory(email="test@example.com")
        self.plan = PlanFactory()
        self.user_plan = UserPlanFactory(user=self.user, plan=self.plan, is_active=True)
        self.client.force_login(self.user)

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_success_view_with_session(self, mock_session_retrieve):
        mock_session_retrieve.return_value.customer_email = self.user.email
        mock_session_retrieve.return_value.metadata = {"plan_id": str(self.plan.id)}

        url = reverse("plans:payment_success") + "?session_id=fake_session_id"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/success_payment.html")
        self.assertEqual(response.context["plan_name"], self.plan.name)
        self.assertEqual(response.context["valid_to"], self.user_plan.valid_to)

    def test_payment_success_view_without_session(self):
        url = reverse("plans:payment_success")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/success_payment.html")
        self.assertIsNone(response.context.get("plan_name"))
        self.assertIsNone(response.context.get("valid_to"))


class TestPaymentCancelView(TestCase):
    def test_payment_cancel_view_renders_correct_template(self):

        response = self.client.get(reverse("plans:payment_cancel"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/cancel.html")


class TestChangePlanView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.old_plan = PlanFactory()
        self.new_plan = PlanFactory()
        self.user_plan = UserPlanFactory(
            user=self.user, plan=self.old_plan, is_active=True
        )
        self.client.force_login(self.user)

    def test_get_change_plan_page(self):
        response = self.client.get(reverse("plans:change"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/change_plan.html")
        self.assertEqual(response.context["user_plan"], self.user_plan)

    def test_post_change_plan_success(self):

        response = self.client.post(
            reverse("plans:change"), {"plan_id": self.new_plan.id}
        )

        self.user_plan.refresh_from_db()
        self.assertEqual(self.user_plan.plan, self.new_plan)
        self.assertRedirects(response, reverse("users:home"))
