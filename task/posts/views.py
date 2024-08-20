from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .models import Post
from .serializers import PostSerializer

# class PostListCreateView(ListCreateAPIView):

#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     queryset = Post.objects.all()
#     serializer = PostSerializer

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#     def get_serializer_class(self):
#         print("eeeeeeeeeeeeeeeeeeeee")
#         if self.request.method == 'POST':
#             return PostDetailSerializer
#         return PostSerializer

class CreatePostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAuthenticated user: {request.user}")
        print(f"User ID: {request.user.id}")
        print(f"User model: {settings.AUTH_USER_MODEL}")
        print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaIs authenticated: {request.user.is_authenticated}")
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                post = serializer.save(author=request.user)
                print(f"bbbbbbbbbbbbbbbbbbbbbbCreated post with ID: {post.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"cccccccccccccccccccccccError saving post: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"dddddddddddddddddddddddddSerializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostPublishToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
            post.is_published = not post.is_published
            post.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

class PostLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
            return Response({'liked': liked}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

