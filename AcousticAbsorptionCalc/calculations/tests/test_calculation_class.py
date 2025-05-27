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
