from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .models import Post
from .serializers import PostSerializer,PostCountSerializer
from rest_framework import generics, permissions, status
from .models import Post, Like
from django.db.models import Count
from django.shortcuts import get_object_or_404


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostPublishUnpublishView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        post.is_published = not post.is_published  # Toggle the is_published field
        post.save()

        
    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        post = self.get_object()
        status_message = f'"{post.title}" has been {"published" if post.is_published else "unpublished"}.'
        return Response({"message": status_message}, status=status.HTTP_200_OK)

class LikeUnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, is_published=True)
        user = request.user

        like_instance, created = Like.objects.get_or_create(user=user, post=post)
        
        if not created:
            # If the Like instance already exists, it means the user has liked it before, so we will unlike it.
            like_instance.delete()
            message = f'You have unliked the post "{post.title}".'
        else:
            # If the Like instance was newly created, it means the user is liking the post now.
            message = f'You have liked the post "{post.title}".'

        return Response({"message": message}, status=status.HTTP_200_OK)
    
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().annotate(likes_count=Count('likes')).order_by('-created_at')
    serializer_class = PostCountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # We can filter posts or order them as required.
        return Post.objects.filter(is_published=True).annotate(likes_count=Count('likes')).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
