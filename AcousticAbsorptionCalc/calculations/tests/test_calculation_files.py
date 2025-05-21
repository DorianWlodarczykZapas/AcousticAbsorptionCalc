from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock, patch

from calculations.factories import NormFactory
from calculations.RoomAcousticCalculator import RoomAcousticCalculator


class RoomAcousticCalculatorTestCase(TestCase):
    def setUp(self):
        self.norm = NormFactory()
        self.height = 3.0
        self.length = 5.0
        self.width = 4.0
        self.furnishing = {"wood": 10.0}
        self.construction = {"concrete": 20.0}
        self.sti = 0.7
        self.calc = RoomAcousticCalculator(
            height=self.height,
            length=self.length,
            width=self.width,
            furnishing=self.furnishing,
            construction=self.construction,
            norm=self.norm,
            sti=self.sti,
        )

    def test_volume_property(self):
        expected_volume = self.height * self.length * self.width
        self.assertAlmostEqual(self.calc.volume, expected_volume)

    def test_all_materials_property(self):
        combined = {**self.furnishing, **self.construction}
        self.assertEqual(self.calc.all_materials, combined)

    @patch("")
    @patch("")
    def test_calculate_rt_for(self, mock_reverb_calc, mock_multiplier_resolver):
        mock_multiplier_instance = MagicMock()
        mock_multiplier_instance.resolve.return_value = Decimal("1.23")
        mock_multiplier_resolver.return_value = mock_multiplier_instance

        mock_reverb_instance = MagicMock()
        mock_reverb_instance.compute_rt.return_value = Decimal("0.56")
        mock_reverb_calc.return_value = mock_reverb_instance

        frequency = "_500"
        result = self.calc.calculate_rt_for(frequency)

        mock_multiplier_resolver.assert_called_once_with(
            self.norm, self.height, self.calc.volume, self.sti
        )
        mock_multiplier_instance.resolve.assert_called_once()

        mock_reverb_calc.assert_called_once_with(
            self.calc.all_materials, Decimal("1.23"), self.calc.volume
        )
        mock_reverb_instance.compute_rt.assert_called_once_with(frequency)

        self.assertEqual(result, Decimal("0.56"))

    @patch("")
    def test_is_within_norm(self, mock_norm_checker):
        mock_checker_instance = MagicMock()
        mock_checker_instance.is_within.return_value = True
        mock_norm_checker.return_value = mock_checker_instance

        rt = Decimal("1.5")
        result = self.calc.is_within_norm(rt)

        mock_norm_checker.assert_called_once_with(
            self.norm, self.height, self.calc.volume, self.sti
        )
        mock_checker_instance.is_within.assert_called_once_with(rt)

        self.assertTrue(result)
