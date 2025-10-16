from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
	STATUS_CHOICES = (
		('new', 'New'),
		('pending', 'Pending'),
		('processing', 'Processing'),
		('paid', 'Paid'),
		('shipped', 'Shipped'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	)

	PAYMENT_STATUS_CHOICES = (
		('pending', 'Pending'),
		('paid', 'Paid'),
		('failed', 'Failed'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	email = models.EmailField()
	mobile = models.CharField(max_length=20, blank=True, null=True)
	address = models.TextField()
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method = models.CharField(max_length=50, blank=True, null=True)
	transaction_id = models.CharField(max_length=200, blank=True, null=True)
	tracking_number = models.CharField(max_length=200, blank=True, null=True)
	payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'Order #{self.id} - {self.first_name} {self.last_name}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f'{self.product} x {self.quantity}'

	def total_price(self):
		return self.price * self.quantity
