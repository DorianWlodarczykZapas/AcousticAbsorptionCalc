import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestRegisterView:
    def test_register_existing_username(self, client):
        existing_user_data = {
            "username": "testuser",
            "email": "existing@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        client.post(reverse("register"), data=existing_user_data)

        new_user_data = {
            "username": "testuser",
            "email": "new@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        response = client.post(reverse("register"), data=new_user_data)
        assert response.status_code == 200
        assert "Username already exists" in response.content.decode()

    def test_register_password_mismatch(self, client):
        invalid_password_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "password123",
            "password2": "password456",
        }
        response = client.post(reverse("register"), data=invalid_password_data)
        assert response.status_code == 200
        assert "Passwords do not match" in response.content.decode()


class TestLoginView:
    def test_login_success(self, client, user):
        logged_in = client.login(username=user.username, password="password123")
        assert logged_in is True
        response = client.get(reverse("users:home"))
        assert response.status_code == 200

    def test_login_fail_invalid_credentials(self, client):
        response = client.post(
            reverse("login"),
            data={
                "identifier": "wronguser",
                "password": "wrongpass",
            },
        )
        assert response.status_code == 200
        assert "Nieprawidłowe dane logowania" in response.content.decode()

    def test_login_missing_fields(self, client):
        response = client.post(reverse("login"), data={})
        assert response.status_code == 200
        assert "Nieprawidłowe dane logowania" in response.content.decode()

    def test_login_fail_wrong_password(self, client, user):
        response = client.post(
            reverse("login"),
            data={
                "identifier": user.username,
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 200
        assert "Invalid username/email or password" in response.content.decode()

    def test_login_missing_credentials(self, client):
        response = client.post(reverse("login"), data={})
        assert response.status_code == 200
        assert "This field is required" in response.content.decode()


class TestLogoutView:
    def test_logout_success(self, client, user):
        client.login(username=user.username, password="password123")
        response = client.post(reverse("logout"))
        assert response.status_code == 302

    def test_logout_when_not_logged_in(self, client):
        response = client.post(reverse("logout"))
        assert response.status_code == 302
        assert reverse("login") in response.url


class TestHomeView:
    def test_home_requires_login(self, client):
        response = client.get(reverse("users:home"))
        assert response.status_code == 302
        assert reverse("login") in response.url

    def test_home_authenticated(self, client, user):
        client.login(username=user.username, password="password123")
        response = client.get(reverse("users:home"))
        assert response.status_code == 200

    def test_home_redirect_when_not_logged_in(self, client):
        response = client.get(reverse("users:home"))
        assert response.status_code == 302
        assert reverse("login") in response.url
