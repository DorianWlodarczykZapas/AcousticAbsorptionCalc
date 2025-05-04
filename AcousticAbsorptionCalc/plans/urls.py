from django.urls import path

from .views import PlanChangeView, PlanListView

app_name = "plans"

urlpatterns = [
    path("plans_list", PlanListView.as_view(), name="list"),
    path("change/", PlanChangeView.as_view(), name="change"),
]
