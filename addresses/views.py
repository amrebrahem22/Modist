from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.conf import settings
from django.contrib import messages
from orders.models import Order
from .models import Address, Payment
from .forms import CheckoutForm
from products.models import Product

import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# this method will generate a random string
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class Checkout(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = get_object_or_404(Order, user=self.request.user, ordered=False)

        context = {
            'form': form,
            'order': order,
        }

        shipping_qs = Address.objects.filter(user=self.request.user, default=True, address_type="S")
        if shipping_qs.exists():
            context.update({'default_shipping_address': shipping_qs[0]})

        billing_qs = Address.objects.filter(user=self.request.user, default=True, address_type="B")
        if billing_qs.exists():
            context.update({'default_billing_address': billing_qs[0]})
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = get_object_or_404(Order, user=self.request.user, ordered=False)
        print(form.is_valid())
        if form.is_valid():
            # get the order
            print(form.cleaned_data)
            billing_country = form.cleaned_data.get('country')
            billing_street_address = form.cleaned_data.get('street_address')
            billing_appartment = form.cleaned_data.get('appartment')
            billing_city = form.cleaned_data.get('city')
            billing_zip = form.cleaned_data.get('zip')
            billing_phone = form.cleaned_data.get('phone')

            shipping_country = form.cleaned_data.get('shipping_country')
            shipping_street_address = form.cleaned_data.get('shipping_street_address')
            shipping_appartment = form.cleaned_data.get('shipping_appartment')
            shipping_city = form.cleaned_data.get('shipping_city')
            shipping_zip = form.cleaned_data.get('shipping_zip')
            shipping_phone = form.cleaned_data.get('shipping_phone')

            set_default_shipping = form.cleaned_data.get('set_default_shipping')
            use_default_shipping = form.cleaned_data.get('use_default_shipping')
            set_default_billing = form.cleaned_data.get('set_default_billing')
            use_default_billing = form.cleaned_data.get('use_default_billing')
            same_billing_address = form.cleaned_data.get('same_billing_address')

            payment_option = form.cleaned_data.get('payment_option')
            

            if use_default_billing:
                print("using default billing")
                billing_address_qs = Address.objects.filter(user=self.request.user, default=True, address_type="B")

                if billing_address_qs.exists():
                    billing_address = billing_address_qs.first()
                    order.billing_address=billing_address
                    order.save()
                else:
                    messages.info(self.request, "No default shipping address available")
                    return redirect('checkout:index')

            else:
                if is_valid_form([billing_country, billing_street_address, billing_appartment, billing_city, billing_zip, billing_phone]):
                    print("billing form is valid")
                    billing_address = Address(
                        user=self.request.user,
                        country=billing_country,
                        street_address=billing_street_address,
                        appartment=billing_appartment,
                        city=billing_city,
                        zip=billing_zip,
                        phone=billing_phone,
                        address_type="B",
                    )
                    billing_address.save()

                    if set_default_billing:
                        billing_address.default=True
                        billing_address.save()

                    order.billing_address=billing_address
                    order.save()
                else:
                    messages.info(self.request, "Please fill in the required shipping address fields")


            if use_default_shipping:
                print("using default shipping")
                shipping_address_qs = Address.objects.filter(user=self.request.user, default=True, address_type="S")

                if shipping_address_qs.exists():
                    shipping_address = shipping_address_qs.first()
                    order.shipping_address=shipping_address
                    order.save()
                else:
                    messages.info(self.request, "No default shipping address available")
                    return redirect('checkout:index')
            else:
                if is_valid_form([shipping_country, shipping_street_address, shipping_appartment, shipping_city, shipping_zip, shipping_phone]):
                    print("shipping address form is valid")
                    shipping_address = Address(
                        user=self.request.user,
                        country=shipping_country,
                        street_address=shipping_street_address,
                        appartment=shipping_appartment,
                        city=shipping_city,
                        zip=shipping_zip,
                        phone=shipping_phone,
                        address_type="S",
                    )

                    shipping_address.save()

                    if set_default_shipping:
                        shipping_address.default=True
                        shipping_address.save()

                    order.shipping_address=shipping_address
                    order.save()
            
            if same_billing_address:
                print('same address set')
                shipping_address = billing_address
                shipping_address.pk = None
                shipping_address.save()
                shipping_address.address_type="S"
                shipping_address.save()

                if set_default_shipping:
                    shipping_address.default=True
                    shipping_address.save()

                order.shipping_address=shipping_address
                order.save()
        
            if payment_option == 'S':
                return redirect('checkout:payment', payment_option='stripe')
            elif payment_option == 'P':
                return redirect('checkout:payment', payment_option='paypal')
            else:
                messages.warning(
                    self.request, "Invalid payment option selected")
                return redirect('checkout:index')
            
        return redirect('checkout:index')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                qs = get_object_or_404(Product,pk=item.id)
                qs.purchasing += int(item.quantity) or 1
                qs.save()
                item.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")