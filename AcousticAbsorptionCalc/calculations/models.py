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


class Norm(models.Model):
    name = models.TextField()


class NormAbsorptionMultiplier(models.Model):
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE)
    absorption_multiplier = models.DecimalField(max_digits=22, decimal_places=2)


class Calculation(models.Model):
    reverberation_time = models.DecimalField(max_digits=10, decimal_places=2)
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE)
    is_within_norm = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
