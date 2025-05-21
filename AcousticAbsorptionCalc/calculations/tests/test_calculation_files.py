from unittest import TestCase

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
