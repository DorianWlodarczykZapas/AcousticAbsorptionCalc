from django.test import TestCase
from django.urls import reverse
from projects.factories import ProjectFactory
from rooms.factories import RoomFactory
from rooms.models import Room


class RoomViewsTestCase(TestCase):
    def setUp(self):
        self.project = ProjectFactory()
        self.other_project = ProjectFactory()

        self.room1 = RoomFactory(project=self.project)
        self.room2 = RoomFactory(project=self.project)
        RoomFactory(project=self.other_project)

    def test_room_list_view_filters_by_project(self):
        url = reverse("rooms:room_list", kwargs={"project_id": self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.room1.name)
        self.assertContains(response, self.room2.name)
        self.assertEqual(len(response.context["rooms"]), 2)

    def test_room_create_view_get(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dodaj nowy pokój")

    def test_room_create_view_post(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Nowy pokój",
            "width": "5.00",
            "length": "6.00",
            "height": "2.80",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        room = Room.objects.get(name="Nowy pokój")
        self.assertEqual(room.project, self.project)
        self.assertEqual(str(room.width), "5.00")

    def test_room_create_missing_name(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "",
            "width": "5.00",
            "length": "6.00",
            "height": "2.80",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "name", "To pole jest wymagane.")
