import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from utils import create_user


CREATE_USER_URL = reverse('user:register')


# Home page tests
@pytest.mark.django_db
def test_home_page_authorized(client, user):
    """Test proper home page template is displayed to authenticated user."""
    client.force_login(user)
    url = reverse('user:home-page')
    response = client.get(url)

    assert response.status_code == 200
    assert 'home_page.html' in [
        template.name for template in response.templates]


@pytest.mark.django_db
def test_home_page_unauthorized(client):
    """Test proper home page template is displayed to unauthenticated user."""
    url = reverse('user:home-page')
    response = client.get(url)

    assert response.status_code == 200
    assert 'home_unauthenticated.html' in [
        template.name for template in response.templates]


# UserRegistrationView tests
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


# UserLoginView tests
@pytest.mark.django_db
def test_login_successful(client, user):
    """Test logging in is successful."""
    url = reverse('user:login')
    login_data = {
        'email': 'test@example.com',
        'password': 'Testpass123'
    }
    response = client.post(url, login_data)

    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_login_invalid_data(client, user):
    """Test logging in is unsuccessful if invalid data."""
    url = reverse('user:login')
    login_data = {
        'email': 'test@example.com',
        'password': 'pass123'
    }
    response = client.post(url, login_data)

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated
