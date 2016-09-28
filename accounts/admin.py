from django.contrib import admin
from .models import UserProfile, SocialUser


admin.site.register(UserProfile)
admin.site.register(SocialUser)