from django.db import models
from django.conf import settings
from products.models import Product

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
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    # get total
    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        return total

