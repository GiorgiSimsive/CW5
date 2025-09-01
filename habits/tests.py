import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from habits.models import Habit


@pytest.mark.django_db
def test_create_habit() -> None:
    User.objects.create_user(username="testuser", password="pass1234")
    client = APIClient()
    response = client.post("/api/token/", {"username": "testuser", "password": "pass1234"})
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {
        "place": "дом",
        "time": "08:00:00",
        "action": "зарядка",
        "is_pleasant": False,
        "periodicity": 1,
        "execution_time": 60,
        "is_public": True,
        "reward": "кофе",
    }

    response = client.post("/api/habits/my/", data)
    assert response.status_code == 201
    assert Habit.objects.count() == 1
