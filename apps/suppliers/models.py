from django.db import models

# from apps.contacts.models import Contact

class Supplier(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=255)
    website = models.URLField(null=True)
    billing_address = models.TextField()
    type = models.CharField(max_length=50, null=True)
    area_covered = models.CharField(max_length=255, null=True)
    contacts = models.ManyToManyField('contacts.Contact', blank=True, null=True)
    remark = models.TextField()
