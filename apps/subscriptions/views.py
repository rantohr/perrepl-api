# apps.subscriptions

from typing import List, Dict

from django.db import models
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer
from .data_validator import SubscriptionValidator
from . import helper

from api_config import mixins
from apps.exceptions import PlanNotFound

class PlanViewset(
    mixins.AdminPermissionMixin,
    viewsets.ModelViewSet
):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def get_permissions(self):
        if self.action == 'list':
            # All user can view plan
            return [permissions.AllowAny()]
        return super().get_permissions()

class SubscriptionView(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # def get_serializer_class(self):
    #     return SubscriptionSerializer
    
    def paginate_response(self, serializer):
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        return self.get_paginated_response([])
    
    def list(self, *args, **kwargs):
        # breakpoint()
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return self.paginate_response(serializer)
    
    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(SubscriptionValidator)
        if not isinstance(validated_data_obj, SubscriptionValidator):
            return Response(validated_data_obj, status=status.HTTP_400_BAD_REQUEST)
        validated_json_data = validated_data_obj.model_dump()

        plan = validated_json_data.pop('plan')
        monthly = validated_json_data.pop('monthly', None)
        yearly = validated_json_data.pop('yearly', None)
        user = request.user

        if monthly and yearly:
            return Response({'errorMessage': 'Setting monthly and yearly both are not allowed'}, status=status.HTTP_400_BAD_REQUEST)\
        
        plan_period = helper.choose_one({"monthly": monthly, "yearly": yearly})
        start_date, end_date = helper.get_period(plan_period)

        # TODO: Get last subscription 
        user_last_subscription = self.get_queryset().filter(user=user).order_by('-end_date').first()
        if user_last_subscription:
            allowed_to_subscribe = self.check_subscription_allowance(user_last_subscription)
            if not allowed_to_subscribe:
                return Response({'errorMessage': 'Not allowed to subscribe'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            plan_instance = self._get_object_instance(Plan, plan)
        except Plan.DoesNotExist:
            raise PlanNotFound(detail=f"Plan with id {plan[0].get('id')} doesn't exist")
        
        sub = Subscription.objects.create(
            start_date=start_date,
            end_date=end_date,
            plan=plan_instance,
            user=user
        )
        return Response(self.get_serializer(sub).data, status=status.HTTP_201_CREATED)
    
    def _get_object_instance(self, model: models.Model, data: List[Dict[str, int]]):
        id_ = data[0].get('id', None)
        if id_:
            return model.objects.get(id=id_)
        
    @staticmethod
    def check_subscription_allowance(user_last_subscription):
        start_date = user_last_subscription.start_date
        end_date = user_last_subscription.end_date
        today = timezone.now()
        if start_date <= today <= end_date:
            return False
        return True
        