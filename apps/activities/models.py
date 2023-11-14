from django.db import models
from apps.mada_countries.models import MadaCountry

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(MadaCountry, on_delete=models.CASCADE)
    
