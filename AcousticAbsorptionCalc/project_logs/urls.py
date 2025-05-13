from django.urls import path

from .views import ProjectChangeLogView

urlpatterns = [
    path(
        "project/<int:project_id>/change-log/",
        ProjectChangeLogView.as_view(),
        name="project_change_log",
    ),
]
