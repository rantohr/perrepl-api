from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.db import transaction

from .models import Hotel
from .data_validators import HotelValidator, HotelPricingValidator
from .serializers import HotelSerializer

from apps.mada_countries.models import MadaCountry
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.rooms.models import Room, RoomPrice
from apps.suppliers.models import Supplier
from apps.apis.exceptions import ActiveRecordSetNotFound
from api_config import mixins



class HotelViewset(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


    def list(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = self.get_serializer(qs, many=True)
        serializer_data = self._exclude_room_price(serializer.data)

        page = self.paginate_queryset(serializer_data)

        if page is not None:
            return self.get_paginated_response(serializer_data)
        
        return Response(serializer_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(HotelValidator)
        if not isinstance(validated_data_obj, HotelValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)
        
        validated_json_data = validated_data_obj.model_dump()
        rooms = validated_json_data.pop('rooms')
        locations = validated_json_data.pop('locations')

        with transaction.atomic():
            hotel = Hotel.objects.create(user=self.request.user, **validated_json_data)

            # Add Hotel location
            for loc in locations:
                loc = MadaCountry.objects.get(**loc)
                hotel.locations.add(loc)

            for room in rooms:
                Room.objects.create(user=self.request.user, hotel=hotel, **room)
        return Response(status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        new_data = {**request.data}
        instance = self.get_object() # Hotel.objects.get(pk=pk)

        self.update_m2m_field(MadaCountry, instance, "locations", new_data)
        self.update_m2o_field(Room, instance, "rooms", new_data)

        self.update_without_relation(instance, new_data)
        instance.save()

        return Response(HotelSerializer(instance).data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_without_relation(self, instance, data):
        if data:
            for key, value in data.items():
                setattr(instance, key, value)

    def update_m2o_field(self, model, instance, field_name, data):
        new_data = data.pop(field_name, None)
        if new_data is not None:
            objects = getattr(instance, field_name)
            objects.all().delete()
            for d in new_data:
                objects.create(**d)

    def update_m2m_field(self, model, instance, field_name, data):
        new_data = data.pop(field_name, None)
        if new_data:
            for d in new_data:
                objects = getattr(instance, field_name)
                objects.clear()
                m = model.objects.get(id=d["id"])
                objects.add(m)

    @action(methods=['post'], detail=True)
    def pricing(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(HotelPricingValidator)
        if not isinstance(validated_data_obj, HotelPricingValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)
        
        validated_json_data = validated_data_obj.model_dump()
        supplier = validated_json_data.pop("supplier")

        # Check if hotel is already attached to the supplier
        if Hotel.objects.filter(pk=self.kwargs.get("pk"), rooms__prices__supplier_id=supplier.get("id")).distinct().count()!=0:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)

        try:
            supplier = Supplier.objects.get(id=supplier.get("id"))
        except:
            return Response(
                {"errorType": "Supplier Error", "errorMessage": "Given Supplier doesn't exist", "context": f"Supplier with id {supplier.get('id')} doesn't exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        hotel_qs = self.get_queryset().filter(**kwargs).first()
        rooms = validated_json_data.pop("rooms")
        with transaction.atomic():
            for room in rooms:
                try:
                    r = Room.objects.get(id=room["id"])
                except:
                    return Response(
                        {"errorType": "Room Error", "ErrorMessage": "Given Room doesn't exist", "context": f"Room with id {supplier_id} doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                if room["hotel"] == hotel_qs.id:
                    room_priced = RoomPrice(
                        supplier=supplier,
                        room=r,
                        price=room.get("price", 0.0),
                        currency=room.get("currency","USD"),
                        season=room.get("season", None),
                        start_season=room.get("start_season", None),
                        end_season=room.get("end_season", None)
                    )
                    room_priced.save()
                else:
                    raise ActiveRecordSetNotFound(detail=f"Given room doesn't belong to the hotel")
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def _exclude_room_price(hotel_data: dict):
        output = []
        for hotel in hotel_data:
            temp_hotel = {k:v for k, v in hotel.items() if k!="rooms"}
            temp_hotel_rooms = []
            for room in hotel["rooms"]:
                temp_room = {k:v for k, v in room.items() if k!="prices"}
                temp_hotel_rooms.append(temp_room)
            temp_hotel["rooms"] = temp_hotel_rooms[:]
            output.append(temp_hotel)
        return output
    