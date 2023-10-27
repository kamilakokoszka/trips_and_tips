"""
URLs for user app.
"""

from django.urls import path

from .views import (
    RegistrationView,
    home_page,
)

app_name = 'user'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('', home_page, name='home-page')
]
