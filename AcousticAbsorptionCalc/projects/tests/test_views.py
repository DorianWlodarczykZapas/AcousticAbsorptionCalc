from django.test import Client, TestCase
from django.urls import reverse
from users.factories import UserFactory
from users.models import User


class ProjectCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        self.user: User = UserFactory()
        self.client.force_login(self.user)
        self.url: str = reverse("projects:project_create")
