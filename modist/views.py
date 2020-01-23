from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import get_template

from blog.models import Post
from products.models import Product
from django.contrib import messages
from accounts.models import Subscribers

def index(request):
    trending = Product.objects.all().order_by('-purchasing')[:6]
    most_viewed = Product.objects.all().order_by('-views')[:4]
    posts = Post.objects.all().order_by('-timestamp')[:3]

    if request.method == "POST":
        email = request.POST.get('email_subscription')

        instance = Subscribers(email=email)
        instance.save()
        messages.success(request, 'Email Added we will Notify you with all News.')
        return redirect('index')

    context = {
        'trending': trending,
        'most_viewed': most_viewed,
        'posts': posts
    }
    return render(request, 'index.html', context)

def contactview(request):
    name=''
    email=''
    message=''


    form= ContactForm(request.POST or None)
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        subject= form.cleaned_data.get("subject")
        message=form.cleaned_data.get("message")

        if request.user.is_authenticated:
            subject= str(request.user.get_full_name()) + " > " + subject
        else:
            subject= "A Visitor's message" + " > " + subject
        
        template = get_template('contact_form.txt')
        content = template.render({'name': name, 'email': email, 'message': message})


        message = "Subject: From > {} {}\n\nMessage: {}".format(subject, email, message)
        # mail_admins(subject, message)
        email =EmailMessage(subject, content, 'Modist Store', [settings.EMAIL_HOST_USER], headers={'Reply to': email})
        email.send()
        # send_mail(subject, message, email, [settings.EMAIL_HOST_USER])
        messages.success(request, 'Message Successfully Sent.')
        return redirect('contact')

    form= ContactForm()
    context= {'form': form}

    return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html')