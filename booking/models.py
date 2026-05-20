from django.db import models
from core.models import FamilyPackage
from users.models import User
import uuid

class TicketType(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

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
    cnic = models.CharField(max_length=20, verbose_name="CNIC/ID Card")
    city = models.CharField(max_length=100)
    address = models.TextField()
    location_key_points = models.TextField(blank=True)
    number_of_members = models.PositiveIntegerField()
    visit_date = models.DateField()
    
    # Either package or ticket type must be selected
    selected_package = models.ForeignKey(FamilyPackage, on_delete=models.SET_NULL, null=True, blank=True)
    selected_ticket = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.full_name}"

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
