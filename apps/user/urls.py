"""
URLs for user app.
"""
from django.urls import path

from .views import (
    home_page,
    RegistrationView,
    UserLoginView
)

app_name = 'user'

urlpatterns = [
    path('home/', home_page, name='home-page'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login')
]
