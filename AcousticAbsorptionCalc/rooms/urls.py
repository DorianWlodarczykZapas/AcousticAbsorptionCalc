from django.urls import path

from .views import RoomDeleteView, RoomListView

app_name = "rooms"

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room_list"),
    path("rooms/<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
]
