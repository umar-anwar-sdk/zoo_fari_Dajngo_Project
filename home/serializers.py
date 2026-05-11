from rest_framework import serializers
from home.models import Address, Contact, Email, Offers, Services, OurAnimals, topslider, Welcometext, Welcomelist

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurAnimals
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = topslider
        fields = '__all__'

class WelcomeTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcometext
        fields = '__all__'

class WelcomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcomelist
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