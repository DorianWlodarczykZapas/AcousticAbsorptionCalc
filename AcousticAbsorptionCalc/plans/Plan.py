from datetime import date, timedelta
from django.utils import timezone
from .models import Plan, UserPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class PlanManager:
    @staticmethod
    def assign_plan_to_user(self):
        return True

    @staticmethod
    def change_user_plan(self):
        return False

    @staticmethod
    def deactivate_user_plan(self):
       return True

    @staticmethod
    def is_plan_active(self):
        return True
