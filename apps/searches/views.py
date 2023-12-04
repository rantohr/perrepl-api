import json

from api_config import mixins
from .configurations import SearchConfiguration
from apps.mada_countries.models import GeographicalCoordinate

from rest_framework import generics
from rest_framework import filters

from django.apps import apps
from django.conf import settings
import django_filters


class SearchListView(
    mixins.PermissionMixin,
    mixins.SerializerContextMixin,
    generics.ListAPIView
):
    configuration = SearchConfiguration()

    def filter_queryset(self, queryset):
        _, app_name = self.get_model_and_app_name()

        filter_backends = [
            django_filters.rest_framework.DjangoFilterBackend, 
            filters.OrderingFilter, 
            self.configuration.appsName_to_searchFilter[app_name]
        ]
        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset
        
    def get(self, request, *args, **kwargs):
        if self.kwargs.get("search_type") == "hotel":
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=self.get_serializer_context(rm_price=True))
                serialized_data = serializer.data
                return self.get_paginated_response(serialized_data)
            
        return self.list(request, *args, **kwargs)

    def get_filterset_class(self):
        _, app_name = self.get_model_and_app_name()
        return self.configuration.get_filter_from_appsName(app_name)
    
    def _get_ordering_fields(self):
        _, app_name = self.get_model_and_app_name()
        return self.configuration.get_ordering_from_appsName(app_name)

    def get_serializer_class(self):
        _, app_name = self.get_model_and_app_name()
        return self.configuration.get_serializer_from_appsName(app_name)
        
    def get_queryset(self, *args, **kwargs):
        model_name, app_name = self.get_model_and_app_name()
        # self.filter_backends.append(self.configuration.appsName_to_searchFilter[app_name])

        if model_name and app_name:
            model = apps.get_model(app_label=app_name, model_name=model_name)

        self.filterset_class = self.get_filterset_class()
        try:
            self.ordering_fields = self._get_ordering_fields()   
        except:
            pass

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