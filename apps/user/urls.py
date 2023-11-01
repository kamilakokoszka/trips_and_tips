"""
URLs for user app.
"""
from django.urls import path

from .views import (
    home_page,
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserSettingsView,
    UserPasswordChangeView,
    UserDeleteView,
)

app_name = 'user'

urlpatterns = [
    path('home/', home_page, name='home-page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserPasswordChangeView.as_view(),
         name='password-change'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),

]
