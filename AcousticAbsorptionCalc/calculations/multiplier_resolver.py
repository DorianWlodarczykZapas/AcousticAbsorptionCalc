# multiplier_resolver.py
from decimal import Decimal

from .models import Norm, NormAbsorptionMultiplier, NormCategory


class AbsorptionMultiplierResolver:
    def __init__(
        self, norm: Norm, height: float, volume: float, sti: float | None = None
    ):
        self.norm = norm
        self.height = height
        self.volume = volume
        self.sti = sti

    def resolve(self) -> Decimal:
        multipliers = NormAbsorptionMultiplier.objects.filter(norm=self.norm)

        for m in multipliers:
            if m.category == NormCategory.HEIGHT:
                if (m.height_min is None or self.height >= m.height_min) and (
                    m.height_max is None or self.height <= m.height_max
                ):
                    return m.absorption_multiplier

            elif m.category == NormCategory.VOLUME:
                if (m.volume_min is None or self.volume >= m.volume_min) and (
                    m.volume_max is None or self.volume <= m.volume_max
                ):
                    return m.absorption_multiplier

            elif m.category == NormCategory.STI and self.sti is not None:
                if (m.sti_min is None or self.sti >= m.sti_min) and (
                    m.sti_max is None or self.sti <= m.sti_max
                ):
                    return m.absorption_multiplier

            elif m.category == NormCategory.NONE:
                return m.absorption_multiplier

        return Decimal("1.0")
