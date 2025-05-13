from django.db import models
from django.utils import timezone
from projects.models import Project
from users.models import User


class ProjectChangeLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=50)
    change_description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.change_type} – {self.project.name} by {self.changed_by.username}"

    class Meta:
        verbose_name = "Project Change Log"
        verbose_name_plural = "Project Change Logs"
