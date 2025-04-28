from django.urls import path

from .views import ProjectCreateView, ProjectPDFView

urlpatterns = [
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path(
        "projects/<int:project_id>/pdf/", ProjectPDFView.as_view(), name="project_pdf"
    ),
]
