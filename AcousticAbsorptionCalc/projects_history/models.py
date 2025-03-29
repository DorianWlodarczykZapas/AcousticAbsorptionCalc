from django.db import models
from users.models import User


class ChangeLog(models.Model):
    class EntityType(models.TextChoices):
        USER = "user", "Użytkownik"
        PROJECT = "project", "Projekt"
        DOCUMENT = "document", "Dokument"
        TAG = "tag", "Tag"

    class ChangeType(models.TextChoices):
        CREATE = "create", "Utworzono"
        UPDATE = "update", "Zmieniono"
        DELETE = "delete", "Usunięto"
        LOGIN = "login", "Logowanie"
        LOGOUT = "logout", "Wylogowanie"
        VIEW = "view", "Podgląd"
        ACTION = "action", "Inna akcja"

    entity_type = models.CharField(
        max_length=100,
        choices=EntityType.choices,
        help_text="Typ obiektu, którego dotyczy akcja"
    )
    entity_id = models.IntegerField(
        help_text="ID obiektu (np. user.id, project.id)"
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Użytkownik, który wykonał akcję"
    )
    change_type = models.CharField(
        max_length=50,
        choices=ChangeType.choices,
        help_text="Typ zmiany lub akcji"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Dodatkowe dane kontekstowe – np. IP, device info, payload"
    )

    def __str__(self):
        return f"{self.get_change_type_display()} – {self.entity_type} [{self.entity_id}] przez {self.changed_by}"
