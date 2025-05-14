from django.db import models
from users.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    active_version = models.ForeignKey(
        "ProjectVersion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")


class SharedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    shared_with_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50)


class ProjectNote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectVersion(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="versions"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "name")

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    def set_active(self):
        ProjectVersion.objects.filter(project=self.project).update(is_active=False)

        self.is_active = True
        self.save()

        self.project.active_version = self
        self.project.save(update_fields=["active_version"])


class ProjectVersionChange(models.Model):
    class EntityType(models.IntegerChoices):
        ROOM = 1, "Room"
        MATERIAL = 2, "Material"
        FURNISHING = 3, "Furnishing"
        OTHER = 4, "Other"

    class ChangeType(models.IntegerChoices):
        CREATE = 1, "Created"
        UPDATE = 2, "Updated"
        DELETE = 3, "Deleted"

    project_version = models.ForeignKey(
        "projects.ProjectVersion", on_delete=models.CASCADE, related_name="changes"
    )
    entity_type = models.IntegerField(choices=EntityType.choices)
    entity_id = models.IntegerField(null=True, blank=True)
    change_type = models.IntegerField(choices=ChangeType.choices)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_change_type_display()} {self.get_entity_type_display()} (ID: {self.entity_id})"
