import factory

from .models import Norm


class NormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Norm

    name = factory.Faker("word")
