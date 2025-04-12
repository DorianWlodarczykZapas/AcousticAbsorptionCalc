from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from projects.forms import ProjectForm
from projects.project_services import ProjectService


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
