from django.contrib.auth.views import LogoutView
from django.urls import path, include

from home import views
from home.views import home, about, services, animals, membership, visting, testmonial, contact, form, thankyou, signup, \
    custom_logout, order_membership

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('animals/', animals, name='animals'),
    path('membership/', membership, name='membership'),
    path('order_membership/', order_membership, name='order_membership'),
    path('visting/', visting, name='visting'),
    path('testmonial/', testmonial, name='testmonial'),
    path('contect/', contact, name='contect'),
    path('form/', form, name='form'),
    path('thankyou/', thankyou, name = 'thankyou'),
    path("signup/", views.signup, name='signup'),
    path('logout/', custom_logout, name='logout'),
    path("accounts/", include('django.contrib.auth.urls')),



]
