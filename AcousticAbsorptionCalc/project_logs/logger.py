from functools import wraps
from typing import Callable

from .models import ProjectChangeLog


def log_project_change(entity_type: str, change_type: str) -> Callable:
    """
    Decorator for logging project changes.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            project = kwargs.get("project") or (args[0] if len(args) > 0 else None)
            changed_by = kwargs.get("changed_by") or (
                args[1] if len(args) > 1 else None
            )
            change_description = kwargs.get("change_description", "")

            if project and changed_by:
                ProjectChangeLog.objects.create(
                    project=project,
                    changed_by=changed_by,
                    change_type=change_type,
                    change_description=change_description,
                )

            return result

        return wrapper

    return decorator
