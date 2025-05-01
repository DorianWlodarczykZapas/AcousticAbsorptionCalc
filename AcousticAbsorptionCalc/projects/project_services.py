from django.conf import settings
from projects.models import Project


class ProjectService:
    @staticmethod
    def create_project(
        user: settings.AUTH_USER_MODEL, name: str, description: str
    ) -> Project:
        project = Project.objects.create(user=user, name=name, description=description)
        return project
