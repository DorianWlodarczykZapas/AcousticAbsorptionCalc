from functools import wraps
from typing import Any, Callable

from .models import ProjectChangeLog


def log_project_change(
    change_type: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for logging project-related changes.

    Args:
        change_type (int): One of ProjectChangeLog.ChangeType values.

    Returns:
        Callable: Decorator.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            project = kwargs.get("project") or (args[0] if len(args) > 0 else None)
            changed_by = kwargs.get("changed_by") or (
                args[1] if len(args) > 1 else None
            )
            change_description = kwargs.get("change_description", "")
            metadata = kwargs.get("metadata", None)

            if project and changed_by:
                ProjectChangeLog.objects.create(
                    project=project,
                    changed_by=changed_by,
                    change_type=change_type,
                    change_description=change_description,
                    metadata=metadata,
                )

            return result

        return wrapper

    return decorator
