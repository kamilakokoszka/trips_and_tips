"""
URLs for user app.
"""
from django.urls import path

from .views import (
    home_page,
    UserRegistrationView,
    UserLoginView,
    UserLogoutView
)

app_name = 'user'

urlpatterns = [
    path('home/', home_page, name='home-page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]
