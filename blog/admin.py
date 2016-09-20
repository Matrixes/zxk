from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
	# list_filter = ['status', 'created', 'publish', 'author']
	search_fields = ['title', 'body']
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']

	#fieldsets = [
	#    (None,      {'fields': ['title', 'slug', 'author']}),
	#    ('Content', {'fields': ['body', 'status']}),
	#    ('Time',    {'fields': ['publish'], 'classes': ['collapse']}),
    #]

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'body')

admin.site.register(Comment, CommentAdmin)