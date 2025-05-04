from django.urls import path

from .views import PlanListView, StripeWebhookView

app_name = "plans"

urlpatterns = [
    path("plans_list", PlanListView.as_view(), name="list"),
    path("payment/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
]
