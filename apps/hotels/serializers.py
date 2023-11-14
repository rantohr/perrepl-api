from rest_framework import serializers
from apps.mada_countries.serializers import MadaCountrySerializer
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    location = MadaCountrySerializer

    class Meta:
        model = Hotel
        fields = '__all__'