from django.contrib import admin

from .models import UserComment, Follow, UserPost, UserProfile

admin.site.register(UserComment)
admin.site.register(Follow)
admin.site.register(UserPost)
admin.site.register(UserProfile)
