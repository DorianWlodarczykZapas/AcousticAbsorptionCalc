from unittest import TestCase

from django.test import Client
from django.urls import reverse
from plans.models import Plan


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
