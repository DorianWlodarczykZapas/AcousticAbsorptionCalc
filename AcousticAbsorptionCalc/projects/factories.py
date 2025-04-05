import factory
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from .models import Project


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Project {n}")
    description = factory.Faker("paragraph")


# Usage
# ProjectFacotry.create() # ...
# ProjectFactory.create(name='new_project')
# ProjectFactory.build()
# ProjectFactory.create_batch(10, user=...)
