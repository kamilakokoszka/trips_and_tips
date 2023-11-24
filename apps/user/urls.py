"""
URLs for user app.
"""
from django.urls import path

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserSettingsView,
    UserPasswordChangeView,
    UserDeleteView,
    UserProfileView,
    UserProfileUpdateView,
)

app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserPasswordChangeView.as_view(),
         name='password-change'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(),
         name='profile-update'),
]
