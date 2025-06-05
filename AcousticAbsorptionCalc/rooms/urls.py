from django.urls import path

from .views import RoomCreateView, RoomDeleteView, RoomListView

app_name = "rooms"

urlpatterns = [
    path("", RoomListView.as_view(), name="room_list"),
    path("<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
    path("create/", RoomCreateView.as_view(), name="room_create"),
]
