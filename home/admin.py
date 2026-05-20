from django.contrib import admin
from .models import Topslider, Welcometext, Welcomelist, Services, Call, Offers, Contact, Address, Email

@admin.register(Topslider)
class TopsliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

@admin.register(Welcometext)
class WelcometextAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Welcomelist)
class WelcomelistAdmin(admin.ModelAdmin):
    list_display = ('list',)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'number')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email',)
