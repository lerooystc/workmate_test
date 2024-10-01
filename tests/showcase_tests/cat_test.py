import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_successful_cat_creation(user_client, test_breed):
    """Тестирует успешное создание и получение кота."""
    url = reverse("cats-list")
    cat_data = {
        "name": "Кошка",
        "age": 18,
        "color": 3,
        "description": "Кошка.",
        "breed": 1,
    }
    response = user_client.post(url, data=cat_data)
    assert response.status_code == status.HTTP_201_CREATED, print(response.json())
    url = reverse("cats-detail", args=(1,))
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data["name"] == cat_data["name"]


@pytest.mark.django_db
def test_failed_cat_creation(user_client, test_breed):
    """Тестирует ошибку при создании кота с недопустимыми значениями возраста и породы."""
    url = reverse("cats-list")
    cat_data = {
        "name": "Кошка",
        "age": 10000,
        "color": 3,
        "description": "Кошка.",
        "breed": 2,
    }
    response = user_client.post(url, data=cat_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, print(response.json())


@pytest.mark.django_db
def test_successful_cat_update(user_client, test_cat):
    """Тестирует успешное изменение кота (через patch)."""
    url = reverse("cats-detail", args=(1,))
    cat_data = {
        "age": 19,
    }
    response = user_client.patch(url, data=cat_data)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    test_cat.refresh_from_db()
    assert test_cat.age == cat_data["age"]
    assert test_cat.name == response.data["name"]


@pytest.mark.django_db
def test_unsuccessful_cat_update(different_user_client, test_cat):
    """Тестирует ошибку при изменении кота не его владельцем (через patch)."""
    url = reverse("cats-detail", args=(1,))
    cat_data = {
        "age": 19,
    }
    response = different_user_client.patch(url, data=cat_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, print(response.json())
    test_cat.refresh_from_db()
    assert test_cat.age != cat_data["age"]


@pytest.mark.django_db
def test_successful_cat_filtering(user_client, test_cats):
    """
    Тестирует фильтрацию по породам котов.
    После фильтрации должно остаться 2 кота.
    """
    url = reverse("cats-list")
    response = user_client.get(url, query_params={"breed": 1})
    assert response.status_code == status.HTTP_200_OK, print(response.data)
    assert len(response.data) == 2
