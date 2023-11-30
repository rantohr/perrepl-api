from django.db import models
from django.utils import timezone

from apps.mada_countries.models import MadaCountry
from apps.users.models import User
from apps.suppliers.models import Supplier


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(MadaCountry, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(default=timezone.now, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ActivityPrice(models.Model):
    CURRENCY = [("USD", "USD"), ("EUR", "EUR")]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY, default="EUR")