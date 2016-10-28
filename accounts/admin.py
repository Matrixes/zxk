from django.contrib import admin
from .models import UserProfile, SocialUser, UserSettings


admin.site.register(UserProfile)
admin.site.register(SocialUser)
admin.site.register(UserSettings)