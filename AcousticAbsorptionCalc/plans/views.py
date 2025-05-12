from datetime import timedelta, timezone

import stripe
from core import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from plans.services import StripeService

from .models import Plan, User, UserPlan


class PlanListView(ListView):
    model = Plan
    template_name = "plans/plan_list.html"
    context_object_name = "plans"

    def get(self, request: HttpRequest, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateCheckoutSessionView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        plan_id = request.POST.get("plan_id")
        plan = get_object_or_404(Plan, id=plan_id)
        user_email = request.user.email

        stripe_service = StripeService()
        checkout_session = stripe_service.create_checkout_session(plan, user_email)

        return redirect(checkout_session.url)


class StripeWebhookView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session.get("customer_email")
            plan_id = session.get("metadata", {}).get("plan_id")

            try:
                user = User.objects.get(email=customer_email)
                plan = get_object_or_404(Plan, id=plan_id)

                UserPlan.objects.update_or_create(
                    user=user,
                    defaults={
                        "plan": plan,
                        "start_date": timezone.now().date(),
                        "valid_to": timezone.now().date() + timedelta(days=30),
                        "is_active": True,
                        "last_payment_date": timezone.now().date(),
                        "next_payment_date": timezone.now().date() + timedelta(days=30),
                    },
                )
            except User.DoesNotExist:
                pass

        return HttpResponse(status=200)


class PaymentSuccessView(TemplateView):
    template_name = "templates/plans/success_payment.html"


class PaymentCancelView(TemplateView):
    template_name = "templates/plans/cancel.html"
