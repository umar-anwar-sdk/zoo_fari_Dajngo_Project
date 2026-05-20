from rest_framework import serializers
from .models import TicketType, Booking, IssuedTicket

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'

class IssuedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedTicket
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    issued_ticket = IssuedTicketSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('selected_package') and not attrs.get('selected_ticket'):
             raise serializers.ValidationError("Either a package or a ticket must be selected.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
        booking = super().create(validated_data)
        
        # Generate ticket automatically
        from .utils import generate_qr_code
        ticket = IssuedTicket.objects.create(booking=booking)
        ticket.qr_code.save(f'{ticket.ticket_id}.png', generate_qr_code(str(ticket.ticket_id)))
        ticket.save()
        
        return booking
