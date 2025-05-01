from datetime import timedelta

from django.contrib import settings
from django.utils.timezone import now

from .models import Plan, UserPlan


class PlanService:
    @staticmethod
    def change_user_plan(
        user: settings.AUTH_USER_MODEL,
        new_plan_type: str,
    ) -> UserPlan:
        try:
            new_plan: Plan = Plan.objects.get(type=new_plan_type)
        except Plan.DoesNotExist:
            raise Exception(f"Plan '{new_plan_type}' does not exist.")

        user_plan, _ = UserPlan.objects.get_or_create(user=user)
        user_plan.plan = new_plan
        user_plan.is_trial = new_plan.type == Plan.PlanType.TRIAL
        user_plan.start_date = now().date()
        user_plan.valid_to = (
            None
            if new_plan.type != Plan.PlanType.TRIAL
            else now().date() + timedelta(days=7)
        )
        user_plan.save(updated_fields=["plan", "is_trail", "start_date", "valid_to"])
        return user_plan
