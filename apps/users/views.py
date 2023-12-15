from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

from apps.apis.models import UserSession
from api_config import mixins
from django.utils import timezone

class UserViewset(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        serialized_data = serializer.data
        serialized_data.pop('users', None)
        serialized_data.pop('last_login', None)

        # password = serialized_data.pop('password', None)
        # email = serialized_data.pop('password', None)
        # brand_name = serialized_data.pop('password', None)
        # password = serialized_data.pop('password', None)

        if user.is_superuser:
            # breakpoint()
            _ = User.objects.create_user(users=user, is_created_by_superuser=True, **serialized_data)
            return Response(status=status.HTTP_201_CREATED)
        
        elif user.is_authenticated and user.is_created_by_superuser:
            _ = User.objects.create_user(users=user ,**serialized_data)
            return Response(status=status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            qs = self.get_queryset()
            qs = self.filter_queryset(qs)
            serializer = self.get_serializer(qs, many=True)
            serializer_data = serializer.data
            page = self.paginate_queryset(serializer_data)
            if page is not None:
                return self.get_paginated_response(serializer_data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
    @action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_session = UserSession.objects.filter(users=user, expires_at__gte=timezone.now())
            if user_session.count() !=0:
                user_session.delete()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
