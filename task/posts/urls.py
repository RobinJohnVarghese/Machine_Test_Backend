from django.urls import path
from .views import  PostPublishToggleView, PostLikeToggleView,CreatePostView

urlpatterns = [
    # path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/publish/', PostPublishToggleView.as_view(), name='post-publish-toggle'),
    path('posts/<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like-toggle'),
]
