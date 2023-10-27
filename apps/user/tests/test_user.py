import pytest
from django.contrib.auth import get_user_model

from django.urls import reverse

CREATE_USER_URL = reverse('user:register')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


@pytest.mark.django_db
def test_user_registration(client):
    """Test creating a user is successful."""
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password1': 'Testpass123',
        'password2': 'Testpass123'
    }
    response = client.post(CREATE_USER_URL, data)

    assert response.status_code == 302
    users = get_user_model().objects.all()
    assert users.count() == 1
    user = get_user_model().objects.get(email=data['email'])
    assert user.check_password(data['password1'])


@pytest.mark.django_db
def test_user_with_email_exists_error(client):
    """Test account is not created if user with email exists."""
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'Testpass123',
    }
    create_user(**data)
    response = client.post(CREATE_USER_URL, data)

    assert response.status_code == 200
    users = get_user_model().objects.count()
    assert users == 1


@pytest.mark.django_db
def test_password_too_short(client):
    """Test account is not created if password less than 5 characters."""
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password1': 'A1b',
        'password2': 'A1b'
    }
    response = client.post(CREATE_USER_URL, data)

    assert response.status_code == 200
    users = get_user_model().objects.all()
    assert users.count() == 0
