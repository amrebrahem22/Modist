from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from .models import Product

class Shop(ListView):
    model = Product
    paginate_by = 8
    template_name = "shop.html"
    context_object_name = "products"


class ProductDetail(View):
    def get(self, *args, **kwargs):
        qs = get_object_or_404(Product, slug=kwargs.get('slug'))
        qs.views += 1
        qs.save()
        return render(self.request, 'product-single.html', {'product': qs})
