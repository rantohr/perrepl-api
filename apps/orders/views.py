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

class OrderViewset(
    mixins.PermissionMixin,
    viewsets.ViewSet
):
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        qs = Order.objects.filter(user=self.request.user, **kwargs)
        if isinstance(qs, QuerySet):
            return qs
        return Order.objects.none()
    
    def _validate_data(self, validator):
        try:
            validated_data_obj = validator(**self.request.data)
        except ValueError as error:
            error_message = json.loads(error.json())[0]
            error_message.pop('url', None)
            error_message.pop('ctx', None)
            return dict(error_message=error_message, status=status.HTTP_400_BAD_REQUEST)
        return validated_data_obj

    def list(self, request, *args, **kwargs):
        # order_status_prefetch = Prefetch(
        #     "orderstatus_set",
        #     queryset=OrderStatus.objects.all().order_by("-updated_at"),
        #     to_attr="latest_statuses"
        # )
        # qs = self.get_queryset(*args, **kwargs).prefetch_related(order_status_prefetch)
        qs = self.get_queryset(*args, **kwargs)
        serializer = OrderSerializer(qs, many=True)
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
            
            # Group created travelers
            traveler_group = TravelerGroup(number_in_party=len(created_travelers))
            traveler_group.save()

            for ct in created_travelers:
                traveler_group.travelers.add(ct)

            order = Order.objects.create(
                user=self.request.user,
                traveler_group=traveler_group,
                **validated_json_data
            )
            order.order_creator.add(lead_traveler)
        serializer = OrderSerializer(order)
        return Response({"Status": "COMPLETED", "OrderData": serializer.data}, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def change_status(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(OrderStatusValidator)
        if not isinstance(validated_data_obj, OrderStatusValidator):
            return Response(validated_data_obj, status=status.HTTP_404_NOT_FOUND)
        qs = self.get_queryset(pk=self.kwargs.get('pk')).first()

        current_status = qs.orderstatus_set.all().order_by("-updated_at").first()
        if current_status and current_status.order_status == request.data.get('order_status'):
            serializer = OrderSerializer(qs)
            return Response(serializer.data)

        _ = OrderStatus.objects.create(
            order=qs,
            **validated_data_obj.model_dump()
        )
        return Response(OrderSerializer(qs).data)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass