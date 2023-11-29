from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View

from django.views.generic import (
    ListView,
    DetailView,
    FormView, UpdateView, DeleteView
)

from apps.core.models import Post, Profile
from apps.post.forms import PostForm, CommentForm

User = get_user_model()


# ------- Home page ------- #

class PostListView(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'home_page.html'
    paginate_by = 5
    context_object_name = 'posts'


# ------- Post views ------- #

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = self.object
            new_comment.save()
            return HttpResponseRedirect(self.request.path_info)

        return self.render_to_response(self.get_context_data(form=form))


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

    def form_valid(self, form):
        post = form.save(commit=False)
        profile = Profile.objects.get(user=self.request.user)
        post.author = profile
        post.status = 1 if 'publish' in self.request.POST else 0
        post.save()
        form.save_m2m()

        if 'publish' in self.request.POST:
            self.success_url = reverse_lazy('post:details',
                                            kwargs={'slug': post.slug})
        else:
            self.success_url = reverse_lazy('post:user-posts')

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/update.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        profile = Profile.objects.get(user=self.request.user)
        if obj.author != profile:
            raise PermissionDenied()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == '1':
            return super().get(request, *args, **kwargs)
        elif self.object.status == '0':
            self.template_name = 'post/draft.html'
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.object.status == '0':
            self.object.status = 1 if 'publish' in self.request.POST else 0
            self.object.save()
        return super(PostUpdateView, self).form_valid(form)

    def get_success_url(self):
        if self.object.status == '1':
            return reverse('post:details', kwargs={'slug': self.object.slug})
        else:
            return reverse('post:user-posts')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:user-posts')
    template_name = 'post/post_confirm_delete.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        profile = Profile.objects.get(user=self.request.user)
        if obj.author != profile:
            raise PermissionDenied()
        return obj


# ------- Tags views ------- #
class FilterPostsByTagView(View):
    template_name = 'post/tag.html'

    def get(self, request, tag):
        posts = (Post.objects
                 .filter(tags__name__in=[tag])
                 .order_by('-created_on'))
        return render(request, self.template_name,
                      {'tag': tag, 'posts': posts})


class SearchPostsByTagView(View):
    template_name = 'post/tag.html'

    def get(self, request):
        tag = request.GET.get('tag')
        posts = (Post.objects
                 .filter(tags__name__in=[tag])
                 .order_by('-created_on'))
        return render(request, self.template_name,
                      {'tag': tag, 'posts': posts})
