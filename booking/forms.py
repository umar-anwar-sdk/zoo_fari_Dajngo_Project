from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    visit_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = [
            'full_name',
            'email',
            'phone_number',
            'cnic',
            'city',
            'address',
            'location_key_points',
            'visit_date',
            'number_of_members',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
