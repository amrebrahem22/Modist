from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from .models import Product

def index(request):
    return render(request, 'index.html')


class Shop(ListView):
    model = Product
    paginate_by = 8
    template_name = "shop.html"
    context_object_name = "products"


class ProductDetail(View):
    def get(self, *args, **kwargs):
        qs = get_object_or_404(Product, slug=kwargs.get('slug'))
        return render(self.request, 'product-single.html', {'product': qs})
