from django.contrib import admin
from .models import UserProfile, SocialUser, UserSettings, Contack, Collections


admin.site.register(UserProfile)
admin.site.register(SocialUser)
admin.site.register(UserSettings)
admin.site.register(Contack)
admin.site.register(Collections)