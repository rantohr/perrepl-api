from rest_framework import serializers
from .models import Room, RoomPrice

from apps.suppliers.serializers import SupplierSerializer

class SimpleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'bed_type', 'is_available')

class RoomPriceSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    room = SimpleRoomSerializer(required=False)

    class Meta:
        model = RoomPrice
        fields = ('supplier', 'price', 'currency', 'season', 'start_season', 'end_season', 'room')

class RoomSerializer(serializers.ModelSerializer):
    prices = RoomPriceSerializer(many=True, required=False)
    class Meta:
        model = Room
        # fields = '__all__'
        exclude = ('user',)
