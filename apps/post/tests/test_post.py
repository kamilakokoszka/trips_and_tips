import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.post.tests.utils import create_sample_post

from apps.core.models import Profile, Post

User = get_user_model()


#  -----POST TESTS -----

# PostListView tests
@pytest.mark.django_db
def test_post_list_view(client, user):
    """Test post list view displayed correctly."""
    client.login(email='test@example.com', password='Testpass123')
    create_sample_post()

    url = reverse('post:list')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['posts'].count() == 1


@pytest.mark.django_db
def test_post_detail_view(client, user):
    """Test post detail view displayed correctly."""
    client.login(email='test@example.com', password='Testpass123')
    create_sample_post()
    post = Post.objects.first()

    url = reverse('post:details', args=[post.slug])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['post'].title == 'Sample post title'
