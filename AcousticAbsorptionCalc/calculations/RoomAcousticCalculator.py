from decimal import Decimal

from .models import Material, Norm, NormAbsorptionMultiplier


class RoomAcousticCalculator:
    def __init__(self, height, length, width, furnishing, construction, norm: Norm):
        """
        furnishing: dict {material_name: area_in_m2}
        construction: dict {material_name: area_in_m2}
        """
        self.height = height
        self.length = length
        self.width = width
        self.furnishing = furnishing
        self.construction = construction
        self.norm = norm

    def volume(self):
        return self.height * self.length * self.width

    def get_absorption_coefficient(self, material: Material, frequency: str) -> Decimal:
        return getattr(material, frequency)

    def get_absorption_multiplier(self) -> Decimal:
        try:
            multiplier = NormAbsorptionMultiplier.objects.get(norm=self.norm)
            return multiplier.absorption_multiplier
        except NormAbsorptionMultiplier.DoesNotExist:
            return Decimal("1.0")
