from django.contrib import admin
from .models import TicketType, Offer, CartItem, Booking, BookingItem, IssuedTicket

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'description')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'discount_value', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'discount_type')
    search_fields = ('title', 'description')
    filter_horizontal = ('applicable_tickets', 'applicable_packages')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'ticket_type', 'package', 'quantity', 'unit_price', 'updated_at')
    list_filter = ('ticket_type', 'package')
    search_fields = ('ticket_type__name', 'package__package_name', 'session_key')


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0
    readonly_fields = ('unit_price', 'line_total')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'visit_date', 'payment_status', 'approval_status', 'original_total', 'discount_amount', 'final_total', 'created_at')
    list_filter = ('payment_status', 'approval_status', 'visit_date')
    search_fields = ('full_name', 'email', 'cnic', 'phone_number', 'booking_reference')
    readonly_fields = ('created_at', 'booking_reference', 'original_total', 'discount_amount', 'final_total')
    inlines = [BookingItemInline]
    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        for booking in queryset:
            if booking.approval_status != 'approved':
                booking.approval_status = 'approved'
                booking.approval_notes = 'Approved via admin action.'
                booking.save()
                booking.issue_ticket()
        self.message_user(request, 'Selected bookings have been approved and tickets issued.')
    approve_bookings.short_description = 'Approve selected bookings and issue tickets'

    def reject_bookings(self, request, queryset):
        for booking in queryset:
            if booking.approval_status != 'rejected':
                booking.reject(notes='Rejected via admin action.')
        self.message_user(request, 'Selected bookings have been rejected.')
    reject_bookings.short_description = 'Reject selected bookings'


@admin.register(IssuedTicket)
class IssuedTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'booking', 'status', 'issued_at')
    list_filter = ('status', 'issued_at')
    search_fields = ('ticket_id', 'booking__full_name')
    readonly_fields = ('ticket_id', 'issued_at')
