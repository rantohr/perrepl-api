from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api_config.viewset_lib import *

router = DefaultRouter()
router.register(r'order', OrderViewset, basename='order')
urlpatterns = [
    path(r'', include(router.urls))
]