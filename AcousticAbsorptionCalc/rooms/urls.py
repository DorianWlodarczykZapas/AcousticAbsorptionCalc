from django.urls import path
from .views import RoomListView, RoomCreateView

app_name = "rooms"

urlpatterns = [
    path('project/<int:project_id>/rooms/', RoomListView.as_view(), name='room_list'),
    path('project/<int:project_id>/rooms/new/', RoomCreateView.as_view(), name='room_create'),
]
