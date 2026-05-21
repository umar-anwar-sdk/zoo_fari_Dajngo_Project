from decimal import Decimal
from rest_framework import serializers
from core.models import FamilyPackage
from .models import TicketType, Booking, IssuedTicket, Offer, CartItem, BookingItem


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    applicable_tickets = serializers.PrimaryKeyRelatedField(many=True, queryset=TicketType.objects.all(), required=False)
    applicable_packages = serializers.PrimaryKeyRelatedField(many=True, queryset=TicketType.objects.none(), required=False)

    class Meta:
        model = Offer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicable_packages'].queryset = FamilyPackage.objects.all()


class BookingItemSerializer(serializers.ModelSerializer):
    ticket_type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all(), required=False, allow_null=True)
    package = serializers.PrimaryKeyRelatedField(queryset=FamilyPackage.objects.all(), required=False, allow_null=True)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = BookingItem
        fields = ['id', 'ticket_type', 'package', 'quantity', 'unit_price', 'line_total']
        read_only_fields = ['unit_price', 'line_total']

    def validate(self, attrs):
        if not attrs.get('ticket_type') and not attrs.get('package'):
            raise serializers.ValidationError('Ticket type or package must be selected.')
        if attrs.get('ticket_type') and attrs.get('package'):
            raise serializers.ValidationError('Only one of ticket type or package may be selected.')
        if attrs.get('quantity', 0) < 1:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    ticket_type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all(), required=False, allow_null=True)
    package = serializers.PrimaryKeyRelatedField(queryset=FamilyPackage.objects.all(), required=False, allow_null=True)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'ticket_type', 'package', 'quantity', 'unit_price', 'line_total', 'created_at', 'updated_at']
        read_only_fields = ['unit_price', 'line_total', 'created_at', 'updated_at']

    def validate(self, attrs):
        if not attrs.get('ticket_type') and not attrs.get('package'):
            raise serializers.ValidationError('Ticket type or package must be selected.')
        if attrs.get('ticket_type') and attrs.get('package'):
            raise serializers.ValidationError('Select either a ticket type or package, not both.')
        if attrs.get('quantity', 0) < 1:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            validated_data['session_key'] = session_key
        return super().create(validated_data)


class IssuedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedTicket
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    issued_ticket = IssuedTicketSerializer(read_only=True)
    items = BookingItemSerializer(many=True, read_only=True)
    cart_items = BookingItemSerializer(many=True, write_only=True, required=False)
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'full_name', 'email', 'phone_number', 'cnic', 'city', 'address',
            'location_key_points', 'number_of_members', 'visit_date', 'offer', 'original_total',
            'discount_amount', 'final_total', 'approval_status', 'payment_status', 'notes', 'booking_reference',
            'created_at', 'items', 'cart_items', 'issued_ticket',
        ]
        read_only_fields = ['id', 'user', 'original_total', 'discount_amount', 'final_total', 'approval_status', 'booking_reference', 'created_at', 'issued_ticket']

    def validate(self, attrs):
        cart_items = attrs.get('cart_items', None)
        if not cart_items:
            raise serializers.ValidationError('At least one cart item is required to complete a booking.')
        return attrs

    def create(self, validated_data):
        cart_items = validated_data.pop('cart_items', [])
        request = self.context['request']
        if request.user.is_authenticated:
            validated_data['user'] = request.user

        booking = super().create(validated_data)
        for item_data in cart_items:
            BookingItem.objects.create(
                booking=booking,
                ticket_type=item_data.get('ticket_type'),
                package=item_data.get('package'),
                quantity=item_data.get('quantity', 1),
            )
        if not booking.offer:
            from .views import calculate_cart_summary
            cart_items_objects = [BookingItem(**{
                'ticket_type': item_data.get('ticket_type'),
                'package': item_data.get('package'),
                'quantity': item_data.get('quantity', 1),
                'unit_price': item_data.get('ticket_type').price if item_data.get('ticket_type') else item_data.get('package').package_price,
            }) for item_data in cart_items]
            summary = calculate_cart_summary(cart_items_objects)
            booking.offer = summary['best_offer']
        booking.calculate_totals()
        booking.save()
        if booking.approval_status == 'approved':
            from .utils import generate_qr_code
            ticket = IssuedTicket.objects.create(booking=booking)
            ticket.qr_code.save(f'{ticket.ticket_id}.png', generate_qr_code(str(ticket.ticket_id)))
            ticket.save()
        return booking
