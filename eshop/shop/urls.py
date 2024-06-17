from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import home, product_detail, cart, register, remove_from_cart, add_to_cart
from django.conf.urls.static import static
from userprofile import views as profile_views

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('register/', register, name='register'),
    # path('login/', custom_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('profile/', profile_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    