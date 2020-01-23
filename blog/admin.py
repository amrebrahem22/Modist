from django.contrib import admin
from .models import Post, PostCategory

from .forms import PostForm

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'overview', 'author', 'tags', 'image', 'timestamp', 'updated',]
    form = PostForm
    class Meta:
        model = Post
        fields = "__all__"


admin.site.register(PostCategory)
