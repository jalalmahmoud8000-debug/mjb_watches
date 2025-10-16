from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from cart.models import CartItem
from .models import Order, OrderItem


def checkout(request):
	# Simple checkout form (no payment integration)
	cart = None
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user).first()
	else:
		session_key = request.session.session_key
		if session_key:
			cart = Cart.objects.filter(session_key=session_key).first()

	if not cart or not cart.items.exists():
		return redirect('products:list')

	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		address = request.POST.get('address')
		payment_method = request.POST.get('payment_method')

		total = cart.total_price()

		# For Instapay, e-wallet and COD per requirements: payment is collected after delivery -> pending
		payment_status = 'pending'

		order = Order.objects.create(
			user=request.user if request.user.is_authenticated else None,
			first_name=first_name,
			last_name=last_name,
			email=email,
			mobile=mobile,
			address=address,
			total_amount=total,
			status='processing',
			payment_method=payment_method,
			payment_status=payment_status
		)

		# create order items from cart items
		for ci in cart.items.all():
			OrderItem.objects.create(order=order, product=ci.product, quantity=ci.quantity, price=ci.price)

		# clear cart
		cart.items.all().delete()

		return redirect('orders:thankyou', order.id)

	# GET -> render checkout form
	return render(request, 'orders/checkout.html', {'cart': cart})


def order_list(request):
	if request.user.is_authenticated:
		qs = Order.objects.filter(user=request.user).order_by('-created_at')
	else:
		qs = Order.objects.none()
	return render(request, 'orders/list.html', {'orders': qs})


def order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	# restrict access: only owner or staff
	if order.user and request.user.is_authenticated and order.user != request.user and not request.user.is_staff:
		return redirect('home')
	if not order.user and not request.user.is_staff:
		# anonymous orders are viewable only via staff tools in this simple app
		return redirect('home')
	return render(request, 'orders/detail.html', {'order': order})


def thankyou(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'orders/thankyou.html', {'order': order})
