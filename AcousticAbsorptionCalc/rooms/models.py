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
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="surfaces")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    surface_type = models.CharField(
        max_length=50,
        choices=[
            ("floor", "Floor"),
            ("ceiling", "Ceiling"),
            ("wall_a", "Wall A"),
            ("wall_b", "Wall B"),
            ("wall_c", "Wall C"),
            ("wall_d", "Wall D"),
        ],
    )
