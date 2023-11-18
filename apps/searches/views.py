import json

from api_config import mixins
from .configurations import SearchConfiguration
from apps.mada_countries.models import GeographicalCoordinate
from rest_framework import generics
from django.apps import apps
from django.conf import settings
from rest_framework.filters import SearchFilter
import django_filters
from rest_framework.response import Response


class SearchListView(
    mixins.PermissionMixin,
    generics.ListAPIView
):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    configuration = SearchConfiguration()

    def get(self, request, *args, **kwargs):
        if self.kwargs.get("search_type") == "hotel":
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                serialized_data = self._exclude_room_price(serializer.data)
                return self.get_paginated_response(serialized_data)
            
        return self.list(request, *args, **kwargs)

    def get_filterset_class(self):
        _, app_name = self.get_model_and_app_name()
        return self.configuration.get_filter_from_appsName(app_name)

    def get_serializer_class(self):
        _, app_name = self.get_model_and_app_name()
        return self.configuration.get_serializer_from_appsName(app_name)
        
    def get_queryset(self, *args, **kwargs):
        model_name, app_name = self.get_model_and_app_name()
        if model_name and app_name:
            model = apps.get_model(app_label=app_name, model_name=model_name)

        self.filterset_class = self.get_filterset_class()
        if set(self.request.query_params.keys()).difference(set(self.filterset_class.get_fields().keys())):
            return model.objects.none()
            
        if app_name == "mada_countries":
            if model.objects.all().count() == 0:
                self._create_mada_country(model)

        if model is not None and app_name != "mada_countries":
            return model.objects.filter(user=self.request.user)
        else:
            return model.objects.all()
        
    def get_model_and_app_name(self):
        search_type = self.kwargs.get('search_type')
        return self.configuration.get_model_and_app_name_from_search_type(search_type)
    
    @staticmethod
    def _create_mada_country(model):
        data = json.load(open(settings.MADA_COUNTRY_FILE_PATH))
        for geo_localization in data:
            geographical_coordinates_data = geo_localization.pop("geographical_coordinates")
            country_instance = model.objects.create(**geo_localization)
            for coord_data in geographical_coordinates_data:
                coordinate_instance = GeographicalCoordinate.objects.create(**coord_data)
                country_instance.geographical_coordinates.add(coordinate_instance)

    @staticmethod
    def _exclude_room_price(hotel_data: dict):
        output = []
        for hotel in hotel_data:
            temp_hotel = {k:v for k, v in hotel.items() if k!="rooms"}
            temp_hotel_rooms = []
            for room in hotel["rooms"]:
                temp_room = {k:v for k, v in room.items() if k!="prices"}
                temp_hotel_rooms.append(temp_room)
            temp_hotel["rooms"] = temp_hotel_rooms[:]
            output.append(temp_hotel)
        return output