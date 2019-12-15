from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

ADDRESS_CHOICES = [
    ("S", "Shipping Address"),
    ("B", "Billing Address"),
]

class Address(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country         = CountryField()
    street_address  = models.CharField(max_length=100)
    appartment      = models.CharField(max_length=100)
    city            = models.CharField(max_length=20)
    zip             = models.CharField(max_length=8)
    phone           = models.CharField(max_length=11)
    address_type    = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default         = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username