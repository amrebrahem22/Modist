from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from django import forms
from orders.models import Order

# create a function to resolve email to username
def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

# create a view that authenticate user with email
def email_login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # username = get_user(email)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "This User in Not Active.")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login.")
            return redirect('login_view')
    return render(request, 'registration/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')

    user = get_user(request.user.email)
    order = Order.objects.filter(user=user, ordered=False)

    order_qs = []
    if order.exists():
        order_qs = order.first()

    ordered = Order.objects.filter(user=user, ordered=True)

    ordered_qs = []
    if ordered.exists():
        ordered_qs = ordered.first()

    context = {
        'user': user, 
        'order': order_qs, 
        'ordered': ordered_qs
    }

    return render(request, 'registration/profile.html', context)
