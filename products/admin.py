from django.contrib import admin

from .models import Product, ProductSizes

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'rating']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizes)
