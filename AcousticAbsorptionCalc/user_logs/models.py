from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class ChangeLog(models.Model):
    class EntityType(models.IntegerChoices):
        USER = 1, _("User")
        PROJECT = 2, _("Project")
        DOCUMENT = 3, _("Document")
        TAG = 4, _("Tag")

    class ChangeType(models.IntegerChoices):
        CREATE = 1, _("Created")
        UPDATE = 2, _("Updated")
        DELETE = 3, _("Deleted")
        LOGIN = 4, _("Login")
        LOGOUT = 5, _("Logout")
        VIEW = 6, _("View")
        ACTION = 7, _("Other action")

    entity_type = models.IntegerField(
        choices=EntityType.choices,
        help_text=_("The entity type to which the action applies"),
    )
    entity_id = models.IntegerField(
        help_text=_("ID of the entity (e.g., user.id, project.id)")
    )
    changed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text=_("The user who performed the action")
    )
    change_type = models.IntegerField(
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
