from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from projects.models import SharedProject

if TYPE_CHECKING:
    from projects.models import Project


def can_view_project(user: User, project: "Project") -> bool:
    return (
        project.user == user
        or user.is_staff
        or SharedProject.objects.filter(project=project, shared_with_user=user).exists()
    )


def can_edit_project(user: User, project: "Project") -> bool:
    return (
        project.user == user
        or user.is_staff
        or SharedProject.objects.filter(
            project=project, shared_with_user=user, access_level="edit"
        ).exists()
    )
