import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from calculations.RoomAcousticCalculator import RoomAcousticCalculator


class TestRoomAcousticCalculator(unittest.TestCase):
    def setUp(self):
        self.norm = MagicMock()
        self.material = MagicMock()
        self.material.oz = Decimal("0.5")

        self.calc = RoomAcousticCalculator(
            height=3.0,
            length=5.0,
            width=4.0,
            furnishing={"Carpet": 10.0},
            construction={"Concrete": 50.0},
            norm=self.norm,
        )

    def test_volume_calculation(self):
        self.assertAlmostEqual(self.calc.volume, 60.0)

    def test_all_materials_merge(self):
        all_mats = self.calc.all_materials
        self.assertIn("Carpet", all_mats)
        self.assertIn("Concrete", all_mats)
        self.assertEqual(all_mats["Carpet"], 10.0)

    @patch("acoustic.room_acoustic_calculator.Material.objects.get")
    def test_get_absorption_coefficient(self, mock_get):
        mock_get.return_value = self.material
        alpha = self.calc.get_absorption_coefficient(self.material, "oz")
        self.assertEqual(alpha, Decimal("0.5"))

    @patch("acoustic.room_acoustic_calculator.NormAbsorptionMultiplier.objects.get")
    def test_get_absorption_multiplier_found(self, mock_get):
        mock_get.return_value.absorption_multiplier = Decimal("1.3")
        self.assertEqual(self.calc.get_absorption_multiplier(), Decimal("1.3"))

    @patch("acoustic.room_acoustic_calculator.NormAbsorptionMultiplier.objects.get")
    def test_get_absorption_multiplier_default(self, mock_get):
        mock_get.side_effect = Exception("Not found")
        self.assertEqual(self.calc.get_absorption_multiplier(), Decimal("1.0"))
