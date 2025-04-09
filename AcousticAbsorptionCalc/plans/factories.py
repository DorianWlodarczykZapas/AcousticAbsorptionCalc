import factory
from factory.django import DjangoModelFactory

from .models import Plan


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
