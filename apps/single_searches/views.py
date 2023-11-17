from rest_framework import generics
from rest_framework import filters
from django.apps import apps

from api_config import mixins
from apps.searches.configurations import SearchConfiguration
from apps.searches.views import SearchListView

class SingleSearchListView(SearchListView):
    configuration = SearchConfiguration()

    def get_queryset(self, *args, **kwargs):
        model_name, app_name = self.get_model_and_app_name()
        self.filter_backends = [self.configuration.appsName_to_searchFilter[app_name]]
        if model_name and app_name:
            model = apps.get_model(app_label=app_name, model_name=model_name)
            
        if app_name == "mada_countries":
            if model.objects.all().count() == 0:
                self._create_mada_country(model)

        if model is not None and app_name != "mada_countries":
            return model.objects.filter(user=self.request.user)
        
        else:
            return model.objects.all()