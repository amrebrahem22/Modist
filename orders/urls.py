from django.urls import path
from .views import add_to_cart, remove_from_cart, Cart, remove_single_item_from_cart


app_name = "cart"

urlpatterns = [
    path('', Cart.as_view(), name="index"),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart')
]