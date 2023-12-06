from rest_framework import serializers
from .models import MadaCountry, GeographicalCoordinate

class GeographicalCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeographicalCoordinate
        fields = [
            "longitude",
            "latitude"
        ]

class MadaCountrySerializer(serializers.ModelSerializer):
    geographical_coordinates = GeographicalCoordinateSerializer(many=True)
    class Meta:
        model = MadaCountry
        # fields = '__all__'
        exclude = ('user',)