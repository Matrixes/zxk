from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
	categories = Category.objects.all()
	last_products = Product.objects.filter(available=True).order_by('-updated')[:5]
	return render(request, 'shop/index.html', {'categories': categories, 'last_products': last_products})


def product_list(request, category_slug='all'):
	category = 'all'
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug != 'all':
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)

	return render(request, 'shop/product-list.html', 
		{'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
	categories = Category.objects.all()
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	return render(request, 'shop/product-detail.html', {'categories': categories, 'product': product})
	