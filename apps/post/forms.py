from django import forms

from apps.core.models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']