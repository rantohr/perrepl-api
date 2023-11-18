
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.hotels.models import Hotel
from apps.hotels.serializers import HotelSerializer
from apps.rooms.serializers import RoomPriceSerializer
from apps.rooms.models import RoomPrice

from .models import Supplier
from .serializers import SupplierSerializer
from api_config import mixins
from rest_framework.decorators import action


# Create your views here.
class SupplierViewSet(
    mixins.PermissionMixin,
    viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'pk'

    @action(methods=['get'], detail=True)
    def hotel(self, *args, **kwargs):
        supplier_id = self.kwargs.get("pk")
        hotels_with_prices = Hotel.objects.filter(rooms__prices__supplier_id=supplier_id).distinct()

        page = self.paginate_queryset(hotels_with_prices)

        hotel_serialized_data = HotelSerializer(hotels_with_prices, many=True).data
        hotel_serialized_data = self._include_only_target_supplier(hotel_serialized_data, supplier_id)

        if page is not None:
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(hotel_serialized_data)

        return Response(hotel_serialized_data, status=status.HTTP_200_OK)

    @staticmethod
    def _include_only_target_supplier(hotel_list: dict, supplier_id: int):
        output = []
        for hotel in hotel_list:
            temp_hotel = {k:v for k, v in hotel.items() if k!="rooms"}
            temp_hotel_rooms = []

            for room in hotel["rooms"]:
                temp_room = {k:v for k, v in room.items() if k!="prices"}
                temp_room_prices = []

                for price in room["prices"]:
                    if price["supplier"] == int(supplier_id):
                        temp_room_prices.append(price)
                        
                temp_room["prices"] = temp_room_prices
                temp_hotel_rooms.append(temp_room)

            temp_hotel["rooms"] = temp_hotel_rooms
            output.append(temp_hotel)
        return output
    