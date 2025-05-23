from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock, patch

from calculations.factories import NormAbsorptionMultiplierFactory, NormFactory
from calculations.models import Calculation, NormCalculationType, NormCategory
from calculations.multiplier_resolver import AbsorptionMultiplierResolver
from calculations.norm_checker import NormComplianceChecker
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

    @patch("calculations.room_acoustic_calculator.AbsorptionMultiplierResolver")
    @patch("calculations.room_acoustic_calculator.ReverberationCalculator")
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

    @patch("calculations.room_acoustic_calculator.NormComplianceChecker")
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

    @patch.object(
        RoomAcousticCalculator, "calculate_rt_for", return_value=Decimal("1.1")
    )
    def test_calculate_all_frequencies(self, mock_calc_rt_for):
        expected_frequencies = ["_250", "_500", "_1000", "_2000", "_4000"]
        result = self.calc.calculate_all_frequencies()

        self.assertEqual(set(result.keys()), set(expected_frequencies))
        self.assertTrue(all(isinstance(v, Decimal) for v in result.values()))
        self.assertEqual(mock_calc_rt_for.call_count, len(expected_frequencies))

    @patch.object(
        RoomAcousticCalculator, "calculate_rt_for", return_value=Decimal("1.0")
    )
    @patch.object(RoomAcousticCalculator, "is_within_norm", return_value=True)
    def test_save_calculation(self, mock_is_within_norm, mock_calculate_rt_for):
        frequency = "_1000"
        calculation = self.calc.save_calculation(frequency)

        mock_calculate_rt_for.assert_called_once_with(frequency)
        mock_is_within_norm.assert_called_once_with(Decimal("1.0"))

        self.assertEqual(calculation.reverberation_time, Decimal("1.0"))
        self.assertEqual(calculation.norm, self.norm)
        self.assertTrue(calculation.is_within_norm)
        self.assertEqual(calculation.room_height, self.height)
        self.assertEqual(calculation.room_volume, self.calc.volume)
        self.assertEqual(calculation.sti, self.sti)

        self.assertEqual(Calculation.objects.count(), 1)

    @patch("calculations.room_acoustic_calculator.AbsorptionMultiplierResolver")
    @patch("calculations.room_acoustic_calculator.ReverberationCalculator")
    def test_calculate_rt_for_returns_zero_when_calculation_fails(
        self, mock_reverb_calc, mock_multiplier_resolver
    ):
        mock_multiplier_instance = MagicMock()
        mock_multiplier_instance.resolve.return_value = Decimal("1.0")
        mock_multiplier_resolver.return_value = mock_multiplier_instance

        mock_reverb_instance = MagicMock()
        mock_reverb_instance.compute_rt.return_value = Decimal("0.0")
        mock_reverb_calc.return_value = mock_reverb_instance

        result = self.calc.calculate_rt_for("_1000")
        self.assertEqual(result, Decimal("0.0"))

    @patch("calculations.room_acoustic_calculator.NormComplianceChecker")
    def test_is_within_norm_false_case(self, mock_norm_checker):
        mock_checker_instance = MagicMock()
        mock_checker_instance.is_within.return_value = False
        mock_norm_checker.return_value = mock_checker_instance

        result = self.calc.is_within_norm(Decimal("2.0"))
        self.assertFalse(result)

    @patch.object(RoomAcousticCalculator, "calculate_rt_for")
    def test_calculate_all_frequencies_with_failure(self, mock_calc_rt_for):
        mock_calc_rt_for.side_effect = [
            Decimal("1.0"),
            Decimal("1.1"),
            Exception("Calculation error"),
            Decimal("1.2"),
            Decimal("1.3"),
        ]

        with self.assertRaises(Exception):
            self.calc.calculate_all_frequencies()

    @patch.object(
        RoomAcousticCalculator, "calculate_rt_for", side_effect=Exception("Failed")
    )
    def test_save_calculation_fails_gracefully(self, mock_calc_rt_for):
        with self.assertRaises(Exception):
            self.calc.save_calculation("_1000")

        self.assertEqual(Calculation.objects.count(), 0)


class AbsorptionMultiplierResolverTest(TestCase):
    def setUp(self):
        self.norm = NormFactory()

    def test_returns_multiplier_for_height(self):
        NormAbsorptionMultiplierFactory(
            norm=self.norm,
            category=NormCategory.HEIGHT,
            multiplier=Decimal("1.2"),
            height_min=2.0,
            height_max=4.0,
        )
        resolver = AbsorptionMultiplierResolver(self.norm, height=3.0, volume=100.0)
        self.assertEqual(resolver.resolve(), Decimal("1.2"))

    def test_returns_multiplier_for_volume(self):
        NormAbsorptionMultiplierFactory(
            norm=self.norm,
            category=NormCategory.VOLUME,
            multiplier=Decimal("1.5"),
            volume_min=50.0,
            volume_max=200.0,
        )
        resolver = AbsorptionMultiplierResolver(self.norm, height=2.5, volume=150.0)
        self.assertEqual(resolver.resolve(), Decimal("1.5"))

    def test_returns_multiplier_for_sti(self):
        NormAbsorptionMultiplierFactory(
            norm=self.norm,
            category=NormCategory.STI,
            multiplier=Decimal("1.3"),
            sti_min=0.6,
            sti_max=0.8,
        )
        resolver = AbsorptionMultiplierResolver(
            self.norm, height=3.0, volume=80.0, sti=0.7
        )
        self.assertEqual(resolver.resolve(), Decimal("1.3"))

    def test_returns_multiplier_for_none_category(self):
        NormAbsorptionMultiplierFactory(
            norm=self.norm,
            category=NormCategory.NONE,
            multiplier=Decimal("1.1"),
        )
        resolver = AbsorptionMultiplierResolver(self.norm, height=5.0, volume=500.0)
        self.assertEqual(resolver.resolve(), Decimal("1.1"))

    def test_returns_default_when_no_match(self):
        NormAbsorptionMultiplierFactory(
            norm=self.norm,
            category=NormCategory.HEIGHT,
            multiplier=Decimal("1.9"),
            height_min=4.0,
            height_max=6.0,
        )
        resolver = AbsorptionMultiplierResolver(self.norm, height=3.0, volume=20.0)
        self.assertEqual(resolver.resolve(), Decimal("1.0"))


class NormComplianceCheckerTests(TestCase):
    def test_sti_type_valid(self):
        norm = NormFactory(application_type=NormCalculationType.STI)
        checker = NormComplianceChecker(norm, height=3.0, volume=100.0, sti=0.7)

        self.assertTrue(checker.is_within(Decimal("1.0")))

    def test_sti_type_invalid(self):
        norm = NormFactory(application_type=NormCalculationType.STI)
        checker = NormComplianceChecker(norm, height=3.0, volume=100.0, sti=0.4)

        self.assertFalse(checker.is_within(Decimal("1.0")))

    def test_sti_type_missing_sti(self):
        norm = NormFactory(application_type=NormCalculationType.STI)
        checker = NormComplianceChecker(norm, height=3.0, volume=100.0, sti=None)

        self.assertFalse(checker.is_within(Decimal("1.0")))

    def test_none_type_valid(self):
        norm = NormFactory(application_type=NormCalculationType.NONE)

        class Dummy:
            no_cubature_req = "1.1"

        norm.norms_reverb_time_no_req = Dummy()

        checker = NormComplianceChecker(norm, height=3.0, volume=100.0)
        self.assertTrue(checker.is_within(Decimal("1.0")))
        self.assertFalse(checker.is_within(Decimal("1.2")))
