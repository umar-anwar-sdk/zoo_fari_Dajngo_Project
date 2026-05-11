from rest_framework import serializers
from .models import Services, OurAnimals

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

# class OurAnimalsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OurAnimals
#         fields = '__all__'