from decimal import Decimal

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

    Attributes:
        height (float): Room height.
        length (float): Room length.
        width (float): Room width.
        furnishing (dict[str, float]): Furnishing materials and areas.
        construction (dict[str, float]): Construction materials and areas.
        norm (Norm): Applied acoustic norm.

    Methods:
        volume: Calculates room volume.
        all_materials: Merges furnishing and construction materials.
        get_absorption_coefficient(material, frequency): Returns the absorption coefficient for a material at a given frequency.
        get_absorption_multiplier(): Returns the multiplier based on the norm.
        total_absorption(frequency): Calculates total sound absorption at a given frequency.
        sabine_reverberation_time(frequency): Computes reverberation time using the Sabine formula.
        check_if_within_norm(rt): Checks if a given reverberation time is within norm limits.
        save_calculation(frequency): Saves the reverberation time calculation result to the database.
    """
    def __init__(self, height, length, width, furnishing, construction, norm: Norm):
       
        self.height = height
        self.length = length
        self.width = width
        self.furnishing = furnishing
        self.construction = construction
        self.norm = norm

    @property
    def volume(self):
        return self.height * self.length * self.width

    @property
    def all_materials(self) -> dict[..., ...]:
        return {**self.furnishing, **self.construction}

    def get_absorption_coefficient(self, material: Material, frequency: str) -> Decimal:
        return getattr(material, frequency)

    def get_absorption_multiplier(self) -> Decimal:
        try:
            multiplier = NormAbsorptionMultiplier.objects.get(norm=self.norm)
            return multiplier.absorption_multiplier
        except NormAbsorptionMultiplier.DoesNotExist:
            return Decimal("1.0")

    def total_absorption(self, frequency: str) -> Decimal:
        multiplier = self.get_absorption_multiplier()
        total = Decimal("0.0")

        for name, area in self.all_materials.items():
            try:
                material = Material.objects.get(name=name)
                alpha = self.get_absorption_coefficient(material, frequency)
                total += Decimal(area) * alpha * multiplier
            except Material.DoesNotExist:
                continue

        return total

    def sabine_reverberation_time(self, frequency: str) -> Decimal:
        A = self.total_absorption(frequency)
        V = Decimal(self.volume)

        if A == 0:
            return Decimal("0.0")

        return Decimal("0.161") * V / A

    def save_calculation(self, frequency: str):
        rt = self.sabine_reverberation_time(frequency)
        is_within = self.check_if_within_norm(rt)
        return Calculation.objects.create(
            reverberation_time=rt, norm=self.norm, is_within_norm=is_within
        )

    def check_if_within_norm(self, rt: Decimal) -> bool:
        return Decimal("0.3") <= rt <= Decimal("1.2")
