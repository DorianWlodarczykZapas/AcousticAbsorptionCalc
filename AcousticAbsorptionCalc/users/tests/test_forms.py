import pytest
from users.forms import UserProfileForm, UserRegistrationForm

pytestmark = pytest.mark.django_db


class TestUserRegistrationForm:

    def test_form_valid_data_creates_user(self, user_data):
        form = UserRegistrationForm(data=user_data)
        assert form.is_valid()

        user = form.save()
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.check_password(user_data["password1"])
        assert user.role == "free_version"

    def test_form_password_mismatch(self):
        data = {
            "username": "tester",
            "email": "tester@example.com",
            "password1": "password123",
            "password2": "wrongpass",
        }
        form = UserRegistrationForm(data=data)
        assert not form.is_valid()
        assert "Hasła muszą być takie same." in str(form.errors)

    def test_form_missing_email(self):
        data = {
            "username": "tester",
            "password1": "password123",
            "password2": "password123",
        }
        form = UserRegistrationForm(data=data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_short_password(self):
        data = {
            "username": "tester",
            "email": "tester@example.com",
            "password1": "123",
            "password2": "123",
        }
        form = UserRegistrationForm(data=data)
        assert not form.is_valid()
        assert "Hasło musi mieć co najmniej 8 znaków." in str(
            form.errors.get("password1", "")
        )


class TestUserProfileForm:

    def test_profile_update_without_password_change(self, user):
        form_data = {
            "username": "newname",
            "email": "newemail@example.com",
            "new_password": "",
        }
        form = UserProfileForm(instance=user, data=form_data)
        assert form.is_valid()

        updated_user = form.save()
        assert updated_user.username == "newname"
        assert updated_user.email == "newemail@example.com"
        assert updated_user.check_password("password123")

    def test_profile_update_with_password_change(self, user):
        form_data = {
            "username": user.username,
            "email": user.email,
            "new_password": "newsecurepass123",
        }
        form = UserProfileForm(instance=user, data=form_data)
        assert form.is_valid()

        updated_user = form.save()
        assert updated_user.check_password("newsecurepass123")

    def test_profile_invalid_email(self, user):
        form_data = {
            "username": "test",
            "email": "not-an-email",
            "new_password": "",
        }
        form = UserProfileForm(instance=user, data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors
