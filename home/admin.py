from django.contrib import admin

from home.models import Topslider, Welcomelist, Welcometext, Services, Call, Offers, Contact, Customer, Address, Email


# Register your models here.


class topsliderAdmin(admin.ModelAdmin):
    list_display = ['image']


admin.site.register(Topslider)


class WelcometextAdmin(admin.ModelAdmin):
    list_display = ['text']


admin.site.register(Welcometext)


class WelcomelistAdmin(admin.ModelAdmin):
    list_display = ['list']


admin.site.register(Welcomelist)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'text']


admin.site.register(Services)


class CallAdmin(admin.ModelAdmin):
    list_display = ['number']


admin.site.register(Call)


class OffersAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'payment', 'list1', 'list2', 'list3']


admin.site.register(Offers)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']


admin.site.register(Contact)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first', 'last', 'email', 'phone', 'address', 'city', 'state', 'zip', 'adult', 'kids']


admin.site.register(Customer)






admin.site.register(Address)


admin.site.register(Email)
