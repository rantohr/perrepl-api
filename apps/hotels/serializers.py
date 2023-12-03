from rest_framework import serializers

from apps.mada_countries.serializers import MadaCountrySerializer
from apps.rooms.serializers import RoomSerializer
from apps.images.serializers import ImageSerializer

from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    locations = MadaCountrySerializer(many=True, required=True)
    rooms = RoomSerializer(many=True, read_only=True, required=False)   
    images = serializers.SerializerMethodField()

    def get_images(self, hotel):
        img_qs = hotel.hotel_images.all()
        return ImageSerializer(img_qs, many=True).data

    class Meta:
        model = Hotel
        fields = '__all__'