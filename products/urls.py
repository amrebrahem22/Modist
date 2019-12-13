from django.urls import path
from .views import index, Shop, ProductDetail

urlpatterns = [
    path('', index, name='index'),
    path('shop/', Shop.as_view(), name='shop'),
    path('shop/<slug>/', ProductDetail.as_view(), name='product'),
]
