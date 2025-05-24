from typing import Any
from unittest.mock import MagicMock, patch

from calculations.factories import NormFactory
from calculations.models import Norm
from calculations.RoomAcousticCalculator import Calculation
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class AcousticCalculationViewTests(TestCase):
    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.url: str = reverse("acoustic-calculate")

    def test_valid_input_returns_success(self) -> None:
        norm: Norm = NormFactory()

        payload: dict[str, Any] = {
            "height": 2.8,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"sofa": 3.0},
            "construction": {"plaster": 1.5},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reverberation_time", data)
        self.assertIn("is_within_norm", data)
        self.assertEqual(data["message"], "Pomiar wykonany poprawnie.")

    def test_missing_required_fields_returns_400(self) -> None:
        payload: dict[str, Any] = {
            "height": 3.0,
            "length": 5.0,
            # brak width
            "norm_id": None,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Brakuje wymaganych danych.")

    def test_invalid_norm_id_returns_404(self) -> None:
        payload: dict[str, Any] = {
            "height": 3.0,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"chair": 2.5},
            "construction": {"brick": 1.5},
            "norm_id": 999999,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 404)

    def test_invalid_data_format_returns_500(self) -> None:
        norm: Norm = NormFactory()

        payload: dict[str, Any] = {
            "height": "wysokość",
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"table": 1.0},
            "construction": {"glass": 1.0},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    def test_calculation_is_saved_in_database(self) -> None:
        norm: Norm = NormFactory()
        initial_count: int = Calculation.objects.count()

        payload: dict[str, Any] = {
            "height": 2.5,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"carpet": 2.0},
            "construction": {"wood": 1.5},
            "norm_id": norm.id,
            "frequency": "1000",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Calculation.objects.count(), initial_count + 1)

    def test_extra_unknown_field_is_ignored(self) -> None:
        norm: Norm = NormFactory()
        payload: dict[str, Any] = {
            "height": 2.8,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"sofa": 3.0},
            "construction": {"plaster": 1.5},
            "norm_id": norm.id,
            "frequency": "500",
            "unexpected_field": "I should be ignored",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("reverberation_time", response.json())

    def test_empty_furnishing_and_construction_still_works(self) -> None:
        norm: Norm = NormFactory()
        payload: dict[str, Any] = {
            "height": 3.0,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {},
            "construction": {},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("reverberation_time", response.json())

    def test_string_frequency_as_number_string_is_accepted(self) -> None:
        norm: Norm = NormFactory()
        payload: dict[str, Any] = {
            "height": 2.6,
            "length": 4.5,
            "width": 3.5,
            "furnishing": {"rug": 2.0},
            "construction": {"concrete": 2.5},
            "norm_id": norm.id,
            "frequency": "1000",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["reverberation_time"], float)

    def test_zero_values_in_dimensions_return_400(self) -> None:
        norm: Norm = NormFactory()
        payload: dict[str, Any] = {
            "height": 0.0,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"sofa": 2.0},
            "construction": {"plaster": 1.5},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_frequency_string_returns_500(self) -> None:
        norm: Norm = NormFactory()
        payload: dict[str, Any] = {
            "height": 2.5,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"carpet": 1.5},
            "construction": {"wood": 2.0},
            "norm_id": norm.id,
            "frequency": "niepoprawna",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    def test_empty_body_returns_400(self) -> None:
        response = self.client.post(self.url, data="", content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    def test_furnishing_wrong_type_returns_500(self) -> None:
        norm = NormFactory()
        payload = {
            "height": 2.5,
            "length": 5.0,
            "width": 4.0,
            "furnishing": ["kanapa", "stół"],
            "construction": {"beton": 1.0},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    def test_negative_material_area_still_works(self) -> None:
        norm = NormFactory()
        payload = {
            "height": 3.0,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"carpet": -5.0},
            "construction": {"concrete": 10.0},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("reverberation_time", response.json())

    def test_missing_frequency_returns_400(self) -> None:
        norm = NormFactory()
        payload = {
            "height": 3.0,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"chair": 2.0},
            "construction": {"brick": 1.0},
            "norm_id": norm.id,
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Brakuje wymaganych danych.")

    @patch("calculations.views.RoomAcousticCalculator")
    def test_calculator_methods_are_called(self, mock_calculator_cls) -> None:
        mock_calculator = MagicMock()
        mock_calculator.sabine_reverberation_time.return_value = 1.23
        mock_calculator.check_if_within_norm.return_value = True
        mock_calculator_cls.return_value = mock_calculator

        norm = NormFactory()

        payload = {
            "height": 2.5,
            "length": 5.0,
            "width": 4.0,
            "furnishing": {"chair": 2.0},
            "construction": {"brick": 1.0},
            "norm_id": norm.id,
            "frequency": "500",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 200)
        mock_calculator.sabine_reverberation_time.assert_called_once_with("500")
        mock_calculator.check_if_within_norm.assert_called_once_with(1.23)
        mock_calculator.save_calculation.assert_called_once_with("500")

    def test_integer_frequency_is_accepted(self):
        norm = NormFactory()
        payload = {
            "height": 2.5,
            "length": 4.0,
            "width": 3.0,
            "furnishing": {"rug": 1.0},
            "construction": {"wood": 1.0},
            "norm_id": norm.id,
            "frequency": 500,
        }

        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("reverberation_time", response.json())
