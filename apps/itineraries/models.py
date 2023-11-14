from django.db import models
from apps.travelers.models import Traveler
from apps.mada_countries.models import MadaCountry
from apps.hotels.models import Hotel
from apps.activities.models import Activity

class ItinerarySegment(models.Model):
    description = models.TextField()
    duration = models.PositiveIntegerField()
    start_location = models.ForeignKey(MadaCountry, on_delete=models.CASCADE, related_name='start_locations_set')
    end_location = models.ForeignKey(MadaCountry, on_delete=models.CASCADE, related_name='end_locations_set')
    distance = models.PositiveIntegerField()
    hotels = models.ManyToManyField(Hotel)
    activities = models.ManyToManyField(Activity)

class Itinerary(models.Model):
    title = models.TextField()
    description = models.TextField()
    duration = models.IntegerField()
    segments = models.ManyToManyField(ItinerarySegment)