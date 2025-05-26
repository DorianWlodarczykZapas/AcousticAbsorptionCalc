from datetime import timezone
from decimal import Decimal

import factory

from .models import (
    Calculation,
    Material,
    Norm,
    NormAbsorptionMultiplier,
    NormCalculationType,
    NormCategory,
)


class NormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Norm

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    application_type = NormCalculationType.NONE


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material

    type = factory.Faker("word")
    name = factory.Sequence(lambda n: f"Material-{n}")
    freq_125 = Decimal("0.50")
    freq_250 = Decimal("0.60")
    freq_500 = Decimal("0.70")
    freq_1000 = Decimal("0.80")
    freq_2000 = Decimal("0.90")
    freq_4000 = Decimal("1.00")


class NormAbsorptionMultiplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NormAbsorptionMultiplier

    norm = factory.SubFactory(NormFactory)
    multiplier = Decimal("1.0")
    category = NormCategory.NONE

    height_min = None
    height_max = None
    volume_min = None
    volume_max = None
    sti_min = None
    sti_max = None


class CalculationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Calculation

    reverberation_time = Decimal("1.23")
    norm = factory.SubFactory(NormFactory)
    is_within_norm = True
    created_at = factory.LazyFunction(timezone.now)
    room_height = Decimal("2.5")
    room_volume = Decimal("50.0")
    sti = Decimal("0.75")
