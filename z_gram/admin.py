from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from z_gram.models import UserComment, Follow, UserPost, UserProfile

admin.register(UserComment)
admin.register(Follow)
admin.register(UserPost)
admin.register(UserProfile)