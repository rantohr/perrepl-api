from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api_config.viewset_lib import *

router = DefaultRouter()
router.register(r'order', OrderViewset, basename='order')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'hotel', HotelViewset, basename='hotel')

urlpatterns = [
    # path('search/client/', SearchListView.as_view(), name='search-client'),
    # path('search/order/', SearchListView.as_view(), name='search-order'),
    # path('search/supplier/', SearchListView.as_view(), name='search-supplier')
    path('find/<str:search_type>/', SearchListView.as_view(), name='search-list')
]
urlpatterns += router.urls