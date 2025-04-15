from django.urls import path

from .views import RoomCreateView, RoomDeleteView, RoomListView, RoomUpdateView

app_name = "rooms"

urlpatterns = [
    path("project/<int:project_id>/rooms/", RoomListView.as_view(), name="room_list"),
    path(
        "project/<int:project_id>/rooms/new/",
        RoomCreateView.as_view(),
        name="room_create",
    ),
    path("rooms/<int:pk>/edit/", RoomUpdateView.as_view(), name="room_edit"),
    path("rooms/<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
]
