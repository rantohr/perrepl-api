from .models import Activity, ActivityPrice

from rest_framework import serializers
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.suppliers.serializers import SupplierSerializer

class ActivityPriceSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    class Meta:
        model = ActivityPrice
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    location = MadaCountrySerializer(required=True)
    prices = ActivityPriceSerializer(many=True, required=False)
    class Meta:
        model = Activity
        # fields = '__all__'
        exclude = ('user',)
