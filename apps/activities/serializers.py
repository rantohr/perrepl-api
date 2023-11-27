from .models import Activity

from rest_framework import serializers
from apps.mada_countries.serializers import MadaCountrySerializer

class ActivitySerializer(serializers.ModelSerializer):
    location = MadaCountrySerializer(required=True)
    class Meta:
        model = Activity
        fields = '__all__'
