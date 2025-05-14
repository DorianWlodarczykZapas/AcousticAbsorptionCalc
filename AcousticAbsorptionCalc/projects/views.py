from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from project_logs.projectlogger import ProjectLogger
from projects.forms import ProjectForm
from projects.services import PDFGeneratorService
from user_logs.logger import Logger

from .models import Project
from .permissions import can_edit_project, can_view_project
from .project_services import ProjectService


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = "projects/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("projects:project_list")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]

        project = ProjectService.create_project(
            user=self.request.user, name=name, description=description
        )

        Logger.log_project_created(user_id=project.pk, changed_by=self.request.user)

        ProjectLogger.log_created(
            project=project,
            changed_by=self.request.user,
            change_description="Project created via form",
        )

        return redirect(self.get_success_url())


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")

    def test_func(self):
        project = self.get_object()
        return can_edit_project(self.request.user, project)

    def form_valid(self, form):
        old_instance = self.get_object()
        response = super().form_valid(form)

        Logger.log_project_updated(user_id=self.object.pk, changed_by=self.request.user)

        metadata = {}
        for field in form.changed_data:
            metadata[field] = {
                "old": getattr(old_instance, field),
                "new": form.cleaned_data.get(field),
            }

        ProjectLogger.log_edit_dimensions(
            project=self.object,
            changed_by=self.request.user,
            change_description="Project fields updated",
            metadata=metadata,
        )

        return response


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project_list")

    def test_func(self):
        project = self.get_object()
        return can_edit_project(self.request.user, project)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        Logger.log_project_deleted(user_id=self.object.pk, changed_by=request.user)

        ProjectLogger.log_deleted(
            project=self.object,
            changed_by=request.user,
            change_description="Project deleted by user",
        )

        return super().delete(request, *args, **kwargs)


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/projects_list.html"
    context_object_name = "projects"

    def get_queryset(self) -> QuerySet[Project]:
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset

        return queryset.filter(
            Q(user=user) | Q(sharedproject__shared_with_user=user)
        ).distinct()


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def test_func(self):
        project = self.get_object()
        return can_view_project(self.request.user, project)


class ProjectPDFView(View):
    def get(self, request, project_id):
        try:
            project = Project.objects.prefetch_related("rooms").get(id=project_id)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")

        Logger.log_project_updated(user_id=project.pk, changed_by=request.user)

        ProjectLogger.log_downloaded(
            project=project,
            changed_by=request.user,
            change_description="Project PDF downloaded",
        )

        context = {
            "project": project,
            "rooms": project.rooms.all(),
        }

        pdf_content = PDFGeneratorService.generate_project_pdf(context)

        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="project_{project.id}.pdf"'
        return response
