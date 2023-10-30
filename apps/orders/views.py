# apps/orders/views.py

import json
from .data_validators import OrderValidator

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.travelers.models import Traveler, TravelerGroup
from apps.orders.models import Order
from apps.users.models import User
from api_config import mixins

from .serializers import OrderSerializer

class OrderViewset(
    mixins.PermissionMixin,
    viewsets.ViewSet
):

    def list(self, request):
        return Response({"message": "Listing order"})

    def create(self, request):
        """
        Create order from user input
        """
        try:
            validated_data_obj = OrderValidator(**self.request.data)
        except ValueError as error:
            error_message = json.loads(error.json())[0]
            error_message.pop('url', None)
            error_message.pop('ctx', None)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a travelers
        created_travelers = []
        validated_json_data = validated_data_obj.model_dump()
        travelers = validated_json_data.pop("travelers")

        with transaction.atomic():
            for traveler in travelers:
                t = Traveler(**traveler)
                t.save()
                created_travelers.append(t)
            # Group created travelers
            traveler_group =  TravelerGroup()
            traveler_group.save()

            for ct in created_travelers:
                traveler_group.travelers.add(ct)

            order = Order.objects.create(
                user=self.request.user,
                traveler_group=traveler_group,
                **validated_json_data
            )
        serializer = OrderSerializer(order)
        return Response({"Status": "COMPLETED", "OrderData": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass