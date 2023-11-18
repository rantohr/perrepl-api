from rest_framework import serializers
from .models import Room, RoomPrice


class RoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrice
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    prices = RoomPriceSerializer(many=True, required=False)
    class Meta:
        model = Room
        fields = '__all__'
