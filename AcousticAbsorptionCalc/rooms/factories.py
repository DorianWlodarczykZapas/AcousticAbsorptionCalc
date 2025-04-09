import factory
from factory.django import DjangoModelFactory
from models import Room
from projects.factories import ProjectFactory


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    project = factory.SubFactory(ProjectFactory)
    name = factory.Sequence(lambda n: f"Room {n}")
    width = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    length = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    height = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
