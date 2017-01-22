from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm


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

	cart_product_form = CartAddProductForm()
	return render(request, 
				  'shop/product-detail.html',  
				  {'categories': categories, 
				  'product': product,
				  'cart_product_form': cart_product_form})


# cart
def cart_detail(request):
	cart = Cart(request)
	return render(request, 'shop/cart-detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=int(product_id))
	form = CartAddProductForm(request.POST)

	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, 
				 quantity=cd['quantity'],
				 update_quantity=cd['update'])
	return redirect('shop:cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('shop:cart_detail')


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, 
										 product=item['product'],
										 price=item['price'],
										 quantity=item['price'])
				cart.clear()
				return render(request, 'shop/order-created.html', {'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'shop/order-create.html', {'cart': cart, 'form': form})


