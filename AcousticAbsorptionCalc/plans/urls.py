from django.urls import path
from .views import PlanListView, PlanChangeView

app_name = "plans"

urlpatterns = [
    path("", PlanListView.as_view(), name="list"),
    path("change/", PlanChangeView.as_view(), name="change"),
]
