from unittest.mock import patch

from calculations.acoustic_calculator import AcousticCalculator
from calculations.models import Material, Norm
from django.test import TestCase
from django.urls import reverse
from projects.factories import ProjectFactory
from rooms.factories import RoomFactory
from rooms.models import Furnishing, Room, RoomMaterial


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

    @patch("user_logs.logger.Logger.log_room_created")
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

    @patch("user_logs.logger.Logger.log_room_updated")
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

    @patch("user_logs.logger.Logger.log_room_deleted")
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

    def test_move_room_same_project(self):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_move", kwargs={"pk": room.pk})
        data = {"target_project": self.project.pk}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "target_project", "Room is already in this project."
        )

    def test_move_room_view_get(self):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_move", kwargs={"pk": room.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Przenieś pokój")

    @patch("project_logs.ProjectLogger.log_edit_furnishing")
    def test_project_logger_called_on_move(self, mock_logger):
        room = RoomFactory(project=self.project)
        url = reverse("rooms:room_move", kwargs={"pk": room.pk})
        data = {"target_project": self.other_project.pk}

        self.client.post(url, data)

        mock_logger.assert_called_once()
        self.assertEqual(mock_logger.call_args[1]["project"], self.other_project)

    def test_room_create_view_context_contains_formset(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("furnishing_formset", response.context)

    def test_room_create_invalid_formset(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Pokój testowy",
            "width": "5.00",
            "length": "5.00",
            "height": "2.80",
            "furnishing_set-TOTAL_FORMS": "1",
            "furnishing_set-INITIAL_FORMS": "0",
            "furnishing_set-MIN_NUM_FORMS": "0",
            "furnishing_set-MAX_NUM_FORMS": "1000",
            "furnishing_set-0-material": "",
            "furnishing_set-0-area": "15.0",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "furnishing_formset", 0, "material", "To pole jest wymagane."
        )

    def test_room_create_with_valid_formset(self):
        url = reverse("rooms:room_add", kwargs={"project_id": self.project.id})
        data = {
            "name": "Pokój testowy",
            "width": "5.00",
            "length": "6.00",
            "height": "2.80",
            "furnishing_set-TOTAL_FORMS": "1",
            "furnishing_set-INITIAL_FORMS": "0",
            "furnishing_set-MIN_NUM_FORMS": "0",
            "furnishing_set-MAX_NUM_FORMS": "1000",
            "furnishing_set-0-material": "1",
            "furnishing_set-0-area": "12.0",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Room.objects.filter(name="Pokój testowy").exists())

    def test_room_update_view_context(self):
        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["room"], self.room1)

    def test_room_update_redirects_to_correct_project_list(self):
        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        data = {
            "name": self.room1.name,
            "width": self.room1.width,
            "length": self.room1.length,
            "height": "3.50",
        }

        response = self.client.post(url, data)
        self.assertRedirects(
            response, reverse("rooms:room_list", kwargs={"project_id": self.project.id})
        )

    def test_move_nonexistent_room(self):
        url = reverse("rooms:room_move", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_room_update_updates_materials_and_furnishings(self):
        material1 = Material.objects.create(
            name="Mat1",
            type="Test",
            freq_125=0.1,
            freq_250=0.2,
            freq_500=0.3,
            freq_1000=0.4,
            freq_2000=0.5,
            freq_4000=0.6,
        )
        material2 = Material.objects.create(
            name="Mat2",
            type="Test",
            freq_125=0.1,
            freq_250=0.2,
            freq_500=0.3,
            freq_1000=0.4,
            freq_2000=0.5,
            freq_4000=0.6,
        )

        url = reverse("rooms:room_update", kwargs={"pk": self.room1.pk})
        data = {
            "name": self.room1.name,
            "width": self.room1.width,
            "length": self.room1.length,
            "height": self.room1.height,
            "floor_material": material1.pk,
            "ceiling_material": material2.pk,
            "wall_a_material": "",
            "wall_b_material": "",
            "wall_c_material": "",
            "wall_d_material": "",
            "furnishing_set-TOTAL_FORMS": "1",
            "furnishing_set-INITIAL_FORMS": "0",
            "furnishing_set-MIN_NUM_FORMS": "0",
            "furnishing_set-MAX_NUM_FORMS": "1000",
            "furnishing_set-0-material": material1.pk,
            "furnishing_set-0-area": "10.0",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(RoomMaterial.objects.filter(room=self.room1).count(), 2)
        self.assertEqual(Furnishing.objects.filter(room=self.room1).count(), 1)

    def test_surface_validation_tolerance(self):
        norm = Norm.objects.create(name="Norma X")
        material = Material.objects.create(
            name="Mat3",
            type="Test",
            freq_125=0.1,
            freq_250=0.2,
            freq_500=0.3,
            freq_1000=0.4,
            freq_2000=0.5,
            freq_4000=0.6,
        )

        calculator = AcousticCalculator(
            norm=norm,
            room_dimensions={"width": 5.0, "length": 6.0, "height": 3.0},
            construction_surfaces=[
                {"material": material, "area_m2": 90.0},
            ],
            furnishing_elements=[],
        )

        result = calculator.validate_surface_match(tolerance=0.3)
        self.assertFalse(result["valid"])
        self.assertTrue(result["difference"] > 0)
