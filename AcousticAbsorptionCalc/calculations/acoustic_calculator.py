from typing import Dict, List, Tuple

from .models import Norm


class AcousticCalculator:
    """
    Handles all acoustic calculations for a single room, including:
    - Volume
    - Surface area
    - Absorption A
    - Reverberation Time (RT)
    - STI
    and comparison against building norms.
    """

    def __init__(
        self,
        norm: Norm,
        room_dimensions: Dict[str, float],
        construction_surfaces: List[Dict[str, object]],
        furnishing_elements: List[Dict[str, object]],
        freq_band: str = "500",
    ) -> None:
        """
        Initializes the calculator with input data.

        Args:
            norm: Norm instance from database
            room_dimensions: Dict with keys: 'width', 'length', 'height' (values in meters)
            construction_surfaces: List of {'area_m2': float, 'material': Material}
            furnishing_elements: List of {'area_m2': float, 'material': Material}
            freq_band: Frequency band as string, e.g. "500"
        """
        self.norm = norm
        self.freq_band = freq_band

        self.width: float = room_dimensions["width"]
        self.length: float = room_dimensions["length"]
        self.height: float = room_dimensions["height"]

        self.construction_surfaces: List[Dict[str, object]] = construction_surfaces
        self.furnishing_elements: List[Dict[str, object]] = furnishing_elements

        self.room_volume: float = 0.0
        self.room_surface_area: float = 0.0

    def calculate_room_geometry(self) -> Tuple[float, float]:
        """
        Calculates and stores the room's volume (m³) and total interior surface area (m²),
        including ceiling, floor, and four walls.

        Returns:
            (volume_m3, surface_area_m2)
        """
        width = self.width
        length = self.length
        height = self.height

        volume = width * length * height

        wall_area = 2 * height * (width + length)
        floor_ceiling_area = 2 * (width * length)
        surface_area = wall_area + floor_ceiling_area

        self.room_volume = volume
        self.room_surface_area = surface_area

        return volume, surface_area

    def calculate_absorption(self) -> float:
        """
        Calculates the total sound absorption A [m²] in the specified frequency band.
        Based on all construction and furnishing surfaces.

        Returns:
            Total absorption (A) in sabins.
        """
        total_absorption = 0.0

        for element in self.construction_surfaces + self.furnishing_elements:
            material = element["material"]
            area = float(element["area_m2"])
            alpha = material.get_alpha(self.freq_band)

            total_absorption += alpha * area

        return round(total_absorption, 3)

    def calculate_rt(self) -> float:
        """
        Calculates the reverberation time (RT60) in seconds
        using the Sabine formula: T = 0.161 * V / A.

        Returns:
            RT60 value in seconds.
        """
        if self.room_volume == 0 or self.room_surface_area == 0:
            self.calculate_room_geometry()

        absorption = self.calculate_absorption()

        if absorption > 0:
            rt = 0.161 * self.room_volume / absorption
            return round(rt, 3)

        return 0.0
