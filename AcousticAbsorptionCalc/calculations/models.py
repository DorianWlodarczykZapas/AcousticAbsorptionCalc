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
