from django.db import models

# Create your models here.

class Traveler(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text="Authenticated Operator Tour")
    email = models.EmailField(unique=True, null=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, db_index=True)
    last_name = models.CharField(max_length=255, null=True, db_index=True)
    phone_number =  models.CharField(max_length=255, null=True)
    lead_traveler = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    created_at = models.DateTimeField(auto_now=True)
    traveler_type = models.CharField(max_length=5, null=True)

class TravelerGroup(models.Model):
    number_in_party = models.IntegerField(null=True)
    travelers = models.ManyToManyField(Traveler)
