from django.db import models
from uuid import uuid4
import pathlib

from apps.hotels.models import Hotel
from apps.suppliers.models import Supplier

def upload_to(instance, filename):
    folder_name = instance.folder_name
    file_name = instance.file_name
    suffix = pathlib.Path(filename).suffix
    return f"{folder_name}s/{file_name}{suffix}"

# Create your models here.
class Image(models.Model):
    folder_name = models.CharField(max_length=255, null=True)
    file_name = models.CharField(max_length=255, null=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    hotel_images = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE, related_name="hotel_images")
    supplier_images = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, related_name="supplier_images")