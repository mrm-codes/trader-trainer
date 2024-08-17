from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('user_dash', views.user_dash, name='user_dash'),
]