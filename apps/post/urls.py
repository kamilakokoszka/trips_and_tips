"""
URLs for post app.
"""
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    UserPostsListView,
    PostCreateView,
    PostUpdateView
)

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('user/list/', UserPostsListView.as_view(), name='user-posts'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdateView.as_view(),
         name='update'),
    path('<slug:slug>/', PostDetailView.as_view(), name='details'),
]
