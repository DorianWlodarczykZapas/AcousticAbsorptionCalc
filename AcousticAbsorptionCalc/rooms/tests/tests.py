from django.test import TestCase
from django.urls import reverse
from projects.factories import ProjectFactory
from rooms.factories import RoomFactory


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
