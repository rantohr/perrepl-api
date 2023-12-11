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
        if request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            _ = User.objects.create_user(**serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
    @action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_session = UserSession.objects.filter(users=user, expires_at__gte=timezone.now())
            if user_session.count() !=0:
                user_session.delete()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
