import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_successful_login(client, test_user):
    """Тестирует успешную авторизацию существующего пользователя"""
    url = reverse("token_obtain_pair")
    login_data = {"username": "testuser", "password": "pass123"}
    response = client.post(url, data=login_data)

    assert response.status_code == status.HTTP_200_OK, print(response.json())


@pytest.mark.django_db
def test_failed_login(client, test_user):
    """Тестирует ошибку авторизации при неправильном пароле"""
    url = reverse("token_obtain_pair")
    login_data = {"username": "testuser", "password": "asdfadsf"}
    response = client.post(url, data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, print(response.json())


@pytest.mark.django_db
def test_successful_refresh(client, test_user):
    """Тестирует успешное обновление JWT токена"""
    login_url = reverse("token_obtain_pair")
    login_data = {"username": "testuser", "password": "pass123"}
    response = client.post(login_url, data=login_data)
    assert response.status_code == status.HTTP_200_OK
    refresh_url = reverse("token_refresh")
    refresh_data = {"refresh": response.data["refresh"]}
    response = client.post(refresh_url, data=refresh_data)
    assert response.status_code == status.HTTP_200_OK, print(response.json())
    assert response.data.get("access") is not None


@pytest.mark.django_db
def test_failed_refresh(client):
    """Тестирует ошибку при обновлении JWT токена"""
    refresh_url = reverse("token_refresh")
    refresh_data = {"refresh": "failed"}
    response = client.post(refresh_url, data=refresh_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, print(response.json())
    assert response.data.get("code") is not None


@pytest.mark.django_db
def test_successful_registration(client):
    """Тестирует успешную регистрацию пользователя"""
    register_url = reverse("register_user")
    register_data = {
        "email": "testuser@mail.ru",
        "username": "bigtest",
        "password": "testpass",
    }
    response = client.post(register_url, data=register_data)
    assert response.status_code == status.HTTP_201_CREATED, print(response.json())
    assert response.data["username"] == register_data["username"]
    login_url = reverse("token_obtain_pair")
    login_data = {"username": "bigtest", "password": "testpass"}
    response = client.post(login_url, data=login_data)
    assert response.status_code == status.HTTP_200_OK
