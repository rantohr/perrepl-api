from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from django.db import transaction

from .models import Itinerary
from .data_validator import ItineraryValidator

from api_config import mixins

class ItineraryViewSet(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    GenericViewSet
):
    queryset = Itinerary.objects.all()

    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(ItineraryValidator)
        if not isinstance(validated_data_obj, ItineraryValidator):
            return Response(validated_data_obj, status=status.HTTP_400_BAD_REQUEST)
        
        validated_json_data = validated_data_obj.model_dump()
        segments = validated_json_data.pop("segments")

        with transaction.atomic():
            ...