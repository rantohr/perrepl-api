from rest_framework import filters

class MadaCountrySingleFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["country_code", "province", "region", "district", "commune",]
    