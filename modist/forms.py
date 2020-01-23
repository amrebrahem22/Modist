from django import forms

class ContactForm(forms.Form):
    name= forms.CharField(max_length=500, label="Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email= forms.EmailField(max_length=500, label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    subject= forms.CharField(max_length=500, label="Subject", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message= forms.CharField(label='',widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your Message here', 'class': 'form-control'}))