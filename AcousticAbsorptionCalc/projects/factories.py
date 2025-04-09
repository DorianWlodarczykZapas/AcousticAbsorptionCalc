import factory
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory

from .models import Project, SharedProject


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Project {n}")
    description = factory.Faker("paragraph")


class SharedProjectFactory(DjangoModelFactory):
    class Meta:
        model = SharedProject

    project = factory.SubFactory(ProjectFactory)
    shared_with_user = factory.SubFactory(UserFactory)
    access_level = factory.Iterator(["read", "write", "admin"])
