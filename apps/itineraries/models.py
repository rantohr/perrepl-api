from django.db import models
from apps.travelers.models import Traveler
from apps.mada_countries.models import MadaCountry
from apps.hotels.models import Hotel
from apps.activities.models import Activity
from django.contrib.postgres.fields import ArrayField

class ItinerarySegment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    start_location = models.ForeignKey(MadaCountry, on_delete=models.SET_NULL, related_name='start_locations_set', null=True)
    end_location = models.ForeignKey(MadaCountry, on_delete=models.SET_NULL, related_name='end_locations_set', null=True)
    departure_time_utc = models.DateTimeField(null=True, blank=True)
    arrival_time_utc = models.DateTimeField(null=True, blank=True)
    distance = models.PositiveIntegerField()
    hotels = models.ManyToManyField(Hotel)
    activities = models.ManyToManyField(Activity)

class Itinerary(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    description = models.TextField()
    duration = models.IntegerField()
    availability = models.TextField(null=True)
    segments = models.ManyToManyField(ItinerarySegment)
    # included_options = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    # not_included_options = ArrayField(models.CharField(max_length=255), null=True, blank=True)