# -- apps/orders/serializers.py --

from rest_framework import serializers
from .models import Order, OrderStatus
from apps.travelers.serializers import TravelerGroupSerializer

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = [
            'updated_at',
            'order_status',
        ]

class OrderSerializer(serializers.ModelSerializer):
    travelers = TravelerGroupSerializer(source='traveler_group')
    order_statuses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "pk",
            "travelers",
            "departure_datetime",
            "arrival_datetime",
            "trip_duration",
            "client_type",
            "room_type",
            "trip_interest",
            "trip_reason",
            "custom_trip_reason",
            "pax_type",
            "created_at",
            "order_statuses",
            "description",
        ]
    
    def get_order_statuses(self, obj):
        order_statuses = OrderStatus.objects.filter(order=obj).order_by('-updated_at').first()
        return OrderStatusSerializer(order_statuses).data
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if repr["order_statuses"]['order_status'] is None:
            repr['order_statuses']['order_status'] = "New"
        return repr