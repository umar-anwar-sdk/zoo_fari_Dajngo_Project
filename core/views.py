from rest_framework import viewsets, permissions
from .models import Category, Animal, FamilyPackage
from .serializers import CategorySerializer, AnimalSerializer, FamilyPackageSerializer
from users.permissions import IsStaffOrAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import User
from booking.models import TicketType, Booking, IssuedTicket, Offer as BookingOffer
from home.models import Offers as HomeOffers
from users.permissions import IsAdminUser

class IsStaffAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admin', 'staff'])

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffAdminOrReadOnly,)

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (IsStaffAdminOrReadOnly,)
    pagination_class = None

class FamilyPackageViewSet(viewsets.ModelViewSet):
    queryset = FamilyPackage.objects.all()
    serializer_class = FamilyPackageSerializer
    permission_classes = (IsStaffAdminOrReadOnly,)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """Return simple counts and status summaries for dashboard."""
    data = {
        'users_count': User.objects.count(),
        'animals_count': Animal.objects.count(),
        'categories_count': Category.objects.count(),
        'packages_count': FamilyPackage.objects.count(),
        'ticket_types_count': TicketType.objects.count(),
        'bookings_count': Booking.objects.count(),
        'issued_tickets_count': IssuedTicket.objects.count(),
        'booking_offers_count': BookingOffer.objects.count(),
        'home_offers_count': HomeOffers.objects.count(),
        'bookings_by_status': {
            'pending': Booking.objects.filter(approval_status='pending').count(),
            'approved': Booking.objects.filter(approval_status='approved').count(),
            'rejected': Booking.objects.filter(approval_status='rejected').count(),
        }
    }
    return Response(data)
