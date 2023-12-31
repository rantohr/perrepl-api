# apps/orders/views.py

import json
import copy
from .data_validators import OrderValidator, OrderStatusValidator

from django.db import transaction
from django.db.models.query import QuerySet
from django.db.models import Prefetch

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from apps.travelers.models import Traveler, TravelerGroup
from apps.orders.models import Order, OrderStatus
from apps.users.models import User
from api_config import mixins

from .serializers import OrderSerializer, OrderStatusSerializer

from apps.hotels.models import Hotel
from apps.suppliers.models import Supplier
from apps.rooms.models import Room
from apps.itineraries.models import Itinerary, ItinerarySegment
from apps.contacts.models import Contact

class OrderViewset(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = OrderSerializer(qs, many=True)

        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create order from user input
        """
        validated_data_obj = self._validate_data(OrderValidator)
        if not isinstance(validated_data_obj, OrderValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)
        
        # Create a travelers
        created_travelers = []
        validated_json_data = validated_data_obj.model_dump()
        travelers = validated_json_data.pop("travelers")

        with transaction.atomic():
            lead_traveler = None
            count_lead_traveler = 0
            for traveler in travelers:
                try:
                    t = Traveler.objects.get(email=traveler["email"])
                except:
                    t = Traveler(user=self.request.user, **traveler)
                    t.save()

                if traveler["lead_traveler"]:
                    lead_traveler = copy.deepcopy(t)
                    count_lead_traveler += 1

                if count_lead_traveler > 1:
                    return Response({"Error message": "Only one lead traveler is allowed"}, status=status.HTTP_400_BAD_REQUEST)
                
                created_travelers.append(t)

            if lead_traveler is None:
                return Response({"Error message": "Need one lead traveler"}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(
                user=self.request.user,
                order_creator=lead_traveler,
                **validated_json_data
            )

        serializer = OrderSerializer(order)
        return Response({"Status": "COMPLETED", "OrderData": serializer.data}, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def change_status(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(OrderStatusValidator)
        if not isinstance(validated_data_obj, OrderStatusValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)

        qs = self.get_object()

        current_status = qs.status.all().order_by("-updated_at").first()
        if current_status and current_status.order_status == request.data.get('order_status'):
            serializer = OrderSerializer(qs)
            return Response(serializer.data)

        _ = OrderStatus.objects.create(
            order=qs,
            **validated_data_obj.model_dump()
        )
        return Response(OrderSerializer(qs).data)

    @action(methods=['get'], detail=False, url_path="client/(?P<client_id>\d+)")
    def client(self, request, client_id, *args, **kwargs):
        qs = Traveler.objects.filter(id=client_id)
        if qs.count() == 0:
            return Response({"errorMessage": "Client Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        qs = qs.first().orders_created.all()
        if qs.count() == 0:
            return Response(qs.none(), status=status.HTTP_404_NOT_FOUND)
        
        qs = qs.order_by('-created_at')
        orders = []
        for q in qs:
            if q.status.all().count() == 0:
                orders.append(q)
        serializer = OrderSerializer(orders, many=True)
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        
    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        instance = self.get_object() # self.get_queryset(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)