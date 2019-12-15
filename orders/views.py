from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from products.models import Product
from .models import Order, OrderItem
from .forms import CouponForm
from orders.models import Coupon


class Cart(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            coupon_form = CouponForm()
            context = {
                'object': order,
                'couponform': coupon_form,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request, slug):
    product_qs = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=product_qs,
        user=request.user ,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=product_qs.slug).exists():
            order_item.quantity += 1
            order_item.save()

            messages.info(request, "Product Quantity Successfully Updated.")
            return redirect('product', slug=slug)
        else:
            order_item.quantity = 1
            order_item.save()
            order.items.add(order_item)
            messages.info(request, "Product Added Successfully to your Cart")
            return redirect('product', slug=slug)
    
    else:
        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now()
        )
        order.items.add(order_item)
        messages.info(request, "Product Added Successfully to your Cart")
        return redirect('product', slug=slug)

@login_required
def remove_from_cart(request, slug):
    product_qs = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs.first()
        if order.items.filter(item__slug=product_qs.slug).exists():
            order_item = OrderItem.objects.filter(
                item=product_qs,
                user=request.user ,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order.save()

            messages.info(request, "Product Removed Successfully From the Cart.")
            return redirect('product', slug=slug)
        else:
            messages.info(request, "Product is not in your Cart")
            return redirect('product', slug=slug)
    
    else:
        messages.info(request, " your Cart is Empty.")
        return redirect('product', slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:index")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This Coupon Does not Exist.")
        return redirect("cart:index")


class AddCoupon(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = self.request.POST.get('code')
                coupon = get_coupon(self.request, code)
                order = Order.objects.filter(
                    user=self.request.user,
                    ordered=False
                )[0]

                order.coupon = coupon
                order.save()
                
                messages.success(self.request, "Successfully added coupon")
                return redirect("cart:index")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("cart:index")
