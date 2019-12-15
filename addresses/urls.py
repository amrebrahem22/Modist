from django.urls import path
from .views import Checkout, PaymentView

app_name ='checkout'

urlpatterns = [
    path('', Checkout.as_view(), name='index'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]
