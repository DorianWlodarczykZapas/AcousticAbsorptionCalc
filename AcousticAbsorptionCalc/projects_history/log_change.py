from functools import wraps
from django.utils import timezone
from .models import ChangeLog


def log_change(entity_type: str, change_type: str):
    """
    Decorator that logs a change in the system by creating a ChangeLog entry.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            user_id = kwargs.get("user_id") or (args[0] if len(args) > 0 else None)
            changed_by = kwargs.get("changed_by") or (args[1] if len(args) > 1 else None)

            if user_id and changed_by:
                ChangeLog.objects.create(
                    entity_type=entity_type,
                    entity_id=user_id,
                    changed_by=changed_by,
                    change_type=change_type,
                    timestamp=timezone.now(),
                )

            return result

        return wrapper

    return decorator
