from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSession(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions", null=True)
    session_key = models.CharField(_("session key"), max_length=40, null=True)
    expires_at = models.DateTimeField(_("expires_at"), null=True)