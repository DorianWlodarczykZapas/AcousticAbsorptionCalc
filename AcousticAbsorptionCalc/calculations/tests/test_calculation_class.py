import unittest
from decimal import Decimal

from calculations.acoustic_calculator import AcousticCalculator
from calculations.factories import MaterialFactory, NormFactory


class TestAcousticCalculator(unittest.TestCase):
    def setUp(self):
        self.norm = NormFactory(
            rt_max=Decimal("0.6"),
            sti_min=Decimal("0.6"),
            absorption_min_factor=Decimal("0.9"),
        )

        self.material = MaterialFactory(
            freq_125=Decimal("0.70"),
            freq_250=Decimal("0.80"),
            freq_500=Decimal("0.90"),
            freq_1000=Decimal("0.95"),
            freq_2000=Decimal("1.00"),
            freq_4000=Decimal("1.00"),
        )

        self.room_dimensions = {
            "width": 5.0,
            "length": 6.0,
            "height": 3.0,
        }

        self.construction_surfaces = [
            {"area_m2": 30.0, "material": self.material},
            {"area_m2": 30.0, "material": self.material},
            {"area_m2": 42.0, "material": self.material},
            {"area_m2": 42.0, "material": self.material},
            {"area_m2": 21.0, "material": self.material},
            {"area_m2": 21.0, "material": self.material},
        ]

        self.furnishings = [
            {"area_m2": 10.0, "material": self.material},
        ]

        self.calculator = AcousticCalculator(
            norm=self.norm,
            room_dimensions=self.room_dimensions,
            construction_surfaces=self.construction_surfaces,
            furnishing_elements=self.furnishings,
            freq_band="500",
        )

    def test_room_geometry(self):
        volume, surface = self.calculator.calculate_room_geometry()
        self.assertEqual(round(volume, 2), 90.0)
        self.assertEqual(round(surface, 2), 186.0)

    def test_total_absorption(self):
        absorption = self.calculator.calculate_absorption()
        expected = sum(
            e["area_m2"] * self.material.freq_500
            for e in self.construction_surfaces + self.furnishings
        )
        self.assertAlmostEqual(absorption, float(expected), places=2)

    def test_reverberation_time(self):
        rt = self.calculator.calculate_rt()
        self.assertGreater(rt, 0)
        self.assertLessEqual(rt, 10.0)

    def test_required_absorption(self):
        required = self.calculator.calculate_required_absorption()
        expected = (
            float(self.norm.absorption_min_factor)
            * self.calculator.calculate_room_geometry()[1]
        )
        self.assertAlmostEqual(required, expected, places=2)

    def test_is_within_norm(self):
        self.assertTrue(self.calculator.is_within_norm())

    def test_result_keys(self):
        result = self.calculator.result()
        self.assertIn("volume_m3", result)
        self.assertIn("surface_area_m2", result)
        self.assertIn("absorption_achieved", result)
        self.assertIn("reverberation_time_s", result)
        self.assertIn("estimated_sti", result)
        self.assertIn("norm_passed", result)

    def test_no_surfaces(self):
        calc = AcousticCalculator(self.norm, self.default_room, [], [])
        result = calc.result()
        self.assertEqual(result["absorption_achieved"], 0.0)
        self.assertEqual(result["reverberation_time_s"], 0.0)
        self.assertFalse(result["norm_passed"])

    def test_zero_area_surface(self):
        surfaces = [{"area_m2": 0.0, "material": self.material}]
        calc = AcousticCalculator(self.norm, self.default_room, surfaces, [])
        result = calc.result()
        self.assertEqual(result["absorption_achieved"], 0.0)
        self.assertFalse(result["norm_passed"])
