from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import UserAccount
from django.conf import settings
# User = get_user_model()
User = UserAccount

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def publish(self):
        self.is_published = True
        self.save()

    def unpublish(self):
        self.is_published = False
        self.save()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

