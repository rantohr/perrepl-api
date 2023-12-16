from django.db import models

from apps.users.models import User

# Create your models here.

class Plan(models.Model):
    CURRENCY = [
        ('$', "USD"),
        ('€', "EUR"),
    ]
    name = models.CharField(max_length=150)
    monthly = models.DecimalField(decimal_places=2, max_digits=10)
    yearly = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=10, choices=CURRENCY)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True)
