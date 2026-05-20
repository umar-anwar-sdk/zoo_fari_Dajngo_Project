from django.contrib import admin
from .models import Category, Animal, FamilyPackage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'age', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')

@admin.register(FamilyPackage)
class FamilyPackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'package_price', 'duration', 'number_of_people', 'status')
    list_filter = ('status',)
    search_fields = ('package_name', 'benefits')
