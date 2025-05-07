from django.urls import path

from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectPDFView,
    ProjectUpdateView,
)

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path(
        "<int:project_id>/download-pdf/",
        ProjectPDFView.as_view(),
        name="project_pdf",
    ),
]
