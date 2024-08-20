from rest_framework import serializers

from accounts.models import UserAccount
from .models import Post,Tag,Like

# class PostSerializer(serializers.ModelSerializer):
#     likes_count = serializers.SerializerMethodField()
#     author = serializers.StringRelatedField(read_only=True)
#     date_created = serializers.DateTimeField(format='%d-%m-%Y')

#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'description', 'tags', 'date_created', 'likes_count', 'author')

#     def get_likes_count(self, obj):
#         return obj.likes.count()

# class PostDetailSerializer(serializers.ModelSerializer):
#     author = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Post
#         fields = ('title', 'description', 'tags', 'author')
        
#     def create(self, validated_data):
#         tags_data = validated_data.pop('tags', [])
#         post = Post.objects.create(**validated_data)
#         for tag in tags_data:
#             tag_obj, created = Tag.objects.get_or_create(name=tag.name)
#             post.tags.add(tag_obj)
#         return post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True, required=False)
    tags = serializers.ListField(child=serializers.CharField(max_length=50), required=False, write_only=True)


    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'updated_at', 'is_published', 'author']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        author = self.context['request'].user
        post = Post.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            author=author
            )
        
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        return post
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation