from django.db import models
from apps.users.models import User
from apps.hotels.models import Hotel

from apps.contacts.models import Contact


class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Authenticated Operator Tour")
    name = models.CharField(max_length=250, db_index=True)
    location = models.CharField(max_length=255)
    website = models.URLField(null=True)
    billing_address = models.TextField()
    type = models.CharField(max_length=50, null=True)
    area_covered = models.CharField(max_length=255, null=True)
    contacts = models.ManyToManyField(Contact)
    remark = models.TextField()