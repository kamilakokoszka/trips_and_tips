import pytest

from django.test import Client
from apps.core.models import CustomUser


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user_data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'Testpass123',
    }
    user = CustomUser(**user_data)
    user.set_password(user_data['password'])
    user.save()
    return user
