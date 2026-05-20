from rest_framework import serializers
from .models import Topslider, Welcometext, Welcomelist, Services, Call, Offers, Contact, Address, Email

class TopsliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topslider
        fields = '__all__'

class WelcometextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcometext
        fields = '__all__'

class WelcomelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcomelist
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'