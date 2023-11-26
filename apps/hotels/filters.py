from rest_framework import filters
import django_filters

from .models import Hotel

class HotelSearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ['name']
    

class HotelFilter(django_filters.FilterSet):
    class Meta:
        fields = {
            "name": ['icontains']
        }