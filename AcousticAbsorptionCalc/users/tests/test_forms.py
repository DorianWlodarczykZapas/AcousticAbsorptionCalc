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


def test_password_mismatch_fails():
    data = {
        "username": "tester",
        "email": "tester@example.com",
        "password1": "password123",
        "password2": "wrongpass",
    }
    form = UserRegistrationForm(data=data)
    assert not form.is_valid()
    assert "Hasła muszą być takie same." in str(form.errors)


def test_missing_email():
    data = {
        "username": "tester",
        "password1": "password123",
        "password2": "password123",
    }
    form = UserRegistrationForm(data=data)
    assert not form.is_valid()
    assert "email" in form.errors
