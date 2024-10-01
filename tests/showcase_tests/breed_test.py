import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_successful_breed_retrieval(user_client, test_breed):
    """Тестирует успешное получение пород."""
    url = reverse("breeds-list")
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data[0]["name"] == test_breed.name


@pytest.mark.django_db
def test_failed_breed_creation(user_client):
    """Тестирует ошибку при создании породы не админом."""
    url = reverse("breeds-list")
    breed_data = {"name": "Обычная"}
    response = user_client.post(url, breed_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, print(response.json())


@pytest.mark.django_db
def test_successful_breed_creation(admin_client):
    """Тестирует успешное создание породы админом."""
    url = reverse("breeds-list")
    breed_data = {"name": "Сиамская"}
    response = admin_client.post(url, breed_data)
    assert response.status_code == status.HTTP_201_CREATED, print(response.json())
    assert response.data["name"] == breed_data["name"]
