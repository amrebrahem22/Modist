from django.urls import path
from .views import BlogListView, blog_post_detail

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name="index"),
    path('<slug>/', blog_post_detail, name="detail"),
]
