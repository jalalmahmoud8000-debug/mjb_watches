from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.add_to_cart, name='add'),
    path('', views.cart_detail, name='detail'),
    path('remove/<int:item_id>/', views.remove_item, name='remove'),
    path('update/<int:item_id>/', views.update_quantity, name='update'),
]
