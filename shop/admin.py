from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ['name']}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'price', 'stock', 
					'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'stock', 'available']
	prepopulated_fields = {'slug': ['name']}

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'email', 'address', 
					'postal_code', 'city', 'paid', 'created', 'updated']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)