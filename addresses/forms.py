from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = [
    ("S", "Stripe"),
    ("P", "Paypal"),
]

class CheckoutForm(forms.Form):
    country = CountryField(blank=True, blank_label='(Select Country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))
    street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"House number and street name"
    }))
    appartment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Appartment, suite, unit etc: (optional)"
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"City or Town"
    }))
    zip = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
    }))

    shipping_country = CountryField(blank=True, blank_label='(Select Country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))
    shipping_street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"House number and street name"
    }))
    shipping_appartment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Appartment, suite, unit etc: (optional)"
    }))
    shipping_city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"City or Town"
    }))
    shipping_zip = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
    }))
    shipping_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':"form-control",
    }))

     # our methods
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        required=False, widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

