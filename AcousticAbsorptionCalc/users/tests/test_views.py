import pytest
from django.urls import reverse
from users.models import User

pytestmark = pytest.mark.django_db


def test_register_view(client, user_data):
    response = client.post(reverse("register"), data=user_data)
    assert response.status_code == 302
    assert User.objects.filter(username=user_data["username"]).exists()
