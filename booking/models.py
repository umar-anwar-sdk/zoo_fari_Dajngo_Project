from django.db import models
from django.utils import timezone
from core.models import FamilyPackage
from users.models import User
from .utils import generate_qr_code
import uuid
from decimal import Decimal


class TicketType(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    applicable_tickets = models.ManyToManyField(TicketType, blank=True, related_name='offers')
    applicable_packages = models.ManyToManyField(FamilyPackage, blank=True, related_name='offers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date

    def calculate_discount(self, amount):
        if not amount:
            return Decimal('0.00')
        if self.discount_type == 'percentage':
            discount = amount * self.discount_value / Decimal('100')
            return discount.quantize(Decimal('0.01'))
        return min(amount, self.discount_value)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(FamilyPackage, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def clean(self):
        if not self.ticket_type and not self.package:
            raise ValueError('A cart item must include a ticket type or package.')
        if self.ticket_type and self.package:
            raise ValueError('A cart item cannot include both ticket type and package.')
        if self.quantity < 1:
            raise ValueError('Quantity must be at least 1.')

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if self.ticket_type:
            self.unit_price = self.ticket_type.price
        elif self.package:
            self.unit_price = self.package.package_price
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        item_name = self.ticket_type.name if self.ticket_type else self.package.package_name
        return f"Cart item: {item_name} x{self.quantity}"


class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    cnic = models.CharField(max_length=20, verbose_name='CNIC/ID Card')
    city = models.CharField(max_length=100)
    address = models.TextField()
    location_key_points = models.TextField(blank=True)
    number_of_members = models.PositiveIntegerField()
    visit_date = models.DateField()
    selected_package = models.ForeignKey(FamilyPackage, on_delete=models.SET_NULL, null=True, blank=True)
    selected_ticket = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    original_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approval_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    approval_notes = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    booking_reference = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_reference} by {self.full_name}"

    def approve(self):
        self.approval_status = 'approved'
        self.approval_notes = ''
        self.save()
        return self.issue_ticket()

    def reject(self, notes=''):
        self.approval_status = 'rejected'
        self.approval_notes = notes
        self.save()
        if hasattr(self, 'issued_ticket'):
            self.issued_ticket.status = 'cancelled'
            self.issued_ticket.save()
        return self

    def issue_ticket(self):
        ticket, created = IssuedTicket.objects.get_or_create(booking=self)
        if created or not ticket.qr_code:
            ticket.qr_code.save(f'{ticket.ticket_id}.png', generate_qr_code(str(ticket.ticket_id)))
            ticket.save()
        return ticket

    def calculate_totals(self):
        total = sum(item.line_total for item in self.items.all())
        self.original_total = total
        discount = 0
        if self.offer and self.offer.is_active:
            discount = self.offer.calculate_discount(total)
        self.discount_amount = discount
        self.final_total = total - discount
        return self.original_total, self.discount_amount, self.final_total


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(FamilyPackage, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def clean(self):
        if not self.ticket_type and not self.package:
            raise ValueError('Booking item must include a ticket type or package.')
        if self.ticket_type and self.package:
            raise ValueError('Booking item cannot include both ticket type and package.')
        if self.quantity < 1:
            raise ValueError('Quantity must be at least 1.')

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if self.ticket_type:
            self.unit_price = self.ticket_type.price
        elif self.package:
            self.unit_price = self.package.package_price
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        item_name = self.ticket_type.name if self.ticket_type else self.package.package_name
        return f"{item_name} x{self.quantity}"


class IssuedTicket(models.Model):
    STATUS_CHOICES = (
        ('valid', 'Valid'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
    )
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='issued_ticket')
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='valid')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ticket_id)
