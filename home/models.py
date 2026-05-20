from django.db import models

class Topslider(models.Model):
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
    text = models.TextField(default='')

    def __str__(self):
        return self.title

class Call(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number

class Offers(models.Model):
    number = models.IntegerField(default=0)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    list1 = models.CharField(max_length=50)
    list2 = models.CharField(max_length=50)
    list3 = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Email(models.Model):
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.email)
