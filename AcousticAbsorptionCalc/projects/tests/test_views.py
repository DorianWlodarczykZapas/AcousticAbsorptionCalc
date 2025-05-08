from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from projects.factories import ProjectFactory, SharedProjectFactory
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

    def test_create_project_invalid_data(self) -> None:
        response = self.client.post(self.url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.exists())


class ProjectUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.other_user: User = UserFactory()
        self.project: Project = ProjectFactory(user=self.user)
        self.client: Client = Client()

    def test_user_can_update_own_project(self) -> None:
        self.client.force_login(self.user)
        url = reverse("projects:project_update", args=[self.project.pk])
        response = self.client.post(
            url, {"name": "Updated Name", "description": "Updated Description"}
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Name")

    def test_other_user_cannot_update(self) -> None:
        self.client.force_login(self.other_user)
        url = reverse("projects:project_update", args=[self.project.pk])
        response = self.client.post(url, {"name": "Hacked", "description": "Nope"})
        self.assertEqual(response.status_code, 403)


class ProjectDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.project: Project = ProjectFactory(user=self.user)
        self.client.force_login(self.user)

    def test_user_can_delete_project(self) -> None:
        url = reverse("projects:project_delete", args=[self.project.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_other_user_cannot_delete(self) -> None:
        other_user = UserFactory()
        self.client.force_login(other_user)
        url = reverse("projects:project_delete", args=[self.project.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)


class ProjectListViewTest(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.other_user: User = UserFactory()
        self.client.force_login(self.user)

        self.own_project = ProjectFactory(user=self.user)
        self.shared_project = SharedProjectFactory(shared_with_user=self.user).project
        self.unrelated_project = ProjectFactory(user=self.other_user)

    def test_list_projects_includes_own_and_shared(self) -> None:
        url = reverse("projects:project_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        projects = response.context["projects"]
        self.assertIn(self.own_project, projects)
        self.assertIn(self.shared_project, projects)
        self.assertNotIn(self.unrelated_project, projects)

    def test_staff_sees_all_projects(self) -> None:
        staff_user = UserFactory(is_staff=True)
        self.client.force_login(staff_user)
        ProjectFactory.create_batch(3)
        url = reverse("projects:project_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["projects"]), Project.objects.count())


class ProjectDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.other_user: User = UserFactory()
        self.project: Project = ProjectFactory(user=self.user)
        self.client = Client()

    def test_view_own_project(self) -> None:
        self.client.force_login(self.user)
        url = reverse("projects:project_detail", args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cannot_view_project_without_permission(self) -> None:
        self.client.force_login(self.other_user)
        url = reverse("projects:project_detail", args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ProjectPDFViewTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = Client()
        self.project = ProjectFactory(user=self.user)
        self.client.force_login(self.user)

    def test_generate_pdf_success(self) -> None:
        url = reverse("projects:project_pdf", args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_404_if_project_does_not_exist(self) -> None:
        url = reverse("projects:project_pdf", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        url = reverse("projects:project_pdf", args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
