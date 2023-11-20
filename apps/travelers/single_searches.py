from rest_framework import filters

class TravelerSingleFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["email", "first_name", "last_name"]