from typing import Dict, List

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
