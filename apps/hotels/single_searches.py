from rest_framework import filters

class HotelSingleFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ['name']