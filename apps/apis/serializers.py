from datetime import datetime


from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.conf import settings

from .models import UserSession

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions


class CustomTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        session_key = self.create_session()
        active_session = UserSession.objects.filter(
            expires_at__gte=timezone.now(),
            users=self.user
        )
        # breakpoint()
        if active_session.count() > settings.MULTIPLE_ACCOUNTS_LOGIN - 1:
            raise exceptions.AuthenticationFailed("Multiple logins are not allowed")
        UserSession.objects.create(users=self.user, session_key=session_key, expires_at=datetime.utcfromtimestamp(refresh.get('exp')))

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    
    def create_session(self):
        request = self.context["request"]
        session_key = self._create_session_key(request)
        return session_key

    @staticmethod
    def _create_session_key(request):
        request.session.create()
        return request.session.session_key