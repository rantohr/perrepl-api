from django.db import models

# Create your models here.

class Traveler(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number =  models.CharField(max_length=255)
    lead_traveler = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER)

class TravelerGroup(models.Model):
    travelers = models.ManyToManyField(Traveler)
