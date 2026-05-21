from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketTypeViewSet, BookingViewSet, IssuedTicketViewSet, OfferViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'ticket-types', TicketTypeViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'cart', CartItemViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'issued-tickets', IssuedTicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
