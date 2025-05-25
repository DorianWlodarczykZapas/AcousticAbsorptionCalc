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

    def __str__(self):
        return self.name
