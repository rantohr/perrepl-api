from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api_config.viewset_lib import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'order', OrderViewset, basename='order')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'hotel', HotelViewset, basename='hotel')
router.register(r'itinerary', ItineraryViewSet, basename='itinerary')
router.register(r'activity', ActivityViewset, basename='activity')
router.register(f'user', UserViewset, basename='user')

urlpatterns = [
    path('find/<str:search_type>/', SearchListView.as_view(), name='multiple-search'),
    # path('search/<str:search_type>/', SingleSearchListView.as_view(), name='single-search')
]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)