from rest_framework import serializers
from .models import Traveler, TravelerGroup

class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        # fields = '__all__'
        exclude = ('user',)

class TravelerGroupSerializer(serializers.ModelSerializer):
    travelers = TravelerSerializer(many=True, read_only=True)
    class Meta:
        model = TravelerGroup
        fields = [
            'travelers',
        ]
