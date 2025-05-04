from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from plans.services import StripeService

from .models import Plan


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
