from calculations.models import Material, Norm
from django.db import models
from projects.models import Project


class Room(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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
    SURFACE_TYPES = [
        (1, "Floor"),
        (2, "Ceiling"),
        (3, "Wall A"),
        (4, "Wall B"),
        (5, "Wall C"),
        (6, "Wall D"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="surfaces")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    area = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Area of material in m²"
    )
    surface_type = models.PositiveSmallIntegerField(choices=SURFACE_TYPES)

    def __str__(self):
        return (
            f"{self.get_surface_type_display()} – {self.material.name} ({self.area} m²)"
        )
