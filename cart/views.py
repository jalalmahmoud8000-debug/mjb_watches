from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem


def _get_or_create_cart(request):
	if request.user.is_authenticated:
		cart, _ = Cart.objects.get_or_create(user=request.user)
		return cart
	session_key = request.session.session_key or request.session.create()
	cart, _ = Cart.objects.get_or_create(session_key=session_key)
	return cart


def add_to_cart(request):
	if request.method != 'POST':
		return redirect('products:list')

	slug = request.POST.get('slug')
	qty = int(request.POST.get('quantity', 1))
	product = get_object_or_404(Product, slug=slug, is_active=True)

	cart = _get_or_create_cart(request)

	# price snapshot
	price = product.price

	item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'price': price, 'quantity': qty})
	if not created:
		item.quantity += qty
		item.price = price
		item.save()

	return redirect('cart:detail')


def cart_detail(request):
	cart = _get_or_create_cart(request)
	return render(request, 'cart/detail.html', {'cart': cart})


def remove_item(request, item_id):
	cart = _get_or_create_cart(request)
	CartItem.objects.filter(id=item_id, cart=cart).delete()
	return redirect('cart:detail')


def update_quantity(request, item_id):
	if request.method != 'POST':
		return redirect('cart:detail')
	qty = int(request.POST.get('quantity', 1))
	cart = _get_or_create_cart(request)
	item = CartItem.objects.filter(id=item_id, cart=cart).first()
	if not item:
		return redirect('cart:detail')
	if qty <= 0:
		item.delete()
	else:
		item.quantity = qty
		item.save()
	return redirect('cart:detail')
