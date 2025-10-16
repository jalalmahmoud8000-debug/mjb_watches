from django.db import models
from django.conf import settings

from products.models import Product


# Cart model: can be linked to a user or stored by session_key for anonymous carts
class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='carts')
	session_key = models.CharField(max_length=128, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']

	def __str__(self):
		if self.user:
			return f'Cart #{self.id} - {self.user}'
		return f'Cart #{self.id} (session={self.session_key})'

	def total_price(self):
		return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('cart', 'product')

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'

	def total_price(self):
		return self.price * self.quantity
