from django.db import models
from apps.users.models import User
from apps.mada_countries.models import MadaCountry

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ManyToManyField(MadaCountry)
