from .configuration_mapper import Mapper

from apps.travelers.serializers import TravelerSerializer
from apps.travelers.filters import TravelerFilter
from apps.orders.filters import OrderFilter
from apps.suppliers.filters import SupplierFilter
from apps.mada_countries.filters import MadaCountryFilter
from apps.orders.serializers import OrderSerializer
from apps.suppliers.serializers import SupplierSerializer
from apps.mada_countries.serializers import MadaCountrySerializer

class SearchConfiguration(Mapper):
    appsName_to_filter = dict(
        travelers=TravelerFilter,
        orders=OrderFilter,
        suppliers=SupplierFilter,
        mada_countries=MadaCountryFilter
    )

    appsName_to_serializer = dict(
        travelers=TravelerSerializer,
        orders=OrderSerializer,
        suppliers=SupplierSerializer,
        mada_countries=MadaCountrySerializer
    )

    search_type_to_model_name = dict(
        client="Traveler", 
        order="Order",
        supplier="Supplier",
        madacountry="MadaCountry"
    )

    search_type_to_apps_name = dict(
        client="travelers",
        order="orders",
        supplier="suppliers",
        madacountry="mada_countries"
    )