from django.db import models

# Create your models here.

class Traveler(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text="Authenticated Operator Tour")
    email = models.EmailField()
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number =  models.CharField(max_length=255, null=True)
    lead_traveler = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER)

class TravelerGroup(models.Model):
    travelers = models.ManyToManyField(Traveler)
