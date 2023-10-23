from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..core.forms import CustomUserCreationForm

User = get_user_model()


class RegistrationView(CreateView):
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
