from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
    update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import CreateView, TemplateView, DeleteView

from apps.user.forms import UserLoginForm, ProfileUpdateForm
from apps.core.forms import CustomUserCreationForm
from apps.core.models import Profile, CustomUser, Post

User = get_user_model()


# ------- User views ------- #

class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/registration.html'

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_valid(self, form):
        form.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginView(View):
    template_name = 'user/login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse_lazy('home-page'))

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home-page'))


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'user/settings.html/'


class UserPasswordChangeView(LoginRequiredMixin, View):
    template_name = 'user/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse_lazy('user:settings'))
        return render(request, self.template_name, {'form': form})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('home-page')
    template_name = 'user/user_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(CustomUser,
                                username=self.request.user.username)
        return obj


# ------- Profile views ------- #

class UserProfileView(TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, user_id):
        context = super().get_context_data()
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        context['profile'] = get_object_or_404(Profile, user=user)
        context['user_posts'] = (Post.objects
                                 .filter(author=user.profile, status=1)
                                 .order_by('-created_on'))
        return context


class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'user/profile_update.html'

    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)
        if form.is_valid():
            if form.cleaned_data.get('set_default_profile_picture'):
                request.user.profile.picture = 'default.jpg'
            form.save()
            return redirect(reverse('user:profile',
                                    args=[request.user.pk]))

        return render(request, self.template_name, {'form': form})
