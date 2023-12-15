# apps.subscriptions

from rest_framework.response import Response
from rest_framework import viewsets, status

from .models import Plan
from .serializers import PlanSerializer

from api_config import mixins

class PlanViewset(
    mixins.AdminPermissionMixin,
    viewsets.ModelViewSet
):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class SubscriptionView(
    mixins.PermissionMixin,
    viewsets.GenericViewSet
):
    def create(self, request, *args, **kwargs):
        ...
