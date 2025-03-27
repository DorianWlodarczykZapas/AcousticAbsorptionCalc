from django.utils import timezone
from users.models import User

from .models import ChangeLog


class Logger:
    @staticmethod
    def log_account_creation(user_id: int, changed_by: User):
        try:
            user = User.objects.get(pk=user_id)

            ChangeLog.objects.create(
                entity_type="konto",
                entity_id=user.id,
                changed_by=changed_by,
                change_type="Utworzono konto",
                timestamp=timezone.now(),
            )
        except User.DoesNotExist:
            print(f"User with id {user_id} does not exist.")
