import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@{faker.free_email_domain()}")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    role = FuzzyChoice(["premium", "free_version"])
