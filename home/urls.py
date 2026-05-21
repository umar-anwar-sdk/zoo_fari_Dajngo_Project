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
    path('contact/', contact, name='contact'),
    path('form/', form, name='form'),
    path('thankyou/', thankyou, name = 'thankyou'),
    path("signup/", views.signup, name='signup'),
    path("register/", views.signup, name='register'),
    path("login/", views.custom_login, name='site_login'),
    path('logout/', custom_logout, name='site_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path("accounts/", include('django.contrib.auth.urls')),



            # ===== GET APIs =====
            path('api/slider/', views.get_topslider_api),
            path('api/welcome_text/', views.get_welcometext_api),
            path('api/welcome_list/', views.get_welcomelist_api),
            path('api/services/', views.get_services_api),
            path('api/call/', views.get_call_api),
            path('api/category/', views.get_category_api),
            path('api/animals/', views.get_ouranimals_api),
            path('api/offers/', views.get_offers_api),
            path('api/customer/', views.get_customer_api),
            path('api/contact/', views.get_contact_api),
            path('api/membership/', views.get_membership_api),
            path('api/membership-card/', views.get_membership_card_api),
            path('api/user/', views.get_UserRegistration_api),
            path('api/address/', views.get_address_api),
            path('api/email/', views.get_email_api),



            # ===== POST APIs =====
            path('api/create/slider/', views.create_topslider_api),
            path('api/create/welcome-text/', views.create_welcometext_api),
            path('api/create/welcome-list/', views.create_welcomelist_api),
            path('api/create/services/', views.create_services_api),
            path('api/create/call/', views.create_call_api),
            path('api/create/category/', views.create_category_api),
            path('api/create/animals/', views.create_ouranimals_api),
            path('api/create/offers/', views.create_offers_api),
            path('api/create/membership/', views.create_membership_api),
            path('api/create/contact/', views.create_contact_api),
            path('api/create/customer/', views.create_customer_api),
            path('api/create/user/', views.create_UserRegistration_api),
            path('api/create/membership-card/', views.create_membershipCard_api),
            path('api/create/address/', views.create_address_api),
            path('api/create/email/', views.create_email_api),
            



            # ===== UPDATE (PATCH) APIs =====
            path('api/update/slider/<int:pk>/', views.update_topslider_api),
            path('api/update/welcome-text/<int:pk>/', views.update_welcometext_api),
            path('api/update/welcome-list/<int:pk>/', views.update_welcomelist_api),
            path('api/update/services/<int:pk>/', views.update_services_api),
            path('api/update/call/<int:pk>/', views.update_call_api),
            path('api/update/category/<int:pk>/', views.update_category_api),
            path('api/update/animals/<int:pk>/', views.update_ouranimals_api),
            path('api/update/offers/<int:pk>/', views.update_offers_api),
            path('api/update/membership/<int:pk>/', views.update_membership_api),
            path('api/update/contact/<int:pk>/', views.update_contact_api),
            path('api/update/customer/<int:pk>/', views.update_customer_api),
            path('api/update/user/<int:pk>/', views.update_UserRegistration_api),
            path('api/update/membership-card/<int:pk>/', views.update_membership_card_api),
            path('api/update/address/<int:pk>/', views.update_address_api),
            path('api/update/email/<int:pk>/', views.update_email_api),


        # ===== DELETE APIs =====
            path('api/delete/slider/<int:pk>/', views.delete_topslider_api),
            path('api/delete/welcome-text/<int:pk>/', views.delete_welcometext_api),
            path('api/delete/welcome-list/<int:pk>/', views.delete_welcomelist_api),
            path('api/delete/services/<int:pk>/', views.delete_services_api),
            path('api/delete/call/<int:pk>/', views.delete_call_api),
            path('api/delete/category/<int:pk>/', views.delete_category_api),
            path('api/delete/animals/<int:pk>/', views.delete_ouranimals_api),
            path('api/delete/offers/<int:pk>/', views.delete_offers_api),
            path('api/delete/membership/<int:pk>/', views.delete_membership_api),
            path('api/delete/contact/<int:pk>/', views.delete_contact_api),
            path('api/delete/customer/<int:pk>/', views.delete_customer_api),
            path('api/delete/user/<int:pk>/', views.delete_UserRegistration_api),
            path('api/delete/membership-card/<int:pk>/', views.delete_membership_card_api),
            path('api/delete/address/<int:pk>/', views.delete_address_api),
            path('api/delete/email/<int:pk>/', views.delete_email_api),


        

        ]



