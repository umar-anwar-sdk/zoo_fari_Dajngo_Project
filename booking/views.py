from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TicketType, Booking, IssuedTicket, Offer, CartItem, BookingItem
from .serializers import (
    TicketTypeSerializer,
    BookingSerializer,
    IssuedTicketSerializer,
    OfferSerializer,
    CartItemSerializer,
)
from .forms import BookingForm
from .utils import generate_ticket_pdf, generate_qr_code
from users.permissions import IsStaffOrAdminUser
from core.models import FamilyPackage


def get_cart_queryset(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        anon_items = CartItem.objects.filter(session_key=session_key, user__isnull=True)
        for item in anon_items:
            item.user = request.user
            item.session_key = None
            item.save()
        return CartItem.objects.filter(user=request.user)
    return CartItem.objects.filter(session_key=session_key)


def get_active_offers():
    today = timezone.now().date()
    return Offer.objects.filter(status='active', start_date__lte=today, end_date__gte=today)


def offer_applies_to_item(offer, item):
    if not offer.applicable_tickets.exists() and not offer.applicable_packages.exists():
        return True
    if item.ticket_type and offer.applicable_tickets.filter(pk=item.ticket_type.pk).exists():
        return True
    if item.package and offer.applicable_packages.filter(pk=item.package.pk).exists():
        return True
    return False


def calculate_cart_summary(cart_items):
    original_total = sum(item.line_total for item in cart_items)
    offers = []
    best_offer = None
    best_discount = Decimal('0.00')
    for offer in get_active_offers():
        eligible_total = sum(
            item.line_total for item in cart_items if offer_applies_to_item(offer, item)
        )
        discount = offer.calculate_discount(eligible_total)
        offers.append({
            'offer': offer,
            'eligible_total': eligible_total,
            'discount': discount,
        })
        if discount > best_discount:
            best_discount = discount
            best_offer = offer
    final_total = original_total - best_discount
    return {
        'original_total': original_total,
        'discount_amount': best_discount,
        'final_total': final_total,
        'active_offers': [entry['offer'] for entry in offers],
        'best_offer': best_offer,
        'offer_details': offers,
    }


def ticket_list(request):
    ticket_types = TicketType.objects.filter(status='active')
    packages = FamilyPackage.objects.filter(status='active')
    active_offers = get_active_offers()
    context = {
        'ticket_types': ticket_types,
        'packages': packages,
        'offers': active_offers,
    }
    return render(request, 'booking/ticket_list.html', context)


def add_to_cart(request):
    if request.method != 'POST':
        return redirect('booking:ticket_list')

    ticket_type_id = request.POST.get('ticket_type')
    package_id = request.POST.get('package')
    quantity = int(request.POST.get('quantity', 1))
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    cart_queryset = get_cart_queryset(request)

    if ticket_type_id:
        ticket = get_object_or_404(TicketType, pk=ticket_type_id, status='active')
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else session_key,
            ticket_type=ticket,
            package=None,
            defaults={'quantity': quantity},
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
    elif package_id:
        package = get_object_or_404(FamilyPackage, pk=package_id, status='active')
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else request.session.session_key,
            package=package,
            ticket_type=None,
            defaults={'quantity': quantity},
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
    return redirect('booking:cart_detail')


def cart_detail(request):
    cart_items = get_cart_queryset(request)
    totals = calculate_cart_summary(cart_items)
    return render(request, 'booking/cart_detail.html', {
        'cart_items': cart_items,
        'totals': totals,
    })


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(get_cart_queryset(request), pk=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = max(1, quantity)
        cart_item.save()
    return redirect('booking:cart_detail')


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(get_cart_queryset(request), pk=item_id)
    cart_item.delete()
    return redirect('booking:cart_detail')


def checkout(request):
    cart_items = get_cart_queryset(request)
    if not cart_items.exists():
        return redirect('booking:ticket_list')

    totals = calculate_cart_summary(cart_items)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.offer = totals['best_offer']
            booking.save()
            for item in cart_items:
                BookingItem.objects.create(
                    booking=booking,
                    ticket_type=item.ticket_type,
                    package=item.package,
                    quantity=item.quantity,
                )
            if cart_items.count() == 1:
                first_item = cart_items.first()
                if first_item.ticket_type:
                    booking.selected_ticket = first_item.ticket_type
                    booking.selected_package = None
                elif first_item.package:
                    booking.selected_package = first_item.package
                    booking.selected_ticket = None
            booking.calculate_totals()
            booking.payment_status = 'paid'
            booking.approval_status = 'pending'
            booking.save()
            cart_items.delete()
            return redirect('booking:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'booking/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'totals': totals,
    })


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})


def my_bookings(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view your bookings.')
        return redirect('site_login')

    bookings = Booking.objects.filter(user=request.user).order_by('-visit_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


def ticket_download(request, ticket_id):
    ticket = get_object_or_404(IssuedTicket, ticket_id=ticket_id)
    if ticket.booking.user != request.user and request.user.role not in ['admin', 'staff']:
        messages.warning(request, 'You do not have permission to view this ticket.')
        return redirect('home')
    return render(request, 'booking/ticket_download.html', {'ticket': ticket})


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsStaffOrAdminUser()]


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsStaffOrAdminUser()]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ticket_type', 'package']
    search_fields = ['ticket_type__name', 'package__package_name']

    def get_queryset(self):
        return get_cart_queryset(self.request)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.context['request'] = self.request
        serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def clear(self, request):
        items = get_cart_queryset(request)
        items.delete()
        return Response({'detail': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['approval_status', 'payment_status', 'visit_date', 'offer']
    search_fields = ['full_name', 'email', 'cnic']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role in ['admin', 'staff']:
                return Booking.objects.all()
            return Booking.objects.filter(user=user)
        return Booking.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'calculate']:
            return [permissions.AllowAny()]
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsStaffOrAdminUser()]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def calculate(self, request):
        cart_items_data = request.data.get('cart_items', [])
        cart_items = []
        for item_data in cart_items_data:
            if item_data.get('ticket_type'):
                ticket = get_object_or_404(TicketType, pk=item_data['ticket_type'])
                cart_item = CartItem(ticket_type=ticket, quantity=item_data.get('quantity', 1), unit_price=ticket.price)
            elif item_data.get('package'):
                package = get_object_or_404(FamilyPackage, pk=item_data['package'])
                cart_item = CartItem(package=package, quantity=item_data.get('quantity', 1), unit_price=package.package_price)
            else:
                continue
            cart_items.append(cart_item)
        summary = calculate_cart_summary(cart_items)
        return Response({
            'original_total': summary['original_total'],
            'discount_amount': summary['discount_amount'],
            'final_total': summary['final_total'],
            'best_offer': OfferSerializer(summary['best_offer']).data if summary['best_offer'] else None,
        })

    @action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdminUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.approval_status = 'approved'
        booking.approval_notes = request.data.get('approval_notes', '')
        booking.save()
        booking.issue_ticket()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsStaffOrAdminUser])
    def bulk_approve(self, request):
        """Bulk approve bookings and issue tickets. Expects JSON: {"ids": [1,2,3]}"""
        ids = request.data.get('ids', [])
        if not isinstance(ids, (list, tuple)):
            return Response({'detail': 'ids must be a list of booking IDs.'}, status=400)
        bookings = Booking.objects.filter(pk__in=ids)
        for booking in bookings:
            if booking.approval_status != 'approved':
                booking.approval_status = 'approved'
                booking.approval_notes = 'Approved via bulk API action.'
                booking.save()
                booking.issue_ticket()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsStaffOrAdminUser])
    def bulk_reject(self, request):
        """Bulk reject bookings. Expects JSON: {"ids": [1,2], "notes": "reason"}"""
        ids = request.data.get('ids', [])
        notes = request.data.get('notes', 'Rejected via bulk API action.')
        if not isinstance(ids, (list, tuple)):
            return Response({'detail': 'ids must be a list of booking IDs.'}, status=400)
        bookings = Booking.objects.filter(pk__in=ids)
        for booking in bookings:
            if booking.approval_status != 'rejected':
                booking.reject(notes=notes)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdminUser])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.reject(notes=request.data.get('approval_notes', 'Rejected by staff/admin'))
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class IssuedTicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IssuedTicket.objects.all()
    serializer_class = IssuedTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['ticket_id', 'booking__full_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role not in ['admin', 'staff']:
            return IssuedTicket.objects.filter(booking__user=user)
        return IssuedTicket.objects.all()

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def download_pdf(self, request, pk=None):
        ticket = self.get_object()
        if request.user.role not in ['admin', 'staff'] and ticket.booking.user != request.user:
            return Response({'detail': 'Not authorized to download this ticket.'}, status=403)

        pdf_data = generate_ticket_pdf(ticket)
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_id}.pdf"'
        return response
