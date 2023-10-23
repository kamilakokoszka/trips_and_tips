import pytest
from django.test import Client
from django.contrib.auth import get_user_model


@pytest.fixture
def admin_client():
    client = Client()
    admin = get_user_model().objects.create_superuser(
        username='testadmin',
        email='admin@example.com',
        password='testsuperpass123'
    )
    client.force_login(admin)
    return client


@pytest.fixture
def test_user():
    return get_user_model().objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
