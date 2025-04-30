from django.urls import path

from .views import UserChangeLogListView

urlpatterns = [
    path("my_logs/", UserChangeLogListView.as_view(), name="user-logs"),
]
