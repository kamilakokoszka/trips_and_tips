"""
URLs for post app.
"""
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
)

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='details')
]
