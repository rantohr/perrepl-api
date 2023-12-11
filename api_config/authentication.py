# myapp/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import exceptions
from django.utils import timezone
from django.conf import settings
from apps.apis.models import UserSession

class SingleSessionJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user = super().authenticate(request)
        except TokenError as e:
            raise exceptions.AuthenticationFailed(str(e))

        # Check for existing sessions
        if user:
            user = user[0]
            active_sessions = UserSession.objects.filter(users=user, expires_at__gte=timezone.now())
            if active_sessions.count() > settings.MULTIPLE_ACCOUNTS_LOGIN:
                # User has more than one active session, disallow login
                raise exceptions.AuthenticationFailed("Multiple logins are not allowed.")

        return user, None
