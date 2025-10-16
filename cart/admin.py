from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 0
	readonly_fields = ('price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'session_key', 'created_at', 'updated_at')
	inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('cart', 'product', 'quantity', 'price', 'added_at')
