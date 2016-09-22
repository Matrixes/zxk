from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'nickname', 'birthday', 'photo']

	raw_id_fields = ['user']

admin.site.register(Profile, ProfileAdmin)