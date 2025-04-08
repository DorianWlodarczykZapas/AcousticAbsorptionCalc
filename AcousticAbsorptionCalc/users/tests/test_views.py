import pytest
from django.urls import reverse
from users.models import User

pytestmark = pytest.mark.django_db


def test_register_view(client, user_data):
    response = client.post(reverse("register"), data=user_data)
    assert response.status_code == 302
    assert User.objects.filter(username=user_data["username"]).exists()


def test_login_success(client, user):
    client.login(username=user.username, password="password123")
    response = client.get(reverse("users:home"))
    assert response.status_code == 200


def test_login_fail(client):
    response = client.post(
        reverse("login"),
        data={
            "identifier": "wronguser",
            "password": "wrongpass",
        },
    )
    assert response.status_code == 200
    assert "Nieprawidłowe dane logowania" in response.content.decode()


def test_logout_view(client, user):
    client.login(username=user.username, password="password123")
    response = client.post(reverse("logout"))
    assert response.status_code == 302
