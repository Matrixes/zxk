from django.contrib import admin
from .models import Tag, Post, Comment


class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'created')

	fields = ['name',]

	search_fields = ['name']

admin.site.register(Tag, TagAdmin)


class PostAdmin(admin.ModelAdmin):
	# list_filter = ['status', 'created', 'publish', 'author']
	search_fields = ['title', 'body']
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

	#prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author', 'tags']

	
	class Media:
		js = (
    		'/static/js/kindeditor/kindeditor-all-min.js',
    		'/static/js/kindeditor/lang/zh-CN.js',
    		'/static/js/kindeditor/config.js',
    	)
    

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

##########
