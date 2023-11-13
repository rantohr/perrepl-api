import json

from api_config import mixins
from .configurations import SearchConfiguration
from apps.mada_countries.models import GeographicalCoordinate
from rest_framework import generics
from django.apps import apps
from django.conf import settings
import django_filters

class SearchListView(
    mixins.PermissionMixin,
    generics.ListAPIView
):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    configuration = SearchConfiguration()

    def get_filterset_class(self):
        _, app_name = self.determine_modelApps_name()
        return self.configuration.get_filter_from_appsName(app_name)

    def get_serializer_class(self):
        _, app_name = self.determine_modelApps_name()
        return self.configuration.get_serializer_from_appsName(app_name)
        
    def get_queryset(self, *args, **kwargs):
        self.filterset_class = self.get_filterset_class()
        model_name, app_name = self.determine_modelApps_name()
        if model_name and app_name:
            model = apps.get_model(app_label=app_name, model_name=model_name)
            
        if app_name == "mada_countries":
            if model.objects.all().count() == 0:
                self._create_mada_country(model)

        if model is not None and app_name != "mada_countries":
            return model.objects.filter(user=self.request.user)
        else:
            return model.objects.all()
        
    def determine_modelApps_name(self):
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