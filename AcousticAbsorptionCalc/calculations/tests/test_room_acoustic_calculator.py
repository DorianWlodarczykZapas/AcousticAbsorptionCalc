import unittest
from decimal import Decimal
from unittest.mock import MagicMock

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
