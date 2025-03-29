from users.models import User


class Logger:
    """Wrapper for user and system logging actions."""

    @staticmethod
    @log_change(entity_type="konto", change_type="Utworzono konto")
    def log_account_creation(user_id: int, changed_by: User) -> None:
        """
        Creates user and logs the action.
        """
        if not User.objects.filter(pk=user_id).exists():
            raise User.DoesNotExist(f"User with id {user_id} does not exist.")
