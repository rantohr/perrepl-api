from rest_framework import serializers
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.rooms.serializers import RoomSerializer
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    locations = MadaCountrySerializer(many=True, required=True)
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = '__all__'