import os
from rest_framework import generics
from django.apps import apps
from api_config import mixins

from apps.travelers.serializers import TravelerSerializer
from apps.travelers.filters import TravelerFilter
from apps.orders.serializers import OrderSerializer

import django_filters

class SearchListView(
    mixins.PermissionMixin,
    generics.ListAPIView
):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_filterset_class(self):
        _, app_name = self.determine_modelApps_name()
        return self.apps_to_filter.get(app_name)

    def get_serializer_class(self):
        _, app_name = self.determine_modelApps_name()
        return self.apps_to_serializer.get(app_name)
        
    def get_queryset(self, *args, **kwargs):
        self.filterset_class = self.get_filterset_class()
        model_name, app_name = self.determine_modelApps_name()
        if model_name and app_name:
            model = apps.get_model(app_label=app_name, model_name=model_name)
        if model is not None:
            return model.objects.filter(user=self.request.user)
        
    def determine_modelApps_name(self):
        app = os.path.basename(self.request.path.rstrip('/'))
        return self.app_to_modelApps.get(app)
    
    @property
    def apps_to_filter(self):
        return dict(
            travelers=TravelerFilter,
            orders=...
        )

    @property
    def apps_to_serializer(self):
        return dict(
            travelers=TravelerSerializer,
            orders=OrderSerializer
        )

    @property
    def app_to_modelApps(self):
        return dict(
            client=("Traveler", "travelers"),
            order=("Order", "orders")
        )
    