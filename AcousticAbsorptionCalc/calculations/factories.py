from datetime import timezone
from decimal import Decimal

import factory

from .models import Calculation, Material, Norm, NormCalculationType, SurfaceElement


class NormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Norm

    name = factory.Sequence(lambda n: f"Norm {n}")
    description = factory.Faker("text")
    application_type = NormCalculationType.NONE
    rt_max = Decimal("0.6")
    sti_min = Decimal("0.6")
    absorption_min_factor = Decimal("0.9")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))


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


class CalculationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Calculation

    reverberation_time = Decimal("1.23")
    norm = factory.SubFactory(NormFactory)
    is_within_norm = True
    created_at = factory.LazyFunction(timezone.now)
    room_height = Decimal("2.5")
    room_volume = Decimal("50.0")
    room_surface_area = Decimal("80.0")
    sti = Decimal("0.75")

    @factory.post_generation
    def surfaces(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for surface in extracted:
                surface.calculation = self
                surface.save()
        else:
            SurfaceElementFactory.create_batch(3, calculation=self)


class SurfaceElementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurfaceElement

    calculation = factory.SubFactory(CalculationFactory)
    material = factory.SubFactory(MaterialFactory)
    area_m2 = Decimal("10.0")
    location = factory.Iterator(["ceiling", "wall A", "wall B", "floor"])
