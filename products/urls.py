from django.urls import path
from .views import Shop, ProductDetail

urlpatterns = [
    path('shop/', Shop.as_view(), name='shop'),
    path('shop/<slug>/', ProductDetail.as_view(), name='product'),
]
