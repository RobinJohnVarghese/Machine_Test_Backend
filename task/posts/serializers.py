from rest_framework import serializers
from .models import Post, Tag,Like
from posts.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'email', 'mobile', 'username', 'is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            mobile=validated_data['mobile'],
        )
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'updated_at', 'is_published', 'author']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def create(self, validated_data):
        # Extract the tags data from the validated data
        tags_data = validated_data.pop('tags', [])
        
        # Create the Post instance
        post = Post.objects.create(**validated_data)
        
        # Assign the tags to the Post instance
        post.tags.set(tags_data)
        return post
    
class PostCountSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'updated_at', 'is_published', 'author', 'likes_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'likes_count']