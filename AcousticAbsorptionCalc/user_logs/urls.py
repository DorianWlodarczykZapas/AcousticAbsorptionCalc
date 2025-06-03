from django.urls import path

from .views import UserChangeLogListView

app_name = "user_logs"

urlpatterns = [
    path("my_logs/", UserChangeLogListView.as_view(), name="user-logs"),
]
