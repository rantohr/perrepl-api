from django.db import models
from apps.users.models import User

class GeographicalCoordinate(models.Model):
    latitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)

class MadaCountry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Authenticated Operator Tour")
    country_code = models.CharField(max_length=255, db_index=True, default="MDG")
    province = models.CharField(max_length=255, db_index=True, null=True)
    region = models.CharField(max_length=255, db_index=True, null=True)
    district = models.CharField(max_length=255, db_index=True, null=True)
    commune = models.CharField(max_length=255, db_index=True, null=True)
    geographical_coordinates = models.ManyToManyField(GeographicalCoordinate)
