"""
Tests for Django admin modifications.
"""

import pytest
from django.urls import reverse


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
