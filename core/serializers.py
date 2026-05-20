from rest_framework import serializers
from .models import Category, Animal, FamilyPackage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'

class FamilyPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyPackage
        fields = '__all__'
