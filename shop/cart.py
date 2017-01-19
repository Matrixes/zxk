# -*- coding: utf8 -*-

'''
CART_SESSION_ID = 'cart' 放进 setitngs.py 最好，不过懒得这么干了。

session 就是类似这个样子的：
session = {
		'a': 00,
		'b': 00,
		'cart': {
				'product_id': {'product': product, 'quantity': 1, 'price': '9.99', total_price: '9.99'},
				'product_id':    ,
				......
			},
		'modified': True|False,
		......
	}
'''


from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart(object):

	def __init__(self, request):
		"""
		Initialize the cart.
		"""
		self.session = request.session
		cart = self.session.get('cart')
		if not cart:
			# 下面的可以简写成这样
			# cart = self.session['cart'] = {}
			self.session['cart'] = {}
			cart = {}
		self.cart = cart

	def __len__(self):
		"""
		Count all items in the cart.
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def __iter__(self):
		"""
		Iterate over the items in the cart and get the products from the database.
		"""
		product_ids = [int(i) for i in self.cart.keys()]
		products = Product.objects.filter(id__in=product_ids)

		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():  # 原作写成了items
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def add(self, product, quantity=1, update_quantity=False):
		"""
		Add a product to the cart or update its quantity.
		"""
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity

		self.save()

	def remove(self, product):
		"""
		Remove a product from the cart.
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def save(self):
		# update the session cart
		self.session['cart'] = self.cart
		# mark the session as "modified" to make sure it is saved
		self.session.modified = True
		# This tells Django that the session has changed and needs to be saved.

	def clear(self):
		# empty cart
		del self.session['cart']
		self.session.modified = True

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
