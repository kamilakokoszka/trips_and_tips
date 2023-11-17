import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.user.tests.utils import create_user

from apps.core.models import Profile

User = get_user_model()
CREATE_USER_URL = reverse('user:register')


# ----- USER TESTS ----- #

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


# UserLogoutView tests
@pytest.mark.django_db
def test_logout_successful(client, user):
    """Test logging out is successful."""
    url = reverse('user:logout')
    response = client.get(url)

    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated


# UserSettingsView tests
@pytest.mark.django_db
def test_user_settings(client, user):
    """Test user settings template is displayed correctly."""
    client.login(email='test@example.com', password='Testpass123')
    url = reverse('user:settings')
    response = client.get(url)

    assert response.status_code == 200


# UserChangePasswordView tests
@pytest.mark.django_db
def test_password_change_successful(client, user):
    """Test changing password is successful."""
    client.login(email='test@example.com', password='Testpass123')
    url = reverse('user:password-change')

    new_password = 'New123456'
    data = {
        'old_password': 'Testpass123',
        'new_password1': new_password,
        'new_password2': new_password
    }

    response = client.post(url, data)

    assert response.status_code == 302
    user = User.objects.get(username='testuser')
    assert user.check_password(new_password)


@pytest.mark.django_db
def test_change_password_too_short(client, user):
    """Test changing password is unsuccessful when password too short."""
    client.login(email='test@example.com', password='Testpass123')
    url = reverse('user:password-change')

    new_password = 'New'
    data = {
        'current_password': 'Testpass123',
        'new_password1': new_password,
        'new_password2': new_password
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert user.check_password('Testpass123')


# UserDeleteView tests
@pytest.mark.django_db
def test_user_delete_successful(client, user):
    """Test user is deleted successfully."""
    client.login(email='test@example.com', password='Testpass123')
    url = reverse('user:delete', args=[user.pk])

    response = client.post(url)

    assert response.status_code == 302
    assert not User.objects.filter(username='testuser').exists()


# ----- PROFILE TESTS ----- #

# UserProfileView tests
@pytest.mark.django_db
def test_user_profile_view(client, user):
    """Test user profile is displayed correctly."""
    url = reverse('user:profile', args=[user.pk])

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile_update(client, user):
    """Test updating user profile is successful."""
    client.login(email='test@example.com', password='Testpass123')
    url = reverse('user:profile-update')

    data = {
        'bio': 'abc',
        'website': 'test.com'
    }

    response = client.post(url, data)

    assert response.status_code == 302
    profile = Profile.objects.get(user=user)
    assert profile.bio == 'abc'
    assert profile.website == 'test.com'
