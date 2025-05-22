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
    name = factory.Faker("word")
    freq_120 = Decimal("0.5")
    _250 = Decimal("0.6")
    _500 = Decimal("0.7")
    _1000 = Decimal("0.8")
    _2000 = Decimal("0.9")
    _4000 = Decimal("1.0")


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
