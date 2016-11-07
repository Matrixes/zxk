from django.contrib import admin
from .models import UserProfile, SocialUser, UserSetting, Contack, Collection


admin.site.register(UserProfile)
admin.site.register(SocialUser)
admin.site.register(UserSetting)
admin.site.register(Contack)
admin.site.register(Collection)