from django.db import models
from apps.hotels.models import Hotel
from apps.users.models import User

# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    bed_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)