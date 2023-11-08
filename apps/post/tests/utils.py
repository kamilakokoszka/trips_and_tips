from django.contrib.auth import get_user_model

from apps.core.models import Profile, Post

User = get_user_model()


def create_sample_profile(user, **params):
    """Create and return a sample user profile."""
    data = {
        'user': user,
        'bio': 'Sample bio',
        'website': 'test.com'
    }


def create_sample_post(**params):
    """Create and return a sample post."""
    user = User.objects.first()
    create_sample_profile(user)
    profile = Profile.objects.first()
    data = {
        'title': 'Sample post title',
        'slug': 'sample-post-title',
        'body': 'xyz',
        'author': profile,
        'status': 1
    }
    data.update(params)

    post = Post.objects.create(**data)
    return post
