from django.db import models

# Create your models here.
class Contact(models.Model):
    ROLES = [
        ('RESERVATION', 'Reservation'),
        ('MANAGER', 'Manager'),
        ('RESPONSIBLE', 'Responsible'),
        ('CORPORATE', 'Corporate'),
    ]
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLES, default='Reservation')