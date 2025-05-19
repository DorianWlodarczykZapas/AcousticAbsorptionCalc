from django.db import models


class Material(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    freq_120 = models.DecimalField(max_digits=22, decimal_places=2)
    _250 = models.DecimalField(max_digits=22, decimal_places=2)
    _500 = models.DecimalField(max_digits=22, decimal_places=2)
    _1000 = models.DecimalField(max_digits=22, decimal_places=2)
    _2000 = models.DecimalField(max_digits=22, decimal_places=2)
    _4000 = models.DecimalField(max_digits=22, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.name}"


class Norm(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class NormCategory(models.TextChoices):
    HEIGHT = "1", "Height-dependent"
    VOLUME = "2", "Volume-dependent"
    STI = "3", "Speech Transmission Index"
    NONE = "4", "No dependency"


class NormAbsorptionMultiplier(models.Model):
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE)
    absorption_multiplier = models.DecimalField(max_digits=22, decimal_places=2)


class Calculation(models.Model):
    reverberation_time = models.DecimalField(max_digits=10, decimal_places=2)
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE)
    is_within_norm = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
