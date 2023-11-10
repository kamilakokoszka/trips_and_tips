from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    ListView,
    DetailView,
    FormView, UpdateView
)

from apps.core.models import Post, Profile
from apps.post.forms import PostForm

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


class UserPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/user_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['user_posts'] = (Post.objects
                                 .filter(author=profile)
                                 .order_by('-created_on'))
        return context


class PostCreateView(LoginRequiredMixin, FormView):
    template_name = 'post/create.html'
    form_class = PostForm
    success_url = reverse_lazy('post:user-posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        profile = Profile.objects.get(user=self.request.user)
        post.author = profile
        post.status = 1 if 'publish' in self.request.POST else 0
        post.save()
        return super().form_valid(form)


class PublishedPostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/update.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post:details', kwargs={'slug': self.object.slug})

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        profile = Profile.objects.get(user=self.request.user)
        if obj.author != profile:
            raise PermissionDenied()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if int(self.object.status) == 1:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('post:user-posts')

    def form_valid(self, form):
        messages.success(self.request, 'The post was updated successfully.')
        return super(PublishedPostUpdateView, self).form_valid(form)
