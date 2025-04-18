from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from services import PlanService

from .models import Plan


class PlanListView(ListView):
    model = Plan
    template_name = "plans/plan_list.html"
    context_object_name = "plans"


class PlanChangeView(View):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        plan_type = request.POST.get("plan_type")
        try:
            PlanService.change_user_plan(request.user, plan_type)
            messages.success(request, f"Zmieniono plan na {plan_type}.")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("plans:list")
