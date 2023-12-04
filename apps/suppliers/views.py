
from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.hotels.models import Hotel
from apps.hotels.serializers import HotelSerializer

from .models import Supplier
from .serializers import SupplierSerializer
from api_config import mixins


# Create your views here.
class SupplierViewSet(
    mixins.PermissionMixin,
    mixins.ImageMixin,
    mixins.SerializerContextMixin,
    viewsets.ModelViewSet
):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'pk'

    @action(methods=['get'], detail=True)
    def hotel(self, *args, **kwargs):
        supplier_id = self.kwargs.get("pk")
        hotels_with_prices = Hotel.objects.filter(rooms__prices__supplier_id=supplier_id).distinct()
        page = self.paginate_queryset(hotels_with_prices)
        hotel_serialized_data = HotelSerializer(hotels_with_prices, many=True, context=self.get_serializer_context(*args, **kwargs)).data
        if page is not None:
            return self.get_paginated_response(hotel_serialized_data)
        return Response(hotel_serialized_data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def upload_image(self, request, *args, **kwargs):
        supplier = self.get_object()
        with transaction.atomic():
            image_obj = self.create_image('supplier')
            supplier.supplier_images.add(image_obj)
            image_obj.save()
            return Response(self.get_serializer(supplier).data, status=status.HTTP_201_CREATED)