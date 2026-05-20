from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Animal(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='animals/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FamilyPackage(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    package_name = models.CharField(max_length=255)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, help_text="e.g., '1 Day', '2 Days'")
    benefits = models.TextField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.package_name
