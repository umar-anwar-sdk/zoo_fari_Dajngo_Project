from rest_framework import viewsets, permissions
from .models import Topslider, Welcometext, Welcomelist, Services, Call, Offers, Contact, Address, Email
from .serializers import (TopsliderSerializer, WelcometextSerializer, WelcomelistSerializer, 
                          ServicesSerializer, CallSerializer, OffersSerializer, 
                          ContactSerializer, AddressSerializer, EmailSerializer)

class IsStaffAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admin', 'staff'])

class TopsliderViewSet(viewsets.ModelViewSet):
    queryset = Topslider.objects.all()
    serializer_class = TopsliderSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class WelcometextViewSet(viewsets.ModelViewSet):
    queryset = Welcometext.objects.all()
    serializer_class = WelcometextSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class WelcomelistViewSet(viewsets.ModelViewSet):
    queryset = Welcomelist.objects.all()
    serializer_class = WelcomelistSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # Anyone can submit a contact form
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [IsStaffAdminOrReadOnly()]

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [IsStaffAdminOrReadOnly]
