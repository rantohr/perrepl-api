from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import check_password

from .models import User
from .serializers import UserSerializer

from api_config import mixins

class UserViewset(mixins.PermissionMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            _ = User.objects.create_user(**serializer.data)
            return Response(status=status.HTTP_201_CREATED)
