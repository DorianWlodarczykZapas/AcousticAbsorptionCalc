from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from projects.models import Project
from users.factories import UserFactory
from users.models import User


class ProjectCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        self.user: User = UserFactory()
        self.client.force_login(self.user)
        self.url: str = reverse("projects:project_create")

    def test_create_project_success(self) -> None:
        response: HttpResponse = self.client.post(
            self.url,
            {
                "name": "New Test Project",
                "description": "Test description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Test Project").exists())

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
