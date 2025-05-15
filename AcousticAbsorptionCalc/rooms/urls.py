from django.urls import path

from .views import (
    ProjectRoomCreateView,
    ProjectRoomUpdateView,
    RoomDeleteView,
    RoomListView,
)

app_name = "rooms"

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room_list"),
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
    path("rooms/<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
]
