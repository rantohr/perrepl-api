from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api_config.viewset_lib import *

router = DefaultRouter()
router.register(r'order', OrderViewset, basename='order')

urlpatterns = [
    path('search/client/', SearchListView.as_view(), name='search-client'),
    path('search/order/', SearchListView.as_view(), name='search-order')
]
urlpatterns += router.urls
# [
#     path(r'^', include(router.urls))
# ]