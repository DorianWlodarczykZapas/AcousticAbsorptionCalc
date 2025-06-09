from calculations.models import Material, Norm
from django.db import models
from django.utils.translation import gettext_lazy as _
from projects.models import Project


class Room(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    norm = models.ForeignKey(Norm, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RoomMaterial(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)


class Furnishing(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="furnishings")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)


class RoomSurface(models.Model):
    SURFACE_TYPE_CHOICES = [
        ("floor", _("Floor")),
        ("ceiling", _("Ceiling")),
        ("wall_a", _("Front Wall")),
        ("wall_b", _("Back Wall")),
        ("wall_c", _("Left Wall")),
        ("wall_d", _("Right Wall")),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="surfaces")
    surface_type = models.CharField(max_length=50, choices=SURFACE_TYPE_CHOICES)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.get_surface_type_display()} – {self.material.name} ({self.area} m²)"
        )
