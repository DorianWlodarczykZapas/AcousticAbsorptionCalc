from unittest.mock import patch

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

    def test_room_create_invalid_width(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Zły pokój",
            "width": "abc",
            "length": "6.00",
            "height": "2.80",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "width", "Wprowadź liczbę.")

    def test_room_create_nonexistent_project(self):
        url = reverse("rooms:room_add", kwargs={"project_id": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_room_list_empty_for_project(self):
        empty_project = ProjectFactory()
        url = reverse("rooms:room_list", kwargs={"project_id": empty_project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak pokoi")
        self.assertEqual(len(response.context["rooms"]), 0)

    def test_room_list_does_not_show_other_project_rooms(self):
        url = reverse("rooms:room_list", kwargs={"project_id": self.project.id})
        response = self.client.get(url)

        other_room = Room.objects.filter(project=self.other_project).first()
        self.assertNotContains(response, other_room.name)

    def test_room_delete(self):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_delete", kwargs={"pk": room.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Room.objects.filter(pk=room.pk).exists())

    def test_room_update_invalid_height(self):
        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        data = {
            "name": self.room1.name,
            "width": self.room1.width,
            "length": self.room1.length,
            "height": "-1.00",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "height", "Wartość musi być dodatnia.")

    @patch("rooms.views.Logger.log_room_created")
    def test_logger_called_on_create(self, mock_logger):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Nowy pokój",
            "width": "5.00",
            "length": "6.00",
            "height": "2.80",
        }
        self.client.post(url, data)
        room = Room.objects.get(name="Nowy pokój")
        mock_logger.assert_called_once_with(
            user_id=room.pk, changed_by=self.client.session.get("_auth_user_id")
        )

    @patch("rooms.views.Logger.log_room_updated")
    def test_logger_called_on_update(self, mock_logger):
        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        data = {
            "name": self.room1.name,
            "width": self.room1.width,
            "length": self.room1.length,
            "height": "3.00",
        }
        self.client.post(url, data)
        mock_logger.assert_called_once_with(
            user_id=self.room1.pk, changed_by=self.client.session.get("_auth_user_id")
        )

    @patch("rooms.views.Logger.log_room_deleted")
    def test_logger_called_on_delete(self, mock_logger):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_delete", kwargs={"pk": room.pk})
        self.client.post(url)
        mock_logger.assert_called_once_with(
            user_id=room.pk, changed_by=self.client.session.get("_auth_user_id")
        )

    def test_room_create_invalid_length(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Pokój",
            "width": "5.00",
            "length": "-2.00",
            "height": "2.50",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "length", "Wartość musi być dodatnia.")

    def test_room_list_invalid_project(self):
        url = reverse("rooms:room_list", kwargs={"project_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak pokoi")

    def test_room_update_view_get(self):
        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edytuj pokój")

    def test_room_delete_view_get(self):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_delete", kwargs={"pk": room.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno chcesz usunąć")

    def test_room_update_nonexistent(self):
        url = reverse("rooms:room_update", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_room_delete_nonexistent(self):
        url = reverse("rooms:room_delete", kwargs={"pk": 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_move_room_valid(self):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_move", kwargs={"pk": room.pk})
        data = {"target_project": self.other_project.pk}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        room.refresh_from_db()
        self.assertEqual(room.project, self.other_project)
