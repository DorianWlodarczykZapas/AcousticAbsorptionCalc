from calculations.guidelines import NORM_GUIDELINES
from django.db import models
from django.utils.text import slugify


class NormCalculationType(models.TextChoices):
    HEIGHT = "1", "Height-dependent"
    NONE = "2", "No dependency"
    VOLUME = "3", "Volume-dependent"
    STI = "4", "Speech Transmission Index"


class Norm(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    application_type = models.CharField(
        max_length=2,
        choices=NormCalculationType.choices,
        default=NormCalculationType.NONE,
    )

    rt_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum allowed reverberation time in seconds (T ≤ ...)",
    )

    sti_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum allowed STI value (STI ≥ ...)",
    )

    absorption_min_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum required sound absorption as a factor of surface area (A ≥ x × S)",
    )

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_guidelines(self):
        return NORM_GUIDELINES.get(self.slug, "")

    def __str__(self):
        return self.name


class SurfaceElement(models.Model):
    calculation = models.ForeignKey(
        "Calculation", on_delete=models.CASCADE, related_name="surfaces"
    )
    material = models.ForeignKey("Material", on_delete=models.PROTECT)
    area_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Surface area of the element in m²"
    )
    location = models.CharField(
        max_length=100,
        help_text="Where this surface is located (e.g., ceiling, wall A)",
    )

    def absorption(self, freq_band: str = "_500"):
        """
        Returns absorption in sabins for a given frequency band.
        """
        alpha = getattr(self.material, freq_band)
        return float(alpha) * float(self.area_m2)

    def __str__(self):
        return f"{self.location} – {self.material.name} ({self.area_m2} m²)"


class Calculation(models.Model):
    norm = models.ForeignKey("Norm", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    room_height = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    room_volume = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    room_surface_area = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    reverberation_time = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sti = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    required_absorption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    achieved_absorption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_within_norm = models.BooleanField(null=True)

    def check_absorption(self, freq_band: str = "_500") -> bool:
        """
        Calculates total absorption and compares it to required norm absorption.
        Returns True if within norm, False otherwise.
        """
        total_absorption = sum(
            [surface.absorption(freq_band) for surface in self.surfaces.all()]
        )
        self.achieved_absorption = total_absorption

        if self.norm and self.norm.absorption_min_factor and self.room_surface_area:
            self.required_absorption = float(self.norm.absorption_min_factor) * float(
                self.room_surface_area
            )
            self.is_within_norm = total_absorption >= self.required_absorption
            self.save(
                update_fields=[
                    "achieved_absorption",
                    "required_absorption",
                    "is_within_norm",
                ]
            )
            return self.is_within_norm
        return False

    def __str__(self):
        return f"Calculation ({self.created_at.date()}) – Norm: {self.norm.name}"


class Material(models.Model):
    type = models.CharField(
        max_length=100,
        help_text="Material category (e.g., ceiling panel, wall absorber)",
    )
    name = models.CharField(max_length=100, unique=True)

    freq_125 = models.DecimalField(max_digits=4, decimal_places=2)
    freq_250 = models.DecimalField(max_digits=4, decimal_places=2)
    freq_500 = models.DecimalField(max_digits=4, decimal_places=2)
    freq_1000 = models.DecimalField(max_digits=4, decimal_places=2)
    freq_2000 = models.DecimalField(max_digits=4, decimal_places=2)
    freq_4000 = models.DecimalField(max_digits=4, decimal_places=2)

    def get_alpha(self, freq_band: str) -> float:
        """
        Returns the absorption coefficient for the given frequency band.
        freq_band should be one of: '125', '250', '500', '1000', '2000', '4000'
        """
        band_field = f"freq_{freq_band}"
        return float(getattr(self, band_field, 0))

    def __str__(self) -> str:
        return f"{self.type} – {self.name}"


class NormRequirement(models.Model):
    norm = models.ForeignKey(
        "Norm", on_delete=models.CASCADE, related_name="requirements"
    )
    volume_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum room volume in m³ (optional)",
    )
    volume_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum room volume in m³ (optional)",
    )
    height_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum room height in meters (optional)",
    )
    height_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum room height in meters (optional)",
    )
    rt_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum reverberation time T in seconds (optional)",
    )
    sti_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum speech transmission index STI (optional)",
    )
    absorption_min_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum required sound absorption factor (optional, e.g. 0.6 × S)",
    )

    def __str__(self):
        range_desc = []
        if self.volume_min is not None and self.volume_max is not None:
            range_desc.append(f"V: {self.volume_min}–{self.volume_max} m³")
        if self.height_min is not None and self.height_max is not None:
            range_desc.append(f"H: {self.height_min}–{self.height_max} m")
        return f"Norm Requirement ({' | '.join(range_desc)})"
