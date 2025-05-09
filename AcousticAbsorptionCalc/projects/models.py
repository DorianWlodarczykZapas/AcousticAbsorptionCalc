from django.db import models
from users.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "name",
        )


class SharedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    shared_with_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50)


class ProjectNote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
