import pytest
from apps.showcase.models import Breed
from apps.showcase.models import Cat
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient

UserModel = get_user_model()


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user():
    new_user = UserModel.objects.create(username="testuser")
    new_user.set_password("pass123")
    new_user.save()
    return new_user


@pytest.fixture
def user_for_client():
    user = UserModel.objects.create(username="client_user")
    user.set_password("client_pass")
    user.save()
    return user


@pytest.fixture
def user_client(user_for_client) -> Client:
    new_client = APIClient()
    new_client.force_authenticate(user=user_for_client)
    return new_client


@pytest.fixture
def different_user_client(test_user) -> Client:
    new_client = APIClient()
    new_client.force_authenticate(user=test_user)
    return new_client


@pytest.fixture
def test_breed() -> Breed:
    breed = Breed.objects.create(name="Сибирская")
    return breed


@pytest.fixture
def test_cat(test_breed, user_for_client) -> Cat:
    cat = Cat.objects.create(
        name="Кошка",
        age=18,
        color=3,
        description="Кошка.",
        breed=test_breed,
        owner=user_for_client,
    )
    return cat


@pytest.fixture
def test_cats(user_for_client) -> list[Cat]:
    breeds = (
        Breed.objects.create(name="Сибирская"),
        Breed.objects.create(name="Персидская"),
    )
    cats = []
    for i in range(1, 6):
        cat = Cat.objects.create(
            name=f"Кошка{i}",
            age=i,
            color=3,
            description=f"Кошка {i}.",
            breed=breeds[i % 2],
            owner=user_for_client,
        )
        cats.append(cat)
    return cats
