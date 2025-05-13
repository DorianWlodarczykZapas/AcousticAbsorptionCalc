from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from projects.models import Project

from .models import ProjectChangeLog


class ProjectChangeLogView(LoginRequiredMixin, ListView):
    model = ProjectChangeLog
    template_name = "project_logs/change_log_list.html"
    context_object_name = "changes"

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return ProjectChangeLog.objects.filter(project_id=project_id).order_by(
            "-timestamp"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        context["project"] = project
        return context
