from django.db import models
from apps.users.models import User
from django.core.validators import MinValueValidator

class OrderStatus(models.Model):
    STATUS = [
        ("CONFIRMED", "Confirmed"),
        ("IN PROGRESS","In progress"),
    ]
    order_status = models.CharField(max_length=50, choices=STATUS, null=True, default='NEW')
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, null=True)

# Create your models here.
class Order(models.Model):
    CLIENT_TYPE = [
        ('B2B', 'Business-to-Business (B2B)'),
        ('DIRECT', 'Direct Client')
    ]
    ROOM_TYPE = [
        ("SINGLE ROOM", "1 Person"),
        ("DOUBLE ROOM", "2 peoples, 1 bed"),
        ("TWIN ROOM", "2 peoples, 2 separate beds"),
        ("TRIPLE ROOM", "3 peoples, 1 or 2 beds"),
        ("FAMILY ROOM", "4 or more people, multiple beds")
    ]
    TRIP_INTEREST = [
        ('MUST SEE ATTRACTIONS', "Must see attractions"),
        ('BEACH', "Beach"),
        ('LOCAL CULTURE', "Local culture"),
        ('WELLNESS & SPA', "Wellness and spa"),
        ('BIRD WATCHING', "Bird Watching"),
        ('BIKING', "Biking"),
        ('SCUBA DIVING', "Scuba diving"),
        ('SNORKELING', "Snorkeling"),
        ('TREKKING', "Trekking"),
        ('SURF', "Surf"),
        ('KITE-SURF', "Kite-surf"),
        ('HISTORY', "History")
    ]
    TRIP_REASON = [
        ("FRIEND", "Friend trip"),
        ("ROAD", "Road trip"),
        ("SOLO", "Solo trip"),
        ("REUNION", "Reunion"),
        ("ANNIVERSARY", "Anniversary"),
        ("HONEYMOON", "Honeymoon"),
        ("FAMILY", "Family vacation"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Authenticated Operator Tour") # Tour owner
    # traveler_group = models.ForeignKey("travelers.TravelerGroup", on_delete=models.SET_NULL, null=True)
    order_creator = models.ForeignKey("travelers.Traveler", on_delete=models.SET_NULL, null=True, related_name='orders_created')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    trip_duration = models.IntegerField(validators=[MinValueValidator(1)])
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPE, default='B2B')
    room_type = models.CharField(max_length=150, choices=ROOM_TYPE, default="")
    description = models.TextField(null=True, blank=True, db_index=True)
    trip_interest = models.CharField(max_length=50, choices=TRIP_INTEREST, default="")
    trip_reason = models.CharField(max_length=50, choices=TRIP_REASON, default="")
    custom_trip_reason = models.CharField(max_length=50, default="") # TODO: trip_reason and custom_trip_reason should not exist both at the same time
    pax_type = models.CharField(max_length=50, help_text="Use colon to map pax code and their number in party")
    created_at = models.DateTimeField(auto_now_add=True)

