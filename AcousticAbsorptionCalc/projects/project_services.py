from projects.models import Project


class ProjectService:
    @staticmethod
    def create_project(user, name, description):
        project = Project.objects.create(user=user, name=name, description=description)
        return project
