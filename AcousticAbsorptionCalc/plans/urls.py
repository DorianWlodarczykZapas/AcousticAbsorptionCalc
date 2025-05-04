from django.urls import path

from .views import PlanListView

app_name = "plans"

urlpatterns = [
    path("plans_list", PlanListView.as_view(), name="list"),
]
