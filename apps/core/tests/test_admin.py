"""
Tests for Django admin modifications.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


# Fixtures
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


# Admin tests
@pytest.mark.django_db
def test_users_list(admin_client, test_user):
    url = reverse('admin:core_customuser_changelist')
    response = admin_client.get(url)
    response_text = response.content.decode('utf-8')

    assert test_user.username in response_text
    assert test_user.email in response_text


@pytest.mark.django_db
def test_edit_user_page(admin_client, test_user):
    url = reverse('admin:core_customuser_change', args=[test_user.id])
    response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_page(admin_client):
    url = reverse('admin:core_customuser_add')
    response = admin_client.get(url)

    assert response.status_code == 200
