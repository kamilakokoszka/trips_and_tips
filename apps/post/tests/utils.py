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
        'tags': 'tag1',
        'status': 1
    }
    data.update(params)

    post = Post.objects.create(**data)
    return post


def create_sample_draft(**params):
    """Create and return a sample post draft."""
    user = User.objects.first()
    profile = Profile.objects.get(user=user)
    data = {
        'title': 'Sample draft title',
        'slug': 'sample-draft-title',
        'body': 'xyzxyz',
        'author': profile,
        'tags': 'tag1',
        'status': 0
    }
    data.update(params)

    draft = Post.objects.create(**data)
    return draft
