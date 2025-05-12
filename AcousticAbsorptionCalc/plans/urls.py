from django.urls import path

from .views import (
    CreateCheckoutSessionView,
    PaymentCancelView,
    PaymentSuccessView,
    PlanListView,
    StripeWebhookView,
)

app_name = "plans"

urlpatterns = [
    path("plans/", PlanListView.as_view(), name="plan_list"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("payment/success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payment/cancel/", PaymentCancelView.as_view(), name="payment_cancel"),
]
