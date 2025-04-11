import factory

from .models import Material, Norm


class NormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Norm

    name = factory.Faker("word")


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material

    type = factory.Faker("word")
    name = factory.Faker("word")
    freq_120 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    _250 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    _500 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    _1000 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    _2000 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    _4000 = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
