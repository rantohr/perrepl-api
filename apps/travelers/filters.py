import django_filters
from django.db.models import Q
from .models import Traveler

class EmailFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            lookup = Q(**{'%s__icontains' % self.field_name: value})
            qs = qs.filter(lookup)
        return qs
    
class TravelerFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains', field_name='email') # EmailFilter(field_name='email')
    last_name = django_filters.CharFilter(lookup_expr='icontains', field_name='last_name')
    first_name = django_filters.CharFilter(lookup_expr='icontains', field_name='first_name')
    lead_traveler = django_filters.BooleanFilter(field_name='lead_traveler')#, method='is_lead_traveler')

    class Meta:
        model = Traveler
        fields = ['first_name', 'last_name', 'email', 'lead_traveler']