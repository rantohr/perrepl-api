from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from api_config import mixins

class UserViewset(mixins.PermissionMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        breakpoint()
        return super().list(request, *args, **kwargs)    
    
    @action(methods=['post'], detail=False, url_name='logout')
    def logout(self, request, *args, **kwargs):
        # try:
        refresh_token = request.data.get("refresh_token")
        access_token = request.data.get("access_token")
        if refresh_token:
            rtoken = RefreshToken(refresh_token)
            rtoken.blacklist()
        if access_token:
            atoken = RefreshToken(access_token)
            atoken.blacklist()

        return Response({"detail": "Successfully logged out."})
        # except Exception as e:
        #     return Response({"detail": "Error logging out."}, status=status.HTTP_400_BAD_REQUEST)