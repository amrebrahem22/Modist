from django.db import models
from django.conf import settings
from products.models import Product
from addresses.models import Address, Payment

User = settings.AUTH_USER_MODEL

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    # get total without discount
    def get_total_price(self):
        return self.quantity * self.item.price

    # get total with discount
    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    # get saved amount
    def amount_saved(self):
        return self.get_total_price() - self.get_total_discount_price()

    # get the final price
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    shipping_address = models.ForeignKey(Address, related_name="ShippingAddress", on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name="BillingAddress", on_delete=models.SET_NULL, blank=True, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon         = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    # get total
    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        if self.coupon:
            total -= int(self.coupon.amount)
        return total


class Coupon(models.Model):
    code    = models.CharField(max_length=15)
    amount  = models.FloatField()

    def __str__(self):
        return self.code


# then create the refound model
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"