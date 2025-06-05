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

    def calculate_required_absorption(self) -> float:
        """
        Calculates the minimum required absorption (A) based on the norm:
        A_required = absorption_min_factor × surface_area

        Returns:
            Required absorption in m² sabins.
        """
        if self.room_surface_area == 0:
            self.calculate_room_geometry()

        factor = self.norm.absorption_min_factor

        if factor is not None:
            required = float(factor) * self.room_surface_area
            return round(required, 3)

        return 0.0

    def is_within_norm(self, estimated_sti: float = None) -> bool:
        """
        Checks whether the room meets the norm requirements for:
        - Absorption A
        - Reverberation Time (RT)
        - STI (estimated or provided)

        Returns:
            True if all applicable criteria are met, False otherwise.
        """
        a_actual = self.calculate_absorption()
        a_required = self.calculate_required_absorption()
        rt = self.calculate_rt()

        absorption_ok = a_actual >= a_required
        rt_ok = True
        sti_ok = True

        if self.norm.rt_max is not None:
            rt_ok = rt <= float(self.norm.rt_max)

        if self.norm.sti_min is not None:
            if estimated_sti is not None:
                sti_ok = estimated_sti >= float(self.norm.sti_min)
            else:
                estimated_sti = round(0.75 - rt * 0.2, 2)
                sti_ok = estimated_sti >= float(self.norm.sti_min)

        return absorption_ok and rt_ok and sti_ok

    def result(self) -> Dict[str, float | bool]:
        """
        Returns a complete summary of the acoustic evaluation.

        Returns:
            Dict with all calculated values and norm compliance flags.
        """
        volume, surface = self.calculate_room_geometry()
        a_actual = self.calculate_absorption()
        a_required = self.calculate_required_absorption()
        rt = self.calculate_rt()
        estimated_sti = round(0.75 - rt * 0.2, 2) if rt > 0 else 0.0
        within_norm = self.is_within_norm(estimated_sti)

        return {
            "volume_m3": round(volume, 2),
            "surface_area_m2": round(surface, 2),
            "absorption_achieved": round(a_actual, 2),
            "absorption_required": round(a_required, 2),
            "reverberation_time_s": round(rt, 2),
            "estimated_sti": estimated_sti,
            "norm_passed": within_norm,
        }

    def validate_surface_match(
        self, tolerance: float = 0.05
    ) -> Dict[str, float | bool]:
        """
        Validates whether the user-provided construction surface areas
        match the expected total surface area from geometry.

        Args:
            tolerance: Acceptable percentage deviation (e.g., 0.05 = 5%)

        Returns:
            Dict with keys:
            - 'valid' (bool)
            - 'expected_area' (float)
            - 'provided_area' (float)
            - 'difference' (float)
            - 'within_tolerance' (bool)
        """
        expected_area = self.calculate_room_geometry()[1]
        provided_area = sum(float(e["area_m2"]) for e in self.construction_surfaces)

        difference = abs(expected_area - provided_area)
        relative_diff = difference / expected_area if expected_area else 1.0
        within_tolerance = relative_diff <= tolerance

        return {
            "valid": within_tolerance,
            "expected_area": round(expected_area, 2),
            "provided_area": round(provided_area, 2),
            "difference": round(difference, 2),
            "within_tolerance": within_tolerance,
        }

    def find_applicable_requirement(self):
        """
        Finds the applicable NormRequirement based on room volume and height.
        """
        if self.room_volume == 0 or self.room_surface_area == 0:
            self.calculate_room_geometry()

        requirements = self.norm.requirements.all()

        for req in requirements:
            volume_ok = True
            height_ok = True

            if req.volume_min is not None and req.volume_max is not None:
                volume_ok = req.volume_min <= self.room_volume <= req.volume_max

            if req.height_min is not None and req.height_max is not None:
                height_ok = req.height_min <= self.height <= req.height_max

            if volume_ok and height_ok:
                return req

        return None
