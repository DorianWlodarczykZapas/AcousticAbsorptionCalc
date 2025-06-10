from datetime import timedelta
from http import HTTPStatus

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

from .models import Plan, User, UserPlan


class PlanListView(ListView):
    model = Plan
    template_name = "plans/plan_list.html"
    context_object_name = "plans"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            has_trial = UserPlan.objects.filter(
                user=self.request.user, is_active=True, plan__type=Plan.PlanType.TRIAL
            ).exists()

            if has_trial:
                queryset = queryset.exclude(type=Plan.PlanType.TRIAL)

        queryset = queryset.exclude(type=Plan.PlanType.BASE)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["user_plan"] = (
                UserPlan.objects.select_related("plan")
                .filter(user=self.request.user, is_active=True)
                .first()
            )

        return context


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

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session.get("customer_email")
            plan_id = session.get("metadata", {}).get("plan_id")

            try:
                user = User.objects.get(email=customer_email)
                plan = get_object_or_404(Plan, id=plan_id)

                user_plan, created = UserPlan.objects.get_or_create(user=user)

                if user_plan.plan.type == Plan.PlanType.TRIAL:
                    user_plan.is_trial = False
                    user_plan.trial_days = None

                user_plan.plan = plan
                user_plan.start_date = timezone.now().date()
                user_plan.valid_to = timezone.now().date() + timedelta(days=30)
                user_plan.is_active = True
                user_plan.last_payment_date = timezone.now().date()
                user_plan.next_payment_date = timezone.now().date() + timedelta(days=30)
                user_plan.save()

            except User.DoesNotExist:
                pass

        return HttpResponse(status=HTTPStatus.OK)


class PaymentSuccessView(TemplateView):
    template_name = "plans/success_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get("session_id")

        if session_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(session_id)
            customer_email = session.get("customer_email")
            plan_id = session.get("metadata", {}).get("plan_id")

            context["customer_email"] = customer_email
            context["plan_name"] = None
            context["valid_to"] = None

            from plans.models import Plan, User, UserPlan

            try:
                user = User.objects.get(email=customer_email)
                plan = Plan.objects.get(id=plan_id)
                user_plan = UserPlan.objects.get(user=user, plan=plan, is_active=True)

                context["plan_name"] = plan.name
                context["valid_to"] = user_plan.valid_to
            except (User.DoesNotExist, Plan.DoesNotExist, UserPlan.DoesNotExist):
                pass

        return context


class PaymentCancelView(TemplateView):
    template_name = "plans/cancel.html"


class ChangePlanView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_plan = UserPlan.objects.filter(user=request.user, is_active=True).first()

        plans = Plan.objects.all()

        context = {
            "user_plan": user_plan,
            "plans": plans,
        }

        return render(request, "plans/change_plan.html", context)

    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get("plan_id")

        if not plan_id:
            messages.error(request, "Nie podano planu.")
            return redirect("plans:change")

        try:
            new_plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            messages.error(request, "Wybrany plan nie istnieje.")
            return redirect("plans:change")

        user_plan = UserPlan.objects.filter(user=request.user, is_active=True).first()

        if user_plan:
            user_plan.plan = new_plan
            user_plan.save()
            messages.success(request, "Your plan has been successfully updated.")

        return redirect("users:home")
