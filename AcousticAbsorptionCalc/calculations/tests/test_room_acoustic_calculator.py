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

    @patch("acoustic.room_acoustic_calculator.Material.objects.get")
    @patch.object(RoomAcousticCalculator, "get_absorption_multiplier")
    def test_total_absorption(self, mock_multiplier, mock_material_get):
        mock_multiplier.return_value = Decimal("1.0")
        mock_mat = MagicMock()
        mock_mat.oz = Decimal("0.2")
        mock_material_get.return_value = mock_mat

        total = self.calc.total_absorption("oz")
        expected = Decimal("0.2") * Decimal("10.0") + Decimal("0.2") * Decimal("50.0")
        self.assertEqual(total, expected)

    @patch.object(RoomAcousticCalculator, "total_absorption")
    def test_sabine_reverberation_time(self, mock_total_abs):
        mock_total_abs.return_value = Decimal("12.0")
        rt = self.calc.sabine_reverberation_time("oz")
        self.assertAlmostEqual(rt, Decimal("0.805"))

    def test_check_if_within_norm(self):
        self.assertTrue(self.calc.check_if_within_norm(Decimal("0.5")))
        self.assertTrue(self.calc.check_if_within_norm(Decimal("0.3")))
        self.assertFalse(self.calc.check_if_within_norm(Decimal("0.2")))

    @patch("acoustic.room_acoustic_calculator.Calculation.objects.create")
    @patch.object(RoomAcousticCalculator, "sabine_reverberation_time")
    @patch.object(RoomAcousticCalculator, "check_if_within_norm")
    def test_save_calculation(self, mock_check, mock_rt, mock_create):
        mock_rt.return_value = Decimal("0.5")
        mock_check.return_value = True
        self.calc.save_calculation("oz")
        mock_create.assert_called_once_with(
            reverberation_time=Decimal("0.5"), norm=self.norm, is_within_norm=True
        )

    def test_volume_zero_dimension(self):
        self.calc.height = 0
        self.assertEqual(self.calc.volume, 0.0)

    def test_all_materials_overlapping_keys(self):
        self.calc.furnishing = {"Carpet": 10.0}
        self.calc.construction = {"Carpet": 5.0}
        all_mats = self.calc.all_materials
        self.assertEqual(all_mats["Carpet"], 5.0)

    def test_get_absorption_coefficient_missing_attribute(self):
        with self.assertRaises(AttributeError):
            mat = MagicMock()
            del mat.oz
            self.calc.get_absorption_coefficient(mat, "oz")

    @patch("acoustic.room_acoustic_calculator.NormAbsorptionMultiplier.objects.get")
    def test_get_absorption_multiplier_raises_unexpected(self, mock_get):
        mock_get.side_effect = Exception("Unexpected error")
        self.assertEqual(self.calc.get_absorption_multiplier(), Decimal("1.0"))
