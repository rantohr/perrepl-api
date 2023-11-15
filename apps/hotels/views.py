from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from .models import Hotel
from .data_validators import HotelValidator
from .serializers import HotelSerializer

from apps.mada_countries.models import MadaCountry
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.rooms.models import Room
from api_config import mixins


class HotelViewset(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = HotelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(HotelValidator)
        if not isinstance(validated_data_obj, HotelValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)
        
        validated_json_data = validated_data_obj.model_dump()
        rooms = validated_json_data.pop('rooms')
        locations = validated_json_data.pop('locations')

        with transaction.atomic():
            hotel = Hotel.objects.create(user=self.request.user, **validated_json_data)

            # Add Hotel location
            for loc in locations:
                loc = MadaCountry.objects.get(**loc)
                hotel.locations.add(loc)

            for room in rooms:
                Room.objects.create(user=self.request.user, hotel=hotel, **room)
        return Response(status=status.HTTP_201_CREATED)

