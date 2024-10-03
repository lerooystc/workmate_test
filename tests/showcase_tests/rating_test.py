import pytest
from rest_framework import status


@pytest.mark.django_db
def test_successful_rating_creation(user_client, test_cat):
    """Тестирует успешное создание и убеждается в добавлении оценки."""
    url = f"/api/v1/showcase/cats/{test_cat.id}/ratings/"
    rating_data = {"rating": 5}
    response = user_client.post(url, data=rating_data)
    assert response.status_code == status.HTTP_201_CREATED, print(response.json())
    url = f"/api/v1/showcase/cats/{test_cat.id}/ratings/get_user_rating/"
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data["rating"] == rating_data["rating"]


@pytest.mark.django_db
def test_successful_rating_retrieval(user_client, test_cat, test_rating):
    """Тестирует успешное получение текущей оценки пользователя на коте."""
    url = f"/api/v1/showcase/cats/{test_cat.id}/ratings/get_user_rating/"
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data["rating"] == test_rating.rating


@pytest.mark.django_db
def test_successful_rating_update(user_client, test_cat, test_rating):
    """Тестирует успешное изменение текущей оценки пользователя на коте."""
    url = f"/api/v1/showcase/cats/{test_cat.id}/ratings/update_user_rating/"
    patch_data = {"rating": 3}
    response = user_client.patch(url, patch_data)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    test_rating.refresh_from_db()
    assert response.data["rating"] == test_rating.rating


@pytest.mark.django_db
def test_successful_user_ratings_retrieval(user_client, test_rating):
    """Тестирует успешное получение оценок пользователя."""
    url = "/api/v1/showcase/user_ratings/"
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data[0]["rating"] == test_rating.rating
