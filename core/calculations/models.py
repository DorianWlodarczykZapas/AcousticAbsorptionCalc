from django.db import models


class Material(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    _120 = models.DecimalField(max_digits=22, decimal_places=2)
    _250 = models.DecimalField(max_digits=22, decimal_places=2)
    _500 = models.DecimalField(max_digits=22, decimal_places=2)
    _1000 = models.DecimalField(max_digits=22, decimal_places=2)
    _2000 = models.DecimalField(max_digits=22, decimal_places=2)
    _4000 = models.DecimalField(max_digits=22, decimal_places=2)


class Norm(models.Model):
    name = models.TextField()


