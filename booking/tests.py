from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TicketType, Offer
from core.models import FamilyPackage


class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketType.objects.create(
            name='Standard Ticket',
            price='2000.00',
            description='Adult ticket',
            status='active',
        )
        self.package = FamilyPackage.objects.create(
            package_name='Family Pass',
            package_price='6500.00',
            duration='1 Day',
            benefits='Family entry and free parking',
            number_of_people=4,
            status='active',
        )
        self.offer = Offer.objects.create(
            title='Summer Discount',
            description='10% off selected tickets',
            discount_type='percentage',
            discount_value='10.00',
            start_date='2020-01-01',
            end_date='2099-12-31',
            status='active',
        )
        self.offer.applicable_tickets.add(self.ticket)

    def test_cart_item_creation_and_calculation(self):
        response = self.client.post('/api/booking/cart/', {
            'ticket_type': self.ticket.id,
            'quantity': 3,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        calculate_response = self.client.post('/api/booking/bookings/calculate/', {
            'cart_items': [
                {'ticket_type': self.ticket.id, 'quantity': 3}
            ]
        }, format='json')
        self.assertEqual(calculate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(str(calculate_response.data['original_total'])), Decimal('6000.00'))
        self.assertEqual(Decimal(str(calculate_response.data['discount_amount'])), Decimal('600.00'))
        self.assertEqual(Decimal(str(calculate_response.data['final_total'])), Decimal('5400.00'))

    def test_booking_checkout_creates_issued_ticket(self):
        payload = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '03001234567',
            'cnic': '12345-1234567-1',
            'city': 'Karachi',
            'address': '123 Zoo Lane',
            'location_key_points': 'Near main gate',
            'number_of_members': 3,
            'visit_date': '2026-12-01',
            'notes': 'Please reserve a family spot.',
            'cart_items': [
                {'ticket_type': self.ticket.id, 'quantity': 3}
            ]
        }
        response = self.client.post('/api/booking/bookings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['original_total'], '6000.00')
        self.assertEqual(response.data['discount_amount'], '600.00')
        self.assertEqual(response.data['final_total'], '5400.00')
        self.assertIn('issued_ticket', response.data)
