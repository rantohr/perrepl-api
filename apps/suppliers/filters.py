import django_filters
from .models import Supplier

from rest_framework import filters

class SupplierSearch(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return super().get_search_fields(view, request)

class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            "name": ["icontains"]
        }