import pytest
from django.urls import reverse
from users.models import User

pytestmark = pytest.mark.django_db


class TestRegisterView:
    def test_register_success(self, client, user_data):
        response = client.post(reverse("register"), data=user_data)
        assert response.status_code == 302
        assert User.objects.filter(username=user_data["username"]).exists()

    def test_register_invalid_data(self, client):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        response = client.post(reverse("register"), data=invalid_data)
        assert response.status_code == 200
        assert "Błąd podczas tworzenia konta" in response.content.decode()


class TestLoginView:
    def test_login_success(self, client, user):
        logged_in = client.login(username=user.username, password="password123")
        assert logged_in is True
        response = client.get(reverse("users:home"))
        assert response.status_code == 200
