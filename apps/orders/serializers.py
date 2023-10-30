# -- apps/orders/serializers.py --

from rest_framework import serializers
from .models import Order
from apps.travelers.serializers import TravelerGroupSerializer

class OrderSerializer(serializers.ModelSerializer):
    travelers = TravelerGroupSerializer(source='traveler_group')
    class Meta:
        model = Order
        fields = [
            "travelers",
            "departure_datetime",
            "arrival_datetime",
            "trip_duration",
            "client_type",
            "room_type",
            "trip_interest",
            "trip_reason",
            "custom_trip_reason",
            "pax_type",
            "created_at",
        ]