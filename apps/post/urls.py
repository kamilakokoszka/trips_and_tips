"""
URLs for post app.
"""
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    UserPostsListView,

)

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='details'),
    path('user/list/', UserPostsListView.as_view(), name='user-posts'),
    #path('create/', PostCreateView.as_view(), name='create'),
    #path('publish/', PostPublishView.as_view(), name='publish'),
    #path('save-draft/', PostSaveDraftView.as_view(), name='save-draft'),
    #path('edit-draft/<int:post_pk>/', PostUpdateDraftView.as_view(),
         #name='update-draft')
]
