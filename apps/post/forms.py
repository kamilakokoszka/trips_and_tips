from django import forms

from apps.core.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'image', 'tags']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

        labels = {
            'body': '',
        }
