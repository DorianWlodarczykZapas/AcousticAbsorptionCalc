from decimal import Decimal

from .models import Material


class ReverberationCalculator:
    def __init__(self, materials: dict[str, float], multiplier: Decimal, volume: float):
        self.materials = materials
        self.multiplier = multiplier
        self.volume = Decimal(str(volume))

    def get_alpha(self, material: Material, frequency: str) -> Decimal:
        if not hasattr(material, frequency):
            raise ValueError(f"Material has no absorption value for {frequency}")
        return getattr(material, frequency)

    def total_absorption(self, frequency: str) -> Decimal:
        total = Decimal("0.0")
        for name, area in self.materials.items():
            try:
                mat = Material.objects.get(name=name)
                alpha = self.get_alpha(mat, frequency)
                total += Decimal(area) * alpha * self.multiplier
            except Material.DoesNotExist:
                continue
        return total

    def compute_rt(self, frequency: str) -> Decimal:
        A = self.total_absorption(frequency)
        if A == 0:
            return Decimal("0.0")
        return Decimal("0.161") * self.volume / A
