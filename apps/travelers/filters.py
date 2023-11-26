import django_filters
from django.db.models import Q
from .models import Traveler

from rest_framework import filters

class TravelerSearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["email", "first_name", "last_name"]

# class EmailFilter(django_filters.CharFilter):
#     def filter(self, qs, value):
#         if value:
#             lookup = Q(**{'%s__icontains' % self.field_name: value})
#             qs = qs.filter(lookup)
#         return qs
    
class TravelerFilter(django_filters.FilterSet):
    class Meta:
        model = Traveler
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'lead_traveler': ['exact']
        }
