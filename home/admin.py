from django.contrib import admin
from .models import Post, IsLike
from .models import Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(IsLike)