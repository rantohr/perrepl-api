import django_filters
from .models import MadaCountry

class MadaCountryFilter(django_filters.FilterSet):
    country_code = django_filters.CharFilter(lookup_expr="icontains")
    province = django_filters.CharFilter(lookup_expr="icontains")
    region = django_filters.CharFilter(lookup_expr="icontains")
    district = django_filters.CharFilter(lookup_expr="icontains")
    commune = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = MadaCountry
        fields = [
            "country_code",
            "province",
            "region",
            "district",
            "commune",
        ]