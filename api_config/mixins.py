import json

from rest_framework import permissions
from rest_framework import status

from django.db import models

class PermissionMixin:
    permission_classes = [
        permissions.IsAuthenticated
    ]

class ValidatorMixin:
    def _validate_data(self, validator):
        try:
            validated_data_obj = validator(**self.request.data)
        except ValueError as error:
            error_message = json.loads(error.json())[0]
            error_message.pop('url', None)
            error_message.pop('ctx', None)
            return dict(error_message=error_message, status=status.HTTP_400_BAD_REQUEST)
        return validated_data_obj
    

class UserQuerySetMixin:
    user_field = 'user'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = dict()
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(**lookup_data)
        return qs
