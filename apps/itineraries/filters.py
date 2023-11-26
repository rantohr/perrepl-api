import django_filters
from .models import Itinerary
from rest_framework import filters

from apps.meta import BaseOrderingMetaclass

class ItineraryOrdering(metaclass=BaseOrderingMetaclass):
    class Meta:
        fields = [
            'created_at'
        ]


class ItinerarySearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["title"]

class ItineraryFilter(django_filters.FilterSet):
    class Meta:
        model = Itinerary
        fields = {
            'created_at': ['gte', 'lte'],
            'updated_at': ['gte', 'lte'],
        }