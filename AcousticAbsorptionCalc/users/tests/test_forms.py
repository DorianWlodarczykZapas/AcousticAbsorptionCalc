import pytest
from users.forms import UserRegistrationForm

pytestmark = pytest.mark.django_db


def test_valid_user_registration_form(user_data):
    form = UserRegistrationForm(data=user_data)
    assert form.is_valid()
    user = form.save()
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password1"])
    assert user.role == "free_version"
