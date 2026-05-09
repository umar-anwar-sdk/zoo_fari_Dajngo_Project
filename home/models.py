from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class topslider(models.Model):
    image = models.ImageField(upload_to='images/')


class Welcometext(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Welcomelist(models.Model):
    list = models.CharField(max_length=55)

    def __str__(self):
        return self.list


class Services(models.Model):
    icon = models.ImageField(upload_to='icons/')
    title = models.CharField(max_length=50)
    text = models.TextField(default=True)

    def __str__(self):
        return self.title


class Call(models.Model):
    number = models.CharField(max_length=20)

    def __int__(self):
        return self.number


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OurAnimals(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='animals/')

    def __int__(self):
        return self.name


class Offers(models.Model):
    number = models.IntegerField()
    image = models.ImageField(upload_to='animals/')
    name = models.CharField(max_length=8)
    price = models.IntegerField(default=0)
    list1 = models.CharField(max_length=50)
    list2 = models.CharField(max_length=50)
    list3 = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MembershipOrder(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user_email} - {self.offer.name}"


# Contact_US

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __int__(self):
        return self.name


class Customer(models.Model):
    first = models.CharField(max_length=100, default=True, null=True)
    last = models.CharField(max_length=100, default=True, null=True)
    email = models.EmailField(default=True, null=True)
    phone = models.IntegerField(default=True, null=True)
    address = models.CharField(max_length=100, default=True, null=True)
    city = models.CharField(max_length=100, default=True)
    state = models.CharField(max_length=56, null=True)
    zip = models.IntegerField(default=True, null=True)
    adult = models.IntegerField(default=True, null=True)
    kids = models.IntegerField(default=True, null=True)


# login system
class UserCreateFrom(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={'exists': 'This Already Exists'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateFrom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class MembershipCardOrder(models.Model):
    user_email = models.EmailField()
    card_number = models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email




class Address(models.Model):
    name = models.CharField(max_length=255)

    def __int__(self):
        return self.name


class Email(models.Model):
    email = models.EmailField(null=True)

    def __int__(self):
        return self.email
