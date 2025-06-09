from django.urls import path

from .views import RoomAcousticCalculationView

urlpatterns = [
    path(
        "api/room-acoustic-calculate/",
        RoomAcousticCalculationView.as_view(),
        name="room_acoustic_calculate",
    ),
]
