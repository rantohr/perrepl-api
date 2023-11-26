from .configuration_mapper import Mapper

from apps.travelers.serializers import TravelerSerializer
from apps.orders.serializers import OrderSerializer
from apps.suppliers.serializers import SupplierSerializer
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.hotels.serializers import HotelSerializer
from apps.itineraries.serializers import ItinerarySerializer

from apps.travelers.filters import TravelerFilter, TravelerSearch
from apps.orders.filters import OrderFilter, OrderSearch, OrderOrdering
from apps.suppliers.filters import SupplierFilter, SupplierSearch
from apps.mada_countries.filters import MadaCountryFilter, MadaCountrySearch
from apps.itineraries.filters import ItineraryFilter, ItinerarySearch, ItineraryOrdering
from apps.hotels.filters import HotelSearch

class SearchConfiguration(Mapper):
    appsName_to_ordering = dict(
        itineraries=ItineraryOrdering,
        orders=OrderOrdering
    )
    appsName_to_searchFilter = dict(
        hotels=HotelSearch,
        mada_countries=MadaCountrySearch,
        travelers=TravelerSearch,
        orders=OrderSearch,
        itineraries=ItinerarySearch,
    )
    
    appsName_to_filter = dict(
        travelers=TravelerFilter,
        orders=OrderFilter,
        suppliers=SupplierFilter,
        mada_countries=MadaCountryFilter,
        itineraries=ItineraryFilter,
    )

    appsName_to_serializer = dict(
        travelers=TravelerSerializer,
        orders=OrderSerializer,
        suppliers=SupplierSerializer,
        mada_countries=MadaCountrySerializer,
        hotels=HotelSerializer,
        itineraries=ItinerarySerializer
    )

    search_type_to_model_name = dict(
        client="Traveler", 
        order="Order",
        supplier="Supplier",
        madacountry="MadaCountry",
        hotel="Hotel",
        itinerary='Itinerary'
    )

    search_type_to_apps_name = dict(
        client="travelers",
        order="orders",
        supplier="suppliers",
        madacountry="mada_countries",
        hotel="hotels",
        itinerary="itineraries"
    )