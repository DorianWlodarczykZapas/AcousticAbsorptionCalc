import pytest
from factory import Faker

from .factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_data():
    faker = Faker()
    password = "secure12345"
    return {
        "username": faker.user_name(),
        "email": faker.email(),
        "password1": password,
        "password2": password,
    }
