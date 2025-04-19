from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class AcousticCalculationViewTests(TestCase):
    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.url: str = reverse("acoustic-calculate")
