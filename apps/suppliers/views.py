from django.shortcuts import render
from rest_framework import viewsets

from .models import Supplier
from .serializers import SupplierSerializer
from api_config import mixins


# Create your views here.
class SupplierViewSet(
    mixins.PermissionMixin,
    viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'pk'