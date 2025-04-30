from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class ChangeLog(models.Model):
    class EntityType(models.TextChoices):
        USER = "user", _("User")
        PROJECT = "project", _("Project")
        DOCUMENT = "document", _("Document")
        TAG = "tag", _("Tag")

    class ChangeType(models.TextChoices):
        CREATE = "create", _("Created")
        UPDATE = "update", _("Updated")
        DELETE = "delete", _("Deleted")
        LOGIN = "login", _("Login")
        LOGOUT = "logout", _("Logout")
        VIEW = "view", _("View")
        ACTION = "action", _("Other action")

    entity_type = models.CharField(
        max_length=100,
        choices=EntityType.choices,
        help_text=_("The entity type to which the action applies"),
    )
    entity_id = models.IntegerField(
        help_text=_("ID of the entity (e.g., user.id, project.id)")
    )
    changed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text=_("The user who performed the action")
    )
    change_type = models.CharField(
        max_length=50,
        choices=ChangeType.choices,
        help_text=_("The type of change or action"),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text=_("Additional contextual data – e.g., IP, device info, payload"),
    )

    def __str__(self):
        return f"{self.get_change_type_display()} – {self.get_entity_type_display()} [{self.entity_id}] by {self.changed_by}"
