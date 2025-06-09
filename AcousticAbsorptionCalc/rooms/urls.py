from django.urls import path

from .views import (
    RoomCalculationSummaryView,
    RoomCreateView,
    RoomDeleteView,
    RoomListView,
    RoomUpdateView,
)

app_name = "rooms"

urlpatterns = [
    path("", RoomListView.as_view(), name="room_list"),
    path("<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
    path("create/", RoomCreateView.as_view(), name="room_create"),
    path("<int:pk>/edit/", RoomUpdateView.as_view(), name="room_edit"),
    path(
        "rooms/<int:pk>/summary/",
        RoomCalculationSummaryView.as_view(),
        name="room_summary",
    ),
]
