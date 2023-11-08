from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
    DeleteView,
    ListView,
    DetailView,
)

from apps.core.models import Post


User = get_user_model()


# ------- Post views ------- #

class PostListView(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post/list.html'
    paginate_by = 5
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/details.html'

