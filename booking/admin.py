from django.contrib import admin
from .models import TicketType, Booking, IssuedTicket

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'visit_date', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'visit_date')
    search_fields = ('full_name', 'email', 'cnic', 'phone_number')
    readonly_fields = ('created_at',)

@admin.register(IssuedTicket)
class IssuedTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'booking', 'status', 'issued_at')
    list_filter = ('status', 'issued_at')
    search_fields = ('ticket_id', 'booking__full_name')
    readonly_fields = ('ticket_id', 'issued_at')
