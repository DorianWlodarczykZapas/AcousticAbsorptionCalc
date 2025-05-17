from datetime import timedelta

import stripe
from core import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from plans.services import StripeService
from pyexpat.errors import messages
from status import HTTPStatus

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
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=webhook_secret
            )
        except ValueError:
            return HttpResponse("Invalid payload", status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse("Invalid signature", status=400)

        if event["type"] == "invoice.payment_succeeded":

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

        return HttpResponse(status=HTTPStatus.OK)


class PaymentSuccessView(TemplateView):
    template_name = "templates/plans/success_payment.html"


class PaymentCancelView(TemplateView):
    template_name = "templates/plans/cancel.html"


class ChangePlanView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):  # is_staff -> wszystkie plany.
        user_plan = UserPlan.objects.filter(user=request.user, is_active=True).first()

        plans = Plan.objects.all()

        context = {
            "user_plan": user_plan,
            "plans": plans,
        }

        return render(request, "plans/change_plan.html", context)

    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get("plan_id")
        new_plan = Plan.objects.get(id=plan_id)  # wyjatek - moze nie byc planu.
        user_plan = UserPlan.objects.filter(user=request.user, is_active=True).first()

        if user_plan:
            user_plan.plan = new_plan
            user_plan.save()
            messages.success(request, "Your plan has been successfully updated.")

        return redirect("users:home")
