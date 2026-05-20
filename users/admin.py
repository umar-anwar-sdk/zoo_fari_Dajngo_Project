from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved_staff', 'is_staff', 'is_active')
    list_filter = ('role', 'is_approved_staff', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'is_approved_staff')}),
    )
    
    actions = ['approve_staff', 'reject_staff']
    
    def approve_staff(self, request, queryset):
        queryset.update(is_approved_staff=True, is_active=True, is_staff=True)
    approve_staff.short_description = "Approve selected staff members"
    
    def reject_staff(self, request, queryset):
        queryset.update(is_approved_staff=False, is_active=False)
    reject_staff.short_description = "Reject/Deactivate selected staff members"
