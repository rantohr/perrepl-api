import uuid

from django.db import models
from django.utils import timezone


from apps.users.models import User
from apps.mada_countries.models import MadaCountry

def upload_to(instance):
    fname = instance.image_name
    return f"hotel_images/{fname}"

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    locations = models.ManyToManyField(MadaCountry)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    # created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    image_name = models.CharField(max_length=255, default=str(uuid.uuid4), unique=True)



