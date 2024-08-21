from django.contrib import admin
from .models import Post,Tag,Like
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'get_tags', 'created_at', 'updated_at', 'is_published', 'author')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', )
    list_per_page = 25

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
admin.site.register(Tag,TagAdmin)
    
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','post','created_at')
admin.site.register(Like,LikeAdmin)