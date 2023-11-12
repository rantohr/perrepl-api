import django_filters
from .models import Order
from django.db.models import Q

# class EmailFilter(django_filters.CharFilter):
#     def filter(self, qs, value):
#         if value:
#             lookup = Q(**{'%s__icontains' % self.field_name: value})
#             qs = qs.filter(lookup)
#         return qs

class OrderFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr='icontains', field_name='order_creator__email')
    class Meta:
        model = Order
        fields = ["description", "email"]