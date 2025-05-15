from django.urls import path

from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectPDFView,
    ProjectRoomCreateView,
    ProjectRoomDeleteView,
    ProjectRoomUpdateView,
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
    path(
        "projects/<int:project_id>/rooms/new/",
        ProjectRoomCreateView.as_view(),
        name="room_create",
    ),
    path(
        "projects/rooms/<int:pk>/edit/",
        ProjectRoomUpdateView.as_view(),
        name="room_edit",
    ),
    path(
        "projects/rooms/<int:pk>/delete/",
        ProjectRoomDeleteView.as_view(),
        name="room_delete",
    ),
]
