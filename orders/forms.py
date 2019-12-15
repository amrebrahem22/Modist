from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Add Coupon Code'
    }))
