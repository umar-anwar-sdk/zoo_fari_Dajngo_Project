from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (TopsliderViewSet, WelcometextViewSet, WelcomelistViewSet, 
                    ServicesViewSet, CallViewSet, OffersViewSet, 
                    ContactViewSet, AddressViewSet, EmailViewSet)

router = DefaultRouter()
router.register(r'sliders', TopsliderViewSet)
router.register(r'welcome-texts', WelcometextViewSet)
router.register(r'welcome-lists', WelcomelistViewSet)
router.register(r'services', ServicesViewSet)
router.register(r'calls', CallViewSet)
router.register(r'offers', OffersViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'emails', EmailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
