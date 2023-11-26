import django_filters
from .models import Order

from apps.meta import BaseOrderingMetaclass

from rest_framework import filters

class OrderOrdering(metaclass=BaseOrderingMetaclass):
    class Meta:
        fields = [
            "created_at",
        ]

class OrderSearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ['order_creator__email']

# class EmailFilter(django_filters.CharFilter):
#     def filter(self, qs, value):
#         if value:
#             lookup = Q(**{'%s__icontains' % self.field_name: value})
#             qs = qs.filter(lookup)
#         return qs

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'description': ['icontains'],
            'created_at': ['gte', 'lte'],
            "order_creator__email": ['icontains'],
        }
        
