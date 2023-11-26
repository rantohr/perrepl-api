from abc import ABC, abstractmethod

class Mapper(ABC):
    @property
    @abstractmethod
    def appsName_to_filter(self):
        pass

    @property
    @abstractmethod
    def appsName_to_searchFilter(self):
        pass

    @property
    @abstractmethod
    def appsName_to_serializer(self):
        pass
    
    @property
    @abstractmethod
    def search_type_to_model_name(self):
        pass

    @property
    @abstractmethod
    def search_type_to_apps_name(self):
        pass

    @property
    @abstractmethod
    def appsName_to_ordering(self):
        pass

    def get_model_and_app_name_from_search_type(self, x):
        model = self.search_type_to_model_name[x]
        apps = self.search_type_to_apps_name[x]
        return model, apps
    
    def get_serializer_from_appsName(self, x):
        return self.appsName_to_serializer[x]
    
    def get_filter_from_appsName(self, x):
        return self.appsName_to_filter[x]
    
    def get_searchFilter_from_appsName(self, x):
        return self.appsName_to_searchFilter[x]
    
    def get_ordering_from_appsName(self, x):
        return self.appsName_to_ordering[x]