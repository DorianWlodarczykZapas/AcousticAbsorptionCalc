from users.models import User

from .log_change import log_change
from .models import ChangeLog


class Logger:
    """Wrapper for user and system logging actions."""

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.USER, change_type=ChangeLog.ChangeType.CREATE
    )
    def log_account_creation(user_id: int, changed_by: User) -> None:
        if not User.objects.filter(pk=user_id).exists():
            raise User.DoesNotExist(f"User with id {user_id} does not exist.")

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.DOCUMENT,
        change_type=ChangeLog.ChangeType.CREATE,
    )
    def log_room_created(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.DOCUMENT,
        change_type=ChangeLog.ChangeType.UPDATE,
    )
    def log_room_updated(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.DOCUMENT,
        change_type=ChangeLog.ChangeType.DELETE,
    )
    def log_room_deleted(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.PROJECT,
        change_type=ChangeLog.ChangeType.CREATE,
    )
    def log_project_created(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.PROJECT,
        change_type=ChangeLog.ChangeType.UPDATE,
    )
    def log_project_updated(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(
        entity_type=ChangeLog.EntityType.PROJECT,
        change_type=ChangeLog.ChangeType.DELETE,
    )
    def log_project_deleted(user_id: int, changed_by: User) -> None:
        pass
