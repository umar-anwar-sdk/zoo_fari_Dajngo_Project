from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .models import TicketType, Booking, IssuedTicket
from .serializers import TicketTypeSerializer, BookingSerializer, IssuedTicketSerializer
from users.permissions import IsStaffOrAdminUser, IsCustomerUser
from .utils import generate_ticket_pdf

class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsStaffOrAdminUser()]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['payment_status', 'visit_date']
    search_fields = ['full_name', 'email', 'cnic']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [IsStaffOrAdminUser()]

class IssuedTicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IssuedTicket.objects.all()
    serializer_class = IssuedTicketSerializer
    permission_classes = [IsStaffOrAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['ticket_id', 'booking__full_name']

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def download_pdf(self, request, pk=None):
        ticket = self.get_object()
        pdf_data = generate_ticket_pdf(ticket)
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_id}.pdf"'
        return response
