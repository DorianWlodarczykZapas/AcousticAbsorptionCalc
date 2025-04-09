from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from .models import Plan, UserPlan


class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Faker("word")
    type = factory.Iterator(
        [Plan.PlanType.BASE, Plan.PlanType.PREMIUM, Plan.PlanType.TRIAL]
    )
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    billing_period = factory.Iterator(["monthly", "yearly"])
    max_projects = factory.Faker("random_int", min=1, max=10)
    max_rooms_per_project = factory.Faker("random_int", min=1, max=20)
    advanced_features_enabled = factory.Faker("boolean")


class UserPlanFactory(DjangoModelFactory):
    class Meta:
        model = UserPlan

    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)
    start_date = factory.LazyFunction(timezone.now)
    valid_to = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=30))
    is_active = True
    last_payment_date = factory.LazyAttribute(lambda o: o.start_date)
    next_payment_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=30)
    )
    is_trial = factory.LazyAttribute(lambda o: o.plan.type == Plan.PlanType.TRIAL)
    trial_days = factory.LazyAttribute(lambda o: 14 if o.is_trial else None)
