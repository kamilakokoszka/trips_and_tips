from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
    update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import UserLoginForm
from ..core.forms import CustomUserCreationForm


User = get_user_model()


def home_page(request):
    if request.user.is_authenticated:
        return render(request, 'home_page.html')
    return render(request, 'home_unauthenticated.html')


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/registration.html'

    def get_success_url(self):
        return reverse_lazy('user:home-page')

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
                return redirect(reverse_lazy('user:home-page'))

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('user:home-page'))


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'user/settings.html/'


class UserPasswordChangeView(LoginRequiredMixin, View):
    template_name = 'user/change_password.html'

    def get(self, request):
        form = PasswordChangeForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password has been changed successfully.')
            return redirect(reverse_lazy('user:settings'))
        else:
            messages.error(request, 'Please correct the error below.')

        return render(request, self.template_name, {'form': form})
