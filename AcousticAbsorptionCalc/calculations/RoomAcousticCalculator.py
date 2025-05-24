from decimal import Decimal
from typing import Dict

from .models import Calculation, Norm
from .multiplier_resolver import AbsorptionMultiplierResolver
from .norm_checker import NormComplianceChecker
from .sabine_calculator import ReverberationCalculator


class RoomAcousticCalculator:
    def __init__(
        self,
        height: float,
        length: float,
        width: float,
        furnishing: Dict[str, float],
        construction: Dict[str, float],
        norm: Norm,
        sti: float | None = None,
    ):
        self.height = height
        self.length = length
        self.width = width
        self.furnishing = furnishing
        self.construction = construction
        self.norm = norm
        self.sti = sti

    def __str__(self):
        return f"RoomAcousticCalculator(volume={self.volume}, sti={self.sti})"

    @property
    def volume(self) -> float:
        return self.height * self.length * self.width

    @property
    def all_materials(self) -> Dict[str, float]:
        return {**self.furnishing, **self.construction}

    def calculate_rt_for(self, frequency: str) -> Decimal:
        multiplier = AbsorptionMultiplierResolver(
            self.norm, self.height, self.volume, self.sti
        ).resolve()

        calculator = ReverberationCalculator(
            self.all_materials, multiplier, self.volume
        )
        return calculator.compute_rt(frequency)

    def is_within_norm(self, rt: Decimal) -> bool:
        return NormComplianceChecker(
            self.norm, self.height, self.volume, self.sti
        ).is_within(rt)

    def calculate_all_frequencies(self) -> Dict[str, Decimal]:
        return {
            freq: self.calculate_rt_for(freq)
            for freq in ["_250", "_500", "_1000", "_2000", "_4000"]
        }

    def save_calculation(self, frequency: str) -> Calculation:
        rt = self.calculate_rt_for(frequency)
        within = self.is_within_norm(rt)
        return Calculation.objects.create(
            reverberation_time=rt,
            norm=self.norm,
            is_within_norm=within,
            room_height=self.height,
            room_volume=self.volume,
            sti=self.sti,
        )
