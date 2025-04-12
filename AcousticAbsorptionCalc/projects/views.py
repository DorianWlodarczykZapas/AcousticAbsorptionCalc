from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from projects.forms import ProjectForm
from projects.project_services import ProjectService

from .models import Project
from .permissions import can_edit_project, can_view_project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = "projects/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("projects:project_list")

    def form_valid(self, form):
        ProjectService.create_project(
            user=self.request.user,
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
        )
        return super().form_valid(form)

    # def form_valid(self, form):
    #     form.instance.useer = self.request.user
    #     reutrn super()...


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")

    def test_func(self):
        project = self.get_object()
        return can_edit_project(self.request.user, project)


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project_list")

    def test_func(self):
        project = self.get_object()
        return can_edit_project(self.request.user, project)


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        user = self.request.user
        own_projects = Project.objects.filter(user=user)
        shared_projects = Project.objects.filter(sharedproject__shared_with_user=user)
        if user.is_staff:
            return Project.objects.all()
        return own_projects.union(shared_projects)


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def test_func(self):
        project = self.get_object()
        return can_view_project(self.request.user, project)
