from rest_framework import serializers
from rest_framework.response import Response

from .models import Itinerary, ItinerarySegment
from .cotation_datasets import CotationDataset

from apps.hotels.serializers import HotelSerializer
from apps.activities.serializers import ActivitySerializer
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.orders.serializers import OrderSerializer
from apps.travelers.serializers import TravelerSerializer

class ItinerarySegmentSerializer(serializers.ModelSerializer):
    hotels = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField() # ActivitySerializer(many=True, required=False)
    start_location = MadaCountrySerializer()
    end_location = MadaCountrySerializer()

    def get_hotels(self, instance: ItinerarySegment):
        hotels = instance.hotels.all()
        serialized_hotels = HotelSerializer(hotels, many=True, required=False, context=self.context)
        return serialized_hotels.data

    def get_activities(self, instance: ItinerarySegment):
        activities = instance.activities.all()
        serialized_activities = ActivitySerializer(activities, many=True, required=False, context=self.context)
        return serialized_activities.data

    class Meta:
        model = ItinerarySegment
        # fields = '__all__'
        exclude = ('user', )

class ItinerarySerializer(serializers.ModelSerializer):
    segments = serializers.SerializerMethodField()
    order = OrderSerializer(required=False)
    client = TravelerSerializer(required=False)
    
    def get_segments(self, instance: Itinerary):
        itinerary_segments = instance.segments.all()
        serialized_itin_seg = ItinerarySegmentSerializer(itinerary_segments, many=True, required=True, context=self.context)
        return serialized_itin_seg.data

    class Meta:
        model = Itinerary
        # fields = '__all__'
        exclude = ('user', )