from django.urls import path
from .views import   PostListView,PostPublishUnpublishView,PostCreateView,LikeUnlikePostView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/publish/', PostPublishUnpublishView.as_view(), name='post-publish-toggle'),
    path('posts/<int:pk>/like-unlike/', LikeUnlikePostView.as_view(), name='post-like-unlike')
]
