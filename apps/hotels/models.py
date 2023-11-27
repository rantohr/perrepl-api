from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.mada_countries.models import MadaCountry

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    locations = models.ManyToManyField(MadaCountry)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
