from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.profile, name='profile'),
    path('', views.profile_view, name='profile_view'),
    path('register/', views.register, name='register'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userprofile/logout.html'), name='logout'),
    # path('create_order/', views.create_order, name='create_order'),
    # path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    # path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='userprofile/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='userprofile/password_change_done.html'), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    