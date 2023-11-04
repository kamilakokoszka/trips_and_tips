import pytest
from django.contrib.auth import get_user_model
from apps.core.models import Profile

User = get_user_model()


# CustomUser model tests
@pytest.mark.django_db
def test_create_user():
    email = 'test@example.com'
    username = 'testuser'
    password = 'testpass123'
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
    )

    assert user.email == email
    assert user.username == username
    assert user.check_password(password) is True
    assert user.is_active is True
    assert user.is_staff is False


@pytest.mark.django_db
def test_create_superuser():
    email = 'admin@example.com'
    username = 'testadmin'
    password = 'testsuperpass123'
    admin = User.objects.create_superuser(
        email=email,
        username=username,
        password=password,
    )

    assert admin.is_superuser is True
    assert admin.is_staff is True


@pytest.mark.django_db
def test_create_profile(test_user):
    """Test profile is created when user is created."""

    assert Profile.objects.all().count() == 1
    assert str(Profile.objects.first()) == 'testuser Profile'
