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

    path('api/home/', views.get_home_api),
    path('api/about/', views.get_about_api),
    path('api/services/', views.get_services_api),
    path('api/animals/', views.get_animals_api),
    path('api/offers/', views.get_offers_api),
    path('api/contact/', views.get_contact_api),
    path('api/address/', views.get_address_api),
    path('api/email/', views.get_email_api),

    path('api/submit_contact/', views.submit_contact_api, name='submit_contact_api'),

    path('api/contact/update/<int:pk>/', views.update_contact_api),
    path('api/contact/delete/<int:pk>/', views.delete_contact_api),

]




