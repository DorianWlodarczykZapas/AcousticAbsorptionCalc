from django.urls import path

from .views import (
    PaymentCancelView,
    PaymentSuccessView,
    PlanListView,
    StripeWebhookView,
)

app_name = "plans"

urlpatterns = [
    path("plans_list", PlanListView.as_view(), name="list"),
    path("payment/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("payment/success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payment/cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
]
