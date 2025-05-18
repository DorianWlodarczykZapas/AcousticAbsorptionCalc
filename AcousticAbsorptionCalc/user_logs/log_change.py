from functools import wraps
from typing import Any, Callable

from django.utils import timezone

from .models import ChangeLog


def log_change(
    entity_type: int, change_type: int
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that logs a change in the system by creating a ChangeLog entry.

    Args:
        entity_type (str): Type of entity being changed (e.g., "User", "Project").
        change_type (str): Description of the type of change (e.g., "update", "delete").

    Returns:
        Callable: A decorator that wraps the target function and logs the change.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            user_id = kwargs.get("user_id") or (args[0] if len(args) > 0 else None)
            changed_by = kwargs.get("changed_by") or (
                args[1] if len(args) > 1 else None
            )

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
