from django.db import models
from django.utils import timezone
from projects.models import Project
from users.models import User


class ProjectChangeLog(models.Model):
    class ChangeType(models.IntegerChoices):
        CREATED = 1, "Created"
        DELETED = 2, "Deleted"
        SHARED = 3, "Shared"
        DOWNLOADED = 4, "Downloaded"
        EDIT_DIMENSIONS = 5, "Edited Dimensions"
        EDIT_FURNISHING = 6, "Edited Furnishing"
        EDIT_STANDARD = 7, "Edited Standard"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.IntegerField(choices=ChangeType.choices)

    change_description = models.TextField(blank=True)

    metadata = models.JSONField(null=True, blank=True)

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_change_type_display()} – {self.project.name} by {self.changed_by.username}"

    class Meta:
        verbose_name = "Project Change Log"
        verbose_name_plural = "Project Change Logs"
        ordering = ["-timestamp"]
