from django.db import models
from apps.hotels.models import Hotel
from apps.users.models import User
from apps.suppliers.models import Supplier

# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10, null=True)
    bed_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)


class RoomPrice(models.Model):
    CURRENCY = [("USD", "USD"), ("EUR", "EUR")]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY)
    season = models.CharField(max_length=255, null=True, blank=True)
    start_season = models.DateField(null=True, blank=True)
    end_season = models.DateField(null=True, blank=True)
    