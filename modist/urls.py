from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path , path, include
# from django.contrib.auth import views as auth_views
from accounts.views import signup, email_login_view, logout_view, profile
from .views import contactview, index, about

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('', index, name='index'),
    path('signup/', signup, name="signup_view"),
    path('login/', email_login_view, name="127.0.0.1:8000"),
    path('logout/', logout_view, name="logout_redirect"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profile, name='profile'),
    path('contact/', contactview, name='contact'),
    path('about/', about, name='about'),
    # re_path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # re_path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    path('', include('products.urls')),
    path('cart/', include('orders.urls', namespace="cart")),
    path('checkout/', include('addresses.urls', namespace='checkout')),
    path('blog/', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
