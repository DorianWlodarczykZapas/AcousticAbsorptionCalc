from users.models import User

from .log_change import log_change


class Logger:
    """Wrapper for user and system logging actions."""

    @staticmethod
    @log_change(entity_type="konto", change_type="Utworzono konto")
    def log_account_creation(user_id: int, changed_by: User) -> None:
        """
        Logs the creation of a user account.

        Args:
            user_id (int): ID of the user whose account was created.
            changed_by (User): The user who performed the action.

        Raises:
            User.DoesNotExist: If the user with the given ID does not exist.
        """
        if not User.objects.filter(pk=user_id).exists():
            raise User.DoesNotExist(f"User with id {user_id} does not exist.")

    @staticmethod
    @log_change(entity_type="pomieszczenie", change_type="Dodano")
    def log_room_created(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(entity_type="pomieszczenie", change_type="Zaktualizowano")
    def log_room_updated(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(entity_type="pomieszczenie", change_type="Usunięto")
    def log_room_deleted(user_id: int, changed_by: User) -> None:
        pass

    @staticmethod
    @log_change(entity_type="projekt", change_type="Utworzono")
    def log_project_created(user_id: int, changed_by: User) -> None:
        pass
