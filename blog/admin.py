from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
	list_filter = ['status', 'created', 'publish', 'author']
	search_fields = ['title', 'body']
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']

	fieldsets = [
	    (None,      {'fields': ['title', 'slug', 'author']}),
	    ('Content', {'fields': ['body', 'status']}),
	    ('Time',    {'fields': ['publish'], 'classes': ['collapse']}),
    ]


admin.site.register(Post, PostAdmin)