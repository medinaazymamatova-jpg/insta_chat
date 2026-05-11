from django.contrib import admin
from .models import *


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [ContentInline]

admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Hashtag)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(SavePost)
admin.site.register(SavePostItem)
admin.site.register(Stories)
