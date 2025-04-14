from decimal import Decimal
from typing import Dict

from .models import Calculation, Material, Norm, NormAbsorptionMultiplier


class RoomAcousticCalculator:
    """Performs room acoustic calculations using the Sabine formula.

    This class calculates the reverberation time of a room based on its
    dimensions, materials, and acoustic norm settings. It supports frequency-specific
    computations and stores results in the database.

    Args:
        height (float): Height of the room in meters.
        length (float): Length of the room in meters.
        width (float): Width of the room in meters.
        furnishing (dict[str, float]): Dictionary of furnishing materials and their areas (in m²).
        construction (dict[str, float]): Dictionary of construction materials and their areas (in m²).
        norm (Norm): The acoustic norm to be applied in the calculation.
    """

    def __init__(
        self,
        height: float,
        length: float,
        width: float,
        furnishing: Dict[str, float],
        construction: Dict[str, float],
        norm: Norm,
    ):
        self.height: float = height
        self.length: float = length
        self.width: float = width
        self.furnishing: Dict[str, float] = furnishing
        self.construction: Dict[str, float] = construction
        self.norm: Norm = norm

    @property
    def volume(self) -> float:
        """Calculates room volume."""
        return self.height * self.length * self.width

    @property
    def all_materials(self) -> Dict[str, float]:
        """Merges furnishing and construction materials."""
        return {**self.furnishing, **self.construction}

    def get_absorption_coefficient(self, material: Material, frequency: str) -> Decimal:
        """Returns the absorption coefficient for a material at a given frequency."""
        return getattr(material, frequency)

    def get_absorption_multiplier(self) -> Decimal:
        """Returns the multiplier based on the norm."""
        try:
            multiplier = NormAbsorptionMultiplier.objects.get(norm=self.norm)
            return multiplier.absorption_multiplier
        except NormAbsorptionMultiplier.DoesNotExist:
            return Decimal("1.0")

    def total_absorption(self, frequency: str) -> Decimal:
        """Calculates total sound absorption at a given frequency."""
        multiplier: Decimal = self.get_absorption_multiplier()
        total: Decimal = Decimal("0.0")

        for name, area in self.all_materials.items():
            try:
                material: Material = Material.objects.get(name=name)
                alpha: Decimal = self.get_absorption_coefficient(material, frequency)
                total += Decimal(area) * alpha * multiplier
            except Material.DoesNotExist:
                continue

        return total

    def sabine_reverberation_time(self, frequency: str) -> Decimal:
        """Computes reverberation time using the Sabine formula."""
        A: Decimal = self.total_absorption(frequency)
        V: Decimal = Decimal(str(self.volume))

        if A == 0:
            return Decimal("0.0")

        return Decimal("0.161") * V / A

    def save_calculation(self, frequency: str) -> Calculation:
        """Saves the reverberation time calculation result to the database."""
        rt: Decimal = self.sabine_reverberation_time(frequency)
        is_within: bool = self.check_if_within_norm(rt)
        return Calculation.objects.create(
            reverberation_time=rt, norm=self.norm, is_within_norm=is_within
        )

    def check_if_within_norm(self, rt: Decimal) -> bool:
        """Checks if a given reverberation time is within norm limits."""
        return Decimal("0.3") <= rt <= Decimal("1.2")
