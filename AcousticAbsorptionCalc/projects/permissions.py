from projects.models import SharedProject


def can_view_project(user, project):
    return (
        project.user == user
        or user.is_staff
        or SharedProject.objects.filter(project=project, shared_with_user=user).exists()
    )


def can_edit_project(user, project):
    return (
        project.user == user
        or user.is_staff
        or SharedProject.objects.filter(
            project=project, shared_with_user=user, access_level="edit"
        ).exists()
    )
