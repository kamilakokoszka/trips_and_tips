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
    data.update(**params)
    profile = Profile.objects.create(**data)
    return profile


def create_sample_post(**params):
    """Create and return a sample post."""
    user = User.objects.first()
    profile = Profile.objects.get(user=user)
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
