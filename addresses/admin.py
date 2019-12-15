from django.contrib import admin

from .models import Address, Payment

admin.site.register(Address)
admin.site.register(Payment)
