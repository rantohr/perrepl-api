import django_filters
from .models import MadaCountry
from rest_framework import filters

from apps.meta import BaseOrderingMetaclass

class MadaCountryOrdering(metaclass=BaseOrderingMetaclass):
    class Meta:
        fields = [
            "province",
            "region",
            "district",
            "commune",
        ]

class MadaCountrySearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["country_code", "province", "region", "district", "commune",]
    

class MadaCountryFilter(django_filters.FilterSet):
    class Meta:
        model = MadaCountry
        fields = {
            "country_code": ["icontains"],
            "province": ["icontains"],
            "region": ["icontains"],
            "district": ["icontains"],
            "commune": ["exact"],
        }