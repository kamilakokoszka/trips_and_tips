import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.post.tests.utils import create_sample_post

from apps.core.models import Post, Profile

User = get_user_model()


#  ----- POST TESTS -----

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


# PostDetailView test
@pytest.mark.django_db
def test_post_detail_view(client, user):
    """Test post detail view is displayed correctly."""
    client.login(email='test@example.com', password='Testpass123')
    create_sample_post()
    post = Post.objects.first()

    url = reverse('post:details', args=[post.slug])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['post'].title == 'Sample post title'


# UserPostListView tests
@pytest.mark.django_db
def test_user_post_list_view(client, user):
    """Test user post list view is displayed correctly."""
    client.login(email='test@example.com', password='Testpass123')
    create_sample_post()

    url = reverse('post:user-posts')
    response = client.get(url)

    assert response.status_code == 200
    assert Post.objects.count() == 1
    assert response.context['user_posts'].count() == 1


@pytest.mark.django_db
def test_user_post_list_limited_to_user(client, user):
    """Test user post list is limited to certain user."""
    client.login(email='test@example.com', password='Testpass123')
    create_sample_post()

    user2 = User.objects.create_user(email='test2@example.com',
                                     username='testuser2',
                                     password='Testpass123')

    profile2 = Profile.objects.get(user=user2)
    Post.objects.create(title='Sample post title 2',
                        slug='sample-post-title-2',
                        body='xyz',
                        author=profile2,
                        status=1)

    url = reverse('post:user-posts')
    response = client.get(url)

    assert response.status_code == 200
    assert Post.objects.count() == 2
    assert response.context['user_posts'].count() == 1


# PostCreateView tests
@pytest.mark.django_db
def test_create_post_view(client, user):
    """Test post is created with valid data."""
    client.login(email='test@example.com', password='Testpass123')
    profile = user.profile

    url = reverse('post:create')
    response = client.get(url)

    assert response.status_code == 200

    data = {
        'title': 'Post title',
        'slug': 'post-title',
        'body': 'xyz',
        'publish': 'Publish'
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert Post.objects.filter(title=data['title']).exists()

    post = Post.objects.get(title=data['title'])

    assert int(post.status) == 1
    assert post.author == profile
