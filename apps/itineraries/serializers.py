from rest_framework import serializers

from .models import Itinerary, ItinerarySegment

from apps.hotels.serializers import HotelSerializer
from apps.activities.serializers import ActivitySerializer
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.orders.serializers import OrderSerializer
from apps.travelers.serializers import TravelerSerializer

class ItinerarySegmentSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, required=False)
    activities = ActivitySerializer(many=True, required=False)
    start_location = MadaCountrySerializer()
    end_location = MadaCountrySerializer()
    class Meta:
        model = ItinerarySegment
        fields = '__all__'

class ItinerarySerializer(serializers.ModelSerializer):
    segments = ItinerarySegmentSerializer(many=True, required=True)
    order = OrderSerializer(required=False)
    client = TravelerSerializer(required=False)
    class Meta:
        model = Itinerary
        fields = '__all__'