from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Plan(models.Model):
    class PlanType(models.IntegerChoices):
        BASE = 1, "Base"
        PREMIUM = 2, "Premium"
        TRIAL = 3, "Trial"

    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=PlanType.choices, default=PlanType.BASE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period = models.CharField(max_length=50)
    max_projects = models.IntegerField()
    max_rooms_per_project = models.IntegerField()
    advanced_features_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    last_payment_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField(null=True, blank=True)
    is_trial = models.BooleanField(default=False)
    trial_days = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
