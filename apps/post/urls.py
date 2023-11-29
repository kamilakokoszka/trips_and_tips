"""
URLs for post app.
"""
from django.urls import path
from .views import (
    PostDetailView,
    UserPostsListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    FilterPostsByTagView,
    SearchPostsByTagView
)

app_name = 'post'

urlpatterns = [
    path('user/list/', UserPostsListView.as_view(), name='user-posts'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdateView.as_view(),
         name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('filter/<tag>/', FilterPostsByTagView.as_view(), name='tag'),
    path('search/', SearchPostsByTagView.as_view(), name='search'),
    path('<slug:slug>/', PostDetailView.as_view(), name='details'),
]
