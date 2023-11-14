from rest_framework import viewsets, status
from api_config import mixins
from .models import Hotel

from apps.mada_countries.models import MadaCountry
from apps.mada_countries.serializers import MadaCountrySerializer

from .data_validators import HotelValidator


class HotelViewset(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    queryset = Hotel.objects.all()

    def create(self, request):
        validated_data_obj = self._validate_data(HotelValidator)
        breakpoint()

